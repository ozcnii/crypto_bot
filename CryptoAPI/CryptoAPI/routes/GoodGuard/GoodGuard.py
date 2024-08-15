import os

from fastapi import APIRouter, UploadFile, File, Depends

from fastapi_simple_rate_limiter import rate_limiter
from sqlalchemy import true
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession

from starlette.responses import JSONResponse
import requests

# GOODGUARD
import good_guard as GoodGuard
from GoodGuard import VIRUSTOTAL_API_KEY
from GoodGuard.requestsUtils import ManyRequestException
from GoodGuard.tokensFabric import check_client_id, check_email_user
from GoodGuard.utils import *

# TOOLS
from schemas import UserEmailModel, UserTokenModel

import Database

router = APIRouter()

Users = Database.Users
VerificationCodes = Database.VerificationCodes
VerificationRestoreCodes = Database.VerificationRestoreCodes

@router.post("/api/v.1.0/oauth/get_verify_email", tags=["GoodGuard"])
@rate_limiter(limit=GoodGuard.max_requests, seconds=GoodGuard.max_time_request_seconds, exception=ManyRequestException)
async def check_verification_email_code(client_id: int, user: UserEmailModel, db: AsyncSession = Depends(Database.get_session)):
    if not check_client_id(client_id):
        return JSONResponse(status_code=401, content={"message": "Не авторизованный клиент"})

    if not check_email_user(user.email):
        return JSONResponse(status_code=400, content={"message": "Некорректный Email адрес"})

    existing_verification = db.query(VerificationCodes).filter(VerificationCodes.user_email == user.email).first()

    if not existing_verification:
        return JSONResponse(status_code=404, content={"message": "Email не найден"})

    if not existing_verification.verify_code.is_(true()):
        return JSONResponse(status_code=200, content={"is_verify_email": False})

    return JSONResponse(status_code=200, content={"is_verify_email": True})


@router.post("/api/v.1.0/oauth/get_verify_email_restore", tags=["GoodGuard"])
@rate_limiter(limit=GoodGuard.max_requests, seconds=GoodGuard.max_time_request_seconds, exception=ManyRequestException)
async def check_verification_email_restore_code(client_id: int, user: UserEmailModel, db: AsyncSession = Depends(Database.get_session)):
    if not check_client_id(client_id):
        return JSONResponse(status_code=401, content={"message": "Не авторизованный клиент"})

    if not check_email_user(user.email):
        return JSONResponse(status_code=400, content={"message": "Некорректный Email адрес"})

    existing_verification = db.query(VerificationRestoreCodes).filter(VerificationRestoreCodes.user_email == user.email).first()

    if not existing_verification:
        return JSONResponse(status_code=404, content={"message": "Email не найден"})

    if not existing_verification.verify_code.is_(true()):
        return JSONResponse(status_code=200, content={"is_verify_email": False})

    return JSONResponse(status_code=200, content={"is_verify_email": True})


@router.post("/api/v.1.0/oauth/get_verify_token", tags=["GoodGuard"])
@rate_limiter(limit=GoodGuard.max_requests, seconds=GoodGuard.max_time_request_seconds, exception=ManyRequestException)
async def check_verification_token(client_id: int, user: UserTokenModel, db: AsyncSession = Depends(Database.get_session)):
    if not check_client_id(client_id):
        return JSONResponse(status_code=401, content={"message": "Не авторизованный клиент"})

    existing_verification = db.query(Users).filter(Users.token == user.token).first()

    if not existing_verification:
        return JSONResponse(status_code=401, content={"is_verify_token": False})

    return JSONResponse(status_code=200, content={"is_verify_token": True})
