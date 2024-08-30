from fastapi import APIRouter, Body, Header, Query, Path, BackgroundTasks
from fastapi import Depends
from fastapi_simple_rate_limiter import rate_limiter
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import update, event
from sqlalchemy.orm import selectinload, joinedload
import os

# GOODGUARD
import Database
from Tools.uploadFileToBucket import upload_avatar, get_s3_file_etag, delete_avatar
from Tools.checkBotInChat import check_bot_in_chat_or_group, download_file
import good_guard as GoodGuard
# import GoodGuard.utils
from GoodGuard.requestsUtils import ManyRequestException
from GoodGuard.tokensFabric import *

# TOOLS
from Tools.ContentUtils import serialize_json_user_token
from Tools.dex import get_current_rate, calculate_pnl
from schemas import UserModel, OrderCreateModel
import asyncio
from datetime import datetime
import pytz

router = APIRouter()

Users = Database.Users
Clans = Database.Clans
League = Database.League
TaskType = Database.TaskType
Task = Database.Task
UserTask = Database.UserTask
Orders = Database.Order

async def update_task_progress(user_id: int, task_type: TaskType, increment_value: int, db: AsyncSession):
    # Найти активное задание для пользователя по типу задания
    result = await db.execute(select(UserTask).join(Task).filter(UserTask.user_id == user_id, Task.type == task_type, UserTask.completed == False).options(selectinload(UserTask.task)))
    user_task = result.scalars().first()
    
    if user_task:
        # Обновить прогресс
        user_task.progress += increment_value
        await db.commit()
        
async def update_tasks_and_invite_friends(
    session: AsyncSession,
    user_id: int,
    referrer: Users = None
):
    # Если у пользователя нет заданий, добавляем их
    task_result = await session.execute(select(UserTask).filter(UserTask.user_id == user_id))
    user_tasks = task_result.scalars().all()

    if not user_tasks:
        tasks = await session.execute(select(Task))
        tasks = tasks.scalars().all()
        for task in tasks:
            user_task = UserTask(user_id=user_id, task_id=task.id)
            session.add(user_task)
        await session.commit()

    # Обновление задания "invite_friends"
    if referrer:
        task_result = await session.execute(
            select(UserTask).filter(UserTask.user_id == referrer.id, UserTask.completed == False)
        )
        user_tasks = task_result.scalars().all()

        for user_task in user_tasks:
            if user_task.task.task_type == 'invite_friends':
                user_task.progress += 1
                if user_task.progress >= user_task.task.target_value:
                    user_task.completed = True
                    referrer.balance += user_task.task.reward
                    session.add(referrer)
                session.add(user_task)

        await session.commit()
        await session.refresh(referrer)
        
async def update_avatar_and_league(
    session: AsyncSession, 
    user_id: int, 
    file_path: str, 
    league_id: int,
    alreadyInLeague: bool
):
    # Загрузка и обновление аватара пользователя
    result = await session.execute(select(Users).filter(Users.id == user_id))
    user = result.scalars().first()
    
    existing_avatar_hash = user.avatar_url
    
    file_content = await download_file(file_path)
    file_hash = hashlib.sha256(file_path.encode('utf-8')).hexdigest()
    avatar_key = f"{file_hash}{os.path.splitext(file_path)[1]}"
    
    if existing_avatar_hash:
        if existing_avatar_hash != avatar_key:
            await delete_avatar(existing_avatar_hash)
            await upload_avatar(file_content=file_content, avatar_key=avatar_key)
            await session.execute(
                update(Users).filter(Users.id == user_id).values({Users.avatar_url: avatar_key})
            )
            await session.commit()
        else:
            avatar_key = existing_avatar_hash
    else:
        await upload_avatar(file_content=file_content, avatar_key=avatar_key)
        await session.execute(
            update(Users).filter(Users.id == user_id).values({Users.avatar_url: avatar_key})
        )
        await session.commit()
    
    # Обновление данных лиги
    if not alreadyInLeague:
        result = await session.execute(select(League).filter(League.id == league_id))
        league = result.scalars().first()
        if league:
            league.user_count += 1
            session.add(league)
            await session.commit()

