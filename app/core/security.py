import os
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.models import UserModel

load_dotenv()

pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")
security = HTTPBearer()

DEV_SECRET_KEY = "change-me-in-production"
APP_ENV = os.getenv("APP_ENV", "development").strip().lower()

JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY") or DEV_SECRET_KEY
if APP_ENV == "production" and JWT_SECRET_KEY == DEV_SECRET_KEY:
    # Falha no boot em vez de subir com uma chave publica: com ela qualquer
    # pessoa forja um token de superuser.
    raise RuntimeError(
        "JWT_SECRET_KEY deve ser definida quando APP_ENV=production. "
        "Gere uma com: python -c \"import secrets; print(secrets.token_urlsafe(64))\""
    )

JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")

try:
    ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60"))
except ValueError as exc:
    raise RuntimeError("ACCESS_TOKEN_EXPIRE_MINUTES deve ser um numero inteiro de minutos") from exc


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    payload = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    payload.update({"exp": expire})
    return jwt.encode(payload, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)


def get_bearer_token(credentials: HTTPAuthorizationCredentials = Depends(security)) -> str:
    return credentials.credentials


def get_current_user(token: str = Depends(get_bearer_token), db: Session = Depends(get_db)) -> UserModel:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Não foi possível validar as credenciais",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
        user_id = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError as exc:
        raise credentials_exception from exc

    user = db.query(UserModel).filter(UserModel.id == int(user_id)).first()
    if user is None:
        raise credentials_exception

    return user


def get_current_active_user(current_user: UserModel = Depends(get_current_user)) -> UserModel:
    if not current_user.active:
        raise HTTPException(status_code=400, detail="Usuário inativo")
    return current_user
