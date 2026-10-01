from sqlalchemy.orm import Session
from sqlalchemy import select
from datetime import datetime

from models.workspace import Workspace
from models.workspace_member import WorkspaceMember, Permission
from models.user import User
from models.transaction import Transaction, Currency

import services.user_services as serv_usr


def get_debt(session: Session, member_id: int):
	member = session.get(WorkspaceMember, member_id)

	if member is None:
		raise ValueError("Workspace member not found.")

	debt_usd = 0
	debt_eur = 0
	debt_rub = 0

	for trans in member.as_source:
		if trans.deleted_at is not None:
			continue

		if trans.currency == Currency.USD:
			debt_usd -= trans.amount
		elif trans.currency == Currency.EUR:
			debt_eur -= trans.amount
		elif trans.currency == Currency.RUB:
			debt_rub -= trans.amount

	for trans in member.as_beneficiary:
		if trans.deleted_at is not None:
			continue

		if trans.currency == Currency.USD:
			debt_usd += trans.amount
		elif trans.currency == Currency.EUR:
			debt_eur += trans.amount
		elif trans.currency == Currency.RUB:
			debt_rub += trans.amount

	return debt_usd, debt_eur, debt_rub

def get_pair_debt(session: Session, caller_member_id: int, object_member_id: int):
	caller_member = session.get(WorkspaceMember, caller_member_id)
	object_member = session.get(WorkspaceMember, object_member_id)
	if not caller_member or not object_member:
		raise ValueError("Workspace member not found.")
	if not caller_member.workspace_id == object_member.workspace_id:
		raise ValueError("Members do not belong to the same workspace.")

	debt_usd = 0
	debt_eur = 0
	debt_rub = 0

	if caller_member.active and object_member.active:
		for trans in caller_member.as_source:
			if trans.deleted_at is not None:
				continue
			if trans.beneficiary_workspace_member == object_member_id:
				if trans.currency == Currency.USD:
					debt_usd -= trans.amount
				elif trans.currency == Currency.EUR:
					debt_eur -= trans.amount
				elif trans.currency == Currency.RUB:
					debt_rub -= trans.amount

		for trans in caller_member.as_beneficiary:
			if trans.deleted_at is not None:
				continue
			if trans.source_workspace_member == object_member_id:
				if trans.currency == Currency.USD:
					debt_usd += trans.amount
				elif trans.currency == Currency.EUR:
					debt_eur += trans.amount
				elif trans.currency == Currency.RUB:
					debt_rub += trans.amount

	return debt_usd, debt_eur, debt_rub

def get_all_pair_debts(session: Session, caller_member_id: int):
	caller_member = session.get(WorkspaceMember, caller_member_id)
	if not caller_member:
		raise ValueError("Workspace member not found.")

	workspace = caller_member.workspace

	members_and_debts = []
	for member in workspace.members:
		if member.id != caller_member_id:
			debts = get_pair_debt(session, caller_member.id, member.id)
			members_and_debts.append((member, debts))

	return members_and_debts

def get_ws_member(
	session: Session,
	workspace_id: int,
	member_user_id: int
):
	member = session.get(WorkspaceMember, member_user_id)
	if member is None:
		raise ValueError("Workspace member not found.")
	if member.workspace_id != workspace_id:
		raise ValueError("Workspace member does not belong to the workspace.")
	if not member.active:
		raise ValueError("Workspace member is not active.")
	return member

def add_ws_member(
	session: Session,
	workspace_id: int,
	member_user_id: int,
	permission: Permission,
	user_id: int
):
	workspace = session.get(Workspace, workspace_id)

	if workspace is None:
		raise ValueError("Workspace not found.")

	requester = serv_usr.get_workspace_member(
		session,
		user_id,
		workspace_id
	)

	if requester is None:
		raise ValueError("User is not a member of this workspace.")

	if requester.permission != Permission.ADMIN:
		raise ValueError("Only workspace admins can add members.")

	target_user = session.get(User, member_user_id)

	if target_user is None:
		raise ValueError("User not found.")

	existing_member = session.scalar(
		select(WorkspaceMember).where(
			WorkspaceMember.user_id == member_user_id,
			WorkspaceMember.workspace_id == workspace_id
		)
	)

	if existing_member is not None:

		if existing_member.active:
			raise ValueError(
				"User is already a member of this workspace."
			)

		existing_member.active = True
		existing_member.permission = permission

		session.commit()
		session.refresh(existing_member)

		return existing_member

	member = WorkspaceMember(
		user_id=member_user_id,
		workspace_id=workspace_id,
		permission=permission,
		active=True
	)

	session.add(member)
	session.commit()
	session.refresh(member)

	return member

def update_ws_member(
	session: Session,
	workspace_id: int,
	member_user_id: int,
	user_id: int,
	permission: Permission
):
	workspace = session.get(Workspace, workspace_id)

	if workspace is None:
		raise ValueError("Workspace not found.")

	requester = serv_usr.get_workspace_member(
		session,
		user_id,
		workspace_id
	)

	if requester is None:
		raise ValueError("User is not a member of this workspace.")

	if requester.permission != Permission.ADMIN:
		raise ValueError("Only workspace admins can change permissions.")

	member = serv_usr.get_workspace_member(
		session,
		member_user_id,
		workspace_id
	)

	if member is None:
		raise ValueError("User is not a member of this workspace.")

	member.permission = permission

	session.commit()
	session.refresh(member)
	return member

def delete_ws_member(
	session: Session,
	workspace_id: int,
	member_user_id: int,
	user_id: int
):
	workspace = session.get(Workspace, workspace_id)

	if workspace is None:
		raise ValueError("Workspace not found.")

	requester = serv_usr.get_workspace_member(
		session,
		user_id,
		workspace_id
	)

	if requester is None:
		raise ValueError("User is not a member of this workspace.")

	if requester.permission != Permission.ADMIN:
		raise ValueError("Only workspace admins can remove members.")

	if member_user_id == user_id:
		raise ValueError("You cannot remove yourself from the workspace.")

	member = serv_usr.get_workspace_member(
		session,
		member_user_id,
		workspace_id
	)

	if member is None:
		raise ValueError("User is not a member of this workspace.")

	member.active = False

	now = datetime.now()

	for tr in member.as_source:
		if tr.deleted_at is None:
			tr.deleted_at = now
			tr.deleted_by = requester.id

	for tr in member.as_beneficiary:
		if tr.deleted_at is None:
			tr.deleted_at = now
			tr.deleted_by = requester.id

	session.commit()

# def is_admin(session: Session, workspace_id:int, member_id: int) -> bool:
# 	query = select(WorkspaceMember).where(WorkspaceMember.id == member_id, WorkspaceMember.workspace_id == workspace_id)
# 	wsm = session.scalar(query)
# 	return (wsm.permission == Permission.ADMIN)

# def can_write(session: Session, workspace_id:int, member_id: int) -> bool:
# 	query = select(WorkspaceMember).where(WorkspaceMember.id == member_id, WorkspaceMember.workspace_id == workspace_id)
# 	wsm = session.scalar(query)
# 	return (wsm.permission == Permission.ADMIN or wsm.permission == Permission.WRITE)
	