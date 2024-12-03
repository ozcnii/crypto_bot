# GOODGUARD
from coinmarketcapapi import CoinMarketCapAPI, CoinMarketCapAPIError
from fastapi import APIRouter, Body, HTTPException, Depends, Header, Query, UploadFile, File
from datetime import datetime, timedelta
from fastapi import Depends
from fastapi_simple_rate_limiter import rate_limiter
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from starlette.responses import JSONResponse
from Tools.uploadFileToBucket import upload_avatar
from schemas import UserModel, UserTokenModel
import requests
from pydantic import BaseModel
# GOODGUARD
from good_guard import max_requests, max_time_request_seconds
import GoodGuard.utils
from GoodGuard.requestsUtils import ManyRequestException
from GoodGuard.tokensFabric import *
import Database
# TOOLS
from schemas import UserTokenModel

router = APIRouter()

Clans = Database.Clans
Users = Database.Users
    
@router.post("/api/v.1.0/users/upload_avatar", tags=["Buckets"])
@rate_limiter(limit=max_requests, seconds=max_time_request_seconds, exception=ManyRequestException)
async def upload_user_avatar(
    client_id: int,
    Authorization: str = Header(...),
    file: UploadFile = File(...),
    db: AsyncSession = Depends(Database.get_session)
):  
    user = Authorization.split(" ")[1]
    async with db as session:
        result = await session.execute(select(Users).filter(Users.token == user))
        person = result.scalars().first()

        if person is None:
            return JSONResponse(status_code=404, content={"message": "Пользователь не найден"})
        if person is False:
            return JSONResponse(status_code=401, content={"message": "Не авторизован"})
        
        if not check_client_id(client_id):
            return JSONResponse(status_code=401, content={"message": "Не авторизованный клиент"})

        avatar_url = await upload_avatar(file.file.read(), file.filename)
        if avatar_url:
            person.avatar_url = avatar_url
            db.commit()
            return {"avatar_url": avatar_url}
        return {"error": "Upload failed"}

@router.post("/api/v.1.0/clans/upload_logo", tags=["Buckets"])
@rate_limiter(limit=max_requests, seconds=max_time_request_seconds, exception=ManyRequestException)
async def upload_clan_logo(
    client_id: int,
    Authorization: str = Header(...),
    file: UploadFile = File(...),
    db: AsyncSession = Depends(Database.get_session)
):
    user = Authorization.split(" ")[1]

    async with db as session:
        result = await session.execute(select(Users).filter(Users.token == user))
        person = result.scalars().first()

        if person is None:
            return JSONResponse(status_code=404, content={"message": "Пользователь не найден"})
        if person is False:
            return JSONResponse(status_code=401, content={"message": "Не авторизован"})
        
        if not check_client_id(client_id):
            return JSONResponse(status_code=401, content={"message": "Не авторизованный клиент"})

        result = await session.execute(select(Clans).filter(Clans.id == int(person.clan_id)))
        clan = result.scalars().first()
        
        if clan is None:
            return JSONResponse(status_code=404, content={"message": "Клан не найден"})
        
        if clan.owner_id != person.id:
            return JSONResponse(status_code=403, content={"message": "У вас нет прав на изменение аватарки этого клана"})
        
        logo_url = await upload_avatar(file.file.read(), file.filename)
        if logo_url:
            clan.logo_url = logo_url
            db.commit()
            return {"logo_url": logo_url}
        return {"error": "Upload failed"}

@router.post("/api/v.1.0/coin/getCoinInfo", tags=["Buckets"])
@rate_limiter(limit=max_requests, seconds=max_time_request_seconds, exception=ManyRequestException)
async def get_coin_info(
    client_id: int = Query(...),
    network: str = Body(...),
    contract_address: str = Body(...),
    Authorization: str = Header(...),
    db: AsyncSession = Depends(Database.get_session)
):
    if not check_client_id(client_id):
        return JSONResponse(status_code=401, content={"message": "Не авторизованный клиент"})
    
    user = Authorization.split(" ")[1]
    
    async with db as session:
        result = await session.execute(select(Users).filter(Users.token == user))
        person = result.scalars().first()

        if person is None:
            return JSONResponse(status_code=404, content={"message": "Пользователь не найден"})
        if person is False:
            return JSONResponse(status_code=401, content={"message": "Не авторизован"})
        API_KEY = '36fe7774-2dc3-4a45-a63b-4d5ea8a4d2da'
        try:
            # Получение текущей информации о криптовалюте
            current_url = f"https://pro-api.coinmarketcap.com/v4/dex/pairs/quotes/latest?network_slug={network}&contract_address={contract_address}"
            headers = { "X-CMC_PRO_API_KEY": API_KEY }  # Замените на ваш API-ключ
            response = requests.get(current_url, headers=headers)
            response.raise_for_status()
            current_data = response.json()
            
            if "data" not in current_data:
                raise HTTPException(status_code=404, detail="Data not found")

            resp = requests.get(f"https://pro-api.coinmarketcap.com/v4/dex/pairs/ohlcv/historical?network_slug={network}&contract_address={contract_address}", headers=headers)
            resp.raise_for_status()
            current = resp.json()
            
            if "data" not in current:
                raise HTTPException(status_code=404, detail="Data not found")

            historical_data = current["data"]
            candles = []
            for entry in historical_data:
                for quote in entry['quotes']:
                    for q in quote['quote']:
                        candles.append({
                            "timestamp": datetime.fromisoformat(quote['time_open'].replace('Z', '+00:00')).strftime('%Y-%m-%d %H:%M:%S'),
                            "open": q['open'],
                            "high": q['high'],
                            "low": q['low'],
                            "close": q['close'],
                            "volume": q['volume']
                        })

            
            return {
                "name": current_data['data'][0]['base_asset_name'],
                "network_slug": current_data['data'][0]['network_slug'],
                "logo": "URL to the logo",
                "price": current_data['data'][0]['quote'][0]['price'],
                "percent_change_24h": current_data['data'][0]['quote'][0]['percent_change_price_24h'],
                "contract_address": contract_address,
                "candles": candles
            }

        except requests.RequestException as e:
            raise HTTPException(status_code=500, detail=str(e))