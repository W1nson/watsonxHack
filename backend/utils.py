from typing import List
from langchain_core.messages import AnyMessage, AIMessage, HumanMessage

# streamming on to console: 
def stream_to_console(agent, inputs, stream_mode="messages"):
    for chunk, metadata in agent.stream(inputs, stream_mode=stream_mode):
        if chunk.content:
            print(chunk.content, end="", flush=True)



def get_query_topic(messages: List[AnyMessage]) -> str:
    """
    Get the query topic from the messages.
    """
    # check if request has a history and combine the messages into a single string
    if len(messages) == 1:
        query_topic = messages[-1].content
    else:
        query_topic = ""
        for message in messages:
            if isinstance(message, HumanMessage):
                query_topic += f"User: {message.content}\n"
            elif isinstance(message, AIMessage):
                query_topic += f"Assistant: {message.content}\n"
    return query_topic