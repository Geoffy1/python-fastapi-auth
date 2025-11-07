from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.schemas import UserCreate, TokenOut
from app.db.session import get_db
from app import crud
from app.utils import create_access_token, create_refresh_token, decode_token
from datetime import datetime


router = APIRouter(prefix="/auth", tags=["auth"])


@router.post('/register')
def register(payload: UserCreate, db: Session = Depends(get_db)):
existing = crud.get_user_by_email(db, payload.email)
if existing:
raise HTTPException(status_code=400, detail="Email already registered")
user = crud.create_user(db, payload.email, payload.password)
return {"ok": True, "id": user.id}


@router.post('/login', response_model=TokenOut)
def login(payload: UserCreate, db: Session = Depends(get_db)):
user = crud.get_user_by_email(db, payload.email)
if not user:
raise HTTPException(status_code=401, detail="Invalid credentials")
from app.utils import verify_password
if not verify_password(payload.password, user.hashed_password):
raise HTTPException(status_code=401, detail="Invalid credentials")
access = create_access_token(str(user.id))
refresh_token, jti = create_refresh_token(str(user.id))
# persist jti
expires_at = datetime.utcnow() + timedelta(days=30)
crud.create_refresh_token(db, user.id, jti, expires_at)
return TokenOut(access_token=access, refresh_token=refresh_token)


@router.post('/refresh', response_model=TokenOut)
def refresh(refresh_token: str, db: Session = Depends(get_db)):
payload = decode_token(refresh_token)
if not payload:
raise HTTPException(status_code=401, detail="Invalid refresh token")
jti = payload.get('jti')
sub = payload.get('sub')
rt = crud.get_refresh_token(db, jti)
if not rt or rt.revoked or rt.expires_at < datetime.utcnow():
raise HTTPException(status_code=401, detail="Refresh token revoked or expired")
# rotate
crud.revoke_refresh_token(db, jti)
new_refresh_token, new_jti = create_refresh_token(sub)
expires_at = datetime.utcnow() + timedelta(days=30)
crud.create_refresh_token(db, int(sub), new_jti, expires_at)
access = create_access_token(sub)
return TokenOut(access_token=access, refresh_token=new_refresh_token)


@router.post('/logout', status_code=204)
def logout(refresh_token: str, db: Session = Depends(get_db)):
payload = decode_token(refresh_token)
if not payload:
raise HTTPException(status_code=401, detail="Invalid refresh token")
jti = payload.get('jti')
crud.revoke_refresh_token(db, jti)
return