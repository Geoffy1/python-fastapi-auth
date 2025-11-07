from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.base import Base


class User(Base):
__tablename__ = "users"
id = Column(Integer, primary_key=True, index=True)
email = Column(String, unique=True, index=True, nullable=False)
hashed_password = Column(String, nullable=False)
is_active = Column(Boolean, default=True)
created_at = Column(DateTime, default=datetime.utcnow)


class RefreshToken(Base):
__tablename__ = "refresh_tokens"
id = Column(Integer, primary_key=True, index=True)
jti = Column(String, unique=True, index=True, nullable=False)
user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
user = relationship("User")
issued_at = Column(DateTime, default=datetime.utcnow)
expires_at = Column(DateTime, nullable=False)
revoked = Column(Boolean, default=False)