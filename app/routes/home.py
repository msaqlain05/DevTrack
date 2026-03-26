from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from pathlib import Path

router = APIRouter(tags=["Frontend Views"])
APP_DIR = Path(__file__).resolve().parents[1]
templates = Jinja2Templates(directory=str(APP_DIR / "templates"))


@router.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Root redirects to dashboard via HTTP redirect. JS handles unauth."""
    return RedirectResponse(url="/dashboard")


@router.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    """Render the authentication page (Login)."""
    return templates.TemplateResponse(request=request, name="auth.html")


@router.get("/signup", response_class=HTMLResponse)
async def signup_page(request: Request):
    """Render the authentication page (Signup)."""
    return templates.TemplateResponse(request=request, name="auth.html")


@router.get("/dashboard", response_class=HTMLResponse)
async def dashboard_page(request: Request):
    """Render the main dashboard."""
    return templates.TemplateResponse(request=request, name="dashboard.html")


@router.get("/project/{project_id}", response_class=HTMLResponse)
async def project_page(request: Request, project_id: int):
    """Render the specific project view."""
    return templates.TemplateResponse(request=request, name="project.html", context={"project_id": project_id})
