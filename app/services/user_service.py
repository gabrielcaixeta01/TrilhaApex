from fastapi import HTTPException
from scripts.script2 import User
from app.schemas.models import UserSchema, UserCreateSchema


def create_user(username: str, password: str, payload: UserCreateSchema):
    user = User(
        user_id=payload.id,
        username=username,
        firstName=payload.firstName,
        lastName=payload.lastName,
        email=payload.email,
        password=password,
        phone=payload.phone,
        userStatus=payload.userStatus,
    )
    result = user.criar()

    if not result:
        raise HTTPException(status_code=400, detail="Failed to create user")
    
    return result

def createWithList(users: list[UserSchema]):
    user_list = [User(
        user_id=user.id,
        username=user.username,
        firstName=user.firstName,
        lastName=user.lastName,
        email=user.email,
        password=user.password,
        phone=user.phone,
        userStatus=user.userStatus,
    ) for user in users]

    result = User.criar_lista(user_list)

    if not result:
        raise HTTPException(status_code=400, detail="Failed to create users")

    return result


def get_user(username):
    result = User.buscar(username)
    
    if not result or (isinstance(result, dict) and result.get("code") == 1):
        raise HTTPException(status_code=404, detail="User not found")
    
    return result


def update_user(username, updates: dict):
    atual = User.buscar(username)

    if not atual or (isinstance(atual, dict) and atual.get("code") == 1):
        raise HTTPException(status_code=404, detail="User not found")

    user = User(
        user_id=atual.get("id", 0),
        username=atual.get("username", username),
        firstName=atual.get("firstName", ""),
        lastName=atual.get("lastName", ""),
        email=atual.get("email", ""),
        password=atual.get("password", ""),
        phone=atual.get("phone", ""),
        userStatus=atual.get("userStatus", 0),
    )

    filtered_updates = {k: v for k, v in updates.items() if v is not None}
    if not filtered_updates:
        return atual

    result = user.atualizar(username, **filtered_updates)

    return result


def delete_user(username):
    result = User.deletar(username)

    if not result:
        raise HTTPException(status_code=400, detail="Failed to delete user")
    
    return result


def login(username, password):
    result = User.login(username, password)

    if not result:
        raise HTTPException(status_code=400, detail="Failed to login")
    
    return result


def logout():
    result = User.logout()

    if not result:
        raise HTTPException(status_code=400, detail="Failed to logout")
    
    return result

