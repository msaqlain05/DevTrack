# 🚀 DevTrack

**DevTrack** is a clean, minimal, and highly scalable Project & Task Management system designed for developers. It combines a robust Python backend built on **FastAPI** with a lightning-fast frontend rendered via **Jinja2**, Vanilla JavaScript, and native CSS Custom Properties.

---

## ✨ Features

- **Robust Authentication**: Fully integrated OAuth2-compatible JWT (JSON Web Token) authentication flow, heavily secured using `bcrypt` password hashing.
- **Strict Data Isolation**: Every resource (Projects, Tasks) is strictly cryptographically bounded to the `owner_id`. A user can *only* interact with their own generated data.
- **Relational Integrity**: Deletion of a Project utilizes SQLite `PRAGMA foreign_keys=ON` event listeners to cleanly cascade and delete all associated child Tasks automatically.
- **Dashboard Aggregation**: A top-level dashboard that dynamically fetches all active projects and aggregates "Today's Tasks" globally utilizing a fast `?date=` query parameter.
- **Premium UI/UX**: Dark-mode natively built with pure CSS. No bulky UI frameworks—just sleek layout engines, Google `Inter` font, Animated Toast notifications, and graceful Loading states.

---

## 🏗️ Technical Stack

### Backend
- **Framework**: [FastAPI](https://fastapi.tiangolo.com/) (High-performance Async API)
- **Database**: SQLite (Perfect for portability, easily upgradeable to PostgreSQL)
- **ORM**: SQLAlchemy 2.0 (Declarative mapping and session management)
- **Validation**: Pydantic V2 (Strict request schema type-checking)
- **Security**: `python-jose` (JWT), `passlib` / `bcrypt` (Hashing)

### Frontend
- **Templating**: Jinja2 (Served directly by Starlette)
- **Styling**: Vanilla CSS (CSS Variables, Flexbox/Grid)
- **Interactivity**: Vanilla JavaScript (ES6 Fetch API `apiFetch` wrapper intercepting JWTs via localStorage)

---

## 📂 Project Architecture

The application strictly follows a **Domain-Driven Design (DDD)** Pattern to eliminate circular imports and maximize maintainability.

```text
app/
 ├── core/              # Global Configurations (Settings, JWT keys, Dependency inj.)
 ├── db/                # DB Session setup, Schema generation, Engine events
 ├── models/            # SQLAlchemy native database entities
 ├── schemas/           # Pydantic validation (Inbound payloads & Outbound serializers)
 ├── services/          # Business Logic (Keeps routers extremely thin)
 ├── routes/            # FASTApi end-routes (Controllers mapping to services)
 ├── static/            # Native CSS and Javascript files
 └── templates/         # Jinja2 HTML layout components
```

---

## ⚙️ Local Development Setup

### 1. Prerequisites
Ensure you have **Python 3.10+** installed on your system.

### 2. Environment Activation
It is highly recommended to run this inside a virtual environment.
```bash
python -m venv venv

# For Linux / Mac (fish shell):
source venv/bin/activate.fish

# For Bash / Zsh:
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the Dev Server
Start the Uvicorn ASGI server with live-reloading enabled:
```bash
uvicorn app.main:app --reload
```
*Note: SQLite database (`app/db/devtrack.db`) is automatically generated upon the first boot via SQLAlchemy's `create_all()` hook.*

---

## 🚦 Usage & Testing

1. **Access the App:** Open your browser and navigate to `http://127.0.0.1:8000`.
2. **Access Swagger Docs:** FastAPI automatically constructs beautiful API swagger documentation. Navigate to `http://127.0.0.1:8000/docs` to test endpoints manually!
3. **App Flow**:
   - Create a new account.
   - Navigate to the Dashboard.
   - Spin up a new Project.
   - Navigate into the Project and create a few Tasks assigned to specific dates.
   - Mark tasks as `Completed` directly from the Dashboard view!

---

## 🔮 Future Roadmap

- Migrating the database connector to `asyncpg` (PostgreSQL) for large-scale production deployments.
- Integrating `Alembic` for automated database schema migrations.
- Adding a collaborative "Team" feature letting users share active Projects via bridging tables.