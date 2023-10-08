import redis.asyncio as redis
from fastapi import FastAPI, Depends, HTTPException
from fastapi_limiter import FastAPILimiter
from sqlalchemy import text
from sqlalchemy.orm import Session
from starlette.middleware.cors import CORSMiddleware

from src.database.db import get_db
from src.routes import contacts, auth
from src.conf.config import config

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup():
    r = await redis.Redis(host=config.redis_host, port=config.redis_port,db=0)
    await FastAPILimiter.init(r)


app.include_router(auth.router)
app.include_router(contacts.router)
app.include_router(contacts.birthday_router)


@app.get("/")
def read_root():
    return {"message": "Application started"}


@app.get("/api/healthchecker")
def healthchecker(session: Session = Depends(get_db)):
    try:
        # Make request
        result = session.execute(text("SELECT 1")).fetchone()
        if result is None:
            raise HTTPException(status_code=500, detail="Database is not configured correctly")
        return {"message": "Welcome to FastAPI!"}
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Error connecting to the database")

# uvicorn main:app --host localhost --port 8000 --reload
