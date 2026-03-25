from backend.state import State
from langgraph.graph import StateGraph
from backend.emotion_classification.emotion_classification import emotion_classification_agent
from backend.final_model.ai_agent import responce_to_user, therapist
from backend.fisrt_layer.agent import agent
from backend.safety_check.safety import safety_check, safety_defy


def Agent_build():
    graph = StateGraph(State)

    graph.add_node("first_layer_agent", agent)
    graph.add_node("safety_check", safety_check)
    graph.add_node("safety_defy", safety_defy)
    graph.add_node("emotion_classification_agent", emotion_classification_agent)
    graph.add_node("therapist", therapist)
    graph.add_node("responce_to_user", responce_to_user)
    
    # -------------------------
    # ENTRY POINT
    # -------------------------
    graph.set_entry_point("first_layer_agent")

    # -------------------------
    # FIRST LAYER ROUTING
    # -------------------------
    def route_first_layer(state: State):
        if state.get("category") == 0:
            return "direct_response"
        return "needs_help"

    graph.add_conditional_edges(
        "first_layer_agent",
        route_first_layer,
        {
            "direct_response": "responce_to_user",
            "needs_help": "safety_check",
        }
    )

    # -------------------------
    # SAFETY FLOW
    # -------------------------
    graph.add_edge("safety_check", "safety_defy")

    def route_safety(state: State):
        if state.get("threat_level") == "HIGH":
            return "emergency"
        return "safe"

    graph.add_conditional_edges(
        "safety_defy",
        route_safety,
        {
            "emergency": "responce_to_user",  # terminate graph
            "safe": "emotion_classification_agent",
        }
    )

    # -------------------------
    # THERAPY FLOW
    # -------------------------
    graph.add_edge("emotion_classification_agent", "therapist")
    
    graph.add_edge("therapist", "responce_to_user")
    
    def therapy_route(state: State):
        if bool(state.get("temp_completion")) is False:
            return "depression_therapy"
        return "general_therapy"
    graph.add_conditional_edges("responce_to_user", therapy_route,
                                {
                                    "depression_therapy": "therapist",
                                    "general_therapy": "first_layer_agent",
                                })

    return graph.compile()


if __name__ == "__main__":
    app = Agent_build()
    query = input("Enter user query: ")
    result = app.invoke(
        {
            "session_id": "",
            "user_id": "",

            "query": query,
            "history": [],

            "category": 0,

            "safety_response": {},
            "threat_level": "",

            "emotions": [],


            "responce": {},
            "temp_context": "",
            "temp_completion": True,
            "temp_history": [],


            "error": "",
            "trace_id": "",
        }
    )
