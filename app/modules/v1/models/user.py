from database import Base
from sqlalchemy.orm import relationship
from sqlalchemy import Boolean, Column, Integer, String, Table, ForeignKey

"""
Model for users representation
"""
class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String, unique=True, index=True, comment="The username chosen by the user")
    email = Column(String, unique=True, index=True, comment="User's email address")
    password = Column(String(length=255), comment="User's password")
    is_deleted = Column(Boolean, default=False, comment="Soft delete for model")

    """List of user's friends"""
    friends = relationship(
        "User",
        secondary="friends_association",
        primaryjoin="User.id==friends_association.c.user_id",
        secondaryjoin="User.id==friends_association.c.friend_id",
        backref="friend_of"
    )

"""
Many-to-many table for user friends
"""
friends_association = Table(
    'friends_association',
    Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id'), primary_key=True),
    Column('friend_id', Integer, ForeignKey('users.id'), primary_key=True)
)