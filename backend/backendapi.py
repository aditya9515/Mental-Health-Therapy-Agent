# backend_api.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import uvicorn
import json

from backend.state import State
from backend.agent_graph import Agent_build  # your Agent_build function

app = FastAPI(title="Therapy AI Agent API")

# Input schema
class AgentRequest(BaseModel):
    query: str
    emotions: List[str] = []

# Initialize the agent once
agent_graph = Agent_build()

@app.get("/")
async def root():
    return {"message": "Therapy AI Agent is running"}

@app.post("/run-agent")
async def run_agent(request: AgentRequest):
    # Prepare the state
    state = {
        "session_id": "",
        "user_id": "",
        "query": request.query,
        "history": [],
        "category": 0,
        "safety_response": {},
        "threat_level": "",
        "emotions": request.emotions,
        "responce": {},
        "temp_context": "",
        "temp_completion": True,
        "temp_history": [],
        "error": "",
        "trace_id": "",
    }

    try:
        result = agent_graph.invoke(state)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run("backend_api:app", host="0.0.0.0", port=8000, reload=True)