from langgraph.prebuilt import create_react_agent
from langchain_ollama.chat_models import ChatOllama
from tools import get_weather, get_current_earthquake


agent = create_react_agent(
    model=ChatOllama(model="granite3.3:latest"),
    tools=[get_weather, get_current_earthquake],
    prompt="You are a helpful assistant"
)

# Run the agent
result = agent.invoke(
    {"messages": [{"role": "user", "content": "what is the weather in sf and what is the current earthquake in sf"}]}
)
print(result)