@router.post('/api/v.1.0/oauth/create_user', tags=["Users Methods"])
@rate_limiter(limit=GoodGuard.max_requests, seconds=GoodGuard.max_time_request_seconds, exception=ManyRequestException)
async def create_v2_user(
    client_id: int = Query(...),
    user: UserModel = Body(...),
    referral_code: str = Query(None),
    background_tasks: BackgroundTasks = BackgroundTasks(),
    db: AsyncSession = Depends(Database.get_session)
):
    if not check_client_id(client_id):
        return JSONResponse(status_code=401, content={"message": "Не авторизован"})

    async with db as session:
        result = await session.execute(select(Users).filter(Users.user_id == user.user_id))
        existing_user = result.scalars().first()

        if existing_user:
            need_to_update = False
            update_values = {}

            if existing_user.referrer_id is None and referral_code:
                referrer_result = await session.execute(select(Users).filter(Users.referral_code == referral_code))
                referrer = referrer_result.scalars().first()
                if referrer:
                    existing_user.referrer_id = referrer.id
                    referrer.balance += 100 if not referrer.is_premium else 1000
                    session.add(referrer)
                    need_to_update = True

            if existing_user.username != user.username:
                update_values[Users.username] = user.username
                need_to_update = True

            if existing_user.is_premium != user.is_premium:
                update_values[Users.is_premium] = user.is_premium
                need_to_update = True

            if need_to_update:
                await session.execute(update(Users).filter(Users.user_id == user.user_id).values(update_values))
                await session.commit()

            # Запуск фоновой задачи для обновления аватара, лиги и заданий
            background_tasks.add_task(update_avatar_and_league, session, existing_user.id, user.file_path, existing_user.league_id, True)
            background_tasks.add_task(update_tasks_and_invite_friends, session, existing_user.id, referrer if referral_code else None)
            
            return existing_user
        else:
            new_user = Users(
                user_id=user.user_id,
                username=user.username,
                token=generate_access_token(user_data=serialize_json_user_token(user)),
                is_premium=user.is_premium,
                referral_code=generate_verification_code(10) if referral_code else None
            )
            session.add(new_user)
            await session.commit()

            referrer = None
            if referral_code:
                referrer_result = await session.execute(select(Users).filter(Users.referral_code == referral_code))
                referrer = referrer_result.scalars().first()
                if referrer:
                    referrer.balance += 100 if not referrer.is_premium else 1000
                    new_user.referrer_id = referrer.id
                    session.add(referrer)
                    await session.commit()

            # Запуск фоновой задачи для обновления аватара, лиги и заданий
            background_tasks.add_task(update_avatar_and_league, session, new_user.id, user.file_path, new_user.league_id, False)
            background_tasks.add_task(update_tasks_and_invite_friends, session, new_user.id, referrer)
            
            return new_user

@router.get("/api/v.1.0/tasks", tags=["Users Methods"])
@rate_limiter(limit=GoodGuard.max_requests, seconds=GoodGuard.max_time_request_seconds, exception=ManyRequestException)
async def get_user_tasks_v2(
    client_id: int,
    Authorization: str = Header(...),
    db: AsyncSession = Depends(Database.get_session)
):
    if not check_client_id(client_id):
        return JSONResponse(status_code=401, content={"message": "Не авторизованный клиент"})

    try:
        user = Authorization.split(" ")[1]
    except:
        return JSONResponse(status_code=401, content={"message": "Не авторизован"})


    async with db as session:
        result = await session.execute(
            select(Users)
            .filter(Users.token == user)
            .options(selectinload(Users.user_tasks).selectinload(UserTask.task))  # Предварительная загрузка связанных данных
        )
        person = result.scalars().first()

        if person is None:
            return JSONResponse(status_code=404, content={"message": "Пользователь не найден"})
        if person is False:
            return JSONResponse(status_code=401, content={"message": "Не авторизован"})

        user_tasks = []
        for user_task in person.user_tasks:
            user_tasks.append({
                "id": user_task.id,
                "name": user_task.task.name,
                "description": user_task.task.description,
                "progress": user_task.progress,
                "target_value": user_task.task.target_value,
                "reward": user_task.task.reward,
                "completed": user_task.completed,
                "task_type": user_task.task.type
            })

        return user_tasks

@router.post("/api/v.1.0/tasks/{task_id}/complete", tags=["Users Methods"])
@rate_limiter(limit=GoodGuard.max_requests, seconds=GoodGuard.max_time_request_seconds, exception=ManyRequestException)
async def complete_user_task_v2(
    client_id: int,
    task_id: int,
    Authorization: str = Header(...),
    db: Session = Depends(Database.get_session)
):
    if not check_client_id(client_id):
        return JSONResponse(status_code=401, content={"message": "Не авторизованный клиент"})

    try:
        user = Authorization.split(" ")[1]
    except:
        return JSONResponse(status_code=401, content={"message": "Не авторизован"})

    async with db as session:
        result = await session.execute(select(Users).filter(Users.token == user).options(selectinload(Users.user_tasks).selectinload(UserTask.task)))
        person = result.scalars().first()

        if person is None:
            return JSONResponse(status_code=404, content={"message": "Пользователь не найден"})
        if person is False:
            return JSONResponse(status_code=401, content={"message": "Не авторизован"})
        
        user_task = {}
        for ut in person.user_tasks:
            if ut.task_id == task_id:
                user_task = ut
        
        if user_task is None:
            return JSONResponse(status_code=404, content={"message": "Задание не найдено"})
        if user_task.completed:
            return JSONResponse(status_code=400, content={"message": "Задание уже завершено"})
        
        if user_task.task.type == TaskType.EARN_COINS:
            if person.balance >= user_task.task.target_value:
                user_task.completed = True
                person.balance += user_task.task.reward

                await session.commit()
                await session.refresh(person)
                return JSONResponse(status_code=200, content={"message": "Задание завершено", "id": user_task.id})
        
        if user_task.progress >= user_task.task.target_value:
            user_task.completed = True
            person.balance += user_task.task.reward
                
            await session.commit()
            await session.refresh(person)
            return JSONResponse(status_code=200, content={"message": "Задание завершено", "id": user_task.id})
        
        return JSONResponse(status_code=400, content={"message": "Задание не завершено"})

