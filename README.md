# 🚀 DevTrack

**DevTrack** is a production-ready, full-stack Project & Task Management system built for developers. It is powered by a modular **FastAPI** backend with JWT authentication and strict ownership security, paired with a premium dark-mode frontend built using **Jinja2 templates**, Vanilla JS, and native CSS.

---

## ✨ Features

| Feature | Details |
|---|---|
| 🔐 JWT Auth | Signup, Login, token expiry handling, auto-redirect |
| 🔒 Ownership | Every resource is strictly scoped to the authenticated user |
| 📁 Projects | Full CRUD — create, view, update, delete projects |
| ✅ Tasks | Full CRUD per project — title, description, date, status |
| 🔄 Status Control | Segmented ⏳ Pending / 🔄 Active / ✅ Done per task |
| 📅 Date Filter | Filter tasks by date on the project page |
| 🗑 Cascade Delete | Deleting a project removes all its tasks (SQLite PRAGMA) |
| 💬 Toast Alerts | Animated success/error flash notifications |
| 💀 Skeleton Loaders | Shimmer animation while data fetches |
| 🛡 XSS Protection | All user content safely HTML-escaped before rendering |

---

## 🏗️ Tech Stack

**Backend**: FastAPI · SQLAlchemy 2.0 · SQLite · Pydantic V2 · python-jose (JWT) · bcrypt

**Frontend**: Jinja2 · Vanilla CSS (CSS Custom Properties) · Vanilla JS (ES6 Fetch API)

---

## 📂 Project Structure

```
DevTrack/
├── app/
│   ├── main.py                # FastAPI app factory + router registration
│   ├── core/
│   │   ├── authorization.py   # verify_resource_owner() utility
│   │   ├── config.py          # Pydantic settings (.env)
│   │   └── security.py        # JWT create/decode, bcrypt hash/verify
│   ├── db/
│   │   ├── base.py            # SQLAlchemy Base
│   │   ├── init_db.py         # create_all() on startup
│   │   ├── mixins.py          # OwnerMixin
│   │   └── session.py         # get_db() + SQLite PRAGMA FK enforcement
│   ├── models/
│   │   ├── project.py         # Project ORM model
│   │   ├── task.py            # Task ORM model (status Enum)
│   │   └── user.py            # User ORM model
│   ├── schemas/
│   │   ├── auth.py            # SignupRequest, TokenResponse, UserOut
│   │   ├── project.py         # ProjectCreate, ProjectUpdate, ProjectOut
│   │   └── task.py            # TaskCreate, TaskUpdate, TaskOut
│   ├── services/
│   │   ├── project_service.py # Project business logic
│   │   └── task_service.py    # Task business logic + date filtering
│   ├── routes/
│   │   ├── auth.py            # POST /auth/signup, /auth/login, /auth/me
│   │   ├── home.py            # Jinja2 page routes (/, /login, /dashboard…)
│   │   ├── project.py         # Project CRUD endpoints
│   │   └── task.py            # Task CRUD + GET /tasks/ (global)
│   ├── static/
│   │   ├── css/style.css      # Premium dark-mode CSS design system
│   │   └── js/app.js          # apiFetch wrapper, toasts, skeleton helpers
│   └── templates/
│       ├── base.html          # Master Jinja2 layout (navbar, toast container)
│       ├── auth.html          # Login & Signup toggle view
│       ├── dashboard.html     # Projects + all tasks overview
│       └── project.html       # Task management per project
├── requirements.txt
└── README.md
```

---

## ⚙️ Setup & Run

```bash
# 1. Create and activate virtual environment
python -m venv venv
source venv/bin/activate        # Bash/Zsh
source venv/bin/activate.fish   # Fish shell

# 2. Install dependencies
pip install -r requirements.txt

# 3. Configure environment variables
# Copy .env.example to .env and set your SECRET_KEY etc.

# 4. Start the dev server
uvicorn app.main:app --reload
```

> The SQLite database (`app/db/devtrack.db`) is **auto-created** on first boot. If you change models, delete the `.db` file to regenerate.

App runs at: **http://127.0.0.1:8000**
API Docs at: **http://127.0.0.1:8000/docs**

---

## 🔑 Environment Variables (`.env`)

| Variable | Description |
|---|---|
| `SECRET_KEY` | General app secret |
| `JWT_SECRET_KEY` | Secret for signing JWT tokens |
| `JWT_ALGORITHM` | e.g. `HS256` |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Token lifetime (e.g. `60`) |
| `DATABASE_URL` | e.g. `sqlite:///./app/db/devtrack.db` |

---

## 🧪 Testing Checklist

- [ ] Navigate to `/` → redirects to `/dashboard` → redirects to `/login` (unauthenticated)
- [ ] Create a new account via Sign Up
- [ ] Login and land on the Dashboard
- [ ] Create a Project and navigate into it
- [ ] Add tasks with different statuses and dates
- [ ] Toggle task status using the ⏳ / 🔄 / ✅ segmented control
- [ ] Filter tasks by date using the date picker (with Clear button)
- [ ] Mark a task "Done" directly from the Dashboard
- [ ] Confirm toast notifications appear for every action
- [ ] Try accessing another user's project URL → should return 403

---

## 🔮 Roadmap

- **Alembic** migrations for safe schema evolution
- **PostgreSQL** support for production deployments
- **Team collaboration** — share projects with other users
- **Pagination** for large task lists