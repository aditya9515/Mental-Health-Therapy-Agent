from typing import List, Optional, Dict
from typing_extensions import TypedDict


class State(TypedDict, total=False):
    # Identity
    session_id: str
    user_id: Optional[str]

    # Conversation
    history: List[Dict[str, str]]

    # RAG
    query: str
    retrieved_docs: List[str]
    doc_metadata: List[Dict]

    # Embeddings
    query_embedding: Optional[List[float]]

    # Agent execution
    tool_calls: List[Dict]
    intermediate_steps: List[str]

    # Output
    final_answer: str
    confidence: Optional[float]

    # Config
    model_name: str
    temperature: float
    max_tokens: int

    # Observability
    error: Optional[str]
    trace_id: Optional[str]
