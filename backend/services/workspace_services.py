from sqlalchemy.orm import Session
from sqlalchemy import select
from datetime import datetime

from models.workspace import Workspace
from models.workspace_member import WorkspaceMember, Permission
from models.user import User
from models.transaction import Transaction, Currency, TransactionType
from models.settlement import Settlement, SettlementItem

import services.workspace_member_services as serv_wsm
import services.user_services as serv_usr


def get_debts(session: Session, workspace_id: int):
	workspace = get_workspace(session, workspace_id)
	return [
		(member, serv_wsm.get_debt(session, member.id))
		for member in workspace.members
		if member.active
	]

def get_latest_settlement_snapshot(session: Session, workspace_id: int, user_id: int, recalculate: bool = False) -> Settlement:
	get_workspace(session, workspace_id)
	serv_usr.require_workspace_member(session, user_id, workspace_id)

	def calculate_simplified_debts():

		def create_settlement_snapshot(simplified_debts: dict):
			try:
				current_time = datetime.now()

				settlement = Settlement(
					workspace_id=workspace_id,
					created_at=current_time
				)
				session.add(settlement)
				session.flush()

				for currency, debt_list in simplified_debts.items():
					for debtor_id, creditor_id, amount in debt_list:
						settl_item = SettlementItem(
							settlement_id=settlement.id,
							debtor_wsm_id=debtor_id,
							creditor_wsm_id=creditor_id,
							amount=amount,
							currency=currency,
							transaction_id=None
						)

						session.add(settl_item)

				session.commit()
				return settlement

			except Exception:
				session.rollback()
				raise

		def simplify_one_currency_debts(debtors, creditors):
			debtors_sorted = sorted(
				debtors,
				key=lambda x: x[1],
				reverse=True
			)
			creditors_sorted = sorted(
				creditors,
				key=lambda x: x[1],
				reverse=True
			)
			if not debtors_sorted or not creditors_sorted:
				return []

			simplified = []
			debtor_index = 0
			creditor_index = 0
			debtor, debtor_amount = debtors_sorted[debtor_index]
			creditor, creditor_amount = creditors_sorted[creditor_index]

			while (
					debtor_index < len(debtors_sorted)
					and creditor_index < len(creditors_sorted)
			):
				amount = min(debtor_amount, creditor_amount)

				simplified.append(
					(debtor.id, creditor.id, amount)
				)

				debtor_amount -= amount
				creditor_amount -= amount

				if debtor_amount == 0:
					debtor_index += 1

					if debtor_index < len(debtors_sorted):
						debtor, debtor_amount = debtors_sorted[debtor_index]

				if creditor_amount == 0:
					creditor_index += 1

					if creditor_index < len(creditors_sorted):
						creditor, creditor_amount = creditors_sorted[creditor_index]

			return simplified

		members_and_debts = get_debts(session, workspace_id)
		debtors_usd = [(member, debt[0])
					for member, debt in members_and_debts if debt[0] > 0]
		creditors_usd = [(member, -debt[0])
						for member, debt in members_and_debts if debt[0] < 0]
		debtors_eur = [(member, debt[1])
					for member, debt in members_and_debts if debt[1] > 0]
		creditors_eur = [(member, -debt[1])
						for member, debt in members_and_debts if debt[1] < 0]
		debtors_rub = [(member, debt[2])
					for member, debt in members_and_debts if debt[2] > 0]
		creditors_rub = [(member, -debt[2])
						for member, debt in members_and_debts if debt[2] < 0]

		if (abs(sum(debt for _, debt in debtors_usd) - sum(debt for _, debt in creditors_usd)) > 0.1 or
				abs(sum(debt for _, debt in debtors_eur) - sum(debt for _, debt in creditors_eur)) > 0.1 or
				abs(sum(debt for _, debt in debtors_rub) - sum(debt for _, debt in creditors_rub)) > 0.1):
			raise ValueError("The debts do not match!")

		usd_simplified = simplify_one_currency_debts(debtors_usd, creditors_usd)
		eur_simplified = simplify_one_currency_debts(debtors_eur, creditors_eur)
		rub_simplified = simplify_one_currency_debts(debtors_rub, creditors_rub)

		return create_settlement_snapshot({
			Currency.USD: usd_simplified,
			Currency.EUR: eur_simplified,
			Currency.RUB: rub_simplified
		})

	if recalculate:
		return calculate_simplified_debts()

	return session.scalars(
		select(Settlement)
		.where(Settlement.workspace_id == workspace_id)
		.order_by(
			Settlement.created_at.desc(),
			Settlement.id.desc()
		)
		.limit(1)
	).first()

def compensate_settlement_item(session: Session, settlement_item_id: int, workspace_id: int , user_id: int):
	# check that the user belongs to ws
	# check that the settlement belongs to ws
	workspace = get_workspace(session, workspace_id)
	user_wsm = serv_usr.require_workspace_member(session, user_id, workspace_id)
	settlement_item = get_settlement_item(session, settlement_item_id)
	if settlement_item.settlement.workspace_id != workspace_id:
		raise ValueError("Settlement item does not belong to this workspace.")
	if settlement_item.transaction_id is not None:
		raise ValueError("Settlement item has already been compensated.")
	try:
		if (settlement_item.creditor_wsm == user_wsm or settlement_item.debtor_wsm == user_wsm or user_wsm.permission == Permission.ADMIN):
			compensating_transaction = Transaction(
				amount=settlement_item.amount, 
				description=f"Compensating Settlement {settlement_item.settlement_id}",
				currency=settlement_item.currency, 
				transact_type=TransactionType.DIRECT_TRANSFER,
				beneficiary_workspace_member=settlement_item.creditor_wsm_id,
				source_workspace_member=settlement_item.debtor_wsm_id,
				workspace_id=workspace.id,
				beneficiary_acc=None,
				source_acc=None,
				created_at=datetime.now()
			)
			session.add(compensating_transaction)
			session.flush()
			settlement_item.transaction_id = compensating_transaction.id
			session.commit()
		else:
			raise ValueError("User is must either be part of the settlement or be a workspace admin!")
	except Exception:
		session.rollback()
		raise

def get_settlement_item(session: Session, settlement_item_id: int) -> SettlementItem:
	settlement_item = session.get(SettlementItem, settlement_item_id)
	if settlement_item is None:
		raise ValueError("Settlement Item not found.")
	return settlement_item


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
		created_at=datetime.now()
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
