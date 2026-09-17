from sqlalchemy.orm import Session
from sqlalchemy import select
from datetime import datetime

from models.workspace import Workspace
from models.workspace_member import WorkspaceMember, Permission
from models.user import User
from models.transaction import Transaction

import services.workspace_member_services as serv_wsm
import services.user_services as serv_usr




def get_debts(session: Session, workspace_id: int):
    workspace = get_workspace(session, workspace_id)

    return [
        (member, serv_wsm.get_debt(session, member.id))
        for member in workspace.members
        if member.active
    ]

def get_transactions(
    session: Session,
    workspace_id: int,
    include_deleted: bool = False
):
    workspace = get_workspace(session, workspace_id)

    transactions = list(workspace.transactions)

    if not include_deleted:
        transactions = [
            transaction
            for transaction in transactions
            if transaction.deleted_at is None
        ]

    return transactions



def get_users(session: Session, workspace_id: int):
    workspace = get_workspace(session, workspace_id)
    return [
        member.user
        for member in workspace.members
        if member.active
    ]

# returns the user list of the workspace except for the workspace member who calls the function
# relevant for adding an expense
def get_other_users(session: Session, workspace_id: int, user_id: int):
    return [
        user
        for user in get_users(session, workspace_id)
        if user.id != user_id
    ]

# returns users, which are not in the WS yet
def get_available_users(session: Session, workspace_id: int):
    workspace = get_workspace(session, workspace_id)

    members_ids = [
        member.user_id
        for member in workspace.members
        if member.active
    ]

    query = select(User).where(
        ~User.id.in_(members_ids)
    )

    return session.scalars(query).all()




def create_workspace(
    session: Session,
    name: str,
    description: str,
    user_id: int
):
    user = session.get(User, user_id)

    if user is None:
        raise ValueError("User not found.")

    workspace = Workspace(
        name=name,
        description=description,
        created_at= datetime.now()
    )

    session.add(workspace)
    session.flush()

    member = WorkspaceMember(
        user_id=user_id,
        workspace_id=workspace.id,
        permission=Permission.ADMIN,
        active=True
    )

    session.add(member)
    session.commit()
    session.refresh(workspace)

    return workspace

def get_workspace(session: Session, workspace_id: int):
    workspace = session.get(Workspace, workspace_id)

    if workspace is None:
        raise ValueError("Workspace not found.")

    if not workspace.active:
        raise ValueError("Workspace is inactive.")

    return workspace

def update_workspace(
    session: Session,
    workspace_id: int,
    user_id: int,
    name: str,
    description: str
):
    workspace = get_workspace(session, workspace_id)

    requester = serv_usr.get_workspace_member(
        session,
        user_id,
        workspace_id
    )

    if requester is None:
        raise ValueError("User is not a member of this workspace.")

    if requester.permission != Permission.ADMIN:
        raise ValueError(
            "Only workspace admins can update the workspace."
        )

    workspace.name = name
    workspace.description = description

    session.commit()
    session.refresh(workspace)

    return workspace

def delete_workspace(session: Session, workspace_id: int, user_id: int):
    workspace = get_workspace(session, workspace_id)


    requester = serv_usr.get_workspace_member(
        session,
        user_id,
        workspace_id
    )

    if requester is None:
        raise ValueError("User is not a member of this workspace.")

    if requester.permission != Permission.ADMIN:
        raise ValueError(
            "Only workspace admins can delete the workspace."
        )

    workspace.active = False

    for member in workspace.members:
        member.active = False

    now = datetime.now()

    for transaction in workspace.transactions:
        if transaction.deleted_at is None:
            transaction.deleted_at = now
            transaction.deleted_by = requester.id

    session.commit()


