from sqlalchemy.orm import Session
from sqlalchemy import select, or_

from models.workspace import Workspace
from models.workspace_member import WorkspaceMember
from models.user import User
from models.transaction import Transaction
from models.account import Account


import services.workspace_member_services as serv_wsm


def get_user(session: Session, user_id: int):
	user = session.get(User, user_id)

	if user is None:
		raise ValueError("User not found.")

	return user

def get_workspaces(session: Session, user_id: int):
	query = select(Workspace).join(WorkspaceMember).where(
		WorkspaceMember.user_id == user_id,
		WorkspaceMember.active.is_(True),
		Workspace.active.is_(True)
	)
	return session.scalars(query).all()

def get_transactions(
	session: Session,
	user_id: int,
	include_deleted: bool = False
):
	user = session.get(User, user_id)

	if user is None:
		raise ValueError("User not found.")

	query = (
		select(Transaction)
		.join(
			WorkspaceMember,
			(WorkspaceMember.id == Transaction.source_workspace_member)
			| (WorkspaceMember.id == Transaction.beneficiary_workspace_member)
		)
		.where(
			WorkspaceMember.user_id == user_id,
			WorkspaceMember.active.is_(True)
		)
		.distinct()
	)

	if not include_deleted:
		query = query.where(Transaction.deleted_at.is_(None))

	return session.scalars(query).all()

def get_cumulative_debt(session: Session, user_id: int):
	user = session.get(User, user_id)

	if user is None:
		raise ValueError("User not found.")

	debt_usd = 0
	debt_eur = 0
	debt_rub = 0

	for member in user.derived_workspace_members:
		member_debt_usd, member_debt_eur, member_debt_rub = \
			serv_wsm.get_debt(session, member.id)

		debt_usd += member_debt_usd
		debt_eur += member_debt_eur
		debt_rub += member_debt_rub

	return debt_usd, debt_eur, debt_rub

def get_workspace_pair_debts(session: Session, user_id: int, workspace_id: int):
	caller_member = get_workspace_member(session, user_id, workspace_id)
	if not caller_member:
		raise ValueError("Workspace member not found.")
	return serv_wsm.get_all_pair_debts(session, caller_member.id)

def get_cumulative_pair_debt(session: Session, caller_user_id: int, object_user_id: int):
	caller_user = get_user(session, caller_user_id)
	object_user = get_user(session, object_user_id)

	debt_usd = 0
	debt_eur = 0
	debt_rub = 0

	for wsm in caller_user.derived_workspace_members:
		for member, (debt_usd_ws,debt_eur_ws,debt_rub_ws) in serv_wsm.get_all_pair_debts(session, wsm.id):
			if member.user_id == object_user_id:
					debt_usd += debt_usd_ws
					debt_eur += debt_eur_ws
					debt_rub += debt_rub_ws

	return debt_usd, debt_eur, debt_rub 

def get_all_cumulative_pair_debts(
	session: Session,
	caller_user_id: int
):
	caller_user = get_user(session, caller_user_id)

	cumulative_debts = []

	users = session.scalars(
		select(User)
		.where(User.id != caller_user_id)
	).all()

	for user in users:
		debt_usd, debt_eur, debt_rub = get_cumulative_pair_debt(
			session,
			caller_user_id,
			user.id
		)

		cumulative_debts.append(
			(user, (debt_usd, debt_eur, debt_rub))
		)

	return cumulative_debts

def get_workspace_member(session: Session, user_id: int, workspace_id: int):
	query = select(WorkspaceMember).where(
		WorkspaceMember.user_id == user_id,
		WorkspaceMember.workspace_id == workspace_id,
		WorkspaceMember.active == True
	)
	return session.scalar(query)

def get_accounts(session: Session, user_id: int):
	user = session.get(User, user_id)

	if user is None:
		raise ValueError("User not found.")

	query = select(Account).where(
		Account.owner_id == user_id
	)

	return session.scalars(query).all()

def get_account(
	session: Session,
	account_id: int,
	user_id: int
):
	account = session.get(Account, account_id)
	if account is None:
		raise ValueError("Account not found.")
	if account.owner_id != user_id:
		raise ValueError("Account does not belong to the user.")
	return account


def require_workspace_member(session: Session, user_id: int, workspace_id: int):
	member = get_workspace_member(session, user_id, workspace_id)
	if member is None:
		raise ValueError("User is not a member of this workspace.")
	return member

