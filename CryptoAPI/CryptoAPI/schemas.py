from pydantic import BaseModel, Field, validator

import Tools.ContentUtils


class UserUpdateOwnerModel(BaseModel):
    # ROOT
    user_id: str = None

    # USER DATA
    name: str = None
    age: int = None
    description_user: str = None

    # GUARD DATA
    email: str = None
    password: str = None

    # BUCKET DATA
    avatar: str = None
    banner: str = None
    status_user: str = None

    # PRIVACY DATA
    verify: bool = None
    verify_mods: bool = None

    verify_icon: str = None

    # SYSTEM DATA
    role: str = None

    blocked: bool = None
    muted: bool = None

    # STATISTIC DATA
    balance: int = None

    downloads_count: int = None
    reactions_count: int = None


class UserUpdateDataModel(BaseModel):
    # USER DATA
    name: str = None
    age: int = None
    description_user: str = None


class UserEmailModel(BaseModel):
    email: str


class UserEmailCodeModel(BaseModel):
    email: str
    code: str


class UserModel(BaseModel):
    user_id: str
    username: str
    file_path: str
    is_premium: bool


class UserTokenModel(BaseModel):
    token: str
    
class OrderCreateModel(BaseModel):
    contract_pair: str
    direction: str
    amount: float
    leverage: int = 1