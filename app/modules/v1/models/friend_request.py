import datetime
from database import Base
from enum import IntEnum
from sqlalchemy.orm import Session
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, ForeignKey, UniqueConstraint, DateTime, event, CheckConstraint

class FriendRequestStatus(IntEnum):
    WAITING = 0
    APPROVED = 1
    REJECTED = 2

"""
Model for friend request
"""
class FriendRequest(Base):
    __tablename__ = 'friend_requests'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    initiator_id = Column(Integer, ForeignKey('users.id'), index=True, comment="User, who want to add to friend")
    receiver_id = Column(Integer, ForeignKey('users.id'), index=True, comment="Reciever of friend request")
    status = Column(Integer, nullable=False, comment="Status of request", default=FriendRequestStatus.WAITING)
    created_at = Column(DateTime, default=datetime.datetime.now(datetime.timezone.utc), nullable=False)
    updated_at = Column(DateTime, default=datetime.datetime.now(datetime.timezone.utc), nullable=False)

    initiator = relationship("User", foreign_keys=[initiator_id], backref="sent_friend_requests")
    receiver = relationship("User", foreign_keys=[receiver_id], backref="received_friend_requests")

    __table_args__ = (
        UniqueConstraint('initiator_id', 'receiver_id', name='uq_initiator_receiver'),
        CheckConstraint(f"status IN ({FriendRequestStatus.WAITING}, {FriendRequestStatus.APPROVED}, {FriendRequestStatus.REJECTED})", name="check_status"),
    )

@event.listens_for(FriendRequest, 'before_update')
def receive_before_update(mapper, connection: Session, target: FriendRequest):
    target.updated_at = datetime.datetime.now(datetime.timezone.utc)