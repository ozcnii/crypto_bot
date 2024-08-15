import httpx
from fastapi import APIRouter, HTTPException
from fastapi import Depends
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi_simple_rate_limiter import rate_limiter

import good_guard as GoodGuard
import Tools.ContentUtils
from GoodGuard.utils import *
from GoodGuard.requestsUtils import ManyRequestException
from GoodGuard.tokensFabric import check_client_id, create_hash
from Tools import Roles

import Database
from schemas import UserTokenModel, UserUpdateOwnerModel

router = APIRouter()

Users = Database.Users

@router.post('/api/v.1.0/owner/users', tags=["Owners"])
@rate_limiter(limit=GoodGuard.max_requests, seconds=GoodGuard.max_time_request_seconds, exception=ManyRequestException)
async def get_all_users(client_id: int, user: UserTokenModel, db: AsyncSession = Depends(Database.get_session)):
    if not check_client_id(client_id):
        return JSONResponse(status_code=401, content={"message": "Не авторизованый клиент"})

    person = db.query(Users).filter(Users.token == user.token).first()
    if person is None:
        return JSONResponse(status_code=401, content={"message": "Не авторизован"})
    if str(person.role) != Roles.OWNER.value:
        return JSONResponse(status_code=403, content={"message": "Недостаточно прав. Доступ запрещён"})

    users = db.query(Users).all()
    return users


@router.post("/api/v.1.0/owner/users/{id}", tags=["Owners"])
@rate_limiter(limit=GoodGuard.max_requests, seconds=GoodGuard.max_time_request_seconds, exception=ManyRequestException)
async def get_person(client_id: int, user: UserTokenModel, id: int, db: AsyncSession = Depends(Database.get_session)):
    if not check_client_id(client_id):
        return JSONResponse(status_code=401, content={"message": "Не авторизованый клиент"})

    person = db.query(Users).filter(Users.token == user.token).first()
    if person is None:
        return JSONResponse(status_code=401, content={"message": "Не авторизован"})
    if str(person.role) != Roles.OWNER.value:
        return JSONResponse(status_code=403, content={"message": "Недостаточно прав. Доступ запрещён"})

    user = db.query(Users).filter(Users.id == id).first()
    if user is None:
        return JSONResponse(status_code=404, content={"message": "Пользователь не найден"})
    
    return user


@router.delete("/api/v.1.0/owner/user/delete/{id}", tags=["Owners"])
@rate_limiter(limit=GoodGuard.max_requests, seconds=GoodGuard.max_time_request_seconds, exception=ManyRequestException)
async def delete_person(client_id: int, user: UserTokenModel, id: int, db: AsyncSession = Depends(Database.get_session)):
    if not check_client_id(client_id):
        raise HTTPException(status_code=401, detail="Не авторизованый клиент")

    # Retrieve the owner from the database
    owner = db.query(Users).filter(Users.token == user.token).first()
    if owner is None:
        raise HTTPException(status_code=401, detail="Не авторизован")
    if str(owner.role) != Roles.OWNER.value:
        raise HTTPException(status_code=403, detail="Недостаточно прав. Доступ запрещён")

    if owner.id == id: # type: ignore
        raise HTTPException(status_code=400, detail="Нельзя удалить самого себя")

    # Retrieve the user to be deleted from the database
    user_to_delete = db.query(Users).filter(Users.id == id).first()
    if user_to_delete is None:
        raise HTTPException(status_code=404, detail="Пользователь не найден")

    # Delete the user
    db.delete(user_to_delete)
    db.commit() 
    return JSONResponse(status_code=200, content={"message": "Пользователь удалён"})