@router.get("/api/v.1.0/users/current_user/fellows", tags=["Users Methods"])
@rate_limiter(limit=GoodGuard.max_requests, seconds=GoodGuard.max_time_request_seconds, exception=ManyRequestException)
async def get_v2_current_user_fellows(
    client_id: int,
    Authorization: str = Header(...),
    db: Session = Depends(Database.get_session)
):
    if not check_client_id(client_id):
        return JSONResponse(status_code=401, content={"message": "Не авторизованный клиент"})

    try:
        user = Authorization.split(" ")[1]
    except:
        return JSONResponse(status_code=401, content={"message": "Не авторизован"})

    async with db as session:
        result = await session.execute(select(Users).filter(Users.token == user))
        person = result.scalars().first()

        if person is None:
            return JSONResponse(status_code=404, content={"message": "Пользователь не найден"})
        if person is False:
            return JSONResponse(status_code=401, content={"message": "Не авторизован"})

        result = await session.execute(select(Users).filter(Users.referrer_id == person.id))
        fellows = result.scalars().all()
        
        fellows_list = []
        for fellow in fellows:
            fellows_list.append({
                "id": fellow.id,
                "username": fellow.username,
                "avatar_url": fellow.avatar_url,
                "salary": fellow.is_premium and 1000 or 100
            })

@router.get("/api/v.1.0/users/current_user", tags=["Users Methods"])
@rate_limiter(limit=GoodGuard.max_requests, seconds=GoodGuard.max_time_request_seconds, exception=ManyRequestException)
async def get_v2_current_user(
    client_id: int,
    Authorization: str = Header(...),
    db: Session = Depends(Database.get_session)
):
    if not check_client_id(client_id):
        return JSONResponse(status_code=401, content={"message": "Не авторизованный клиент"})

    try:
        user = Authorization.split(" ")[1]
    except:
        return JSONResponse(status_code=401, content={"message": "Не авторизован"})

    async with db as session:
        result = await session.execute(select(Users).filter(Users.token == user))
        person = result.scalars().first()

        if person is None:
            return JSONResponse(status_code=404, content={"message": "Пользователь не найден"})
        if person is False:
            return JSONResponse(status_code=401, content={"message": "Не авторизован"})

        return person


@router.get("/api/v.1.0/users/current_user/clan", tags=["Users Methods"])
@rate_limiter(limit=GoodGuard.max_requests, seconds=GoodGuard.max_time_request_seconds, exception=ManyRequestException)
async def get_v2_current_user_clan(
    client_id: int,
    Authorization: str = Header(...),
    db: AsyncSession = Depends(Database.get_session)
):
    if not check_client_id(client_id):
        return JSONResponse(status_code=401, content={"message": "Не авторизованный клиент"})

    try:
        user = Authorization.split(" ")[1]
    except:
        return JSONResponse(status_code=401, content={"message": "Не авторизован"})

    
    async with db as session:
        result = await session.execute(select(Users).filter(Users.token == user))
        person = result.scalars().first()

        if person is None:
            return JSONResponse(status_code=404, content={"message": "Пользователь не найден"})
        if person is False:
            return JSONResponse(status_code=401, content={"message": "Не авторизован"})

        if person.clan_id is None:
            return JSONResponse(status_code=404, content={"message": "Клан не найден"})

        result = await session.execute(select(Clans).filter(Clans.id == person.clan_id))
        clan = result.scalars().first()

        if clan is None:
            return JSONResponse(status_code=404, content={"message": "Клан не найден"})

        return clan


@router.post("/api/v.1.0/users/clan/create", tags=["Users Methods"])
@rate_limiter(limit=GoodGuard.max_requests, seconds=GoodGuard.max_time_request_seconds, exception=ManyRequestException)
async def create_v2_clan(
    link: str = Body(...),
    client_id: int = Query(...),
    Authorization: str = Header(...),
    db: AsyncSession = Depends(Database.get_session)
):
    try:
        user = Authorization.split(" ")[1]
    except:
        return JSONResponse(status_code=401, content={"message": "Не авторизован"})

    
    if not check_client_id(client_id):
        return JSONResponse(status_code=401, content={"message": "Не авторизованный клиент"})

    async with db as session:
        result = await session.execute(select(Users).filter(Users.token == user))
        person = result.scalars().first()

        if person is None:
            return JSONResponse(status_code=404, content={"message": "Пользователь не найден"})
        if person is False:
            return JSONResponse(status_code=401, content={"message": "Не авторизован"})
    
        match = re.search(r't\.me/([a-zA-Z0-9_]+)', link)
        if match:
            name = match.group(1)
        else:
            return JSONResponse(status_code=400, content={"message": "Некорректная ссылка"})
    
        bot_in_chat = await check_bot_in_chat_or_group(link)
        if not bot_in_chat:
            return JSONResponse(status_code=400, content={"message": "Бот не найден в указанном канале или группе"})
    
        result = await session.execute(select(Clans).filter(Clans.name == name))
        clan = result.scalars().first()
        
        if clan is not None:
            return JSONResponse(status_code=400, content={"message": "Клан уже существует"})
    
        # Создание нового клана
        new_clan = Clans(
            name=name,
            link=link,
            users=1,
            owner_id=person.id
        )

        session.add(new_clan)
        await session.commit()

        new_clan.balance += person.balance
        # Обновление параметра clan_by в person
        person.clan_id = new_clan.id
        session.add(person)
        await session.commit()
        
        # Обновление задания "join_clan"
        await update_task_progress(person.id, TaskType.JOIN_SQUAD, 1, session)
        
        return JSONResponse(status_code=200, content={
            "id": new_clan.id,
            "message": "Клан успешно создан"
        })
        
