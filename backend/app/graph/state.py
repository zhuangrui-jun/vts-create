from typing import TypedDict


class GraphState(TypedDict):
    conversation_id: str
    user_message: str
    history_messages: list[dict]
    response_text: str
    emotion: str
    expression: str
