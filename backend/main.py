from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from agent import run_agent
from database.router import db_router

app = FastAPI()

app.include_router(db_router, prefix="/db", tags=["database"])

class ChatRequest(BaseModel):
    user_input: str

class ChatResponse(BaseModel):
    response: str

@app.post("/chat", response_model=ChatResponse)
def chat_endpoint(req: ChatRequest):
    response = run_agent(req.user_input)
    return StreamingResponse(response, media_type="text/plain")



if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
    