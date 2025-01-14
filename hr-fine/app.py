import logging
from contextlib import asynccontextmanager
import subprocess
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.routes import router
from database.db import ensure_database_exists, create_db_and_tables

@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        logging.info("Auth Service Starting...")
        logging.info("Ensuring database exists and tables are created...")
        ensure_database_exists() 
        create_db_and_tables()
        logging.info("Database setup complete.")
        yield
    except Exception as e:
        logging.error(f"Error during service startup: {e}", exc_info=True)
        raise
    finally:
        logging.info("Shutting down...")

app = FastAPI(lifespan=lifespan)

origins = [
    "http://127.0.0.1:3000",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins = origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)