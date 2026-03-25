from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from contextlib import asynccontextmanager

from app.core.config import settings
from app.db.init_db import init_db
from app.routes import home


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Run startup / shutdown tasks."""
    init_db()  # Create tables on first run
    yield
    # Add shutdown cleanup here if needed


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    debug=settings.DEBUG,
    lifespan=lifespan,
)

# ── Static files ────────────────────────────────────────────────────────────
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# ── Jinja2 templates ─────────────────────────────────────────────────────────
templates = Jinja2Templates(directory="app/templates")

# ── Routers ──────────────────────────────────────────────────────────────────
app.include_router(home.router)
