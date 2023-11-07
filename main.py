import redis.asyncio as redis
from fastapi import FastAPI, Depends, HTTPException
from fastapi_limiter import FastAPILimiter
from sqlalchemy import text
from sqlalchemy.orm import Session
from starlette.middleware.cors import CORSMiddleware

from src.conf.config import config
from src.database.db import get_db
from src.routes import contacts, auth, users

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
    r = await redis.Redis(host=config.redis_host, port=config.redis_port, db=0)
    await FastAPILimiter.init(r)


app.include_router(auth.router)
app.include_router(contacts.router)
app.include_router(contacts.birthday_router)
app.include_router(users.router)


@app.get("/")
def read_root():
    """
    The read_root function returns a dictionary with the key &quot;message&quot; and value &quot;Application started&quot;.
    This is used to test that the application has been deployed correctly.

    :return: A dictionary with a single key-value pair
    """
    return {"message": "Application started"}


@app.get("/api/healthchecker")
def healthchecker(session: Session = Depends(get_db)):
    """
    The healthchecker function is a simple function that checks if the database is configured correctly.
    It does this by making a request to the database and checking if it returns any results.
    If there are no results, then we know something went wrong with our connection.

    :param session: Session: Pass the database session into the function
    :return: A dictionary with a message
    """
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
