from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.orm import relationship

from models.base import Base

class Transaction(Base):
	__tablename__ = "transactions"

	id: Mapped[int] = mapped_column(primary_key=True)
	created_at: Mapped[str] = mapped_column(String(80)) # some date format
	description: Mapped[str] = mapped_column(String(255))
	transact_type: Mapped[str] = mapped_column(String(255)) # here lets make some enum presets like transfer to someone else directly / payment 	
	workspace_id: Mapped[int] = mapped_column(ForeignKey("workspaces.id"))
	deleted_by: Mapped[int] = mapped_column(ForeignKey("workspace_members.id")) # workspace_member.id
	deleted_at: Mapped[str] = mapped_column(String(80)) # some date format 
	amount: Mapped[float] = mapped_column() # or what shall the right number be
	currency: Mapped[str] = mapped_column(String(50)) # here lets make some enum presets like usd / eur/ rub	
	beneficiary_acc: Mapped[int] = mapped_column(ForeignKey("accounts.id")) # account.id
	source_acc: Mapped[int] = mapped_column(ForeignKey("accounts.id")) # account.id
	beneficiary_workspace_member: Mapped[int] = mapped_column(ForeignKey("workspace_members.id")) # workspace_member.id
	source_workspace_member: Mapped[int] = mapped_column(ForeignKey("workspace_members.id")) # workspace_member.id
	data_source: Mapped[str] = mapped_column(String(50)) # here lets make some enum presets like manual / csv / api	


	benef_acc = relationship("Account", foreign_keys=[beneficiary_acc], back_populates = "as_beneficiary")
	sou_acc = relationship("Account", foreign_keys=[source_acc], back_populates ="as_source")

	benef_worksp_memb = relationship("WorkspaceMember", 
									foreign_keys=[beneficiary_workspace_member],
									back_populates = "as_beneficiary")
	sou_worksp_memb= relationship("WorkspaceMember", 
									foreign_keys=[source_workspace_member],
									back_populates = "as_source") # how does the mapping work here with severla foreignkeys from same table lol

	workspace = relationship("Workspace", back_populates = "transactions")

	#deleter = relationship() # 2-level stuff again, as must go up to the user