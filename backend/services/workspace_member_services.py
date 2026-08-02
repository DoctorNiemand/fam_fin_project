from sqlalchemy.orm import Session
from sqlalchemy import select

from models.workspace import Workspace
from models.workspace_member import WorkspaceMember
from models.user import User
from models.transaction import Transaction


def get_debt(member: WorkspaceMember):
	debt = 0 
	for trans in member.as_source:
		debt -= trans.amount
	for trans in member.as_beneficiary:
		debt += trans.amount
	return debt
