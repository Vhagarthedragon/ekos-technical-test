from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.infrastructure.config import settings
from src.infrastructure.database import close_pool, get_pool
from src.presentation.admin import router as admin_router
from src.presentation.sales import router as sales_router
from src.presentation.support import router as support_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    await get_pool()
    yield
    await close_pool()


app = FastAPI(
    title="ClinicDesk AI Agents",
    description="Support and Sales agents for dental and medical clinics.",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.frontend_url, "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(support_router, prefix="/api")
app.include_router(sales_router, prefix="/api")
app.include_router(admin_router, prefix="/api")


@app.get("/health")
async def health():
    return {"status": "ok"}
