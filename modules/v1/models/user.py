from sqlalchemy import Boolean, Column, Integer, String, Table, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String(length=255))
    is_deleted = Column(Boolean, default=False)

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