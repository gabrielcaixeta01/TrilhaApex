"""
Router para operações de Pets (CRUD)
Endpoints documentados automaticamente no Swagger
"""
from typing import Literal
from fastapi import APIRouter
from app.schemas.models import Pet, Category, Tag
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
) -> dict:
    """
    Criar um novo pet
    
    - **pet_id**: ID único do pet
    - **name**: Nome do pet
    - **status**: Status do pet (available, pending, sold)
    """
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
    """
    Buscar pets por status
    
    - **status**: Status para filtrar (available, pending, sold)
    """
    return list_pets_by_status(status)


@router.get("/{pet_id}", response_model=dict)
def buscar_pet(pet_id: int) -> dict:
    """
    Buscar um pet específico por ID
    
    - **pet_id**: ID do pet
    """
    return get_pet(pet_id)


@router.put("/{pet_id}", response_model=dict)
def atualizar_pet(
    pet_id: int,
    name: str | None = None,
    status: Literal["available", "pending", "sold"] | None = None,
    category_id: int | None = None,
    category_name: str | None = None,
    photoUrls: list[str] | None = None
) -> dict:
    """
    Atualizar informações de um pet
    
    - **pet_id**: ID do pet a atualizar
    """
    return update_pet(
        pet_id=pet_id,
        name=name,
        status=status,
        category_id=category_id,
        category_name=category_name,
        photoUrls=photoUrls
    )


@router.delete("/{pet_id}", status_code=204)
def deletar_pet(pet_id: int) -> None:
    """
    Deletar um pet
    
    - **pet_id**: ID do pet a deletar
    """
    delete_pet(pet_id)