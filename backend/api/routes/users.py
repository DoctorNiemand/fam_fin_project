from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from database import Session
from models.user import User, Role
import services.db_services as serv_db
import services.user_services as serv_usr


router = APIRouter(
    prefix="/users",
    tags=["users"]
)

session = Session()


class UserCreate(BaseModel):
    name: str
    login: str
    password: str
    role: Role

class LoginRequest(BaseModel):
    login: str
    password: str

class DebtResponse(BaseModel):
    usd: float
    eur: float
    rub: float

class PairDebtResponse(BaseModel):
    user_id: int
    workspace_member_id: int | None = None
    name: str
    usd: float
    eur: float
    rub: float


@router.get("/")
def get_users():
    users = serv_db.get_users(session)

    return [
        {
            "id": user.id,
            "name": user.name,
            "login": user.login,
            "role": user.role.value
        }
        for user in users
    ]

@router.get("/{user_id}")
def get_user(user_id: int):

    try:
        user = serv_usr.get_user(
            session,
            user_id
        )
    except ValueError as e:
        raise HTTPException(
            status_code=404,
            detail=str(e)
        )

    return {
        "id": user.id,
        "name": user.name,
        "login": user.login,
        "role": user.role.value
    }

@router.get("/{user_id}/debts", response_model=DebtResponse)
def get_user_debt(user_id: int):
    try:
        debt_usd, debt_eur, debt_rub = serv_usr.get_cumulative_debt(
            session,
            user_id
        )
    except ValueError as e:
        raise HTTPException(
            status_code=404,
            detail=str(e)
        )

    return {
        "usd": debt_usd,
        "eur": debt_eur,
        "rub": debt_rub
    }

@router.get("/{user_id}/workspace_pair_debts", response_model=list[PairDebtResponse])
def get_workspace_pair_debts(workspace_id: int, user_id: int):
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
        debts = serv_usr.get_workspace_pair_debts(
            session,
            user_id,
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
            "workspace_member_id": member.id,
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

@router.get("/{user_id}/cumulative_pair_debts", response_model=list[PairDebtResponse])
def get_cumulative_pair_debts(user_id: int):
    try:
        debts = serv_usr.get_all_cumulative_pair_debts(
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
            "user_id": user.id,
            "name": user.name,
            "usd": debt_usd,
            "eur": debt_eur,
            "rub": debt_rub
        }
        for user, (
            debt_usd,
            debt_eur,
            debt_rub
        ) in debts
    ]


@router.get("/{user_id}/workspaces")
def get_user_workspaces(user_id: int):

    try:
        workspaces = serv_usr.get_workspaces(
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
            "id": workspace.id,
            "name": workspace.name,
            "description": workspace.description
        }
        for workspace in workspaces
    ]

@router.post("/")
def create_user(user_data: UserCreate):

    user = User(
        name=user_data.name,
        login=user_data.login,
        password_hash=user_data.password,
        role=user_data.role
    )

    session.add(user)
    session.commit()
    session.refresh(user)

    return {
        "id": user.id,
        "name": user.name,
        "login": user.login,
        "role": user.role.value
    }


@router.post("/login")
def login(data: LoginRequest):

    user = serv_db.user_login(
        session,
        data.login,
        data.password
    )

    if user is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid login or password"
        )

    return {
        "id": user.id,
        "name": user.name,
        "login": user.login,
        "role": user.role.value
    }