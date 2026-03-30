from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.core.security import decode_access_token, normalize_email
from app.db.session import get_db
from app.models.user import User

# OAuth2PasswordBearer expects the token from the "Authorization: Bearer <token>" header.
# tokenUrl points to the login endpoint so Swagger UI's "Authorize" button works.
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

_credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
) -> User:
    """
    FastAPI dependency — resolves the JWT bearer token to a User ORM object.

    Raises HTTP 401 if the token is missing, expired, or the user no longer exists.
    """
    try:
        payload = decode_access_token(token)
        email: str | None = payload.get("sub")
        if email is None:
            raise _credentials_exception
    except JWTError:
        raise _credentials_exception

    user = (
        db.query(User)
        .filter(func.lower(User.email) == normalize_email(email))
        .first()
    )
    if user is None:
        raise _credentials_exception

    return user
