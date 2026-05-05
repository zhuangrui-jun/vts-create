import json
import logging
import os
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from openai import OpenAI

from app.db.database import get_session_factory
from app.db.models import Conversation, Message
from app.config.emotion_mapping import resolve_expression, normalize_emotion
from app.api.schemas import (
    ConversationOut,
    ConversationListItem,
    ConversationListOut,
    ConversationCreateOut,
    SendMessageIn,
    MessageOut,
    DeleteOut,
)

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/conversations", tags=["conversations"])

SYSTEM_PROMPT = os.environ.get(
    "CHARACTER_PERSONA",
    "你是一个温柔、优雅的AI角色。用中文回复，语气亲切自然。",
)

EMOTION_PROMPT = """根据你上一条回复的内容，判断角色当前的情绪状态。
只能从以下选项中选择一个：happy, very_happy, embarrassed, sad, neutral

只输出情绪标签，不要输出其他内容。"""


def _get_llm_client():
    return OpenAI(
        api_key=os.environ.get("OPENAI_API_KEY"),
        base_url=os.environ.get("OPENAI_BASE_URL", "https://api.openai.com/v1"),
    )


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


def _extract_emotion(response_text: str) -> str:
    client = _get_llm_client()
    model = os.environ.get("OPENAI_MODEL", "gpt-4o-mini")
    emotion_response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": EMOTION_PROMPT},
            {"role": "user", "content": response_text},
        ],
        temperature=0.3,
        max_tokens=16,
    )
    raw = emotion_response.choices[0].message.content or "neutral"
    return normalize_emotion(raw)


@router.post("/{conv_id}/messages")
def send_message_stream(
    conv_id: str,
    body: SendMessageIn,
    db: Session = Depends(_get_db),
):
    conv = db.query(Conversation).filter(Conversation.id == conv_id).first()
    if not conv:
        raise HTTPException(status_code=404, detail="Conversation not found")

    # Persist user message immediately
    user_msg = Message(
        conversation_id=conv_id,
        role="user",
        content=body.content,
    )
    db.add(user_msg)

    # Update conversation title if first exchange
    is_first = len(conv.messages) == 0
    if is_first:
        conv.title = body.content[:50]

    db.commit()
    db.refresh(user_msg)

    # Build message history for LLM context
    history = [
        {"role": m.role, "content": m.content}
        for m in conv.messages
    ]
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    messages.extend(history)

    def generate():
        client = _get_llm_client()
        model = os.environ.get("OPENAI_MODEL", "gpt-4o-mini")

        # Send user message info first
        yield f"data: {json.dumps({'type': 'user_message', 'id': user_msg.id, 'content': user_msg.content, 'created_at': user_msg.created_at.isoformat()})}\n\n"

        # Stream LLM tokens
        full_text = ""
        stream = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=0.8,
            max_tokens=512,
            stream=True,
        )
        for chunk in stream:
            if not chunk.choices:
                continue
            delta = chunk.choices[0].delta
            if delta.content:
                full_text += delta.content
                yield f"data: {json.dumps({'type': 'token', 'content': delta.content})}\n\n"

        # Extract emotion from full response
        emotion = _extract_emotion(full_text)
        expression = resolve_expression(emotion)

        # Persist assistant message
        new_db = next(_get_db())
        try:
            assistant_msg = Message(
                conversation_id=conv_id,
                role="assistant",
                content=full_text,
                emotion=emotion,
                expression=expression,
            )
            new_db.add(assistant_msg)
            new_db.commit()
            new_db.refresh(assistant_msg)

            yield f"data: {json.dumps({'type': 'done', 'emotion': emotion, 'expression': expression, 'user_message_id': user_msg.id, 'assistant_message_id': assistant_msg.id})}\n\n"
        finally:
            new_db.close()

    return StreamingResponse(generate(), media_type="text/event-stream")
