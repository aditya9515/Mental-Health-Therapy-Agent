# setting up Fast API
# print("Setting up Fast API...")

from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn
from ai_agent import agent, parse_response

app = FastAPI()

# print("Fast API is set up.")

#reciveing and validating user input
class Query(BaseModel):
    message : str



@app.post("/ask")
async def ask(request: Query):
    # AI agent logic would go here
    # response = ai_agent(query)

    inputs = {"messages": [{"role": "user", "content": request.message}]}
    stream = agent.invoke(inputs, stream_mode="updates")
    tool_call_name, final_response = parse_response(stream)
    return {
        "response": final_response,
        "tool_called": tool_call_name
    }




# hosting my api
if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000,reload=True)