from typing import Literal
from fastapi import APIRouter
from app.services.pet_service import (
    create_pet,
    get_pet,
    update_pet,
    delete_pet,
    list_pets_by_status
)

router = APIRouter(prefix="/pet", tags=["Pets"])


@router.post("", status_code=201, response_model=dict)
def criar_pet(
    pet_id: int,
    name: str,
    category_id: int | None = None,
    category_name: str | None = None,
    photoUrls: list[str] | None = None,
    status: Literal["available", "pending", "sold"] = "available",
    tags: list[dict] | None = None
):
    
    return create_pet(
        pet_id=pet_id,
        name=name,
        category_id=category_id,
        category_name=category_name,
        photoUrls=photoUrls,
        status=status,
        tags=tags
    )


@router.get("/findByStatus", response_model=list[dict])
def buscar_por_status(status: Literal["available", "pending", "sold"]) -> list[dict]:
    return list_pets_by_status(status)


@router.get("/{pet_id}", response_model=dict)
def buscar_pet(pet_id: int):
    return get_pet(pet_id)


@router.put("/{pet_id}", response_model=dict)
def atualizar_pet(
    pet_id: int,
    name: str | None = None,
    status: Literal["available", "pending", "sold"] | None = None,
    category_id: int | None = None,
    category_name: str | None = None,
    photoUrls: list[str] | None = None
):
   
    return update_pet(
        pet_id=pet_id,
        name=name,
        status=status,
        category_id=category_id,
        category_name=category_name,
        photoUrls=photoUrls
    )


@router.delete("/{pet_id}", status_code=204)
def deletar_pet(pet_id: int):
    delete_pet(pet_id)