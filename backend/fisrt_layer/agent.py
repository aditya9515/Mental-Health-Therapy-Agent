from langchain_ollama import ChatOllama
from backend.state import State
import json

llm = ChatOllama(model="qwen2.5:3b", format="json")


def agent(state: State):
    query = state["query"]
    history = state["history"]
    prompt = f"""
    You MUST return ONLY valid JSON.

    Format:
    {{
    "category": 0 or 1,
    "reply": "string (only if category == 0)"
    }}

    Rules:
    - category = 1 → user needs professional help → no reply
    - category = 0 → normal conversation → include reply
    - NO extra text
    - NO explanation

    History:
    {history}

    User Input:
    {query}
    """
    
    response = llm.invoke(prompt).content
    response = json.loads(response)
    if response["category"] == 1:
        return {"category": 1}
    else:
        return {"category": 0, "final_answer": response["reply"]}
    
    
def test(query: str):
    prompt = f"""
    You MUST return ONLY valid JSON.

    Format:
    {{
    "category": 0 or 1,
    "reply": "string (only if category == 0)"
    }}

    Rules:
    - category = 1 → user needs professional therapy help → no reply
    - category = 0 → normal conversation → include reply
    - NO extra text
    - NO explanation

    User Input:
    {query}
    """
    
    responce = llm.invoke(prompt)
    return responce
    # if responce.content["category"] == 1:
    #     return {"category": 1}
    # else:
    #     return {"category": 0, "final_answer": responce.content["prompt"]}


if __name__ == "__main__":
    query = "i feel sad and lonely"
    result = test(query)
    print(result.content)
