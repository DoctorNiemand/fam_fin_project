from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from datetime import datetime

from database import Session
from models.transaction import Transaction, Currency, TransactionType
from models.user import User

import services.transaction_services as serv_tr
import services.workspace_services as serv_ws
import services.user_services as serv_usr
import services.account_services as serv_acc


router = APIRouter(
	prefix="/transactions",
	tags=["transactions"]
)

session = Session()


class ExpenseCreate(BaseModel):
	workspace_id: int
	member_id: int
	value: float
	currency: str
	payer_acc_id: int | None = None
	recipient_acc_id: int | None = None
	description: str | None = None

class DirectTransferCreate(BaseModel):
	workspace_id: int
	payer_member_id: int
	recipient_member_id: int
	value: float
	currency: str
	payer_acc_id: int | None = None
	recipient_acc_id: int | None = None
	description: str | None = None

class SharedPaymentCreate(BaseModel):
	workspace_id: int
	payer_id: int
	value: float
	currency: str
	description: str
	recipients: list[int]
	shares: list[float] | None = None

class TransactionMemberResponse(BaseModel):
	user_id: int
	name: str
class TransactionAccountResponse(BaseModel):
	id: int
	name: str
class TransactionResponse(BaseModel):
	id: int
	operation_id: int | None
	created_at: datetime
	type: str
	amount: float
	currency: str
	description: str | None

	workspace_id: int
	workspace_name: str

	paid_by: TransactionMemberResponse
	paid_to: TransactionMemberResponse

	source_account: TransactionAccountResponse | None
	beneficiary_account: TransactionAccountResponse | None

	deleted: bool

def transaction_to_response(transaction: Transaction):
	return {
		"id": transaction.id,
		"operation_id": transaction.operation_id,
		"created_at": transaction.created_at,

		"type": transaction.transact_type.value,
		"amount": float(transaction.amount),
		"currency": transaction.currency.value,
		"description": transaction.description,

		"workspace_id": transaction.workspace_id,
		"workspace_name": transaction.workspace.name,

		"paid_by": {
			"user_id": transaction.sou_worksp_memb.user_id,
			"name": transaction.sou_worksp_memb.user.name
		},

		"paid_to": {
			"user_id": transaction.benef_worksp_memb.user_id,
			"name": transaction.benef_worksp_memb.user.name
		},

		"source_account": (
			{
				"id": transaction.sou_acc.id,
				"name": transaction.sou_acc.name
			}
			if transaction.sou_acc is not None
			else None
		),

		"beneficiary_account": (
			{
				"id": transaction.benef_acc.id,
				"name": transaction.benef_acc.name
			}
			if transaction.benef_acc is not None
			else None
		),

		"deleted": transaction.deleted_at is not None
	}

class TransactionRestore(BaseModel):
	user_id: int

class TransactionUpdate(BaseModel):
	user_id: int
	amount: float
	currency: str
	description: str | None = None
	source_acc_id: int | None = None
	beneficiary_acc_id: int | None = None

class MessageResponse(BaseModel):
	message: str


@router.get("/user/{user_id}", response_model=list[TransactionResponse])
def get_user_transactions(
	user_id: int,
	include_deleted: bool = False
):
	try:
		transactions = serv_usr.get_transactions(
			session,
			user_id,
			include_deleted
		)
	except ValueError as e:
		raise HTTPException(
			status_code=404,
			detail=str(e)
		)

	return [
		transaction_to_response(t)
		for t in transactions
	]

@router.get("/{transaction_id}", response_model=TransactionResponse)
def get_transaction(
	transaction_id: int,
	user_id: int
):
	try:
		transaction = serv_tr.get_transaction(
			session,
			transaction_id
		)

		serv_usr.require_workspace_member(
			session,
			user_id,
			transaction.workspace_id
		)

	except ValueError as e:
		raise HTTPException(
			status_code=404,
			detail=str(e)
		)

	return transaction_to_response(transaction)

@router.get("/workspace/{workspace_id}", response_model=list[TransactionResponse])
def get_workspace_transactions(
	workspace_id: int,
	user_id: int,
	include_deleted: bool = False
):
	try:
		serv_usr.require_workspace_member(
			session,
			user_id,
			workspace_id
		)
	except ValueError as e:
		raise HTTPException(
			status_code=403,
			detail=str(e)
		)

	try:
		transactions = serv_ws.get_transactions(
			session,
			workspace_id,
			include_deleted
		)
	except ValueError as e:
		raise HTTPException(
			status_code=404,
			detail=str(e)
		)

	return [
		transaction_to_response(t)
		for t in transactions
	]

@router.get("/account/{account_id}", response_model=list[TransactionResponse])
def get_account_transactions(
	account_id: int,
	user_id: int,
	include_deleted: bool = False
):
	try:
		account = serv_acc.get_account(
			session,
			account_id
		)

		transactions = serv_acc.get_transactions(
			session,
			account_id,
			include_deleted
		)
	except ValueError as e:
		raise HTTPException(
			status_code=404,
			detail=str(e)
		)

	if account.owner_id != user_id:
		raise HTTPException(
			status_code=403,
			detail="User does not own this account."
		)

	return [
		transaction_to_response(t)
		for t in transactions
	]


