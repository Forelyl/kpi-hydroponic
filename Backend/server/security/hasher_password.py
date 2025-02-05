from passlib.context import CryptContext


__hash_context = CryptContext(schemes=["argon2"], deprecated="auto")


def hash_password(password: str):
    return __hash_context.hash(password)


def verify_password(plain_password, hashed_password):
    return __hash_context.verify(plain_password, hashed_password)