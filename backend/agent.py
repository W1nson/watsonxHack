import uuid
import logging
from new_graph import agent
from langchain_core.messages import HumanMessage

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Generate a unique thread ID for the conversation
thread_id = str(1)

def run_agent(user_id: int):
    """
    Runs the conversational agent.
    """
    config = {"configurable": {"thread_id": thread_id}}
    logging.info(f"Starting agent with config: {config}")
    
    while True:
        user_input = input("You: ")
        if user_input.lower() == 'exit':
            break

        logging.info(f"User input: {user_input}")
        # The input to the agent is a dictionary with the user_id and the message.
        # The message is a list of HumanMessage objects.
        for chunk in agent.stream({"user_id": user_id, "messages": [HumanMessage(content=user_input)]}, config=config, stream_mode='debug'):
            print(chunk)
        
if __name__ == "__main__":
    # You can change the user_id to test with different users.
    run_agent(user_id=1)