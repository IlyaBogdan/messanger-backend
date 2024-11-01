from database import Base
from enum import Enum as PyEnum
from sqlalchemy.orm import relationship
from sqlalchemy import Boolean, Column, Integer, ForeignKey, Enum, Table

class ChatEventType(PyEnum):
    MESSAGE = 0
    CALL = 1

"""
Model for chat events representation
"""
class ChatEvent(Base):
    __tablename__ = 'chat_events'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    chat_id = Column(Integer, ForeignKey('chats.id'), comment="Event's chat")
    initiator_id = Column(Integer, ForeignKey('users.id'), comment="Event's initiator. Sender of message")
    receiver_id = Column(Integer, ForeignKey('users.id'), comment="Event's receiver. Receiver of message")
    type = Column(Enum(ChatEventType), nullable=False, comment="Type of event")
    browsed = Column(Boolean, default=False, comment="If receiver of event browsed this event")
    is_deleted = Column(Boolean, default=False, comment="Soft delete for model")

    chat = relationship("Chat", back_populates="events")
    initiator = relationship("User", foreign_keys=[initiator_id])
    receiver = relationship("User", foreign_keys=[receiver_id])

    """List of browsed this event users"""
    browsed_users = relationship(
        "User",
        secondary="browsed_users",
        primaryjoin="User.id==browsed_users.c.user_id",
        backref="browsed_events",
    )

"""
One-to-many table for list of browsed this event users
"""
browsed_users = Table(
    'browsed_users',
    Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id'), primary_key=True, comment="User in chat"),
    Column('event_id', Integer, ForeignKey('chat_events.id'), primary_key=True, comment="Chat event")
)