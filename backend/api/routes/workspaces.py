from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from datetime import datetime
from sqlalchemy import select

from database import Session
from models.workspace import Workspace
from models.workspace_member import WorkspaceMember, Permission
from models.user import User
from models.settlement import Settlement, SettlementItem

import services.user_services as serv_usr
import services.workspace_services as serv_ws
import services.workspace_member_services as serv_wsm


router = APIRouter(
    prefix="/workspaces",
    tags=["workspaces"]
)

session = Session()


class MemberCreate(BaseModel):
    user_id: int
    permission: Permission

class WorkspaceMemberResponse(BaseModel):
    id: int
    user_id: int
    name: str
    permission: str
    active: bool

class WorkspaceResponse(BaseModel):
    id: int
    name: str
    description: str

class WorkspaceUpdate(BaseModel):
    name: str
    description: str

class WorkspaceCreate(BaseModel):
    name: str
    description: str

class MessageResponse(BaseModel):
    message: str

class DebtResponse(BaseModel):
    user_id: int
    name: str
    usd: float
    eur: float
    rub: float

class TransactionResponse(BaseModel):
    id: int
    created_at: datetime
    description: str | None
    transact_type: str
    amount: float
    currency: str
    source_workspace_member: int
    beneficiary_workspace_member: int
    source_member_name: str
    beneficiary_member_name: str

class SettlementItemResponse(BaseModel):
    debtor_wsm_id: int
    debtor_name: str
    creditor_wsm_id: int
    creditor_name: str
    amount: float
    currency: str
    transaction_id: int | None

class SettlementResponse(BaseModel):
    id: int
    workspace_id: int
    created_at: datetime
    items: list[SettlementItemResponse]

def settlement_to_response(settlement: Settlement):
    return {
        "id": settlement.id,
        "workspace_id": settlement.workspace_id,
        "created_at": settlement.created_at,
        "items": [
            {
                "debtor_wsm_id": item.debtor_wsm_id,
                "debtor_name": item.debtor_wsm.user.name,
                "creditor_wsm_id": item.creditor_wsm_id,
                "creditor_name": item.creditor_wsm.user.name,
                "amount": float(item.amount),
                "currency": item.currency.value,
                "transaction_id": item.transaction_id
            }
            for item in settlement.items
        ]
    }


@router.get("/{workspace_id}/transactions", response_model=list[TransactionResponse])
def get_workspace_transactions(
    workspace_id: int,
    user_id: int
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
            workspace_id
        )
    except ValueError as e:
        raise HTTPException(
            status_code=404,
            detail=str(e)
        )

    return [
        {
            "id": transaction.id,
            "created_at": transaction.created_at,
            "description": transaction.description,
            "transact_type": transaction.transact_type.value,
            "amount": float(transaction.amount),
            "currency": transaction.currency.value,
            "source_workspace_member": transaction.source_workspace_member,
            "beneficiary_workspace_member": transaction.beneficiary_workspace_member,
            "source_member_name": transaction.sou_worksp_memb.user.name,
            "beneficiary_member_name": transaction.benef_worksp_memb.user.name,
        }
        for transaction in transactions
    ]


@router.get("/{workspace_id}/members", response_model=list[WorkspaceMemberResponse])
def get_workspace_members(
        workspace_id: int,
        user_id: int
):
    try:
        workspace = serv_ws.get_workspace(
            session,
            workspace_id
        )
    except ValueError as e:
        raise HTTPException(
            status_code=404,
            detail=str(e)
        )

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

    return [{
            "id": member.id,
            "user_id": member.user_id,
            "name": member.user.name,
            "permission": member.permission.value,
            "active": member.active
            } for member in workspace.members]


@router.get("/{workspace_id}/debts/simplified", response_model=SettlementResponse)
def get_simplified_workspace_debts(
    workspace_id: int,
    user_id: int,
    recalculate: bool = False
):
    try:
        settlement = serv_ws.get_latest_settlement_snapshot(
            session,
            workspace_id,
            user_id,
            recalculate
        )
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )

    if settlement is None:
        raise HTTPException(
            status_code=404,
            detail="No settlement snapshot exists for this workspace."
        )

    return settlement_to_response(settlement)