@event.listens_for(Users.balance, 'set', propagate=True)
def update_clan_balance_on_user_balance_change(target, value, oldvalue, initiator):
    if target.clan:
        asyncio.create_task(_update_clan_balance(target.clan))

async def _update_clan_balance(clan):
    async with Database.get_session() as session:
        await clan.update_balance()
        session.add(clan)
        await session.commit()
        
@router.delete("/api/v.1.0/users/clan/delete", tags=["Users Methods"])
@rate_limiter(limit=GoodGuard.max_requests, seconds=GoodGuard.max_time_request_seconds, exception=ManyRequestException)
async def delete_v2_clan(
    link: str = Body(...),
    client_id: int = Query(...),
    Authorization: str = Header(...),
    db: AsyncSession = Depends(Database.get_session)
):
    try:
        user = Authorization.split(" ")[1]
    except:
        return JSONResponse(status_code=401, content={"message": "Не авторизован"})

    
    if not check_client_id(client_id):
        return JSONResponse(status_code=401, content={"message": "Не авторизованный клиент"})

    async with db as session:
        result = await session.execute(select(Users).filter(Users.token == user))
        person = result.scalars().first()

        if person is None:
            return JSONResponse(status_code=404, content={"message": "Пользователь не найден"})
        if person is False:
            return JSONResponse(status_code=401, content={"message": "Не авторизован"})

        result = await session.execute(select(Clans).filter(Clans.link == link))
        clan = result.scalars().first()

        if clan is None:
            return JSONResponse(status_code=404, content={"message": "Клан не найден"})

        if clan.owner_id != person.id:
            return JSONResponse(status_code=403, content={"message": "У вас нет прав на удаление этого клана"})

        # Удаление клана
        await session.delete(clan)
        await session.commit()
        
        # Обновление параметра clan_by в person
        person.clan_id = None
        session.add(person)
        await session.commit()

        return JSONResponse(status_code=200, content={"message": "Клан успешно удален"})


@router.get("/api/v.1.0/users/clan/leave", tags=["Users Methods"])
@rate_limiter(limit=GoodGuard.max_requests, seconds=GoodGuard.max_time_request_seconds, exception=ManyRequestException)
async def clan_leave(
    Authorization: str = Header(...),
    client_id: int = Query(...),
    db: AsyncSession = Depends(Database.get_session)
):
    if not check_client_id(client_id):
        return JSONResponse(status_code=401, content={"message": "Не авторизованный клиент"})
    
    try:
        user = Authorization.split(" ")[1]
    except:
        return JSONResponse(status_code=401, content={"message": "Не авторизован"})

    
    async with db as session:
        result = await session.execute(select(Users).filter(Users.token == user))
        person = result.scalars().first()

        if person is None:
            return JSONResponse(status_code=404, content={"message": "Пользователь не найден"})
        if person is False:
            return JSONResponse(status_code=401, content={"message": "Не авторизован"})

        if person.clan_id == None:
            return JSONResponse(status_code=400, content={"message": "Вы не состоите в клане"})

        result = await session.execute(select(Clans).filter(Clans.id == person.clan_id))
        clan = result.scalars().first()
        
        if clan is None:
            return JSONResponse(status_code=404, content={"message": "Клан не найден"})

        person.clan_id = None
        session.add(person)
        clan.users -= 1
        clan.balance -= person.balance
        session.add(clan)
        
        await session.commit()

        return JSONResponse(status_code=200, content={"message": "Пользователь успешно покинул клан"})


