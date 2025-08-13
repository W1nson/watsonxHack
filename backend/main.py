from fastapi import FastAPI
from pydantic import BaseModel
from database.router import db_router
from new_graph import agent
from langchain_core.messages import AIMessage
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
    recommendations: list[str]
    answer: list[str]
    follow_up: list[str]

@app.post("/chat", response_model=ChatResponse)
def chat_endpoint(req: ChatRequest):
    config = {"configurable": {"thread_id": "1"}}

    result = agent.invoke({"messages": [{"role": "user", "content": req.user_input}], "user_id": req.user_id, "web_search_count": 0}, config=config)

    response = [Message(role="assistant" if isinstance(message, AIMessage) else "user", content=message.content) for message in result["messages"]]

    ai_msg = result["messages"][-1].content
    tags = extract_tags(ai_msg)
    out = {"response": response, "recommendations": tags["recommendations"], "answer": tags["answer"], "follow_up": tags["follow_up"]}
    return out

def extract_tags(msg): 
    recommendations = [tag.strip() for tag in re.findall(r"(?<=<recommendation>)[\s\S]*?(?=<\/recommendation>)", msg, re.IGNORECASE)]
    answer = [tag.strip() for tag in re.findall(r"(?<=<answer>)[\s\S]*?(?=<\/answer>)", msg, re.IGNORECASE)]
    follow_up = [tag.strip() for tag in re.findall(r"(?<=<follow-up>)[\s\S]*?(?=<\/follow-up>)", msg, re.IGNORECASE)]
    
    return {"recommendations": recommendations, "answer": answer, "follow_up": follow_up}



if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
    