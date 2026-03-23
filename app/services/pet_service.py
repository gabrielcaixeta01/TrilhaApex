"""
Service de Pets - Lógica de negócio para operações com pets
"""
from typing import Literal
from fastapi import HTTPException
from scripts.script2 import Category, Tag, Pet as PetScript


# Armazém em memória (substituir por banco de dados depois)
pets_db: dict[int, dict] = {}


def create_pet(
    pet_id: int,
    name: str,
    category_id: int | None = None,
    category_name: str | None = None,
    photoUrls: list[str] | None = None,
    status: Literal["available", "pending", "sold"] = "available",
    tags: list[dict] | None = None
) -> dict:
    """Criar um novo pet"""
    try:
        # Usar classe Pet do script2
        category = None
        if category_id or category_name:
            category = Category(category_id or 0, category_name or "")
        
        pet = PetScript(
            category=category,
            pet_id=pet_id,
            name=name,
            status=status,
        )
        
        # Adicionar URLs de foto
        if photoUrls:
            for url in photoUrls:
                pet.add_photo_url(url)
        
        # Adicionar tags
        if tags:
            for tag in tags:
                pet.add_tag(Tag(tag.get("id", 0), tag.get("name", "")))
        
        result = pet.criar()
        
        if not result:
            raise HTTPException(status_code=400, detail="Erro ao criar pet")
        
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Erro ao criar pet: {str(e)}")


def get_pet(pet_id: int) -> dict:
    """Obter um pet por ID"""
    result = PetScript.buscar(pet_id)
    
    if not result or (isinstance(result, dict) and result.get("code") == 1):
        raise HTTPException(status_code=404, detail="Pet não encontrado")
    
    return result


def list_pets_by_status(status: Literal["available", "pending", "sold"]) -> list[dict]:
    """Listar pets por status"""
    valid_statuses = ["available", "pending", "sold"]
    if status not in valid_statuses:
        raise HTTPException(
            status_code=400,
            detail=f"Status inválido. Use: {', '.join(valid_statuses)}"
        )
    
    result = PetScript.por_status(status)
    
    if not result:
        raise HTTPException(status_code=404, detail="Nenhum pet encontrado com este status")
    
    return result


def update_pet(
    pet_id: int,
    name: str | None = None,
    status: Literal["available", "pending", "sold"] | None = None,
    category_id: int | None = None,
    category_name: str | None = None,
    photoUrls: list[str] | None = None
) -> dict:
    """Atualizar um pet"""
    try:
        # Buscar pet atual
        atual = PetScript.buscar(pet_id)
        
        if not atual or (isinstance(atual, dict) and atual.get("code") == 1):
            raise HTTPException(status_code=404, detail="Pet não encontrado")
        
        # Construir objeto Pet com dados atualizados
        category_data = atual.get("category") or {}
        pet = PetScript(
            category=Category(category_data.get("id", 0), category_data.get("name", "")),
            pet_id=pet_id,
            name=name if name is not None else atual.get("name", ""),
            status=status if status is not None else atual.get("status", "available"),
        )
        
        # Adicionar URLs de foto
        for url in atual.get("photoUrls", []):
            pet.add_photo_url(url)
        
        # Adicionar tags
        for tag in atual.get("tags", []):
            pet.add_tag(Tag(tag.get("id", 0), tag.get("name", "")))
        
        # Atualizar categoria se fornecida
        if category_id or category_name:
            pet.category = Category(
                category_id or category_data.get("id", 0),
                category_name or category_data.get("name", "")
            )
        
        # Atualizar fotos se fornecidas
        if photoUrls:
            for url in photoUrls:
                if url not in atual.get("photoUrls", []):
                    pet.add_photo_url(url)
        
        result = pet.atualizar()
        
        if not result or (isinstance(result, dict) and result.get("code") == 1):
            raise HTTPException(status_code=404, detail="Pet não encontrado")
        
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Erro ao atualizar pet: {str(e)}")


def delete_pet(pet_id: int) -> None:
    """Deletar um pet"""
    try:
        result = PetScript.deletar(pet_id)
        if not result:
            raise HTTPException(status_code=400, detail="Erro ao deletar pet")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Erro ao deletar pet: {str(e)}")
