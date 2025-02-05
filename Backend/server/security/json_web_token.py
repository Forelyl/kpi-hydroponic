from typing import Annotated
import jwt as json_web_token
from jwt.exceptions import InvalidTokenError
from datetime import datetime, timedelta, timezone
from fastapi import Depends, HTTPException, status

from server.security.dataclasses import oauth2_scheme, User
import server.database_driver.database as database_manager


# openssl rand -hex 32
__SECRET_KEY                  = '98edae7b95e936b0124bfc6b3619728663e0dbfe3dd25652f07f944184782472'
__ALGORITHM                   = 'HS256'
__ACCESS_TOKEN_EXPIRE_MINUTES = 10


def generate_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=__ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = json_web_token.encode(to_encode, __SECRET_KEY, algorithm=__ALGORITHM)
    return encoded_jwt


async def process_access_token(token: Annotated[str, Depends(oauth2_scheme)]) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    # Check&decode token
    try:
        payload = json_web_token.decode(token, __SECRET_KEY, algorithms=[__ALGORITHM])
    except InvalidTokenError:
        raise credentials_exception

    # Check&get payload
    username: str | None = payload.get("sub")
    user_id : int | None = payload.get("id")
    if user_id is None or username is None:
        raise credentials_exception

    # Check if the user exists in the database
    database_user = await database_manager.get_user_by_id(user_id)
    if database_user is None or database_user.username != username:
        raise credentials_exception

    # Return user
    return User(id=user_id, username=username)


async def get_user(user: Annotated[User, Depends(process_access_token)]):
    return user