@router.post("/api/v.1.0/users/clan/join", tags=["Users Methods"])
@rate_limiter(limit=GoodGuard.max_requests, seconds=GoodGuard.max_time_request_seconds, exception=ManyRequestException)
async def clan_join(
    Authorization: str = Header(...),
    id: int = Body(...),
    client_id: int = Query(...),
    db: AsyncSession = Depends(Database.get_session)
):
    if not check_client_id(client_id):
        return JSONResponse(status_code=401, content={"message": "Не авторизованный клиент"})

    try:
        user_token = Authorization.split(" ")[1]
    except:
        return JSONResponse(status_code=401, content={"message": "Не авторизован"})

    
    async with db as session:
        result = await session.execute(select(Users).filter(Users.token == user_token))
        person = result.scalars().first()

        if person is None:
            return JSONResponse(status_code=404, content={"message": "Пользователь не найден"})
        if person is False:
            return JSONResponse(status_code=401, content={"message": "Не авторизован"})

        result = await session.execute(select(Clans).filter(Clans.id == id))
        clan = result.scalars().first()

        if clan is None:
            return JSONResponse(status_code=404, content={"message": "Клан не найден"})
        
        if person.clan_id is not None:
            return JSONResponse(status_code=400, content={"message": "Вы уже состоите в клане"})

        person.clan_id = id
        session.add(person)
        clan.users += 1
        clan.balance += person.balance
        session.add(clan)

        # Проверка и обновление задачи
        task_result = await session.execute(
            select(UserTask).filter(UserTask.user_id == person.id, UserTask.completed == False)
        )
        user_tasks = task_result.scalars().all()

        for user_task in user_tasks:
            if user_task.task.task_type == 'join_clan':
                user_task.completed = True
                session.add(user_task)

                # Добавление награды
                person.balance += user_task.task.reward
                session.add(person)

        await session.commit()

        return JSONResponse(status_code=200, content={"message": "Пользователь успешно присоединился к клану"})


@router.get("/api/v.1.0/users/clan/list", tags=["Users Methods"])
@rate_limiter(limit=GoodGuard.max_requests, seconds=GoodGuard.max_time_request_seconds, exception=ManyRequestException)
async def get_v2_current_user_clan_list(
    client_id: int,
    Authorization: str = Header(...),
    db: AsyncSession = Depends(Database.get_session)
):
    if not check_client_id(client_id):
        return JSONResponse(status_code=401, content={"message": "Не авторизованный клиент"})

    try:
        user = Authorization.split(" ")[1]
    except:
        return JSONResponse(status_code=401, content={"message": "Не авторизован"})

    
    async with db as session:
        result = await session.execute(select(Users).filter(Users.token == user))
        person = result.scalars().first()

        if person is None:
            return JSONResponse(status_code=404, content={"message": "Пользователь не найден"})
        if person is False:
            return JSONResponse(status_code=401, content={"message": "Не авторизован"})

        result = await session.execute(select(Clans).filter(Clans.id == person.clan_id))
        clan = result.scalars().first()
        
        if clan is None:
            return JSONResponse(status_code=404, content={"message": "Клан не найден"})

        result = await session.execute(select(Users).filter(Users.clan_id == int(person.clan_id)).order_by(Users.balance.desc()))
        
        users = result.scalars().all()

        user_list = []
        for user in users:
            user_list.append({
                "username": user.username,
                "balance": user.balance,
                "p_n_l": user.p_n_l
            })

        return user_list

@router.get("/api/v.1.0/clans/list", tags=["Users Methods"])
@rate_limiter(limit=GoodGuard.max_requests, seconds=GoodGuard.max_time_request_seconds, exception=ManyRequestException)
async def get_v2_clan_list(
    client_id: int,
    Authorization: str = Header(...),
    db: AsyncSession = Depends(Database.get_session)
):
    if not check_client_id(client_id):
        return JSONResponse(status_code=401, content={"message": "Не авторизованный клиент"})

    try:
        user = Authorization.split(" ")[1]
    except:
        return JSONResponse(status_code=401, content={"message": "Не авторизован"})

    
    async with db as session:
        result = await session.execute(select(Users).filter(Users.token == user))
        person = result.scalars().first()

        if person is None:
            return JSONResponse(status_code=404, content={"message": "Пользователь не найден"})
        if person is False:
            return JSONResponse(status_code=401, content={"message": "Не авторизован"})

        result = await session.execute(select(Clans).options(selectinload(Clans.league)))

        clans = result.scalars().all()

        clan_list = []
        for clan in clans:
            clan_list.append({
                "id": clan.id,
                "name": clan.name,
                "league": clan.league.name,
                "logo_url": clan.logo_url
            })

        return clan_list

