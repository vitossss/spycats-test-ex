from contextlib import asynccontextmanager
from fastapi import FastAPI
from .routers import (spycats_router as sp_router,
                      missions_router as m_router,
                      targets_router as t_router)
from .db import create_db_and_tables

@asynccontextmanager
async def init_db(app: FastAPI):
    create_db_and_tables()
    yield

app = FastAPI(lifespan=init_db)
app.include_router(sp_router.router)
app.include_router(m_router.router)
app.include_router(t_router.router)
