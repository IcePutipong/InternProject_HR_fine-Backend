from sqlalchemy import create_engine, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import OperationalError
from decouple import config

Base = declarative_base()

mysql_user = config("MYSQL_USER")
mysql_password = config("MYSQL_ROOT_PASSWORD")
mysql_host = config("MYSQL_HOST")
mysql_port = config("MYSQL_PORT")
mysql_db = config("MYSQL_DB")

mysql_url_no_db = f"mysql+pymysql://{mysql_user}:{mysql_password}@{mysql_host}:{mysql_port}"
db_url = f"mysql+pymysql://{mysql_user}:{mysql_password}@{mysql_host}:{mysql_port}/{mysql_db}"
print(db_url)

def ensure_database_exists():
    try:
        engine_no_db = create_engine(mysql_url_no_db, echo=True)
        with engine_no_db.connect() as connection:
            connection.execute(text(f"CREATE DATABASE IF NOT EXISTS `{mysql_db}`;"))
            print(f"Database '{mysql_db}' created or already exists.")
    except OperationalError as e:
        print(f"Error connecting to MySQL server: {e}")
        raise

engine = create_engine(db_url, echo=True)
SessionLocal = sessionmaker(bind=engine, expire_on_commit=False)

def create_db_and_tables():
    try:
        Base.metadata.create_all(engine)
        print("Tables created successfully.")
    except Exception as e:
        print(f"Error creating tables: {e}")

def get_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()
