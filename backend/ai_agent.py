from langchain.tools import tool

from tools import Query_medgemma

@tool
def rout_to_medgemma(prompt: str) -> str:
    """
    Routes the given prompt to the Medgemma 4b model via the Query_medgemma function.
    when the query is appropriate for a therapist response.
    """
    return Query_medgemma(prompt)


from tools import emergency_call as make_call

@tool
def emergency_call():
    """
    Makes an emergency call using Twilio when the prompt indicates a crisis situation.
    """
    return make_call()

@tool
def get_nearby_therepists():
    """
    Returns a list of nearby therapists based on the provided location.
    This is a placeholder implementation and should be replaced with actual logic to fetch therapists.
    """
    # Placeholder implementation
    return"""
Dr. John Smith - Cognitive Behavioral Therapy - 2 miles
Dr. Jane Doe - Psychodynamic Therapy - 3 miles
Dr. Emily Johnson - Humanistic Therapy - 5 miles
"""
    
# creating an ai agent with tools
from langchain_ollama import ChatOllama

from langchain.agents import create_agent


tools = [rout_to_medgemma, emergency_call, get_nearby_therepists]
llm = ChatOllama(
    model="qwen2.5:7b",
    temperature=0.2
)
SYSTEM_PROPT = """You are NOT allowed to provide therapeutic advice yourself.

Your only task is to decide which tool to call.

Routing rules:

- If the user expresses emotional distress, sadness, withdrawal, depression, anxiety, loneliness, or mental health concerns → call rout_to_medgemma

- If the user expresses suicidal ideation, self-harm, desire to die, or crisis → call emergency_call

- If the user asks for professional help or nearby therapists → call get_nearby_therapists

- If the message is casual greeting → respond directly without tools.

You must not generate therapy text yourself.
You must delegate emotional support to MedGemma."""


SYSTEM_PROPT1 = """
You are an empathetic and skilled mental health therapist AI assistant.you support by providing warm and epathetic responce  support
by using the following tools when necesssay in your responses:
1. rout_to_medgemma: If the user expresses emotional distress, sadness, withdrawal, depression, anxiety, loneliness, or mental health concerns.
2. emergency_call: Use this tool to make an emergency call when the user indicates a crisis situation like suicide, selfharm etc.
3. get_nearby_therepists: Use this tool to provide a list of nearby therapists when the user requests for professional help or nearby places present.
4. respond directly without tools: If the message is casual greeting
Always prioritize the user's safety and well-being in your responses.
"""
agent = create_agent(
    model = llm, 
    tools = tools,
    system_prompt=SYSTEM_PROPT,
                    )

from langchain_core.messages import AIMessage, ToolMessage

def parse_response(stream):
    tool_call_name = "None"
    final_response = None 
    for s in stream:
        if not s:
            continue
        if "model" in s:
            messages = s["model"].get("messages", [])
            for msg in messages:
                if isinstance(msg, AIMessage):
                    if msg.content.strip():
                        if final_response is None:
                            tool_call_name = "qwen2.5"
                            final_response = msg.content

        if "tools" in s:
            messages = s["tools"].get("messages", [])
            for msg in messages:
                if isinstance(msg, ToolMessage):
                    tool_call_name = msg.name
                    final_response = msg.content    
    return tool_call_name, final_response


if __name__ == "__main__":    
    while True:
        user_input = input("User :")
        inputs = {"messages": [{"role": "user", "content": user_input}]}
        stream = agent.invoke(inputs, stream_mode="updates")
        tool_call_name, final_response = parse_response(stream)
        print("tool called: ", tool_call_name)
        print("response: ", final_response)