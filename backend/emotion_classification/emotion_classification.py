from backend.state import State
from langchain_ollama import ChatOllama
import json


llm = ChatOllama(model="qwen2.5:3b",format="json")


def emotion_classification_agent(state: State):
    print("ADA error in classification function")
    history = state["history"][-3:]
    query = state["query"]
    prompt = f"""
    USER INPUT:
    {query}
    
    HISTORY:
    {history}
    
    INSTRUCTIONS:
    Your are tasked with catigorizing user emotions based on the conversation 
    history and the new user input.
    
    FORMATE json:
    {{"emotions": ["like", "say", "sad", "angry", "depressed", "happy", "anxious", "etc"]}}
    """
    responce = llm.invoke(prompt).content
    response = json.loads(responce)
    return {"category": list(response["emotions"])}


def test(query: str):
    prompt = f"""
    USER INPUT:
    {query}
    
    INSTRUCTIONS:
    Your are tasked with catigorizing user emotions based on the conversation 
    history and the new user input.
    
    FORMATE json:
    {{"emotions": ["like", "say", "sad", "angry", "depressed", "happy", "anxious", "etc"]}}
    """
    responce = llm.invoke(prompt).content
    response = json.loads(responce)
    return list(response["emotions"])


if __name__ == "__main__":
    query = "today i had the worst beakup i dont this its woth living for at this point now i feel like everyone is judging me "
    print(test(query))