from fastapi import APIRouter
from app.schemas.models import PetSchema
from app.services.pet_service import (create_pet, get_pet, update_pet, delete_pet, list_pets_by_status)

router = APIRouter(prefix="/pet", tags=["Pets"])

@router.post("", status_code=201)
def criar_pet(name: str, payload: PetSchema):
    return create_pet(name, payload)


@router.get("/findByStatus")
def buscar_por_status(status: str):
    return list_pets_by_status(status)

@router.get("/{pet_id}")
def buscar_pet(pet_id: int):
    return get_pet(pet_id)

@router.put("/{pet_id}")
def atualizar_pet(pet_id: int, payload: PetSchema):
    return update_pet(pet_id, payload)


@router.delete("/{pet_id}", status_code=204)
def deletar_pet(pet_id: int):
    return delete_pet(pet_id)