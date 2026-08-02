from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.orm import relationship

from models.base import Base

class WorkspaceMember(Base):
	__tablename__ = "workspace_members"

	id: Mapped[int] = mapped_column(primary_key=True)
	permission: Mapped[str] = mapped_column(String(100)) # enumereate
	workspace_id: Mapped[int] = mapped_column(ForeignKey("workspaces.id"))
	user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

	user = relationship("User", back_populates="derived_workspace_members")
	workspace = relationship("Workspace", back_populates="members")

	as_beneficiary = relationship("Transaction",  foreign_keys="Transaction.beneficiary_workspace_member", back_populates = "benef_worksp_memb")
	as_source = relationship("Transaction", foreign_keys="Transaction.source_workspace_member", back_populates = "sou_worksp_memb")