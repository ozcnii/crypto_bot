from typing import Any

import uvicorn
from fastapi import FastAPI, Request, Depends
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.middleware.cors import CORSMiddleware
import contextlib
from typing import AsyncIterator

from fastapi_simple_rate_limiter import rate_limiter
from starlette.responses import JSONResponse

import GoodGuard
from database import Base, create_async_engine, AsyncSession, get_db, engine
from good_guard import DATABASE_URL

# GOODGUARD
from GoodGuard import *
from GoodGuard.requestsUtils import *

# FASTAPI Routes
from routes import owners_routes
from routes import users_routes
from routes import admins_routes
from routes import bucket_routes
from routes import good_guard_routes
from routes import moderation_routes

import Database

tags_metadata = [
    {"name": "Owners", "description": "Methods for the owner"},
    {"name": "Admins", "description": "Methods for the admins"},
    {"name": "Moderators", "description": "Methods for the moderators"},
    {"name": "Users Methods", "description": "User management"},
    {"name": "Friends Methods", "description": "User management"},
    {"name": "Test A/B", "description": "These methods are not yet available to ordinary users, but they will be available soon"},
    {"name": "Buckets", "description": "Getting bucket database elements"},
    {"name": "Old Methods", "description": "deprecated methods that will be removed soon"}
]

@contextlib.asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    Database.db_manager.init(DATABASE_URL)
    yield
    await Database.db_manager.close()

app = FastAPI(
    title='CryptoAPI', version='1.0.0',
    openapi_tags=tags_metadata,
    docs_url="/Q29Cryptonashka", redoc_url=None,
    lifespan=lifespan
)

app.add_middleware(TrustedHostMiddleware, allowed_hosts=["*"])

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(owners_routes)
app.include_router(admins_routes)
app.include_router(moderation_routes)
app.include_router(good_guard_routes)
app.include_router(users_routes)
app.include_router(bucket_routes)

@app.exception_handler(ManyRequestException)
async def custom_exception_handler(request: Request, exc: ManyRequestException):
    content = {
        "success": False,
        "error": {
            "message": exc.message
        }
    }
    return JSONResponse(
        status_code=exc.status_code,
        content=content,
    )

@app.get("/")
@rate_limiter(limit=GoodGuard.max_requests, seconds=GoodGuard.max_time_request_seconds, exception=ManyRequestException)
async def root(db: AsyncSession = Depends(Database.get_session)):
    return {"message": "Hello Crypto!"}

if __name__ == "__main__":
    uvicorn.run('main:app', host='0.0.0.0', port=8080, reload=True)