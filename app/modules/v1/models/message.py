from database import Base
from sqlalchemy import Column, Integer, String, ForeignKey

"""
Model for messages representation
"""
class Message(Base):
    __tablename__ = 'messages'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    event = Column('event_id', Integer, ForeignKey('chat_events.id'), comment="Message's event")
    message = Column(String, comment="Message content")