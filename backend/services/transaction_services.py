from sqlalchemy.orm import Session
from sqlalchemy import select
from datetime import datetime

from models.workspace import Workspace
from models.workspace_member import WorkspaceMember, Permission
from models.user import User, Role
from models.transaction import Transaction, TransactionType, Currency
from models.account import Account

import services.user_services as serv_usr
import services.workspace_member_services as serv_wsm
import services.workspace_services as serv_ws
import services.account_services as serv_ac


# payer_id_id is a workspace member id
# beneficiaries are worksp members too
def shared_payment(
		session: Session,
		workspace_id: int,
		payer_id: int,
		value: float,
		currency: str,
		description: str,
		recipients_list: list[int],
		shares_list: list[float] | None = None
):

	if value <= 0:
		raise ValueError("Transaction value must be greater than zero.")
	try:
		currency = Currency(currency)
	except ValueError:
		raise ValueError(
			f"Invalid currency. Supported currencies: "
			f"{', '.join(c.value for c in Currency)}."
		)
	if not recipients_list:
		raise ValueError("At least one recipient is required.")
	if len(set(recipients_list)) != len(recipients_list):
		raise ValueError("Recipients must be unique.")
	if shares_list is None:
		shares_list = [
			1 / len(recipients_list)
		] * len(recipients_list)
	elif len(shares_list) != len(recipients_list):
		raise ValueError("Shares and recipients have different lengths.")
	elif any(share < 0 for share in shares_list):
		raise ValueError("Shares cannot be negative.")
	elif abs(sum(shares_list) - 1) > 1e-6:
		raise ValueError("Shares must sum to 1.")

	try:
		workspace = serv_ws.get_workspace(
			session,
			workspace_id
		)
		payer = serv_wsm.get_ws_member(
			session,
			workspace_id,
			payer_id
		)
	except ValueError as e:
		raise ValueError(str(e))

	for recipient_id in recipients_list:
		try:
			recipient = serv_wsm.get_ws_member(
				session,
				workspace_id,
				recipient_id
			)
		except ValueError as e:
			raise ValueError(str(e))

	trans_list = []
	for recipient, share in zip(
			recipients_list,
			shares_list
	):
		transaction = Transaction(
			amount=value * share,
			description=description,
			currency=currency,
			transact_type=TransactionType.SHARED_PAYMENT,
			beneficiary_workspace_member=recipient,
			source_workspace_member=payer_id,
			workspace_id=workspace_id,
			created_at=datetime.now()
		)

		trans_list.append(transaction)
		session.add(transaction)

	session.commit()

	return trans_list


def direct_transfer(
		session: Session,
		workspace_id: int,
		payer_member_id: int,
		recipient_member_id: int,
		value: float,
		currency: str,
		payer_acc_id: int | None = None,
		recipient_acc_id: int | None = None,
		description: str | None = None
):
	if value <= 0:
		raise ValueError("Transaction value must be greater than zero.")
	try:
		currency = Currency(currency)
	except ValueError:
		raise ValueError(
			f"Invalid currency. Supported currencies: "
			f"{', '.join(c.value for c in Currency)}."
		)

	try:
		workspace = serv_ws.get_workspace(
			session,
			workspace_id
		)
		payer = serv_wsm.get_ws_member(
			session,
			workspace_id,
			payer_member_id
		)
		recipient = serv_wsm.get_ws_member(
			session,
			workspace_id,
			recipient_member_id
		)

		if payer_acc_id is not None:
			payer_acc = serv_usr.get_account(
				session,
				payer_acc_id,
				payer.user_id
			)
		if recipient_acc_id is not None:
			recipient_acc = serv_usr.get_account(
				session,
				recipient_acc_id,
				recipient.user_id
			)
	except ValueError as e:
		raise ValueError(str(e))

	transaction = Transaction(amount=value, description=description,
							  currency=currency, transact_type=TransactionType.DIRECT_TRANSFER,
							  beneficiary_workspace_member=recipient_member_id,
							  source_workspace_member=payer_member_id,
							  workspace_id=workspace_id,
							  beneficiary_acc=recipient_acc_id,
							  source_acc=payer_acc_id,
							  created_at=datetime.now()
							  )
	session.add(transaction)
	session.commit()

	return transaction

