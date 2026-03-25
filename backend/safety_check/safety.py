from backend.state import State
from langchain_ollama import ChatOllama
import json
from backend.tools.emergency_call import emergency_call


llm = ChatOllama(model="qwen2.5:7b-instruct", format="json")


def safety_check(state: State):
    print("ADA error in safety function")
    history = state["history"][-3:]
    query = state["query"]

    prompt = f"""
    You are a strict mental health safety classifier.

    Conversation:
    {history}

    New message:
    {query}

    Rules:
    - If the user expresses ANY desire to die → HIGH
    - Includes typos like "wnat to die"
    - Includes indirect phrases like "life is not worth living"
    - Emotional distress only → MEDIUM
    - Otherwise → LOW

    Return ONLY valid JSON:
    {{
        "risk": "HIGH" or "MEDIUM" or "LOW",
        "escalation": true or false,
        "confidence": number between 0 and 1
    }}
    """
    response = llm.invoke(prompt).content
    response = json.loads(response)
    return {"safety_response": response}


def safety_defy(state: State):
    print("ADA error in safety_defy function")
    response = state["safety_response"]
    threath = "LOW"
    if response["risk"] == "HIGH":
        emergency_call()
        threath = "HIGH"
    if threath == "HIGH":
        return {"threat_level": threath,
                "responce": "making emergency call"}
    output = {"threat_level": threath}
    return output


def test(query: str):

    prompt = f"""
    You are a strict mental health safety classifier.

    New message:
    {query}

    Rules:
    - If the user expresses ANY desire to die → HIGH
    - Includes typos like "wnat to die"
    - Includes indirect phrases like "life is not worth living"
    - Emotional distress only → MEDIUM
    - Otherwise → LOW

    Return ONLY valid JSON:
    {{
        "risk": "HIGH" or "MEDIUM" or "LOW",
        "escalation": true or false,
        "confidence": number between 0 and 1
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
    query = "i wnat to die"
    response = test(query)
    print(response)
