import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, Text, DateTime, Integer, ForeignKey
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


def _utcnow():
    return datetime.now(timezone.utc)


def _gen_uuid():
    return str(uuid.uuid4())


class Conversation(Base):
    __tablename__ = "conversations"

    id = Column(Text, primary_key=True, default=_gen_uuid)
    title = Column(Text, nullable=False, default="新对话")
    created_at = Column(DateTime, nullable=False, default=_utcnow)
    updated_at = Column(DateTime, nullable=False, default=_utcnow, onupdate=_utcnow)

    messages = relationship(
        "Message",
        back_populates="conversation",
        cascade="all, delete-orphan",
        order_by="Message.created_at",
    )


class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, autoincrement=True)
    conversation_id = Column(
        Text, ForeignKey("conversations.id", ondelete="CASCADE"), nullable=False
    )
    role = Column(Text, nullable=False)
    content = Column(Text, nullable=False)
    emotion = Column(Text, nullable=True)
    expression = Column(Text, nullable=True)
    created_at = Column(DateTime, nullable=False, default=_utcnow)

    conversation = relationship("Conversation", back_populates="messages")
