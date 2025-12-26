

#? Every model in sqlalchemy represents a table in the database

from datetime import datetime
from pydantic import Field
from sqlalchemy import Boolean, ForeignKey, String, TIMESTAMP, null
from sqlalchemy.orm import DeclarativeBase, mapped_column
# from .database import Base 
from sqlalchemy.sql.expression import text
from sqlalchemy.orm import Mapped, Relationship
from sqlalchemy.sql.functions import now
# from sqlalchemy.sql.expression import null

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True, nullable=False)
    email: Mapped[str] = mapped_column(nullable=False, unique=True)
    password: Mapped[str] = mapped_column(nullable=False)
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))

class Posts(Base):

    __tablename__ = "posts"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(30), nullable=False) #? Mapped[int] says “this attribute is mapped by SQLAlchemy, and when accessed on an instance it behaves like an int (or whatever type you put inside Mapped[...])
    content: Mapped[str] = mapped_column(String(30), nullable=False)
    is_published: Mapped[bool] = mapped_column(Boolean, server_default='FALSE', nullable=False)
    created_at : Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE", onupdate="CASCADE"), nullable=False)
    #! server_default is used to provide default value
    user = Relationship(User)


class Vote(Base):

    __tablename__ = 'votes'

    post_id: Mapped[int] = mapped_column(ForeignKey("posts.id", ondelete='CASCADE'), primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete='CASCADE'), primary_key=True)
    post = Relationship(Posts)