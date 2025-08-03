from langgraph.prebuilt import create_react_agent
from langchain_ollama import ChatOllama
from utils import stream_to_console
from tools import get_weather, get_current_earthquake, get_current_date
from prompts import disaster_advisor_instructions

agent = create_react_agent(
    model=ChatOllama(model="granite3.3:latest", stream=True),
    tools=[get_weather, get_current_earthquake, get_current_date],
    prompt=disaster_advisor_instructions,
)

def run_agent(user_input):
    """
    Streams agent responses for a given user input.
    Yields each message chunk for FastAPI StreamingResponse.
    """
    for chunk in agent.stream({"messages": [{"role": "human", "content": user_input}]}, stream_mode="updates"):
        print(chunk['agent']['messages'][-1].content, end="", flush=True)


if __name__ == "__main__":
    run_agent("Who are you?")
        
# Run the agent
result = agent.invoke(
    {"messages": [{"role": "user", "content": "Who are you?"}]}
)

# for message in result:
#     print(message['messages'][-1].content)


# llm = ChatOllama(model="granite3.3:latest")
# messages = [
#     ("human", "Write me 1000 words story"),
# ]
# for chunk in llm.stream(messages):
#     print(chunk.text(), end="", flush=True)


from langgraph.prebuilt import create_react_agent

graph = create_react_agent(
    ChatOllama(model="granite3.3:latest"),
    tools=[check_weather],
    prompt="You are a helpful assistant",
)
inputs = {"messages": [{"role": "user", "content": "what is the weather in sf"}]}
stream_to_console(graph, inputs)

# for message_chunk, metadata in graph.stream( 
#     {"topic": "ice cream"},
#     stream_mode="messages",
# ):
#     if message_chunk.content:
#         print(message_chunk.content, end="|", flush=True)