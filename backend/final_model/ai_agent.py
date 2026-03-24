from langchain_ollama import ChatOllama
from backend.state import State
import json
from backend.tools.rag import get_retriever

# creating an ai agent with tools
llm = ChatOllama(
    model="alibayram/medgemma:4b",
    format="json",
    temperature=0.5
)


def therapist(state: State):
    print("ADA error in therapist function")
    history = state["temp_history"]
    query = state["query"]
    emotions = state["emotions"]
    retriever = get_retriever()
    if ((not history) or (state["temp_completion"] == True)):
        docs = retriever.invoke(f"{query}and the user is feeling {', '.join(emotions)}.")
        context = "\n".join([doc.page_content for doc in docs[:3]])
        history = []
    else:
        context = state["temp_context"]
    prompt = f"""
    HISTORY:
    {history}
    
    USER INPUT:
    {query}
    
    USER EMOTIONS:
    {emotions}
    
    RETRIEVED TECHNIQUES:
    {context}
    
    INSTRUCTIONS:
    1.You are Emily Hartman, a warm and experienced clinical psychologist. 
    Respond with emotional attunement.
    
    2.if the previous conversation is not concluded then always continue the conversation with the
    previous technique used. if concluded or empty then you can use a new technique from the retrieved techniques.
    
    3. Your response should include:
        {{
        "final_answer": "string",
        "technique": the technique you used from the retrieved techniques or previous conversation full json technique should be there
        "completion": True or False if the conversation is concluded or not
        }}
    
    4. you try to gather more information about the user's situation and feelings to 
    provide better support. If needed
    """
    j = 1
    while j == 1:
        try:
            j = 0
            responce = llm.invoke(prompt).content
            responce = json.loads(responce)
        except json.JSONDecodeError:
            j =1
            print("JSON decode error, retrying...")
            
    history.append({"User": query,
                    "Agent": responce.get("final_answer"),
                    })
    
    return {"responce": responce.get("final_answer"), "temp_history": history, "temp_context": responce.get("technique"), "temp_completion": bool(responce.get("completion"))}


def responce_to_user(state: State):
    print("ADA error in responce function")
    responce = state["responce"]
    print(responce)
    query = input("Enter user query: ")

    return {"responce": responce,
            "query": query,
            }


def test(query: str,emotions: list):
    retriever = get_retriever()
    docs = retriever.invoke(f"{query}and the user is feeling {', '.join(emotions)}.")
    context = "\n".join([doc.page_content for doc in docs[:3]])
    if True:
        prompt = f"""
        HISTORY:
        
        
        USER INPUT:
        {query}
        
        USER EMOTIONS:
        {emotions}
        
        RETRIEVED TECHNIQUES:
        {context}
        
        INSTRUCTIONS:
        1.You are Emily Hartman, a warm and experienced clinical psychologist. 
        Respond with emotional attunement.
        
        2.if the previous conversation is not concluded then always continue the conversation with the
        previous technique used. if concluded then you can use a new technique steps from the retrieved techniques steps.
        
        3. Your response should include:
        {{
        "final_answer": "string",
        "technique": the technique you used from the retrieved techniques or previous conversation full json technique should be there
        "completion": True or False if the conversation is concluded or not
        }}
    
        4. you try to gather more information about the user's situation and feelings to 
        provide better support. If needed

        """
    responce = llm.invoke(prompt).content
    responce = json.loads(responce)
    return {"responce": responce}, docs


if __name__ == "__main__":
    query = "I have been feeling really down lately and I don't know why."
    emotions = ["sadness", "hopelessness"]
    answer, docs = test(query, emotions)
    print(json.dumps(answer, indent=4))
    context = "\n\n".join([doc.page_content for doc in docs[:3]])
    print(context)


