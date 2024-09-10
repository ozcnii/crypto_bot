import GoodGuard
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, Request, HTTPException
from fastapi_simple_rate_limiter import rate_limiter
from GoodGuard.requestsUtils import ManyRequestException
from .services import TMAAuthentication
from .auth import create_access_token, create_refresh_token, decode_token
import Database
import good_guard

router = APIRouter()

@router.get("/api/v1/user/me", tags=["user"])
@rate_limiter(limit=GoodGuard.max_requests, seconds=GoodGuard.max_time_request_seconds, exception=ManyRequestException)
async def get_user(
    request: Request,
    db: AsyncSession = Depends(Database.get_session)
):
    tma_auth = TMAAuthentication()
    user, is_new = await tma_auth.authenticate(request, db=db)
  
    if is_new:
        access_token = create_access_token({
            "sub": user.username
        })
        refresh_token = create_refresh_token({
            "sub": user.username
        })
        return {
            "access_token": access_token,
            "refresh_token": refresh_token
        }

    auth_header = request.headers.get("authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=400, detail="Invalid or missing Authorization header")
    
    # Extract the token after "Bearer "
    access_token = auth_header.split("Bearer ")[1]

    try:
        payload = decode_token(access_token)
        return user
    except HTTPException: 
        refresh_token = request.headers.get("refresh-token")
        if not refresh_token:
            raise HTTPException(status_code=401, detail="Missing refresh token")

        decoded_refresh = decode_token(refresh_token)
        if decoded_refresh["sub"] != user.username: 
            raise HTTPException(status_code=401, detail="Invalid refresh token")
    
        new_access_token = create_access_token({
            "sub": user.username
        })
        new_refresh_token = create_refresh_token({
            "sub": user.username
        })
        return {
            "access_token": new_access_token,
            "refresh_token": new_refresh_token
        }