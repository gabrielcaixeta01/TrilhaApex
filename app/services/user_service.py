from fastapi import HTTPException
from scripts.script2 import User
from app.schemas.models import UserSchema

def build_user(payload: UserSchema):
    user = User(
        user_id=payload.id,
        username=payload.username,
        firstName=payload.firstName,
        lastName=payload.lastName,
        email=payload.email,
        password=payload.password,
        phone=payload.phone,
        userStatus=payload.userStatus,
    )
    return user


def create_user(payload: UserSchema):
    user = build_user(payload)
    result = user.criar()
    return result

def createWithList(users: list[UserSchema]):
    user_list = [build_user(user) for user in users]
    result = User.criar_lista(user_list)

    return result


def get_user(username):
    result = User.buscar(username)

    return result


def update_user(username, payload: UserSchema):
    atual = User.buscar(username)
    result = atual.atualizar(
        firstName=payload.firstName,
        lastName=payload.lastName,
        email=payload.email,
        password=payload.password,
        phone=payload.phone,
        userStatus=payload.userStatus,
    )

    return result


def delete_user(username):
    alvo = User.buscar(username)
    result = alvo.deletar(username)

    return result


def login(username, password):
    result = User.login(username, password)
    return result


def logout():
    result = User.logout()
    return result

