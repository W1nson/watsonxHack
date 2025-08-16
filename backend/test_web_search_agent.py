import pytest
import uuid
from new_graph import agent
from langchain_core.messages import HumanMessage

@pytest.fixture
def thread_id():
    return str(uuid.uuid4())

def test_web_search(thread_id):
    config = {"configurable": {"thread_id": thread_id}}
    
    # This question should trigger the web search tool
    user_input = "What is the current price of a Netflix Premium subscription in the US?"
    response = agent.invoke({"user_id": 1, "messages": [HumanMessage(content=user_input)]}, config=config)
    ai_message = response['messages'][-1].content
    
    assert isinstance(ai_message, str)
    # The response should contain the price of the subscription
    assert "22.99" in ai_message or "23" in ai_message
