from langgraph.prebuilt import create_react_agent
from langchain_ollama import ChatOllama
from utils import stream_to_console
from tools import get_weather, get_current_earthquake, get_current_date
from prompts import disaster_advisor_instructions

agent = create_react_agent(
    model=ChatOllama(model="granite3.3:latest"),
    tools=[get_weather, get_current_earthquake, get_current_date],
    prompt=disaster_advisor_instructions,
)

def run_agent(user_input):
    """
    Streams agent responses for a given user input.
    Yields each message chunk for FastAPI StreamingResponse.
    """
    # stream_to_console(agent, {"messages": [{"role": "user", "content": user_input}]})
    for chunk, metadata in agent.stream({"messages": [{"role": "human", "content": user_input}]}, stream_mode="messages"):
        if chunk.content:
            # print(chunk.content, end="", flush=True)
            yield chunk.content

if __name__ == "__main__":
    run_agent("Who are you?")
        