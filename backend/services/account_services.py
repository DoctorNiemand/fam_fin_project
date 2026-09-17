from sqlalchemy.orm import Session
from sqlalchemy import select
from datetime import datetime

from models.workspace import Workspace
from models.workspace_member import WorkspaceMember
from models.user import User
from models.account import Account, AccountType
from shared.currency import Currency

import services.workspace_member_services as wms

def to_currency(value: str) -> Currency:
	return {
		"eur": Currency.EUR,
		"rub": Currency.RUB,
		"usd": Currency.USD
	}[value.lower()]

def get_account_value (session: Session, account_id: int):
	account = session.get(Account, account_id)
	val = 0
	for tr in account.as_beneficiary:
		val += tr.amount
	for tr in account.as_source:
		val -= tr.amount
	return val

def create_account(
	session: Session,
	user_id: int,
	name: str,
	acc_type: AccountType | str,
	currency: Currency | str 
):
	user = session.get(User, user_id)

	if user is None:
		raise ValueError("User not found.")

	account = Account(
		name=name,
		acc_type=acc_type,
		currency=currency,
		owner_id=user_id,
		created_at=datetime.now()
	)

	session.add(account)
	session.commit()
	session.refresh(account)

	return account

def get_account(session: Session, account_id: int):
	account = session.get(Account, account_id)
	if account is None:
		raise ValueError("Account not found.")

	return account

def update_account(
	session: Session,
	account_id: int,
	user_id: int,
	name: str,
	acc_type: AccountType
):
	account = session.get(Account, account_id)

	if account is None:
		raise ValueError("Account not found.")

	if account.owner_id != user_id:
		raise ValueError("User does not own this account.")

	account.name = name
	account.acc_type = acc_type

	session.commit()
	session.refresh(account)

	return account

def get_transactions(
	session: Session,
	account_id: int,
	include_deleted: bool = False
):
	account = session.get(Account, account_id)

	if account is None:
		raise ValueError("Account not found.")

	transactions = list(
		set(account.as_source) |
		set(account.as_beneficiary)
	)

	if not include_deleted:
		transactions = [
			transaction
			for transaction in transactions
			if transaction.deleted_at is None
		]

	return transactions

