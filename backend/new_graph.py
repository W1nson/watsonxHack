from database.database import SessionLocal
from sqlalchemy import text

from langgraph.graph import StateGraph
from langgraph.graph import START, END

from langchain_core.runnables import RunnableConfig
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate

from configuration import Configuration

from langchain_tavily import TavilySearch

from langchain_core.tools import Tool
from langgraph.prebuilt import ToolNode, tools_condition

from llm import watsonx_model as llm
from prompts import chatbot_prompt, get_current_date

from state import OverallState


def get_user_subscription(state: OverallState, config: RunnableConfig):
    db = SessionLocal()
    user_id = state["user_id"]
    out = db.execute(text(f"""SELECT
    s.start_date as subscription_start,
    s.current_status as subscription_status,
    st.tier_name,
    st.price_usd,
    sv.name as service_name,
    sv.category
    FROM users u
    LEFT JOIN subscriptions s ON u.id = s.user_id
    LEFT JOIN service_tiers st ON s.tier_id = st.id
    LEFT JOIN services sv ON st.service_id = sv.id
    WHERE u.id = {user_id};""" ))

    subscriptions = []
    rows_as_dicts = [row._asdict() for row in out]
    for row_dict in rows_as_dicts:
        subscriptions.append(row_dict)

    out = db.execute(text(f"""SELECT
    u.firstName,
    u.lastName
    FROM users u
    WHERE u.id = {user_id};""" ))
    out = [row._asdict() for row in out]
    firstName = out[0]["firstName"]
    lastName = out[0]["lastName"]
    
    return {'subscriptions': subscriptions, "firstName": firstName, "lastName": lastName}


# Web Search tool node 

tool = TavilySearch(max_results=2)
tools = [tool]
# tool.invoke("What's a 'node' in LangGraph?")
search_tool_node = ToolNode(tools)



def route_tools(
    state: OverallState,
):
    """Route to tools only if the latest message is an AI message with tool calls."""
    messages = state.get("messages", [])
    if not messages:
        return "continue"

    last = messages[-1]
    print(f"Last message: {last}")
    if isinstance(last, AIMessage) and getattr(last, "tool_calls", None):
        return "tools"

    return "continue"


def generate_response(state: OverallState, config: RunnableConfig):
    # configurable = Configuration.from_runnable_config(config)
    firstName = state["firstName"]
    subscription_history = state["subscriptions"]
    messages = state["messages"]
    question = state["messages"][-1].content
    # Construct the conversation history
    conversation_history = ""
    for message in messages:
        if isinstance(message, HumanMessage):
            conversation_history += f"You: {message.content}\n"
        else:
            conversation_history += f"SpendWise: {message.content}\n"

    column = "service_name | category | tier_name | price_usd | subscription_start | subscription_status\n"
    format_subscription_history = column + "\n".join([f"{sub['service_name']} | {sub['category']} | {sub['tier_name']} | {sub['price_usd']} | {sub['subscription_start']} | {sub['subscription_status']}" for sub in subscription_history])

    # The user's question is now the last message in the list
    system_template = chatbot_prompt.format(
        subscriptions=format_subscription_history,
        firstName=firstName,
        conversation_history=conversation_history, 
        current_date=get_current_date(),
    )
    


    prompt_template = ChatPromptTemplate.from_messages(
        [("system", system_template), ("user", "{question}")]
    )
    prompt = prompt_template.invoke({"question": question})
    model_with_tools = llm.bind_tools(tools)
    message = model_with_tools.invoke(prompt)

    # Return a dictionary with the new message to be added to the list of messages
    return {'messages': [message]}


def conversation_entry(state: OverallState, config: RunnableConfig):
    # This node is a placeholder for user input.
    # It doesn't do anything, but it's a necessary part of the loop.
    return {}


def should_continue(state: OverallState):
    """
    Continue only when the latest message is from the user.
    If the user typed "exit", stop. If the latest message is from the AI or a tool,
    end the graph run and wait for the next user input to resume. This prevents
    recursion loops where the agent keeps calling itself without a new user turn.
    """
    if not state.get("messages"):
        return END

    last = state["messages"][-1]

    # Proceed only on a fresh HumanMessage
    if isinstance(last, HumanMessage):
        if isinstance(last.content, str) and last.content.strip().lower() == "exit":
            return END
        return "generate_response"

    # Last turn is AI/tool output — stop this run and wait for the next user input
    return END


def save_graph(graph):
    from IPython.display import Image, display
    from langchain_core.runnables.graph import CurveStyle, MermaidDrawMethod, NodeStyles

    graph.get_graph().draw_mermaid_png(output_file_path="graph.png")


from langgraph.checkpoint.memory import InMemorySaver

memory = InMemorySaver()
builder = StateGraph(OverallState, config=Configuration)

builder.add_node("get_user_subscription", get_user_subscription)
builder.add_node("generate_response", generate_response)
builder.add_node("conversation_entry", conversation_entry)
builder.add_node("search_tool_node", search_tool_node)


builder.add_edge(START, "get_user_subscription")
builder.add_edge("get_user_subscription", "conversation_entry")

builder.add_conditional_edges(
    "conversation_entry",
    should_continue,
    {
        "generate_response": "generate_response",
        END: END
    }
)

builder.add_conditional_edges(
    "generate_response",
    route_tools,
    {
        "tools": "search_tool_node",
        "continue": "conversation_entry",
    },
)
builder.add_edge("search_tool_node", "generate_response")


agent = builder.compile(name="finance-budget-search-agent", checkpointer=memory)


save_graph(agent)
