from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse

router = APIRouter(tags=["Frontend Views"])
templates = Jinja2Templates(directory="app/templates")


@router.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Root redirects to dashboard via HTTP redirect. JS handles unauth."""
    return RedirectResponse(url="/dashboard")


@router.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    """Render the authentication page (Login)."""
    return templates.TemplateResponse("auth.html", {"request": request})


@router.get("/signup", response_class=HTMLResponse)
async def signup_page(request: Request):
    """Render the authentication page (Signup)."""
    return templates.TemplateResponse("auth.html", {"request": request})


@router.get("/dashboard", response_class=HTMLResponse)
async def dashboard_page(request: Request):
    """Render the main dashboard."""
    return templates.TemplateResponse("dashboard.html", {"request": request})


@router.get("/project/{project_id}", response_class=HTMLResponse)
async def project_page(request: Request, project_id: int):
    """Render the specific project view."""
    return templates.TemplateResponse("project.html", {"request": request, "project_id": project_id})
