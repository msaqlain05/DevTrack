from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.security import create_access_token, hash_password, verify_password
from app.db.session import get_db
from app.models.user import User
from app.schemas.auth import SignupRequest, TokenResponse, UserOut

router = APIRouter(prefix="/auth", tags=["Auth"])


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
    - Raises **400** if the email is already registered.
    """
    existing = db.query(User).filter(User.email == payload.email).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )

    user = User(
        email=payload.email,
        hashed_password=hash_password(payload.password),
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


# ── POST /auth/login ──────────────────────────────────────────────────────────

from fastapi.security import OAuth2PasswordRequestForm

@router.post(
    "/login",
    response_model=TokenResponse,
    summary="Login and receive a JWT access token",
)
def login(
    payload: OAuth2PasswordRequestForm = Depends(), 
    db: Session = Depends(get_db)
) -> TokenResponse:
    """
    Authenticate a user and return a JWT bearer token.

    - Raised **401** if credentials are invalid.
    """
    # OAuth2PasswordRequestForm inherently uses the 'username' field, which maps to our email
    user = db.query(User).filter(User.email == payload.username).first()

    if not user or not verify_password(payload.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(data={"sub": user.email})
    return TokenResponse(access_token=access_token)


# ── GET /auth/me ──────────────────────────────────────────────────────────────
# Example of a protected route using get_current_user

from app.dependencies import get_current_user  # noqa: E402 — avoids circular import


@router.get(
    "/me",
    response_model=UserOut,
    summary="Get the currently authenticated user",
)
def me(current_user: User = Depends(get_current_user)) -> User:
    """Returns the profile of the authenticated user."""
    return current_user