@router.put("/{transaction_id}", response_model=TransactionResponse)
def update_transaction(
	transaction_id: int,
	data: TransactionUpdate
):
	try:
		transaction = serv_tr.update_transaction(
			session=session,
			transaction_id=transaction_id,
			user_id=data.user_id,
			amount=data.amount,
			currency=data.currency,
			description=data.description,
			source_acc_id=data.source_acc_id,
			beneficiary_acc_id=data.beneficiary_acc_id
		)
	except ValueError as e:
		raise HTTPException(
			status_code=400,
			detail=str(e)
		)

	return transaction_to_response(transaction)


@router.post("/shared", response_model=list[TransactionResponse])
def create_shared_payment(data: SharedPaymentCreate):

	try:
		transactions = serv_tr.shared_payment(
			session=session,
			workspace_id=data.workspace_id,
			payer_id=data.payer_id,
			value=data.value,
			currency=data.currency,
			description=data.description,
			recipients_list=data.recipients,
			shares_list=data.shares
		)
	except ValueError as e:
		raise HTTPException(
			status_code=400,
			detail=str(e)
		)

	return [
		transaction_to_response(t)
		for t in transactions
	]

@router.post("/transfer", response_model=TransactionResponse)
def create_direct_transfer(data: DirectTransferCreate):

	try:
		transaction = serv_tr.direct_transfer(
			session=session,
			workspace_id=data.workspace_id,
			payer_member_id=data.payer_member_id,
			recipient_member_id=data.recipient_member_id,
			value=data.value,
			currency=data.currency,
			payer_acc_id=data.payer_acc_id,
			recipient_acc_id=data.recipient_acc_id,
			description=data.description
		)
	except ValueError as e:
		raise HTTPException(
			status_code=400,
			detail=str(e)
		)

	return transaction_to_response(transaction)

@router.post("/expense", response_model=TransactionResponse)
def create_expense(data: ExpenseCreate):

	try:
		transaction = serv_tr.expense(
			session=session,
			workspace_id=data.workspace_id,
			value=data.value,
			currency=data.currency,
			member_id=data.member_id,
			payer_acc_id=data.payer_acc_id,
			recipient_acc_id=data.recipient_acc_id,
			description=data.description
		)
	except ValueError as e:
		raise HTTPException(
			status_code=400,
			detail=str(e)
		)
	
	return transaction_to_response(transaction)


@router.delete("/{transaction_id}", response_model= MessageResponse)
def delete_transaction(
	transaction_id: int,
	user_id: int
):
	try:
		serv_tr.delete(
			session=session,
			transaction_id=transaction_id,
			user_id=user_id
		)
	except ValueError as e:
		raise HTTPException(
			status_code=400,
			detail=str(e)
		)

	return {"message": "Transaction deleted"}

@router.post("/{transaction_id}/restore", response_model= MessageResponse)
def restore_transaction(
	transaction_id: int,
	data: TransactionRestore
):
	try:
		serv_tr.restore(
			session=session,
			transaction_id=transaction_id,
			user_id=data.user_id
		)
	except ValueError as e:
		raise HTTPException(
			status_code=400,
			detail=str(e)
		)

	return {"message": "Transaction restored"}

@router.delete("/operation/{operation_id}", response_model= MessageResponse)
def delete_operation(
	operation_id: int,
	user_id: int
):
	try:
		for trans in serv_tr.get_all_transactions_by_operation_id(session, operation_id):
			serv_tr.delete(
				session=session,
				transaction_id=trans.id,
				user_id=user_id
			)
	except ValueError as e:
		raise HTTPException(
			status_code=400,
			detail=str(e)
		)

	return {"message": "Operation deleted"}

@router.post("/operation/{operation_id}/restore", response_model= MessageResponse)
def restore_operation(
	operation_id: int,
	user_id: int
):
	try:
		for trans in serv_tr.get_all_transactions_by_operation_id(session, operation_id):
			serv_tr.restore(
				session=session,
				transaction_id=trans.id,
				user_id=user_id
			)
	except ValueError as e:
		raise HTTPException(
			status_code=400,
			detail=str(e)
		)

	return {"message": "Operation restored"}

@router.post("/compensate", response_model= MessageResponse)
def compensate_debt(
    workspace_id: int,
    user_id: int,
    other_member_id: int,
    amount: float,
    currency: Currency
):
	try:
		usr_member = serv_usr.require_workspace_member(session, user_id, workspace_id)
		if amount < 0:
			benef = usr_member.id
			source = other_member_id
		else:
			benef = other_member_id
			source = usr_member.id
		comp_trans = Transaction(
			amount=abs(amount), 
			description= f"Compensating debt",
			currency=currency, 
			transact_type=TransactionType.DIRECT_TRANSFER,
			beneficiary_workspace_member=benef,
			source_workspace_member=source,
			workspace_id=workspace_id,
			created_at=datetime.now()
			)
		session.add(comp_trans)
		session.flush()
		comp_trans.operation_id = comp_trans.id
		session.commit()
	except ValueError as e:
		raise HTTPException(
			status_code=400,
			detail=str(e)
		)

	return {"message": "Transaction compensated"}