@router.get("/api/v.1.0/clans/info", tags=["Users Methods"])
@rate_limiter(limit=GoodGuard.max_requests, seconds=GoodGuard.max_time_request_seconds, exception=ManyRequestException)
async def get_v2_clan_info(
    client_id: int = Query(...),
    Authorization: str = Header(...),
    db: AsyncSession = Depends(Database.get_session),
    clan_id: int = Query(...)
):
    if not check_client_id(client_id):
        return JSONResponse(status_code=401, content={"message": "Не авторизованный клиент"})
    
    try:
        user = Authorization.split(" ")[1]
    except:
        return JSONResponse(status_code=401, content={"message": "Не авторизован"})


    async with db.begin():  # Используйте контекстное управление транзакциями
        result = await db.execute(select(Users).filter(Users.token == user))
        person = result.scalars().first()

        if person is None:
            return JSONResponse(status_code=404, content={"message": "Пользователь не найден"})
        if person is False:
            return JSONResponse(status_code=401, content={"message": "Не авторизован"})
        
        result = await db.execute(select(Users).filter(Users.clan_id == clan_id).order_by(Users.balance.desc()))
        users = result.scalars().all()
        
        result = await db.execute(select(Clans).filter(Clans.id == clan_id))
        clan = result.scalars().first()
        
        users_list = []
        for user in users:
            users_list.append({
                "name": user.username,
                "balance": user.balance,
                "p_n_l": user.p_n_l,
                "avatar_url": user.avatar_url
            })
        
        return {
            "id": clan_id,
            "name": clan.name,
            "league_id": clan.league_id,
            "logo_url": clan.logo_url,
            "users": clan.users,
            "balance": clan.balance,
            "link": clan.link,
            "owner_id": clan.owner_id,
            "usersList": users_list
        }

@router.get("/api/v.1.0/users/current_user/league", tags=["Users Methods"])
@rate_limiter(limit=GoodGuard.max_requests, seconds=GoodGuard.max_time_request_seconds, exception=ManyRequestException)
async def get_v2_current_user_league(
    client_id: int,
    Authorization: str = Header(...),
    db: AsyncSession = Depends(Database.get_session)
):
    if not check_client_id(client_id):
        return JSONResponse(status_code=401, content={"message": "Не авторизованный клиент"})

    try:
        user = Authorization.split(" ")[1]
    except:
        return JSONResponse(status_code=401, content={"message": "Не авторизован"})

    
    async with db as session:
        result = await session.execute(select(Users).filter(Users.token == user))
        person = result.scalars().first()

        if person is None:
            return JSONResponse(status_code=404, content={"message": "Пользователь не найден"})
        if person is False:
            return JSONResponse(status_code=401, content={"message": "Не авторизован"})

        result = await session.execute(select(League).filter(League.id == person.league_id))
        league = result.scalars().first()
        
        if league is None:
            return JSONResponse(status_code=404, content={"message": "Лига не найдена"})
        
        return league
    
@router.get("/api/v.1.0/league/info", tags=["Users Methods"])
@rate_limiter(limit=GoodGuard.max_requests, seconds=GoodGuard.max_time_request_seconds, exception=ManyRequestException)
async def get_v2_league_info(
    client_id: int,
    Authorization: str = Header(...),
    league_id: int = Query(...),
    db: AsyncSession = Depends(Database.get_session)
):
    if not check_client_id(client_id):
        return JSONResponse(status_code=401, content={"message": "Не авторизованный клиент"})

    try:
        user = Authorization.split(" ")[1]
    except:
        return JSONResponse(status_code=401, content={"message": "Не авторизован"})

    
    async with db as session:
        result = await session.execute(select(Users).filter(Users.token == user))
        person = result.scalars().first()

        if person is None:
            return JSONResponse(status_code=404, content={"message": "Пользователь не найден"})
        if person is False:
            return JSONResponse(status_code=401, content={"message": "Не авторизован"})

        result = await session.execute(select(League).filter(League.id == league_id))
        league = result.scalars().first()
        
        if league is None:
            return JSONResponse(status_code=404, content={"message": "Лига не найдена"})
        
        return league
    
@router.get("/api/v.1.0/league/info/{leagueName}", tags=["Users Methods"])
@rate_limiter(limit=GoodGuard.max_requests, seconds=GoodGuard.max_time_request_seconds, exception=ManyRequestException)
async def get_v2_league_info_by_name(
    client_id: int,
    Authorization: str = Header(...),
    leagueName: str = Path(...),
    db: AsyncSession = Depends(Database.get_session)
):
    if not check_client_id(client_id):
        return JSONResponse(status_code=401, content={"message": "Не авторизованный клиент"})

    try:
        user = Authorization.split(" ")[1]
    except:
        return JSONResponse(status_code=401, content={"message": "Не авторизован"})

    
    async with db as session:
        result = await session.execute(select(Users).filter(Users.token == user))
        person = result.scalars().first()

        if person is None:
            return JSONResponse(status_code=404, content={"message": "Пользователь не найден"})
        if person is False:
            return JSONResponse(status_code=401, content={"message": "Не авторизован"})

        result = await session.execute(select(League).filter(League.name == leagueName))
        league = result.scalars().first()
        
        if league is None:
            return JSONResponse(status_code=404, content={"message": "Лига не найдена"})
        
        return league
    
