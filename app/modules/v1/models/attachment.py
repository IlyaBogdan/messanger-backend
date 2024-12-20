from database import Base
from enum import IntEnum
from sqlalchemy import Boolean, Column, Integer, String, Enum, ForeignKey, CheckConstraint

class AttachmentEnum(IntEnum):
    PHOTO = 1
    VIDEO = 2

"""
Model for attachments representation
"""
class Attachment(Base):
    __tablename__ = 'attachments'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    path = Column(String, unique=True, index=True, comment="Resource path")
    type = Column(Integer, nullable=False, comment="Type of attachment")
    message = Column('message_id', Integer, ForeignKey('messages.id'), comment="Attachment's message")
    is_deleted = Column(Boolean, default=False, comment="Soft delete for model")

    __table_args__ = (
        CheckConstraint(f"status IN ({AttachmentEnum.PHOTO}, {AttachmentEnum.VIDEO})", name="check_type"),
    )