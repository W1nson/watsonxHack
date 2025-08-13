from database.database import SessionLocal
from sqlalchemy import text

from langgraph.graph import StateGraph
from langgraph.graph import START, END

from langchain_core.runnables import RunnableConfig
from configuration import Configuration

from langchain_community.utilities import SerpAPIWrapper
from langchain_core.tools import Tool
from langgraph.prebuilt import ToolNode, tools_condition

from llm import watsonx_model as llm 
from prompts import subscription_analysis_prompt, test_prompt

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
    WHERE u.id = {user_id};"""))

    subscriptions = []
    rows_as_dicts = [row._asdict() for row in out]
    for row_dict in rows_as_dicts:
        subscriptions.append(row_dict)

    out = db.execute(text(f"""SELECT 
    u.firstName,
    u.lastName
    FROM users u
    WHERE u.id = {user_id};"""))
    out = [row._asdict() for row in out]
    firstName = out[0]["firstName"]
    lastName = out[0]["lastName"]
    
    return {'subscriptions': subscriptions, "firstName": firstName, "lastName": lastName}


# Generate Query for websearch 
# def generate_query(state: OverallState, config: RunnableConfig):
#     subscription_history = state["subscriptions"]
#     column = "service_name | category | tier_name | price_usd | subscription_start | subscription_status\n"
#     format_subscription_history = column + "\n".join([f"{sub['service_name']} | {sub['category']} | {sub['tier_name']} | {sub['price_usd']} | {sub['subscription_start']} | {sub['subscription_status']}" for sub in subscription_history])

#     query_prompt = query_prompt.format(subscription_history=format_subscription_history, number_queries=5, current_date=get_current_date())

#     query = llm.invoke(query_prompt)
#     out = query.content.replace('-','').strip().split('\n ')
#     print(len(out))
#     return {"query": out}


# Web Search tool node 

search = SerpAPIWrapper()
search_tool = Tool(
    name="web_search",
    description="Search the web for information",
    func=search.run,
)
# You can create the tool to pass to an agent
search_tool_node = ToolNode([search_tool])



def route_tools(
    state: OverallState,
    config: RunnableConfig,
):
    """
    Use in the conditional_edge to route to the ToolNode if the last message
    has tool calls. Otherwise, route to the end.
    """
    configurable = Configuration.from_runnable_config(config)
    
    if state['web_search_count'] >= configurable.maximum_web_search:
        return END
    elif messages := state.get("messages", []):
        ai_message = messages[-1]
    else:
        raise ValueError(f"No messages found in input state to tool_edge: {state}")
    print(ai_message)
    if hasattr(ai_message, "tool_calls") and len(ai_message.tool_calls) > 0:
        state['web_search_count'] += 1
        return "tools"
    return END


def agent_review_user_subscription(state: OverallState, config: RunnableConfig):
    # configurable = Configuration.from_runnable_config(config)
    firstName = state["firstName"]
    question = state["messages"][0].content
    subscription_history = state["subscriptions"]

    column = "service_name | category | tier_name | price_usd | subscription_start | subscription_status\n"
    format_subscription_history = column + "\n".join([f"{sub['service_name']} | {sub['category']} | {sub['tier_name']} | {sub['price_usd']} | {sub['subscription_start']} | {sub['subscription_status']}" for sub in subscription_history])

    subscription_analysis = test_prompt.format(subscriptions=format_subscription_history, firstName=firstName, question=question)

    message = llm.invoke(subscription_analysis)

    return {'messages': message, 'subscription_suggestion': message}



def save_graph(graph): 
    from IPython.display import Image, display
    from langchain_core.runnables.graph import CurveStyle, MermaidDrawMethod, NodeStyles

    graph.get_graph().draw_mermaid_png(output_file_path="graph.png")





from langgraph.checkpoint.memory import InMemorySaver

memory = InMemorySaver()
builder = StateGraph(OverallState, config=Configuration)

builder.add_node("get_user_subscription", get_user_subscription)
builder.add_node("agent_review_user_subscription", agent_review_user_subscription)
# builder.add_node("search_tool_node", search_tool_node)
# builder.add_node("generate_query", generate_query)

builder.add_edge(START, "get_user_subscription")
builder.add_edge("get_user_subscription", "agent_review_user_subscription")
# builder.add_conditional_edges(
#     "agent_review_user_subscription",
#     route_tools,  # Routes to "tools" or "__end__"
#     {"tools": "search_tool_node", END: END}
# )
# builder.add_edge("search_tool_node", "agent_review_user_subscription")

builder.add_edge("agent_review_user_subscription", END)

agent = builder.compile(name="finance-budget-search-agent", checkpointer=memory)


save_graph(agent)

