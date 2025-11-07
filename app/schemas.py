from pydantic import BaseModel, EmailStr
from typing import Optional


class UserCreate(BaseModel):
email: EmailStr
password: str


class TokenOut(BaseModel):
access_token: str
refresh_token: str
token_type: str = "bearer"


class TokenPayload(BaseModel):
sub: Optional[str]
exp: Optional[int]
jti: Optional[str]

---


### `app/utils.py`
```python
from passlib.context import CryptContext
from jose import jwt, JWTError
from datetime import datetime, timedelta
import uuid
from app.core.config import settings


pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")


def hash_password(password: str) -> str:
return pwd_context.hash(password)


def verify_password(plain: str, hashed: str) -> bool:
return pwd_context.verify(plain, hashed)


def create_access_token(sub: str) -> str:
expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
payload = {"sub": sub, "exp": expire, "iat": datetime.utcnow()}
return jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.ALGORITHM)

def create_refresh_token(sub: str, jti: str = None):
jti = jti or str(uuid.uuid4())
expire = datetime.utcnow() + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
payload = {"sub": sub, "jti": jti, "exp": expire, "iat": datetime.utcnow()}
token = jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.ALGORITHM)
return token, jti


def decode_token(token: str):
try:
payload = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.ALGORITHM])
return payload
except JWTError:
return None