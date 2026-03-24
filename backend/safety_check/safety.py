from backend.state import State
from langchain_ollama import ChatOllama
import json
from backend.tools import emergency_call


llm = ChatOllama(model="qwen2.5:3b", format="json")


def safety_check(state: State):
    print("ADA error in safety function")
    history = state["history"][-3:]
    query = state["query"]

    prompt = f"""
    Conversation:
    {history}

    New message:
    {query}

    Task:
    Classify risk level:
    - HIGH (self-harm/suicide)- needs instent action
    - MEDIUM (distress)
    - LOW (safe)

    Also detect escalation (yes/no)

    Return JSON:
        {{
        "risk": ["HIGH","MEDIUM","LOW"],
        "escalation": true/false,
        "confidence": 0 to 1
        }}
    """
    response = llm.invoke(prompt).content
    response = json.loads(response)
    return {"safety_response": response}


def safety_defy(state: State):
    print("ADA error in safety_defy function")
    response = state["safety_response"]
    threath = "LOW"
    if response["risk"] == "HIGH" and response["confidence"] > 0.7:
        emergency_call()
        threath = "HIGH"
    if threath == "HIGH":
        return {"threat_level": threath,
                "final_answer": "making emergency call"}
    else:
        return {"threat_level": threath}


def test(query: str):

    prompt = f"""
    New message:
    {query}

    Task:
    Classify risk level:
    - HIGH (self-harm/suicide)- needs instent action
    - MEDIUM (distress)
    - LOW (safe)

    Also detect escalation (yes/no)

    Return JSON:
        Return JSON:
        {{
        "risk": ["HIGH","MEDIUM","LOW"],
        "escalation": true/false,
        "confidence": 0 to 1
        }}
    """
    response = llm.invoke(prompt).content
    response = json.loads(response)
    # return response
    threath = "LOW"
    if response["risk"] == "HIGH" and response["confidence"] > 0.7:
        emergency_call()
        threath = "HIGH"
    if threath == "HIGH":
        return {"threat_level": threath,
                "final_answer": "making emergency call"}
    return {"threat_level": threath}


if __name__ == "__main__":
    query = "i do have light head ache"
    response = test(query)
    print(response)
