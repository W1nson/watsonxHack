from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from agent import run_agent
from database.router import db_router
from new_graph import agent
from langchain_core.messages import AIMessage

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

@app.post("/chat", response_model=ChatResponse)
def chat_endpoint(req: ChatRequest):
    print(req)
    result = agent.invoke({"messages": [{"role": "user", "content": req.user_input}], "user_id": req.user_id})
    print(result)
    response = [Message(role="assistant" if isinstance(message, AIMessage) else "user", content=message.content) for message in result["messages"]]

    return {"response": response[1:]}





if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
    