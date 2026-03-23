from fastapi import HTTPException
from scripts.script2 import User


def create_user(id: int, username: str, password: str, firstName: str | None = None, lastName: str | None = None, email: str | None = None, phone: str | None = None, userStatus: int = 0):
    try:
        user = User(
            user_id=id,
            username=username,
            firstName=firstName,
            lastName=lastName,
            email=email,
            password=password,
            phone=phone,
            userStatus=userStatus,
        )
        result = user.criar()
        
        if not result:
            raise HTTPException(status_code=400, detail="Erro ao criar usuário")
        
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Erro ao criar usuário: {str(e)}")


def create_with_list(users: list[dict]) -> list[dict]:
    try:
        user_list = [
            User(
                user_id=user.get("id", 0),
                username=user.get("username", ""),
                firstName=user.get("firstName", ""),
                lastName=user.get("lastName", ""),
                email=user.get("email", ""),
                password=user.get("password", ""),
                phone=user.get("phone"),
                userStatus=user.get("userStatus", 0),
            )
            for user in users
        ]
        
        result = User.criar_lista(user_list)
        
        if not result:
            raise HTTPException(status_code=400, detail="Erro ao criar usuários")
        
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Erro ao criar usuários: {str(e)}")


def get_user(username: str) -> dict:
    try:
        result = User.buscar(username)
        
        if not result or (isinstance(result, dict) and result.get("code") == 1):
            raise HTTPException(status_code=404, detail="Usuário não encontrado")
        
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Erro ao buscar usuário: {str(e)}")


def update_user(username: str, firstName: str | None = None, lastName: str | None = None, email: str | None = None, password: str | None = None, phone: str | None = None, userStatus: int | None = None):
    try:
        atual = User.buscar(username)
        
        if not atual or (isinstance(atual, dict) and atual.get("code") == 1):
            raise HTTPException(status_code=404, detail="Usuário não encontrado")
        
        user = User(
            user_id=atual.get("id", 0),
            username=atual.get("username", username),
            firstName=firstName if firstName is not None else atual.get("firstName", ""),
            lastName=lastName if lastName is not None else atual.get("lastName", ""),
            email=email if email is not None else atual.get("email", ""),
            password=password if password is not None else atual.get("password", ""),
            phone=phone if phone is not None else atual.get("phone", ""),
            userStatus=userStatus if userStatus is not None else atual.get("userStatus", 0),
        )
        
        updates = {
            "firstName": firstName,
            "lastName": lastName,
            "email": email,
            "password": password,
            "phone": phone,
            "userStatus": userStatus,
        }
        filtered_updates = {k: v for k, v in updates.items() if v is not None}
        
        if not filtered_updates:
            return atual
        
        result = user.atualizar(username, **filtered_updates)
        
        if not result or (isinstance(result, dict) and result.get("code") == 1):
            raise HTTPException(status_code=404, detail="Usuário não encontrado")
        
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Erro ao atualizar usuário: {str(e)}")


def delete_user(username: str):
    try:
        result = User.deletar(username)
        
        if not result:
            raise HTTPException(status_code=400, detail="Erro ao deletar usuário")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Erro ao deletar usuário: {str(e)}")


def login(username: str, password: str):
    try:
        result = User.login(username, password)
        
        if not result:
            raise HTTPException(status_code=401, detail="Erro ao fazer login")
        
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Erro ao fazer login: {str(e)}")


def logout():
    try:
        result = User.logout()
        
        if not result:
            raise HTTPException(status_code=400, detail="Erro ao fazer logout")
        
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Erro ao fazer logout: {str(e)}")
