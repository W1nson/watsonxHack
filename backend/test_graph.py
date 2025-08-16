import os
from typing import TypedDict, List, Dict, Any, Optional

from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver

# from langchain_openai import ChatOpenAI
from langchain_ibm import ChatWatsonx
from langchain.tools import tool
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain.schema import AIMessage, HumanMessage, SystemMessage

from dotenv import load_dotenv
load_dotenv()

# -----------------------------
# 0) Configuration
# -----------------------------
# os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY", "")
WATSONX_APIKEY = os.getenv("WATSONX_APIKEY")
WATSONX_PROJECT_ID = os.getenv("WATSONX_PROJECT_ID")

os.environ["TAVILY_API_KEY"] = os.getenv("TAVILY_API_KEY", "")

# Example in-memory user subscription profile
user_subscriptions = [
    {"service": "Netflix", "plan": "Standard", "price_month": 15.49, "usage": "2-3 hrs/week"},
    {"service": "Spotify", "plan": "Individual", "price_month": 10.99, "usage": "daily"},
    {"service": "HBO Max", "plan": "With Ads", "price_month": 9.99, "usage": "rarely"}
]

# -----------------------------
# 1) Tools
# -----------------------------

# Web search tool via Tavily (returns top snippets with links)
web_search = TavilySearchResults(max_results=5)

@tool("profile_read", return_direct=False)
def profile_read_tool(query: str) -> str:
    """
    Read the user's known subscription profile and return a short JSON summary.
    Input: a short query or 'all'
    """
    import json
    if query.strip().lower() in ["all", "subscriptions", "plans"]:
        return json.dumps(user_subscriptions)
    # simple filter
    q = query.strip().lower()
    filtered = [s for s in user_subscriptions if q in s["service"].lower()]
    return json.dumps(filtered if filtered else user_subscriptions)

@tool("price_math", return_direct=False)
def price_math_tool(prompt: str) -> str:
    """
    Perform simple savings math. Example prompt:
    'Current: 15.49, Alternative: 9.99, Horizon: 12 months'
    """
    import re
    nums = [float(x) for x in re.findall(r"\d+\.\d+|\d+", prompt)]
    # crude heuristic:
    # if two numbers, interpret as current and alternative, default horizon 12 months
    # if three numbers, third is months
    if len(nums) >= 2:
        current = nums[0]
        alt = nums[1]
        months = int(nums[2]) if len(nums) >= 3 else 12
        monthly_saving = max(0.0, current - alt)
        annual_saving = monthly_saving * months
        return (f"Monthly saving: ${monthly_saving:.2f}. "
                f"Horizon: {months} months. "
                f"Total saving: ${annual_saving:.2f}.")
    return "No calculation performed. Provide 'Current, Alternative, Horizon-months'."

# -----------------------------
# 2) LLM with tool calling
# -----------------------------
# Watsonx LLM
llm = ChatWatsonx(
    model_id="ibm/granite-3-3-8b-instruct",
    url="https://us-south.ml.cloud.ibm.com",
    project_id=WATSONX_PROJECT_ID,
    api_key=WATSONX_APIKEY,
    params={"temperature": 0.7},
)

TOOLS = [web_search, profile_read_tool, price_math_tool]

SYSTEM_PROMPT = """You are a subscription-savings assistant that behaves like a friendly chatbot.
Goals:
1) Understand the user's subscriptions and goals (save money, compare, or ask).
2) Use web_search to fetch latest plan names, features, regional availability, and prices.
3) Suggest concrete actions: cancel, downgrade, switch, or bundle.
4) Use price_math to compute potential savings where helpful.
5) Be transparent about uncertainty. Cite links you found in short form.

Constraints:
- Always keep conversation flow natural.
- Ask for missing info only if it blocks a helpful answer.
- Keep suggestions easy to act on.
- Keep responses concise and structured.
"""

