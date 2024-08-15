from fastapi import APIRouter
from fastapi import Depends
from fastapi_simple_rate_limiter import rate_limiter
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import JSONResponse

# GOODGUARD
import good_guard as GoodGuard
from GoodGuard.requestsUtils import ManyRequestException
from GoodGuard.tokensFabric import check_client_id

# TOOLS
from Tools import Roles
import Database
from schemas import UserTokenModel

router = APIRouter()

Users = Database.Users

@router.post("/api/v.1.0/moderator/users", tags=["Moderators"])
@rate_limiter(limit=GoodGuard.max_requests, seconds=GoodGuard.max_time_request_seconds, exception=ManyRequestException)
async def get_v2_peoples(client_id: int, user: UserTokenModel, db: AsyncSession = Depends(Database.get_session)):
    if not check_client_id(client_id):
        return JSONResponse(status_code=401, content={"message": "Не авторизованый клиент"})

    person = db.query(Users).filter(Users.token == user.token).first()
    if person is None:
        return JSONResponse(status_code=401, content={"message": "Не авторизован"})
    if person.role != Roles.MODERATOR.value and person.role != Roles.OWNER.value:
        return JSONResponse(status_code=403, content={"message": "Недостаточно прав. Доступ запрещён"})

    users_list = db.query(Users).all()
    return JSONResponse(status_code=200, content={
        "success": True,
        "data": [{
            # ROOT
            "id": user.id,
            "user_id": user.user_id,

            # USER DATA
            "username": user.username,
            "league": user.league,
            "clan_by": user.clan_by,

            # SYSTEM DATA
            "role": user.role,

            "blocked": user.blocked,
            "created_at": user.created_at,

            # STATISTIC DATA
            "balance": user.balance,

            "p_n_l": user.p_n_l,
            "power": user.power,
        } for user in users_list],
        "meta": {"total_users": len(users_list)}
    })