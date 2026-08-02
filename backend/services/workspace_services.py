from sqlalchemy.orm import Session
from sqlalchemy import select

from models.workspace import Workspace
from models.workspace_member import WorkspaceMember
from models.user import User


def get_users (session: Session, workspace_id: int):
	query = select(Workspace).where(Workspace.id == workspace_id)
	workspace = session.scalar(query)
	user_list = []
	for member in workspace.members:
		user_list.append(member.user)
	return user_list


