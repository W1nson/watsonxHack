from fastapi import FastAPI
from pydantic import BaseModel
from database.router import db_router
from new_graph import agent
from langchain_core.messages import AIMessage, HumanMessage
import re 

app = FastAPI()

app.include_router(db_router, prefix="/db", tags=["database"])

class ChatRequest(BaseModel):
    user_input: str
    user_id: str 
class Message(BaseModel): 
    role: str
    content: str
class ChatResponse(BaseModel):
    response: list[Message]
    # recommendations: list[str]
    # answer: list[str]
    # follow_up: list[str]

messages = []
@app.post("/chat", response_model=ChatResponse)
def chat_endpoint(req: ChatRequest):
    config = {"configurable": {"thread_id": "1"}}
    messages.append({"role": "user", "content": req.user_input})
    result = agent.stream({"messages": messages, "user_id": req.user_id, "web_search_count": 0}, config=config, stream_mode='values')

    for update in result:
        print(update['messages'])
        print(update['messages'][-1].content)
    # debug
    # for update in result:
    #     print(update)
    #     for msg in update.get("values", []):
    #         if isinstance(msg, AIMessage):
    #             messages.append({"role": "assistant", "content": msg.content})
    #             print(msg.content)
    #         elif isinstance(msg, HumanMessage):
    #             messages.append({"role": "user", "content": msg.content})
    #             print(msg.content)
    #         else:
    #             print(f"Unknown message type: {type(msg)}")
        
       
    # response = [Message(role="assistant" if isinstance(message, AIMessage) else "user", content=message.content) for message in result["messages"]]

    # ai_msg = result["messages"][-1].content
    # tags = extract_tags(ai_msg)
    # print(tags)

    out = {"response": messages, }
    return out

def extract_tags(msg): 
    print(msg)
    # Remove both recommendation and follow-up tags and their content
    msg_cleaned = re.sub(r'<recommendation>[\s\S]*?<\/recommendation>', '', msg, flags=re.IGNORECASE)
    msg_cleaned = re.sub(r'<follow-up>[\s\S]*?<\/follow-up>', '', msg_cleaned, flags=re.IGNORECASE)
    
    # Extract the answer from the cleaned message
    answer = [tag.strip() for tag in re.findall(r"(?<=<answer>)[\s\S]*?(?=<\/answer>)", msg_cleaned, re.IGNORECASE)]
    recommendations = [tag.strip() for tag in re.findall(r"(?<=<recommendation>)[\s\S]*?(?=<\/recommendation>)", msg, re.IGNORECASE)]
    follow_up = [tag.strip() for tag in re.findall(r"(?<=<follow-up>)[\s\S]*?(?=<\/follow-up>)", msg, re.IGNORECASE)]
    print(answer)
    return {"recommendations": recommendations, "answer": answer, "follow_up": follow_up}



if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)