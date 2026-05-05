import logging
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.database import get_session_factory
from app.db.models import Conversation, Message
from app.graph.graph import build_graph
from app.graph.state import GraphState
from app.api.schemas import (
    ConversationOut,
    ConversationListItem,
    ConversationListOut,
    ConversationCreateOut,
    SendMessageIn,
    MessageResponse,
    MessageOut,
    DeleteOut,
)

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/conversations", tags=["conversations"])

_graph = None


def _get_graph():
    global _graph
    if _graph is None:
        _graph = build_graph()
    return _graph


def _get_db():
    factory = get_session_factory()
    db = factory()
    try:
        yield db
    finally:
        db.close()


def _to_message_out(msg: Message) -> MessageOut:
    return MessageOut(
        id=msg.id,
        conversation_id=msg.conversation_id,
        role=msg.role,
        content=msg.content,
        emotion=msg.emotion,
        expression=msg.expression,
        created_at=msg.created_at,
    )


@router.post("", response_model=ConversationCreateOut, status_code=201)
def create_conversation(db: Session = Depends(_get_db)):
    conv = Conversation()
    db.add(conv)
    db.commit()
    db.refresh(conv)
    return conv


@router.get("", response_model=ConversationListOut)
def list_conversations(db: Session = Depends(_get_db)):
    convs = (
        db.query(Conversation)
        .order_by(Conversation.updated_at.desc())
        .all()
    )
    items = [
        ConversationListItem(
            id=c.id,
            title=c.title,
            created_at=c.created_at,
            updated_at=c.updated_at,
        )
        for c in convs
    ]
    return ConversationListOut(conversations=items)


@router.get("/{conv_id}", response_model=ConversationOut)
def get_conversation(conv_id: str, db: Session = Depends(_get_db)):
    conv = db.query(Conversation).filter(Conversation.id == conv_id).first()
    if not conv:
        raise HTTPException(status_code=404, detail="Conversation not found")
    return ConversationOut(
        id=conv.id,
        title=conv.title,
        created_at=conv.created_at,
        updated_at=conv.updated_at,
        messages=[_to_message_out(m) for m in conv.messages],
    )


@router.delete("/{conv_id}", response_model=DeleteOut)
def delete_conversation(conv_id: str, db: Session = Depends(_get_db)):
    conv = db.query(Conversation).filter(Conversation.id == conv_id).first()
    if not conv:
        raise HTTPException(status_code=404, detail="Conversation not found")
    db.delete(conv)
    db.commit()
    return DeleteOut()


@router.post("/{conv_id}/messages", response_model=MessageResponse)
def send_message(
    conv_id: str,
    body: SendMessageIn,
    db: Session = Depends(_get_db),
):
    conv = db.query(Conversation).filter(Conversation.id == conv_id).first()
    if not conv:
        raise HTTPException(status_code=404, detail="Conversation not found")

    # Persist user message
    user_msg = Message(
        conversation_id=conv_id,
        role="user",
        content=body.content,
    )
    db.add(user_msg)

    # Build history as list of {role, content} dicts
    history = [
        {"role": m.role, "content": m.content}
        for m in conv.messages
    ]

    # Run LangGraph
    graph = _get_graph()
    state: GraphState = {
        "conversation_id": conv_id,
        "user_message": body.content,
        "history_messages": history,
        "response_text": "",
        "emotion": "",
        "expression": "",
    }
    result = graph.invoke(state)

    # Persist assistant message
    assistant_msg = Message(
        conversation_id=conv_id,
        role="assistant",
        content=result["response_text"],
        emotion=result["emotion"],
        expression=result["expression"],
    )
    db.add(assistant_msg)

    # Update conversation title if it's the first exchange
    if len(conv.messages) == 0:
        conv.title = body.content[:50]

    db.commit()
    db.refresh(user_msg)
    db.refresh(assistant_msg)

    return MessageResponse(
        message=_to_message_out(user_msg),
        response=_to_message_out(assistant_msg),
    )
