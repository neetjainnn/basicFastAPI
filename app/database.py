from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base
from app.config import settings

# import psycopg2
# from psycopg2.extras import RealDictCursor

SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}"


engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# dependency for SQLAlchemy sessions
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# DATABASE CONNECTION
# while True:
#     try:
#         conn = psycopg2.connect(
#             host='localhost',
#             database='postgres',
#             user='postgres',
#             password='neet@symbo14db',
#             cursor_factory=RealDictCursor
#         )
#         cursor = conn.cursor()
#         print("Connection to database successful!")
#         break
#     except Exception as error:
#         print("Connection to database failed:", error)
#         time.sleep(2)


