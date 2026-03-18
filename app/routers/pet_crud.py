from fastapi import APIRouter, Response
from app.schemas.pet import PetCreateSchema, PetUpdateSchema, PetResponseSchema
from app.services.pet_service import (
    create_pet,
    get_pet,
    update_pet,
    delete_pet,
    list_pets_by_status,
)

router = APIRouter(prefix="/pets", tags=["Pets"])

@router.post("/{pet_id}", response_model=PetResponseSchema, status_code=201)
def criar_pet(pet_id: int, payload: PetCreateSchema):
    return create_pet(pet_id, payload)


@router.get("/{pet_id}", response_model=PetResponseSchema)
def buscar_pet(pet_id: int):
    return get_pet(pet_id)

@router.put("/{pet_id}", response_model=PetResponseSchema)
def atualizar_pet(pet_id: int, payload: PetUpdateSchema):
    return update_pet(pet_id, payload)


@router.delete("/{pet_id}", status_code=204)
def deletar_pet(pet_id: int):
    delete_pet(pet_id)
    return Response(status_code=204)


@router.get("/status/{status}")
def buscar_por_status(status: str):
    return list_pets_by_status(status)