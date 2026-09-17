from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from database import Session
from models.account import AccountType
from shared.currency import Currency

import services.account_services as serv_acc
import services.user_services as serv_usr


router = APIRouter(
    prefix="/accounts",
    tags=["accounts"]
)

session = Session()


class AccountCreate(BaseModel):
    user_id: int
    name: str
    acc_type: AccountType
    currency: Currency

class AccountResponse(BaseModel):
    id: int
    name: str
    acc_type: str
    currency: str
    owner_id: int

class AccountUpdate(BaseModel):
    name: str
    acc_type: AccountType

class MessageResponse(BaseModel):
	message: str


@router.post("/", response_model=AccountResponse)
def create_account(data: AccountCreate):

    try:
        account = serv_acc.create_account(
            session=session,
            user_id=data.user_id,
            name=data.name,
            acc_type=data.acc_type,
            currency=data.currency
        )
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )

    return {
        "id": account.id,
        "name": account.name,
        "acc_type": account.acc_type.value,
        "currency": account.currency.value,
        "owner_id": account.owner_id
    }

@router.get("/user/{user_id}", response_model=list[AccountResponse])
def get_user_accounts(user_id: int):

    try:
        accounts = serv_usr.get_accounts(
            session,
            user_id
        )
    except ValueError as e:
        raise HTTPException(
            status_code=404,
            detail=str(e)
        )

    return [
        {
            "id": account.id,
            "name": account.name,
            "acc_type": account.acc_type.value,
            "currency": account.currency.value,
            "owner_id": account.owner_id
        }
        for account in accounts
    ]

@router.get("/{account_id}", response_model=AccountResponse)
def get_account(
    account_id: int,
    user_id: int
):
    try:
        account = serv_usr.get_account(
            session,
            account_id,
            user_id
        )
    except ValueError as e:
        raise HTTPException(
            status_code=404,
            detail=str(e)
        )

    return {
        "id": account.id,
        "name": account.name,
        "acc_type": account.acc_type.value,
        "currency": account.currency.value,
        "owner_id": account.owner_id
    }

@router.get("/{account_id}/value")
def get_account_value(
    account_id: int,
    user_id: int
):
    try:
        serv_usr.get_account(
            session,
            account_id,
            user_id
        )

        value = serv_acc.get_account_value(
            session,
            account_id
        )
    except ValueError as e:
        raise HTTPException(
            status_code=404,
            detail=str(e)
        )

    return {
        "account_id": account_id,
        "value": value
    }

@router.patch("/{account_id}", response_model=AccountResponse)
def update_account(
    account_id: int,
    data: AccountUpdate,
    user_id: int
):
    try:
        account = serv_acc.update_account(
            session,
            account_id,
            user_id,
            data.name,
            data.acc_type
        )
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )

    return {
        "id": account.id,
        "name": account.name,
        "acc_type": account.acc_type.value,
        "currency": account.currency.value,
        "owner_id": account.owner_id
    }

@router.delete("/{account_id}",response_model=MessageResponse)
def delete_account(
    account_id: int,
    user_id: int,
    delete_related_transactions: bool = False
):
    try:
        serv_acc.delete_account(
            session,
            account_id,
            user_id,
            delete_related_transactions
        )
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )

    return {"message": "Account deleted"}
