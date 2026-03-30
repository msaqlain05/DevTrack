from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import func
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.security import create_access_token, hash_password, normalize_email, verify_password
from app.db.session import get_db
from app.dependencies import get_current_user
from app.models.user import User
from app.schemas.auth import LoginRequest, SignupRequest, TokenResponse, UserOut

router = APIRouter(prefix="/auth", tags=["Auth"])


def _user_by_email(db: Session, email: str) -> User | None:
    """Case-insensitive lookup (handles legacy rows and normalized JWT sub)."""
    key = normalize_email(email)
    return db.query(User).filter(func.lower(User.email) == key).first()


def _is_unique_constraint_violation(exc: IntegrityError) -> bool:
    orig = getattr(exc, "orig", None)
    if orig is None:
        return False
    code = getattr(orig, "pgcode", None)
    if code == "23505":  # PostgreSQL unique_violation
        return True
    text = str(orig).lower()
    return "unique constraint failed" in text  # SQLite


# ── POST /auth/signup ─────────────────────────────────────────────────────────

@router.post(
    "/signup",
    response_model=UserOut,
    status_code=status.HTTP_201_CREATED,
    summary="Register a new user",
)
def signup(payload: SignupRequest, db: Session = Depends(get_db)) -> User:
    """
    Create a new user account.

    - Returns the created user (without password).
    - Raises **409** if the email is already registered.
    """
    if _user_by_email(db, payload.email):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already registered",
        )

    user = User(
        email=payload.email,
        hashed_password=hash_password(payload.password),
    )
    db.add(user)
    try:
        db.commit()
    except IntegrityError as e:
        db.rollback()
        if _is_unique_constraint_violation(e):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Email already registered",
            ) from None
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Could not create account.",
        ) from e
    db.refresh(user)
    return user


# ── POST /auth/login ──────────────────────────────────────────────────────────

@router.post(
    "/login",
    response_model=TokenResponse,
    summary="Login and receive a JWT access token",
)
def login(payload: LoginRequest, db: Session = Depends(get_db)) -> TokenResponse:
    """
    Authenticate a user and return a JWT bearer token.

    - Raises **401** if credentials are invalid.
    """
    user = _user_by_email(db, payload.email)

    if not user or not verify_password(payload.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(data={"sub": normalize_email(user.email)})
    return TokenResponse(access_token=access_token)


# ── GET /auth/me ──────────────────────────────────────────────────────────────

@router.get(
    "/me",
    response_model=UserOut,
    summary="Get the currently authenticated user",
)
def me(current_user: User = Depends(get_current_user)) -> User:
    """Returns the profile of the authenticated user."""
    return current_user