# -----------------------------
# 3) State definition
# -----------------------------
class GraphState(TypedDict):
    messages: List[Any]           # chat history for the LLM
    user_profile: Dict[str, Any]  # subscriptions and preferences
    scratch: Dict[str, Any]       # tool outputs or temporary data
    done: bool                    # signal to stop

# -----------------------------
# 4) Nodes
# -----------------------------
def chat_orchestrator(state: GraphState) -> GraphState:
    """Run the model. It can decide to call tools."""
    msgs = [SystemMessage(content=SYSTEM_PROMPT)] + state["messages"]
    # Bind tools for tool-calling
    runnable = llm.bind_tools(TOOLS)
    ai = runnable.invoke(msgs)
    # Append AI message to history
    state["messages"].append(ai)

    # Check for tool calls
    if hasattr(ai, "tool_calls") and ai.tool_calls:
        state["scratch"]["pending_tools"] = ai.tool_calls
        state["done"] = False
    else:
        state["scratch"]["pending_tools"] = []
        state["done"] = True
    return state

def tool_executor(state: GraphState) -> GraphState:
    """Execute any queued tools and feed results back to the model."""
    tool_calls = state["scratch"].get("pending_tools", [])
    if not tool_calls:
        return state

    tool_results_text = []
    for call in tool_calls:
        name = call["name"]
        args = call.get("args") or {}
        # Execute
        if name == "tavily_search_results_json" or name == "tavily_search_results_json" in str(web_search.name):
            # LangChain tool wrapper
            result = web_search.invoke(args.get("query", ""))
        elif name == "profile_read":
            result = profile_read_tool.invoke(args.get("query", "all"))
        elif name == "price_math":
            result = price_math_tool.invoke(args.get("prompt", ""))
        else:
            result = f"Unknown tool: {name}"
        tool_results_text.append(f"[{name} result] {result}")

    # Feed tool outputs back to the LLM for synthesis
    follow_up = llm.invoke([
        SystemMessage(content=SYSTEM_PROMPT),
        *state["messages"],
        AIMessage(content="\n".join(tool_results_text))
    ])
    state["messages"].append(follow_up)
    # After one round of tools, we stop. You can loop if you want deeper plans.
    state["done"] = True
    return state

def post_processor(state: GraphState) -> GraphState:
    """Optional final formatting or policy hints."""
    # You can add formatting rules here. For simplicity, we do nothing.
    return state

# -----------------------------
# 5) Build the graph
# -----------------------------
builder = StateGraph(GraphState)
builder.add_node("chat_orchestrator", chat_orchestrator)
builder.add_node("tool_executor", tool_executor)
builder.add_node("post_processor", post_processor)

# Edges
builder.set_entry_point("chat_orchestrator")

def need_tools_router(state: GraphState) -> str:
    pending = state["scratch"].get("pending_tools", [])
    return "tool_executor" if pending else "post_processor"

builder.add_conditional_edges(
    "chat_orchestrator",
    need_tools_router,
    {"tool_executor": "tool_executor", "post_processor": "post_processor"},
)

builder.add_edge("tool_executor", "post_processor")
builder.add_edge("post_processor", END)

graph = builder.compile(checkpointer=MemorySaver())

# -----------------------------
# 6) Minimal run helper
# -----------------------------
def run_chat(session_id: str, user_text: str, user_profile: Optional[Dict[str, Any]] = None):
    """Call this per user message. session_id persists the thread via MemorySaver."""
    state: GraphState = {
        "messages": [HumanMessage(content=user_text)],
        "user_profile": user_profile or {"subscriptions": user_subscriptions},
        "scratch": {},
        "done": False,
    }
    result = graph.invoke(state, config={"configurable": {"thread_id": session_id}})
    # The last AI message is at the end
    final_msgs = [m for m in result["messages"] if isinstance(m, AIMessage)]
    return final_msgs[-1].content if final_msgs else "(no reply)"

# Example:
if __name__ == "__main__":
    print(run_chat("demo-user", "Can you find cheaper options for my Netflix and HBO Max?"))