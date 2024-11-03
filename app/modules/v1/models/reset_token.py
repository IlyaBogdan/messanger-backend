from database import Base
import datetime
from sqlalchemy import DateTime, Column, Integer, String, Enum, ForeignKey

"""
Model for reset password token representation
"""
class ResetToken(Base):
    __tablename__ = 'reset_tokens'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    token = Column(String, unique=True, index=True, comment="Reset token value")
    expired_date = Column(DateTime, default=datetime.datetime.now(datetime.timezone.utc), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), comment="User, who reset password")