from typing import List, Optional, Dict
from typing_extensions import TypedDict


class State(TypedDict, total=False):
    # Identity
    session_id: str
    user_id: str

    # Conversation
    query: str
    history: List[Dict]
    
    #fisrt layer
    category: int
    
    # Safety
    safety_response: Dict
    threat_level: str
    
    # emotion classification
    emotions: List[str]

    # Therapy
    responce: Dict
    temp_context: str
    temp_completion: bool
    temp_history: List[Dict]

    # Observability
    error: Optional[str]
    trace_id: Optional[str]
