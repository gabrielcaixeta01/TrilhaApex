from fastapi import HTTPException
from scripts.script2 import User
from app.schemas.user import UserSchema

def build_user(user_id: int, payload: UserSchema) -> User:
    user = User(
        user_id=user_id,
        username=payload.username,
        firstName=payload.firstName,
        lastName=payload.lastName,
        email=payload.email,
        password=payload.password,
        phone=payload.phone,
        userStatus=payload.userStatus,
    )
    return user


def create_user(user_id: int, payload: UserSchema) -> dict:
    user = build_user(user_id, payload)
    result = user.criar()

    if not isinstance(result, dict) or result.get("id") is None:
        raise HTTPException(status_code=502, detail="Falha ao criar usuário na API externa")

    return result


def get_user(username):
    result = User.buscar(username)

    if isinstance(result, dict) and result.get("code") == 1:
        raise HTTPException(status_code=404, detail="Usuario n encontrado")

    return result


def update_user(username, payload: UserSchema):
    user = User(
        user_id=payload.id,
        username=username,
        firstName=payload.firstName,
        lastName=payload.lastName,
        email=payload.email,
        password=payload.password,
        phone=payload.phone,
        userStatus=payload.userStatus,
    )
    result = user.atualizar(
        firstName=payload.firstName,
        lastName=payload.lastName,
        email=payload.email,
        password=payload.password,
        phone=payload.phone,
        userStatus=payload.userStatus,
    )

    if isinstance(result, dict) and result.get("code") == 1:
        raise HTTPException(status_code=404, detail="User n encontrado")

    return result


def delete_user(username):
    user = User(
        user_id=0,
        username=username,
        firstName="",
        lastName="",
        email="",
        password="",
        phone="",
        userStatus=0,
    )
    result = user.deletar(username)

    if isinstance(result, dict) and result.get("code") == '1':
        raise HTTPException(status_code=404, detail="Usuario n encontrado")

    return result


def login(username, password):
    result = User.login(username, password)

    if isinstance(result, dict) and result.get("code") == 1:
        raise HTTPException(status_code=401, detail="Falha ao fazer login")

    if not isinstance(result, dict):
        raise HTTPException(status_code=502, detail="Falha ao fazer login")

    return result


def logout():
    result = User.logout()

    if not isinstance(result, dict):
        raise HTTPException(status_code=502, detail="Falha ao fazer logout")

    return result

def createWithList(users: list[UserSchema]):
    user_list = [build_user(user.id, user) for user in users]
    result = User.criar_lista(user_list)

    if not isinstance(result, dict):
        raise HTTPException(status_code=502, detail="Falha ao criar lista de usuarios na API externa")

    if result.get("code") not in (None, 200):
        raise HTTPException(status_code=502, detail=f"Falha ao criar lista de usuarios: {result}")

    return result