from database import Base
from enum import Enum as PyEnum
from sqlalchemy import Boolean, Column, Integer, String, Enum, ForeignKey

class AttachmentEnum(PyEnum):
    PHOTO = 1
    VIDEO = 2

"""
Model for attachments representation
"""
class Attachment(Base):
    __tablename__ = 'attachments'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    path = Column(String, unique=True, index=True, comment="Resource path")
    type = Column(Enum(AttachmentEnum), nullable=False, comment="Type of attachment")
    message = Column('message_id', Integer, ForeignKey('messages.id'), comment="Attachment's message")
    is_deleted = Column(Boolean, default=False, comment="Soft delete for model")