@router.get("/{workspace_id}/debts", response_model=list[DebtResponse])
def get_workspace_debts(
    workspace_id: int,
    user_id: int
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
        debts = serv_ws.get_debts(
            session,
            workspace_id
        )
    except ValueError as e:
        raise HTTPException(
            status_code=404,
            detail=str(e)
        )

    return [
        {
            "user_id": member.user_id,
            "name": member.user.name,
            "usd": debt_usd,
            "eur": debt_eur,
            "rub": debt_rub
        }
        for member, (
            debt_usd,
            debt_eur,
            debt_rub
        ) in debts
    ]


@router.get("/{workspace_id}", response_model=WorkspaceResponse)
def get_workspace(workspace_id: int, user_id: int):
    try:
        workspace = serv_ws.get_workspace(
            session,
            workspace_id
        )
    except ValueError as e:
        raise HTTPException(
            status_code=404,
            detail=str(e)
        )
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

    return {
        "id": workspace.id,
        "name": workspace.name,
        "description": workspace.description
    }



@router.post("/{workspace_id}/debts/simplified/items/{settlement_item_id}/compensate", response_model=MessageResponse)
def compensate_settlement_item(
    workspace_id: int,
    settlement_item_id: int,
    user_id: int
):
    try:
        serv_ws.compensate_settlement_item(
            session,
            settlement_item_id,
            workspace_id,
            user_id
        )
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )

    return {"message": "Settlement item compensated"}

@router.post("/", response_model=WorkspaceResponse)
def create_workspace(
        workspace_data: WorkspaceCreate,
        user_id: int
):
    try:
        workspace = serv_ws.create_workspace(
            session,
            workspace_data.name,
            workspace_data.description,
            user_id
        )
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )

    return {
        "id": workspace.id,
        "name": workspace.name,
        "description": workspace.description
    }


@router.post("/{workspace_id}/members", response_model=WorkspaceMemberResponse)
def add_workspace_member(
        workspace_id: int,
        member_data: MemberCreate,
        user_id: int
):
    try:
        member = serv_wsm.add_ws_member(
            session,
            workspace_id,
            member_data.user_id,
            member_data.permission,
            user_id
        )
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )

    return {
        "id": member.id,
        "user_id": member.user_id,
        "name": member.user.name,
        "permission": member.permission.value,
        "active": member.active
    }


@router.patch("/{workspace_id}", response_model=WorkspaceResponse)
def update_workspace(
    workspace_id: int,
    workspace_data: WorkspaceUpdate,
    user_id: int
):
    try:
        workspace = serv_ws.update_workspace(
            session,
            workspace_id,
            user_id,
            workspace_data.name,
            workspace_data.description
        )
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )

    return {
        "id": workspace.id,
        "name": workspace.name,
        "description": workspace.description
    }


@router.patch("/{workspace_id}/members/{member_user_id}", response_model=WorkspaceMemberResponse)
def update_workspace_member(
        workspace_id: int,
        member_user_id: int,
        member_data: MemberCreate,
        user_id: int
):
    try:
        member = serv_wsm.update_ws_member(
            session,
            workspace_id,
            member_user_id,
            user_id,
            member_data.permission
        )
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )

    return {
        "id": member.id,
        "user_id": member.user_id,
        "name": member.user.name,
        "permission": member.permission.value,
        "active": member.active
    }


@router.delete("/{workspace_id}/members/{member_user_id}", response_model=MessageResponse)
def remove_workspace_member(
        workspace_id: int,
        member_user_id: int,
        user_id: int
):
    try:
        serv_wsm.delete_ws_member(
            session,
            workspace_id,
            member_user_id,
            user_id
        )
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )

    return {"message": "Member removed"}


@router.delete("/{workspace_id}", response_model=MessageResponse)
def delete_workspace(
    workspace_id: int,
    user_id: int
):
    try:
        serv_ws.delete_workspace(
            session,
            workspace_id,
            user_id
        )
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )

    return {"message": "Workspace deleted"}
