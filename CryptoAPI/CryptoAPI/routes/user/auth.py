from datetime import datetime, timedelta
from fastapi import HTTPException
from jose import JWTError, jwt
import good_guard

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, good_guard.SECRET_KEY, algorithm=good_guard.ALGORITHM)

def create_refresh_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(days=30)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, good_guard.SECRET_KEY, algorithm=good_guard.ALGORITHM)

def decode_token(token: str):
    try:
        payload = jwt.decode(token, good_guard.SECRET_KEY, algorithms=[good_guard.ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(status_code=403, detail="Invalid token")