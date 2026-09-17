from sqlalchemy import String, Enum
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.orm import relationship
from enum import Enum as PyEnum
from sqlalchemy import DateTime
from datetime import datetime

from models.base import Base

class Role(PyEnum):
    USER = "user"
    ADMIN = "admin"

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    login: Mapped[str] = mapped_column(String(100), unique=True)
    password_hash: Mapped[str] = mapped_column(String(255))
    created_at: Mapped[datetime] = mapped_column(DateTime)
    role: Mapped[Role] = mapped_column(
                                        Enum(Role))

###
    accounts = relationship("Account", back_populates="owner")

    derived_workspace_members = relationship("WorkspaceMember", back_populates="user")

    #workspaces = relationship() # kinda a two-level relationship, as we needa get all the workspace_members with user_in == user.id, and from there find the worksp.id
    #transactions = relationship() # same idea, also access through workspace_member
    #as_deleter = relationship() # 2-level again as we need to see which transactions they deleted