from fastapi import FastAPI
from app.api import auth
from app.db.base import Base
from app.db.session import engine


# create tables (for dev only)
Base.metadata.create_all(bind=engine)


app = FastAPI(title="Auth Service")
app.include_router(auth.router)


@app.get('/')
def root():
return {"ok": True}