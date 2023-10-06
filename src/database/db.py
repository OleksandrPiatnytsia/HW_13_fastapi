import configparser
import pathlib

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# URI:  postgresql://username:password@domain:port/database
file_config = pathlib.Path(__file__).parent.parent.joinpath('config/config.ini')
config = configparser.ConfigParser()
config.read(file_config)

username = config.get('DB', 'USER')
password = config.get('DB', 'PASSWORD')
domain = config.get('DB', 'DOMAIN')
port = config.get('DB', 'PORT')
database = config.get('DB', 'DB_NAME')

secret_key = config.get('AUTH', 'SECRET_KEY')
algorithm = config.get('AUTH', 'ALGORITHM')

URI = f"postgresql://{username}:{password}@{domain}:{port}/{database}"
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
