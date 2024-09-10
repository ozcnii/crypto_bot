from fastapi import HTTPException, Header, Request, status, Depends
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from urllib.parse import unquote_plus, parse_qs
from GoodGuard.tokensFabric import generate_verification_code
import jwt
import good_guard
import hmac
import hashlib
import json
import Database

Users = Database.Users

def validate_data(data: str, secret_key: str):
    decoded = unquote_plus(data).split("&")
    print(f"Decoded data: {decoded}")  # Debugging
    
    # Filter out the hash
    hash_parts = list(filter(lambda a: a.startswith("hash="), decoded))
    if not hash_parts:
        raise ValueError("Hash is missing from the data")
    data_hash = ''.join(hash_parts[0][5:])
    print(f"Data hash: {data_hash}")  # Debugging
    
    # Remove the hash and sort the rest of the data
    filtered = filter(lambda a: not a.startswith("hash="), decoded)
    sorted_data = sorted(filtered)
    
    # Rebuild the data string for the HMAC check
    data_check = '\n'.join(sorted_data)
    print(f"Data check string: {data_check}")  # Debugging
    
    # Ensure the secret key is in bytes format
    if isinstance(secret_key, str):
        secret_key = secret_key.encode()  # Encode only if it's a string

    # Generate the HMAC hash using the secret key
    generated_hash = hmac.new(secret_key, data_check.encode(), hashlib.sha256).hexdigest()
    print(f"Generated hash: {generated_hash}")  # Debugging
    
    return generated_hash == data_hash

class TMAAuthentication:
  secret_key = hmac.new("WebAppData".encode(), good_guard.TELEGRAM_API_TOKEN.encode(), hashlib.sha256).digest()
  async def authenticate(self, request: Request, db: AsyncSession):
    tma_data = request.headers.get("tma-data", None)
    prefix = tma_data.split(" ")[0]
    
    if prefix != "tma":
      raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    tmAdata = tma_data.split(" ")[1]
    
    if tmAdata is None or not validate_data(data=tmAdata, secret_key=self.secret_key):
      raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid TMA token")
    
    data = parse_qs(tmAdata)
    user_data = self.get_user_data(data)
    
    if user_data is None:
      raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid user data")
    
    user, is_new = await self.get_user_or_create(user_data, db=db, request=request)
    return user, is_new
  
  def get_user_data(self, data):
    """
    Extract user data from TMA init data.
    """
    try:
        # Parse the 'user' field from JSON
        user_data = json.loads(data.get("user", [None])[0])
    except (json.JSONDecodeError, TypeError):
        raise HTTPException(status_code=400, detail="Invalid user data format")

    # Safely extract the fields from the parsed JSON
    user_id = user_data.get("id")
    username = user_data.get("username")
    is_premium = user_data.get("is_premium", False)  # Assuming False as default for 'is_premium'

    # Check if any of the required fields are missing
    if user_id is None or username is None:
        raise HTTPException(status_code=400, detail="Missing user data in the request")

    return {
        "id": user_id,
        "username": username,
        "is_premium": is_premium,
    }
  
  async def get_user_or_create(self, user_data, db: AsyncSession, request: Request):
    """
    Check if user exists in database. If not, create new user.
    """
    # Ensure user_id is treated as a string
    user_id_str = str(user_data["id"])

    # Query the database with the correct data type
    result = await db.execute(
        select(Users).filter(Users.user_id == user_id_str)
    )    
    user = result.scalars().first()
    referred_by = request.query_params.get("referral_code")
    if referred_by is None:
        referred_by = None
    else:
        result = await db.execute(
          select(Users).filter(Users.user_id == referred_by)
        )

        referrer = result.scalars().first()
    
        if referrer is None:
            referred_by = None
    
    # If user does not exist, create a new user
    if user is None:
        new_user = Users(
            user_id=user_id_str,  # Store the user_id as a string
            username=user_data.get("username"),
            is_premium=user_data.get("is_premium"),
            referrer_id=referred_by
        )
        db.add(new_user)
        await db.commit()
        return new_user, True
    
    return user, False