from typing import Annotated
from fastapi import Depends, Form, HTTPException, Query, status
from fastapi.security import OAuth2PasswordRequestForm

import server.database_driver.database as database_manager
from server.security.dataclasses import Token, User
import server.security.json_web_token as token_manager
import server.security.hasher_password as password_manager
from server.security.dataclasses import UserInDB


# --- Hash check ---
async def authenticate_user(username: str, password: str) -> UserInDB:
    user = await database_manager.get_user_by_username(username)
    if user is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect username or password")
    if not password_manager.verify_password(password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect username or password")
    return user


# --- Give token to user ---
def add_token_endpoint(app):
    @app.post("/token")
    async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]) -> Token:
        user = await authenticate_user(form_data.username, form_data.password)
        access_token = token_manager.generate_access_token({
            "id":  user.id,
            "sub": user.username
        })
        return Token(access_token=access_token, token_type="bearer")

    @app.post("/register")
    async def register(
        username: Annotated[str, Form(min_length=1, max_length=120, pattern=r"^[a-zA-Z0-9_\.]+$")],
        password: Annotated[str, Form(min_length=1, max_length=120, pattern=r"^[a-zA-Z0-9!@#$%\^&*\(\)\.,]+$")]
    ) -> Token:
        if not await database_manager.add_user(username, password):
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User already exists")

        user = await authenticate_user(username, password)
        access_token = token_manager.generate_access_token({
            "id":  user.id,
            "sub": user.username
        })
        return Token(access_token=access_token, token_type="bearer")

    @app.get("/user/exists")
    async def user_exist(username: Annotated[str, Query(min_length=1, max_length=120, pattern=r"^[a-zA-Z0-9_\.]+$")]) -> bool:
        return await database_manager.check_username_exists(username)

    @app.delete("/user")
    async def delete_user(user: Annotated[User, Depends(get_user)]):
        await database_manager.delete_user(user.id)


# --- Get user from token  ---
get_user = token_manager.get_user


# --- Test request ---
def add_test_endpoint(app):
    @app.get("/users/me")
    async def read_users_me(current_user: Annotated[User, Depends(get_user)]):
        return current_user