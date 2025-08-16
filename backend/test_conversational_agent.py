import pytest
import uuid
from new_graph import agent
from langchain_core.messages import HumanMessage

@pytest.fixture
def thread_id():
    return str(uuid.uuid4())

def test_full_conversation(thread_id):
    config = {"configurable": {"thread_id": thread_id}}
    
    # First message
    user_input = "Hello, I would like to review my subscriptions."
    response = agent.invoke({"user_id": 1, "messages": [HumanMessage(content=user_input)]}, config=config)
    ai_message = response['messages'][-1].content
    assert isinstance(ai_message, str)
    assert len(ai_message) > 0

    # Second message
    user_input = "What are my current subscriptions?"
    response = agent.invoke({"user_id": 1, "messages": [HumanMessage(content=user_input)]}, config=config)
    ai_message = response['messages'][-1].content
    assert isinstance(ai_message, str)
    assert "Netflix" in ai_message
    assert "Spotify" in ai_message

    # Third message
    user_input = "How can I save money on my Netflix subscription?"
    response = agent.invoke({"user_id": 1, "messages": [HumanMessage(content=user_input)]}, config=config)
    ai_message = response['messages'][-1].content
    assert isinstance(ai_message, str)
    assert "downgrade" in ai_message.lower() or "family plan" in ai_message.lower()

    # Fourth message
    user_input = "Thanks for the help!"
    response = agent.invoke({"user_id": 1, "messages": [HumanMessage(content=user_input)]}, config=config)
    ai_message = response['messages'][-1].content
    assert isinstance(ai_message, str)
    assert "you're welcome" in ai_message.lower() or "happy to help" in ai_message.lower()
