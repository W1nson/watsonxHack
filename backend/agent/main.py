from fastapi import FastAPI
from pydantic import BaseModel
from graph import agent
from langchain_core.messages import AIMessage, HumanMessage
import re 

app = FastAPI()


class ChatRequest(BaseModel):
    user_input: str
    user_id: str 

class Message(BaseModel): 
    role: str
    content: str
class ChatResponse(BaseModel):
    response: list[Message]
    recommendation: list[str]
    reason: str
    answer: str
    followup_question: str

messages = []

user = { "1": "James", "2": "Alice", "3": "Bob"}
config = {"configurable": {"thread_id": "1"}}
@app.post("/chat", response_model=ChatResponse)
def chat_endpoint(req: ChatRequest):
    firstName = user[req.user_id] if req.user_id in user else "User"
    print(f"User {firstName} input: {req.user_input}")
    # events = agent.stream({"messages": [{"role": "user", "content": req.user_input}], "fristName": firstName}, config, stream_mode='values')
    # output = [] 
    # for event in events:
    #     msg = event["messages"][-1]
    #     msg.pretty_print()
    #     if isinstance(msg, AIMessage):
    #         output.append({"role": "assistant", "content": msg.content})
    #     # else:
        #     print(f"Unknown message type: {type(msg)}")
    output = agent.invoke({"messages": [{"role": "user", "content": req.user_input}], "lookuped": False}, config)
    response = [Message(role="assistant" if isinstance(message, AIMessage) else "user", content=message.content) for message in output["messages"]]

   
    print(output['messages'][-1].content)
    print(output['structured_output'])
    out = {"response": response}
    out.update(output['structured_output'])
    return out
    

def extract_tags(msg): 
    print(msg)
    # Remove both recommendation and follow-up tags and their content
    msg_cleaned = re.sub(r'<recommend>[\s\S]*?<\/recommend>', '', msg, flags=re.IGNORECASE)
    msg_cleaned = re.sub(r'<follow-up>[\s\S]*?<\/follow-up>', '', msg_cleaned, flags=re.IGNORECASE)
    # Extract the answer from the cleaned message
    answer = [tag.strip() for tag in re.findall(r"(?<=<answer>)[\s\S]*?(?=<\/answer>)", msg_cleaned, re.IGNORECASE)]
    recommendations = [tag.strip() for tag in re.findall(r"(?<=<recommend>)[\s\S]*?(?=<\/recommend>)", msg, re.IGNORECASE)]
    follow_up = [tag.strip() for tag in re.findall(r"(?<=<follow-up>)[\s\S]*?(?=<\/follow-up>)", msg, re.IGNORECASE)]
    print(answer)
    return {"recommendations": recommendations, "answer": answer, "follow_up": follow_up}



if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)