@router.get("/api/v.1.0/league/info/{leagueName}/users", tags=["Users Methods"])
@rate_limiter(limit=GoodGuard.max_requests, seconds=GoodGuard.max_time_request_seconds, exception=ManyRequestException)
async def get_v2_league_info_by_name_users(
    client_id: int,
    Authorization: str = Header(...),
    leagueName: str = Path(...),
    db: AsyncSession = Depends(Database.get_session)
):
    if not check_client_id(client_id):
        return JSONResponse(status_code=401, content={"message": "Не авторизованный клиент"})

    try:
        user = Authorization.split(" ")[1]
    except:
        return JSONResponse(status_code=401, content={"message": "Не авторизован"})

    
    async with db as session:
        result = await session.execute(select(Users).filter(Users.token == user))
        person = result.scalars().first()

        if person is None:
            return JSONResponse(status_code=404, content={"message": "Пользователь не найден"})
        if person is False:
            return JSONResponse(status_code=401, content={"message": "Не авторизован"})

        result = await session.execute(select(League).filter(League.name == leagueName))
        league = result.scalars().first()
        
        if league is None:
            return JSONResponse(status_code=404, content={"message": "Лига не найдена"})
        
        result = await session.execute(select(Users).filter(Users.league_id == league.id).order_by(Users.balance.desc()))
        users = result.scalars().all()
        
        users_list = []

        for user in users:
            users_list.append({
                "id": user.id,
                "balance": user.balance,
                "avatar_url": user.avatar_url,
                "name": user.username
            })
            
        return users_list
    
@router.get("/api/v.1.0/league/info/{leagueName}/clans", tags=["Users Methods"])
@rate_limiter(limit=GoodGuard.max_requests, seconds=GoodGuard.max_time_request_seconds, exception=ManyRequestException)
async def get_v2_league_info_by_name_clans(
    client_id: int,
    Authorization: str = Header(...),
    leagueName: str = Path(...),
    db: AsyncSession = Depends(Database.get_session)
):
    if not check_client_id(client_id):
        return JSONResponse(status_code=401, content={"message": "Не авторизованный клиент"})

    try:
        user = Authorization.split(" ")[1]
    except:
        return JSONResponse(status_code=401, content={"message": "Не авторизован"})

    
    async with db as session:
        result = await session.execute(select(Users).filter(Users.token == user))
        person = result.scalars().first()

        if person is None:
            return JSONResponse(status_code=404, content={"message": "Пользователь не найден"})
        if person is False:
            return JSONResponse(status_code=401, content={"message": "Не авторизован"})

        result = await session.execute(select(League).filter(League.name == leagueName))
        league = result.scalars().first()
        
        if league is None:
            return JSONResponse(status_code=404, content={"message": "Лига не найдена"})
        
        result = await session.execute(select(Clans).filter(Clans.league_id == league.id).order_by(Clans.balance.desc()))
        clans = result.scalars().all()
        
        clans_list = []
        
        for clan in clans:
            clans_list.append({
                "id": clan.id,
                "balance": clan.balance,
                "logo_url": clan.logo_url,
                "name": clan.name
            })
            
        return clans_list
    
@router.post("/api/v.1.0/orders/create", tags=["Users Methods"])
@rate_limiter(limit=GoodGuard.max_requests, seconds=GoodGuard.max_time_request_seconds, exception=ManyRequestException)
async def post_v2_orders_create(
    client_id: int,
    Authorization: str = Header(...),
    db: AsyncSession = Depends(Database.get_session),
    order: OrderCreateModel = Body(...)
):
    # Проверка client_id
    if not check_client_id(client_id):
        return JSONResponse(status_code=401, content={"message": "Не авторизованный клиент"})

    # Извлечение и проверка токена авторизации
    try:
        token = Authorization.split(" ")[1]
    except IndexError:
        return JSONResponse(status_code=401, content={"message": "Не авторизован"})

    # Поиск пользователя по токену
    async with db as session:
        result = await session.execute(select(Users).filter(Users.token == token))
        person = result.scalars().first()
        
        if person is None:
            return JSONResponse(status_code=404, content={"message": "Пользователь не найден"})
        
        if person is False:
            return JSONResponse(status_code=401, content={"message": "Не авторизован"})
        
        if person.balance < order.amount:
            return JSONResponse(status_code=409, content={"message": "Недостаточно средств"})
        
        result = await session.execute(select(Orders).filter(Orders.user_id == person.id, Orders.status == "open"))
        orders = result.scalars().all()
        
        if len(orders) > 0:
            return JSONResponse(status_code=409, content={"message": "У пользователя уже есть открытый ордер"})
        
        entry_rate = get_current_rate(order.contract_pair)
        
        # Создание нового ордера
        new_order = Orders(
            user_id=person.id,
            contract_pair=order.contract_pair,
            direction=order.direction,
            amount=order.amount,
            entry_rate=entry_rate,
            leverage=order.leverage,
            status="open"
        )

        # Добавление и сохранение ордера в базу данных
        db.add(new_order)
        await db.commit()
        return JSONResponse(status_code=201, content={"message": "Ордер создан", "order_id": new_order.id})
    
