from typing import TypedDict, Optional


class GraphState(TypedDict):
    conversation_id: str
    user_message: str
    history_messages: list[dict]
    response_text: str
    emotion: str
    expression: str
    # Search tool fields
    assembled_messages: list[dict]
    search_query: Optional[str]
    search_results: Optional[str]
    needs_search: bool
