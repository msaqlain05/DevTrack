from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from contextlib import asynccontextmanager
from pathlib import Path

from app.core.config import settings
from app.db.init_db import init_db
from app.routes import auth
from app.routes import home
from app.routes import project
from app.routes import task

APP_DIR = Path(__file__).resolve().parent
STATIC_DIR = APP_DIR / "static"
TEMPLATES_DIR = APP_DIR / "templates"


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
app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")

# ── Jinja2 templates ─────────────────────────────────────────────────────────
templates = Jinja2Templates(directory=str(TEMPLATES_DIR))

# ── Routers ──────────────────────────────────────────────────────────────────
app.include_router(home.router)
app.include_router(auth.router)
app.include_router(project.router)
app.include_router(task.router)
