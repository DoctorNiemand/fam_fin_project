from sqlalchemy import String, ForeignKey, Enum, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.orm import relationship
from enum import Enum as PyEnum

from models.base import Base


class Permission(PyEnum):
	READ = "read"
	WRITE = "write"
	ADMIN = "admin"


class WorkspaceMember(Base):
	__tablename__ = "workspace_members"
	__table_args__ = (
		UniqueConstraint(
			"workspace_id",
			"user_id",
			name="uq_workspace_member"
		),
	)

	id: Mapped[int] = mapped_column(primary_key=True)
	permission: Mapped[Permission] = mapped_column(
    								Enum(Permission))
	workspace_id: Mapped[int] = mapped_column(ForeignKey("workspaces.id"))
	user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
	active: Mapped[bool] = mapped_column(default=True, nullable= False)

###
	user = relationship("User", back_populates="derived_workspace_members")
	workspace = relationship("Workspace", back_populates="members")

	as_beneficiary = relationship("Transaction",  foreign_keys="Transaction.beneficiary_workspace_member", back_populates = "benef_worksp_memb")
	as_source = relationship("Transaction", foreign_keys="Transaction.source_workspace_member", back_populates = "sou_worksp_memb")