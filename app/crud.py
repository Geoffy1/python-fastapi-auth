from sqlalchemy.orm import Session
from app.db import models
from app.utils import hash_password
from datetime import datetime, timedelta


def get_user_by_email(db: Session, email: str):
return db.query(models.User).filter(models.User.email == email).first()


def create_user(db: Session, email: str, password: str):
user = models.User(email=email, hashed_password=hash_password(password))
db.add(user)
db.commit()
db.refresh(user)
return user


def create_refresh_token(db: Session, user_id: int, jti: str, expires_at: datetime):
rt = models.RefreshToken(jti=jti, user_id=user_id, expires_at=expires_at)
db.add(rt)
db.commit()
db.refresh(rt)
return rt


def get_refresh_token(db: Session, jti: str):
return db.query(models.RefreshToken).filter(models.RefreshToken.jti == jti).first()


def revoke_refresh_token(db: Session, jti: str):
rt = get_refresh_token(db, jti)
if rt:
rt.revoked = True
db.add(rt)
db.commit()
return rt