@router.get("/api/v.1.0/orders/list", tags=["Users Methods"])
@rate_limiter(limit=GoodGuard.max_requests, seconds=GoodGuard.max_time_request_seconds, exception=ManyRequestException)
async def get_v2_orders_list(
    client_id: int,
    Authorization: str = Header(...),
    db: AsyncSession = Depends(Database.get_session)
):
    if not check_client_id(client_id):
        return JSONResponse(status_code=401, content={"message": "Не авторизованный клиент"})

    try:
        user = Authorization.split(" ")[1]
    except:
        return JSONResponse(status_code=401, content={"message": "Не авторизован"})
    
    async with db as session:
        result = await session.execute(select(Users).filter(Users.token == user))
        person = result.scalars().first()

        if person is None:
            return JSONResponse(status_code=404, content={"message": "Пользователь не найден"})
        if person is False:
            return JSONResponse(status_code=401, content={"message": "Не авторизован"})

        result = await session.execute(select(Orders).filter(Orders.user_id == person.id))
        orders = result.scalars().all()
        
        orders_list = []
        
        for order in orders:
            orders_list.append({
                "id": order.id,
                "contract_pair": order.contract_pair,
                "direction": order.direction,
                "amount": order.amount,
                "entry_rate": order.entry_rate,
                "leverage": order.leverage,
                "status": order.status
            })
            
        return orders_list
    
@router.get("/api/v.1.0/orders/current/{contract_pair}", tags=["Users Methods"])
@rate_limiter(limit=GoodGuard.max_requests, seconds=GoodGuard.max_time_request_seconds, exception=ManyRequestException)
async def get_v2_orders_current(
    client_id: int,
    Authorization: str = Header(...),
    db: AsyncSession = Depends(Database.get_session),
    contract_pair: str = Path(...)
):
    if not check_client_id(client_id):
        return JSONResponse(status_code=401, content={"message": "Не авторизованный клиент"})

    try:
        user = Authorization.split(" ")[1]
    except:
        return JSONResponse(status_code=401, content={"message": "Не авторизован"})
    
    async with db as session:
        result = await session.execute(select(Users).filter(Users.token == user))
        person = result.scalars().first()

        if person is None:
            return JSONResponse(status_code=404, content={"message": "Пользователь не найден"})
        if person is False:
            return JSONResponse(status_code=401, content={"message": "Не авторизован"})

        result = await session.execute(select(Orders).filter(Orders.user_id == person.id, Orders.status == "open", Orders.contract_pair == contract_pair))
        orders = result.scalars().all()
        
        if len(orders) == 0:
            return JSONResponse(status_code=404, content={"message": "Нет открытых ордеров"})
        
        order = orders[0]
        
        pairs = {
            'EQARK5MKz_MK51U5AZjK3hxhLg1SmQG2Z-4Pb7Zapi_xwmrN': 'NOTUSDT',
            'EQA-X_yo3fzzbDbJ_0bzFWKqtRuZFIRa1sJsveZJ1YpViO3r': 'TONUSDT',
            '0xc7bbec68d12a0d1830360f8ec58fa599ba1b0e9b': 'ETHUSDT',
            '0xa43fe16908251ee70ef74718545e4fe6c5ccec9f': 'PEPEUSDT',
            '0x6aa9c4eda3bf8ac038ad5c243133d6d25aa9cc73': 'BTCUSDT',
            'DSUvc5qf5LJHHV5e2tD184ixotSnCnwj7i4jJa4Xsrmt': 'SOLUSDT'
        }
        print(order.id)
        return {
            "id": order.id,
            "contract_pair": pairs.get(order.contract_pair),
            "direction": order.direction,
            "amount": order.amount,
            "entry_rate": order.entry_rate,
            "leverage": order.leverage,
            "status": order.status
        }
    
@router.post("/api/v.1.0/orders/close/{order_id}", tags=["Users Methods"])
@rate_limiter(limit=GoodGuard.max_requests, seconds=GoodGuard.max_time_request_seconds, exception=ManyRequestException)
async def post_v2_orders_close(
    client_id: int,
    Authorization: str = Header(...),
    db: AsyncSession = Depends(Database.get_session),
    order_id: int = Path(...)
):
    if not check_client_id(client_id):
        return JSONResponse(status_code=401, content={"message": "Не авторизованный клиент"})

    try:
        user = Authorization.split(" ")[1]
    except:
        return JSONResponse(status_code=401, content={"message": "Не авторизован"})
    
    async with db as session:
        result = await session.execute(select(Users).filter(Users.token == user))
        person = result.scalars().first()

        if person is None:
            return JSONResponse(status_code=404, content={"message": "Пользователь не найден"})
        if person is False:
            return JSONResponse(status_code=401, content={"message": "Не авторизован"})

        result = await session.execute(select(Orders).filter(Orders.id == order_id, Orders.user_id == person.id))
        order = result.scalars().first()

        if order is None or order.status != "open":
            return JSONResponse(status_code=404, content={"message": "Ордер не найден или уже закрыт"})
        
        exit_rate = get_current_rate(order.contract_pair)
        
        order.exit_rate = exit_rate
        order.closed_at = datetime.now()
        order.status = "closed"
        
        pnl = calculate_pnl(order, exit_rate)
        person.balance += pnl
        
        await db.commit()
        return JSONResponse(status_code=200, content={"message": "Ордер закрыт", "pnl": pnl})