# from sqlalchemy import create_engine
# from sqlalchemy.orm import declarative_base
# from sqlalchemy.orm import sessionmaker

# SQLALCHEMY_DATABASE_URL = "sqlite:///C:\\Users\\aryan\\OneDrive\\Desktop\\coding\\Task management system\\task_management2.db"

# engine = create_engine(
#     SQLALCHEMY_DATABASE_URL,
#     connect_args={"check_same_thread": False} 
# )

# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base = declarative_base()

# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()



from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# MySQL connection URL
SQLALCHEMY_DATABASE_URL = "mysql+mysqlconnector://root:root@localhost:3306/task_management"

# ❌ REMOVE SQLite-only connect_args
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    echo=True  # optional: shows SQL queries in console
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
