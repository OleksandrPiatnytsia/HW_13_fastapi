from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.conf.config import config

URI = config.sqlalchemy_database_url
print(URI)

engine = create_engine(URI, echo=False, pool_size=5, max_overflow=0)
DBSession = sessionmaker(bind=engine)


# session_debug = DBSession()


# Dependency
def get_db():
    session = DBSession()
    try:
        yield session
    finally:
        session.close()
