from typing import Literal
from fastapi import APIRouter
from app.schemas.models import PetCreateSchema
from app.services.pet_service import (create_pet, get_pet, update_pet, delete_pet, list_pets_by_status)

router = APIRouter(prefix="/pet", tags=["Pets"])

@router.post("", status_code=201)
def criar_pet(pet_id: int, name: str, payload: PetCreateSchema):
    return create_pet(pet_id, name, payload)


@router.get("/findByStatus")
def buscar_por_status(status: str):
    return list_pets_by_status(status)

@router.get("/{pet_id}")
def buscar_pet(pet_id: int):
    return get_pet(pet_id)

@router.put("/{pet_id}")
def atualizar_pet(
    pet_id: int,
    name: str | None = None,
    status: Literal["available", "pending", "sold"] | None = None,
    category_id: int | None = None,
    category_name: str | None = None,
):
    updates = {
        "name": name,
        "status": status,
        "category_id": category_id,
        "category_name": category_name,
    }
    return update_pet(pet_id, updates)


@router.delete("/{pet_id}", status_code=204)
def deletar_pet(pet_id: int):
    return delete_pet(pet_id)