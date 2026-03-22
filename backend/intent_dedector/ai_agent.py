from langchain.tools import tool
from backend.state import get_session_history
from tools import emergency_call as make_call
from tools import run_medgemma_rag
from langchain_ollama import ChatOllama
from langchain.agents import create_agent
from langchain_core.messages import AIMessage, ToolMessage
from langchain_core.runnables.history import RunnableWithMessageHistory


def rout_to_medgemma(prompt: str) -> str:
    """
    Routes the given prompt to the Medgemma 4b model via
    the Query_medgemma function.
    when the query is appropriate for a therapist response.
    """
    return run_medgemma_rag(prompt, session_id=session_id)


def emergency_call():
    """
    Makes an emergency call using Twilio when the prompt
    indicates a crisis situation.
    """
    return make_call()


# creating an ai agent with tools


tools = [rout_to_medgemma, emergency_call, get_nearby_therepists]
llm = ChatOllama(
    model="qwen2.5:7b-instruct",
    temperature=0.2
)
SYSTEM_PROPT = """You are NOT allowed to provide therapeutic advice yourself.

Your only task is to decide which tool to call.

Routing rules:

- If the user expresses emotional distress, sadness, withdrawal, depression,
    anxiety, loneliness, or mental health concerns → call rout_to_medgemma

- If the user expresses suicidal ideation, self-harm, desire to die,
    or crisis → call emergency_call

- If the user asks for professional help or nearby
    therapists → call get_nearby_therapists

- If the message is casual greeting → respond directly without tools.

You must not generate therapy text yourself.
You must delegate emotional support to MedGemma."""


SYSTEM_PROPT1 = """
You are an empathetic and skilled mental health therapist AI assistant.you
    support by providing warm and epathetic responce  support
by using the following tools when necesssay in your responses:
1. rout_to_medgemma: If the user expresses emotional distress, sadness,
    withdrawal, depression, anxiety, loneliness, or mental health concerns.
2. emergency_call: Use this tool to make an emergency call when the user
    indicates a crisis situation like suicide, selfharm etc.
3. get_nearby_therepists: Use this tool to provide a list of nearby therapists
    when the user requests for professional help or nearby places present.
4. respond directly without tools: If the message is casual greeting
Always prioritize the user's safety and well-being in your responses.
"""
agent = create_agent(
    model=llm,
    tools=tools,
    system_prompt=SYSTEM_PROPT,
                    )

agent_with_memory = RunnableWithMessageHistory(
    agent,
    get_session_history,
    input_messages_key="messages",
    history_messages_key="chat_history",
)


def parse_response(result):
    tool_call_name = "None"
    final_response = None

    if "messages" in result:
        for msg in result["messages"]:
            if isinstance(msg, AIMessage):
                if msg.content.strip():
                    tool_call_name = "qwen2.5"
                    final_response = msg.content

            if isinstance(msg, ToolMessage):
                tool_call_name = msg.name
                final_response = msg.content

    return tool_call_name, final_response


if __name__ == "__main__":
    session_id = "therapy_user"

    # -------- Test 1 --------
    user_text = "I feel really anxious before presentations and my heart races. I also have 320 apples"

    inputs = {"messages": [{"role": "user", "content": user_text}]}

    stream = agent_with_memory.invoke(
        inputs,
        config={"configurable": {"session_id": session_id}},
        stream_mode="updates"
    )

    tool_call_name, final_response = parse_response(stream)

    print("\n--- TEST 1 ---")
    print("User:", user_text)
    print("Tool called:", tool_call_name)
    print("Response:", final_response)

    # -------- Test 2 --------
    user_text = "how many apples do i have"

    inputs = {"messages": [{"role": "user", "content": user_text}]}

    stream = agent_with_memory.stream(
        inputs,
        config={"configurable": {"session_id": session_id}},
        stream_mode="updates",
    )

    tool_call_name, final_response = parse_response(stream)

    print("\n--- TEST 2 ---")
    print("User:", user_text)
    print("Tool called:", tool_call_name)
    print("Response:", final_response)