# for own fin only -> no workspace_member id needed, always 1


def expense(
		session: Session,
		workspace_id: int,
		value: float,
		currency: str,
		member_id: int,
		payer_acc_id: int | None = None,
		recipient_acc_id: int | None = None,
		description: str | None = None
):
	return direct_transfer(
		session=session,
		workspace_id=workspace_id,
		payer_member_id=member_id,
		recipient_member_id=member_id,
		value=value,
		currency=currency,
		payer_acc_id=payer_acc_id,
		recipient_acc_id=recipient_acc_id,
		description=description
	)


def get_transaction(session: Session, transaction_id: int):
	trans = session.get(Transaction, transaction_id)
	if trans is None:
		raise ValueError("Transaction not found.")

	return trans


def delete(session: Session, transaction_id: int, user_id: int):
	trans = get_transaction(session, transaction_id)
	if trans.deleted_at is not None:
		raise ValueError("Transaction is already deleted.")

	wsm = serv_usr.get_workspace_member(session, user_id, trans.workspace_id)
	if wsm is None:
		raise ValueError("User is not a member of this workspace.")
	if not ((
		wsm.permission == Permission.WRITE
		and
		(trans.benef_worksp_memb.user_id ==
		 user_id or trans.sou_worksp_memb.user_id == user_id)
	)
		or
		wsm.permission == Permission.ADMIN
	):
		raise ValueError("This member cannot delete this transaction.")

	trans.deleted_at = datetime.now()
	trans.deleted_by = wsm.id

	session.commit()


def restore(session: Session, transaction_id: int, user_id: int):
	trans = get_transaction(session, transaction_id)

	if trans.deleted_at is None:
		raise ValueError("Transaction is not deleted.")

	wsm = serv_usr.get_workspace_member(
		session,
		user_id,
		trans.workspace_id
	)

	if wsm is None:
		raise ValueError("User is not a member of this workspace.")

	if not (
			(
				wsm.permission == Permission.WRITE
				and (
					trans.benef_worksp_memb.user_id == user_id
					or trans.sou_worksp_memb.user_id == user_id
				)
			)
			or wsm.permission == Permission.ADMIN
	):
		raise ValueError("This member cannot restore this transaction.")

	trans.deleted_at = None
	trans.deleted_by = None

	session.commit()


def update_transaction(
	session: Session,
	transaction_id: int,
	user_id: int,
	amount: float,
	currency: str,
	description: str | None = None,
	source_acc_id: int | None = None,
	beneficiary_acc_id: int | None = None
):
	trans = get_transaction(session, transaction_id)

	if trans.deleted_at is not None:
		raise ValueError("Cannot edit a deleted transaction.")

	wsm = serv_usr.get_workspace_member(
		session,
		user_id,
		trans.workspace_id
	)

	usr = serv_usr.get_user(session, user_id)
	if usr.role != Role.ADMIN:
		if wsm is None:
			raise ValueError("User is not a member of the transaction's workspace.")

		if not (
			(
				wsm.permission == Permission.WRITE
				and (
					trans.benef_worksp_memb.user_id == user_id
					or trans.sou_worksp_memb.user_id == user_id
				)
			)
			or wsm.permission == Permission.ADMIN
		):
			raise ValueError("This member cannot edit this transaction.")

	if amount <= 0:
		raise ValueError("Transaction value must be greater than zero.")

	try:
		currency = Currency(currency)
	except ValueError:
		raise ValueError(
			f"Invalid currency. Supported currencies: "
			f"{', '.join(c.value for c in Currency)}."
		)

	if source_acc_id is not None:
		serv_usr.get_account(
			session,
			source_acc_id,
			trans.sou_worksp_memb.user_id
		)

	if beneficiary_acc_id is not None:
		serv_usr.get_account(
			session,
			beneficiary_acc_id,
			trans.benef_worksp_memb.user_id
		)

	trans.amount = amount
	trans.currency = currency
	trans.description = description
	trans.source_acc = source_acc_id
	trans.beneficiary_acc = beneficiary_acc_id

	session.commit()
	session.refresh(trans)

	return trans
