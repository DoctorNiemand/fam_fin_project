from sqlalchemy.orm import Session
from sqlalchemy import select

from models.workspace import Workspace
from models.workspace_member import WorkspaceMember
from models.user import User


import services.workspace_member_services as wms



def user_login(session: Session, login, password):
	query = select(User).where(User.login == login, User.password_hash == password)
	return session.scalar(query)


def get_users(session: Session):
    query = select(User)
    return session.scalars(query).all()