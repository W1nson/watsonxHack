from langgraph.graph import StateGraph, START, END
from langchain_ibm import ChatWatsonx
from langchain_tavily import TavilySearch
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage, ToolMessage
from langgraph.checkpoint.memory import InMemorySaver

from util import get_current_date, get_user_sub, format_table
from prompt import SYSTEM_PROMPT
from state import State
from pydantic import BaseModel, Field

import os 
import json 

from dotenv import load_dotenv
load_dotenv()

class ResponseFormatter(BaseModel):
    """Always use this tool to structure your response to the user."""
    answer: str = Field(description="The answer to the user's question, provide an accurate savings for user based on your suggestions if applicable")
    reason: str = Field(description="The reason to the user's question that supports the recommendations proposed")
    followup_question: str = Field(description="A followup question the user could ask, such as asking for more suggestions")
    recommendation: list[str] = Field(description="Suggestions that could potentially solve user's question", min_length=1, max_length=2)




# Load environment variables
WATSONX_APIKEY = os.getenv("WATSONX_APIKEY")
WATSONX_PROJECT_ID = os.getenv("WATSONX_PROJECT_ID")


# Define LLM that is being used for the agent 
llm = ChatWatsonx(
    model_id="ibm/granite-3-3-8b-instruct",
    url="https://us-south.ml.cloud.ibm.com",
    project_id=WATSONX_PROJECT_ID,
    api_key=WATSONX_APIKEY,
    params={"temperature": 0.7},
)

# Setup Tavily Search tool
tool = TavilySearch(max_results=5)
tools = [tool]

# Bind the tools to the LLM allowing LLM to able to call the tools 
llm_with_tools = llm.bind_tools(tools, tool_choice="tavily_search")




# Define the chatbot node where this chatbot will be the main entry point of the graph
def chatbot(state: State):
    structured_output = None
    subs = get_user_sub()
    formatted_subs = format_table(subs)    
    prompt = SYSTEM_PROMPT.format(
        firstName="James",
        current_date=get_current_date(),
        subscriptions=formatted_subs,
    )
    if not isinstance(state["messages"][0], SystemMessage):
        state["messages"].insert(0, SystemMessage(content=prompt))
    
    if not state.get("looked_up"):
        ai = llm_with_tools.invoke(state["messages"]) # will emit a tool call
    else:
        llm_with_structure_output = llm.with_structured_output(ResponseFormatter)
        structured_output = llm_with_structure_output.invoke(state["messages"]) 
        ai = llm.invoke(state["messages"])

    
    return {"messages": [ai], "subscriptions": subs, "firstName": "James", "lookuped": False, "structured_output": structured_output}



class BasicToolNode:
    """A node that runs the tools requested in the last AIMessage."""

    def __init__(self, tools: list) -> None:
        self.tools_by_name = {tool.name: tool for tool in tools}

    def __call__(self, inputs: dict):
        if messages := inputs.get("messages", []):
            message = messages[-1]
        else:
            raise ValueError("No message found in input")
        outputs = []
        for tool_call in message.tool_calls:
            tool_result = self.tools_by_name[tool_call["name"]].invoke(
                tool_call["args"]
            )
            outputs.append(
                ToolMessage(
                    content=json.dumps(tool_result),
                    name=tool_call["name"],
                    tool_call_id=tool_call["id"],
                )
            )
        return {"messages": outputs}



# Define route that can conditionally route to the ToolNode if the last message has tool calls
def route_tools(
    state: State,
):
    """
    Use in the conditional_edge to route to the ToolNode if the last message
    has tool calls. Otherwise, route to the end.
    """
    if isinstance(state, list):
        ai_message = state[-1]
    elif messages := state.get("messages", []):
        ai_message = messages[-1]
    else:
        raise ValueError(f"No messages found in input state to tool_edge: {state}")
    if hasattr(ai_message, "tool_calls") and len(ai_message.tool_calls) > 0:
        return "tools"
    return END



# Define the node that just sets the looked_up flag to True after the tool execution
def set_looked_up(state: State):
    # After any tool execution, mark the flag so we switch to no-tools LLM
    return {"looked_up": True}


def save_graph(graph):
    graph.get_graph().draw_mermaid_png(output_file_path="graph.png")




tool_node = BasicToolNode(tools=[tool])

# initialize the memory that stores the memory in local memory
memory = InMemorySaver()

# Building the graph 
graph_builder = StateGraph(State)
graph_builder.add_node("chatbot", chatbot)
graph_builder.add_node("tools", tool_node)
graph_builder.add_node("mark_done", set_looked_up)

graph_builder.add_edge(START, "chatbot")
# graph_builder.add_edge("tools", "chatbot")
graph_builder.add_edge("tools", "mark_done")
graph_builder.add_edge("mark_done", "chatbot")
graph_builder.add_conditional_edges(
    "chatbot",
    route_tools,
    # The following dictionary lets you tell the graph to interpret the condition's outputs as a specific node
    # It defaults to the identity function, but if you
    # want to use a node named something else apart from "tools",
    # You can update the value of the dictionary to something else
    # e.g., "tools": "my_tools"
    {"tools": "tools", END: END},
)


agent = graph_builder.compile(checkpointer=memory)
# Save the graph to a file for visualization
save_graph(agent)



config = {"configurable": {"thread_id": "1"}}

def stream_graph_updates(user_input: str, stream_mode: str = 'default'):
    if stream_mode == 'debug':
        for event in agent.stream({"messages": [{"role": "user", "content": user_input}]}, config, stream_mode='debug'):
            print(event)
    elif stream_mode == 'values':
        events = agent.stream(
            {"messages": [{"role": "user", "content": user_input}]},
            config,
            stream_mode="values",
        )
        for event in events:
            event["messages"][-1].pretty_print()
    else:
        for event in agent.stream({"messages": [{"role": "user", "content": user_input}]}, config):
            for value in event.values():
                print("Assistant:", value["messages"][-1].content)
    



