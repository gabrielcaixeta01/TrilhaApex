from typing import Literal
from fastapi import HTTPException
from scripts.script2 import Category, Tag, Pet as PetScript


def create_pet(pet_id: int, name: str,category_id: int | None = None, category_name: str | None = None, photoUrls: list[str] | None = None, status: Literal["available", "pending", "sold"] = "available", tags: list[dict] | None = None):
    try:
        # A classe Pet do script externo sempre chama category.to_dict().
        # Quando categoria nao e enviada, usamos um valor padrao para evitar NoneType.
        category = Category(category_id or 0, category_name or "")
        
        pet = PetScript(
            category=category,
            pet_id=pet_id,
            name=name,
            status=status,
        )
        
        if photoUrls:
            for url in photoUrls:
                pet.add_photo_url(url)
        
        if tags:
            for tag in tags:
                pet.add_tag(Tag(tag.get("id", 0), tag.get("name", "")))
        
        result = pet.criar()
        
        if not result:
            raise HTTPException(status_code=400, detail="Erro ao criar pet")
        
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Erro ao criar pet: {str(e)}")


def get_pet(pet_id: int):
    result = PetScript.buscar(pet_id)
    
    if not result or (isinstance(result, dict) and result.get("code") == 1):
        raise HTTPException(status_code=404, detail="Pet não encontrado")
    
    return result


def list_pets_by_status(status: Literal["available", "pending", "sold"]):
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


def update_pet(pet_id: int,name: str | None = None, status: Literal["available", "pending", "sold"] | None = None, category_id: int | None = None, category_name: str | None = None, photoUrls: list[str] | None = None):
    try:
        atual = PetScript.buscar(pet_id)
        
        if not atual or (isinstance(atual, dict) and atual.get("code") == 1):
            raise HTTPException(status_code=404, detail="Pet não encontrado")
        
        category_data = atual.get("category") or {}
        pet = PetScript(
            category=Category(category_data.get("id", 0), category_data.get("name", "")),
            pet_id=pet_id,
            name=atual.get("name", ""),
            status=atual.get("status", "available"),
        )

        updates = {}
        if name is not None:
            updates["name"] = name
        if status is not None:
            updates["status"] = status
        if category_id is not None or category_name is not None:
            updates["category"] = {
                "id": category_id if category_id is not None else category_data.get("id", 0),
                "name": category_name if category_name is not None else category_data.get("name", ""),
            }
        if photoUrls is not None:
            updates["photoUrls"] = photoUrls

        if not updates:
            return atual

        result = pet.atualizar(**updates)
        
        if not result or (isinstance(result, dict) and result.get("code") == 1):
            raise HTTPException(status_code=404, detail="Pet não encontrado")
        
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Erro ao atualizar pet: {str(e)}")


def delete_pet(pet_id: int):
    try:
        result = PetScript.deletar(pet_id)
        if not result:
            raise HTTPException(status_code=400, detail="Erro ao deletar pet")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Erro ao deletar pet: {str(e)}")
