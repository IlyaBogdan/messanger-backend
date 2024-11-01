from database import Base
from sqlalchemy.orm import relationship
from modules.v1.models.chat_event import ChatEvent
from sqlalchemy import Boolean, Column, Integer, String, Table, ForeignKey

"""
Model for chats representation
"""
class Chat(Base):
    __tablename__ = 'chats'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String, unique=True, index=True, comment="Title of chat")
    is_deleted = Column(Boolean, default=False, comment="Soft delete for model")

    """List of events in this chat"""
    events = relationship(
        "ChatEvent",
        secondary="events_association",
        primaryjoin="Chat.id==events_association.c.chat_id",
        backref="chat_events",
    )

    """List of users in this chat"""
    users = relationship(
        "User",
        secondary="users_association",
        primaryjoin="Chat.id==users_association.c.chat_id",
        backref="chats",
    )

"""
One-to-many table for chat's users
"""
users_association = Table(
    'users_association',
    Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id'), primary_key=True, comment="User in chat"),
    Column('chat_id', Integer, ForeignKey('chats.id'), primary_key=True, comment="Chat")
)

"""
One-to-many table for chat's events
"""
events_association = Table(
    'events_association',
    Base.metadata,
    Column('event_id', Integer, ForeignKey('chat_events.id'), primary_key=True, comment="Chat's event"),
    Column('chat_id', Integer, ForeignKey('chats.id'), primary_key=True, comment="Chat")
)