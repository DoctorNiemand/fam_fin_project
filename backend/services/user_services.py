from sqlalchemy.orm import Session
from sqlalchemy import select

from models.workspace import Workspace
from models.workspace_member import WorkspaceMember
from models.user import User

import workspace_member_services as wms



def get_workspaces (session: Session, user_id: int):
	query = select(User).where(User.id == user_id)
	user = session.scalar(query)
	return _get_workspaces(user)


def get_cumulative_debt (session: Session, user_id: int):
	query = select(User).where(User.id == user_id)
	user = session.scalar(query)
	return _get_cumulative_debt(user)


def _get_workspaces (user: User):
	return [member.workspace for member in user.derived_workspace_members]

def _get_cumulative_debt (user: User):
	debt = 0
	for member in user.derived_workspace_members:
		debt += wms.get_debt(member)
	return debt



