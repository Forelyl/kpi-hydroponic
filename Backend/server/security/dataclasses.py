from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


# ---

class User(BaseModel):
    id:        int
    username:  str


class UserInDB(User):
    hashed_password: str


# ---

class Token(BaseModel):
    access_token: str
    token_type:   str


class TokenData(BaseModel):
    username: str | None = None