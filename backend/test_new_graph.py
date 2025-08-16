import pytest
from new_graph import agent
from langchain_core.messages import HumanMessage

def test_agent_with_web_search():
    config = {"configurable": {"thread_id": "1"}}
    question = "How can I save money on my subscriptions?"
    
    state = {
        "messages": [HumanMessage(content=question)],
        "user_id": 1,
    }
    
    result = agent.invoke(state, config=config)
    
    assert result is not None

    assert "subscription_suggestion" in result
    assert isinstance(result["subscription_suggestion"], str)
    assert len(result["subscription_suggestion"]) > 0
ß