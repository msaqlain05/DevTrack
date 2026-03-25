# DevTrack — FastAPI Starter

A production-ready, modular FastAPI project with Jinja2 templates, SQLite, and SQLAlchemy.

---

## Project Structure

```
DevTrack/
├── app/
│   ├── main.py            # FastAPI entry point
│   ├── core/
│   │   └── config.py      # Pydantic settings (reads .env)
│   ├── db/
│   │   ├── base.py        # SQLAlchemy declarative base
│   │   ├── session.py     # Engine, SessionLocal, get_db()
│   │   └── init_db.py     # Table creation helper
│   ├── models/            # ORM models (add your models here)
│   ├── schemas/           # Pydantic schemas (request/response)
│   ├── routes/
│   │   └── home.py        # Home page route
│   ├── services/          # Business logic layer
│   ├── templates/
│   │   ├── base.html      # Base Jinja2 template
│   │   └── index.html     # Home page
│   └── static/
│       └── css/main.css   # Styles
├── .env                   # Environment variables (never commit!)
├── requirements.txt
└── README.md
```

---

## Quick Start

### 1. Clone / enter the project

```bash
cd DevTrack
```

### 2. Create and activate a virtual environment

```bash
python -m venv venv
source venv/bin/activate        # Linux / macOS
# venv\Scripts\activate         # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Edit `.env` and update values (especially `SECRET_KEY` in production):

```bash
nano .env
```

### 5. Run the development server

```bash
uvicorn app.main:app --reload
```

Visit **http://127.0.0.1:8000** — the home page will load.
Interactive API docs are at **http://127.0.0.1:8000/docs**.

---

## Adding a New Feature (recommended pattern)

| Layer | Where | What goes there |
|---|---|---|
| Model | `app/models/` | SQLAlchemy ORM class |
| Schema | `app/schemas/` | Pydantic request/response models |
| Service | `app/services/` | Business logic (CRUD helpers) |
| Route | `app/routes/` | FastAPI router with endpoints |
| Template | `app/templates/` | Jinja2 HTML templates |

After adding a model, import it in `app/db/init_db.py` so the table is created automatically on startup.

---

## Security Checklist (before deploying)

- [ ] Set `DEBUG=False` in `.env`
- [ ] Replace `SECRET_KEY` with a strong random value
- [ ] Move to a production database (PostgreSQL recommended)
- [ ] Put the app behind a reverse proxy (Nginx / Caddy)
- [ ] Add HTTPS (Let's Encrypt / Cloudflare)