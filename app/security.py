from datetime import datetime, timedelta, timezone
from typing import Iterable
import os
import hashlib
import hmac

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwt
from dotenv import load_dotenv
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.models import UserModel


load_dotenv()


ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
SECRET_KEY = os.getenv("JWT_SECRET_KEY", "dev-only-secret-change-in-production")

PBKDF2_ALGORITHM = "sha256"
PBKDF2_ITERATIONS = 210000

bearer_scheme = HTTPBearer(auto_error=False)


def _pbkdf2_hash(password: str, salt_hex: str) -> str:
    dk = hashlib.pbkdf2_hmac(
        PBKDF2_ALGORITHM,
        password.encode("utf-8"),
        bytes.fromhex(salt_hex),
        PBKDF2_ITERATIONS,
    )
    return dk.hex()


def hash_password(password: str) -> str:
    salt_hex = os.urandom(16).hex()
    hash_hex = _pbkdf2_hash(password, salt_hex)
    return f"pbkdf2_sha256${PBKDF2_ITERATIONS}${salt_hex}${hash_hex}"


def verify_password(plain_password: str, hashed_password: str) -> bool:
    if not hashed_password:
        return False

    if hashed_password.startswith("pbkdf2_sha256$"):
        try:
            _, iterations_str, salt_hex, stored_hash_hex = hashed_password.split("$", 3)
            iterations = int(iterations_str)
            candidate = hashlib.pbkdf2_hmac(
                PBKDF2_ALGORITHM,
                plain_password.encode("utf-8"),
                bytes.fromhex(salt_hex),
                iterations,
            ).hex()
            return hmac.compare_digest(candidate, stored_hash_hex)
        except (ValueError, TypeError):
            return False

    # Compatibilidade com hashes gravados sem prefixo de algoritmo.
    if hashed_password.startswith("$"):
        try:
            _, iterations_str, salt_hex, stored_hash_hex = hashed_password.split("$", 3)
            iterations = int(iterations_str)
            candidate = hashlib.pbkdf2_hmac(
                PBKDF2_ALGORITHM,
                plain_password.encode("utf-8"),
                bytes.fromhex(salt_hex),
                iterations,
            ).hex()
            return hmac.compare_digest(candidate, stored_hash_hex)
        except (ValueError, TypeError):
            return False

    # Compatibilidade transitória para registros antigos em texto puro.
    return hmac.compare_digest(plain_password, hashed_password)


def create_access_token(subject: str, role: str, expires_minutes: int = ACCESS_TOKEN_EXPIRE_MINUTES) -> str:
    now = datetime.now(timezone.utc)
    expire = now + timedelta(minutes=expires_minutes)
    payload = {
        "sub": subject,
        "role": role,
        "iat": int(now.timestamp()),
        "exp": expire,
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def decode_access_token(token: str) -> dict:
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido ou expirado",
        ) from exc


def get_current_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
    db: Session = Depends(get_db),
) -> UserModel:
    if credentials is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token ausente")

    payload = decode_access_token(credentials.credentials)
    username = payload.get("sub")
    if not username:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido")

    user = db.query(UserModel).filter(UserModel.username == username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Usuário do token não existe")
    if user.userStatus != 1:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Usuário inativo")
    return user


def get_current_user_optional(
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
    db: Session = Depends(get_db),
) -> UserModel | None:
    if credentials is None:
        return None

    payload = decode_access_token(credentials.credentials)
    username = payload.get("sub")
    if not username:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido")

    user = db.query(UserModel).filter(UserModel.username == username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Usuário do token não existe")
    if user.userStatus != 1:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Usuário inativo")
    return user


def require_roles(allowed_roles: Iterable[str]):
    allowed = set(allowed_roles)

    def _dependency(current_user: UserModel = Depends(get_current_user)) -> UserModel:
        if current_user.role not in allowed:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Sem permissão")
        return current_user

    return _dependency