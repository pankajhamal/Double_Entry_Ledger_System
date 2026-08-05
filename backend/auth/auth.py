from passlib.context import CryptContext
from jose import jwt

from datetime import datetime, timedelta
from backend.core.config import settings

pwd_context = CryptContext(
    schemes = ["bcrypt"],
    deprecated = "auto"
)

def hash_password(password: str):
    return pwd_context.hash(password)

def verify_password(plain_password, password_hash):
    return pwd_context.verify(
        plain_password,
        password_hash
    )

def create_access_token(data: dict):
    expire = datetime.utcnow() + timedelta(minutes = 30)

    payload = data.copy()

    payload.update({
        "exp": expire
    })

    token = jwt.encode(
        payload,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM
    )

    return token