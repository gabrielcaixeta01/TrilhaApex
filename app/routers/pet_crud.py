from alembic.util import status
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.services import pet_service
from app.schemas.schemas import Pet

router = APIRouter(prefix="/pet", tags=["Pets"])


@router.post("", status_code=201, response_model=Pet, summary="Criar novo pet",
             description="Cria um novo pet no catálogo")
def criar_pet(
    name: str = Query(..., description="Nome do pet", example="Rex"),
    photoUrls: str | None = Query(None, description="URL de foto do pet"),
    status: str = Query("available", description="Status do pet (available, pending, sold)"),
    category_id: int | None = Query(None, description="ID da categoria do pet"),
    db: Session = Depends(get_db),
):
    created_pet = pet_service.create_pet(
        db, name, photoUrls, status, category_id
    )
    return created_pet


@router.get("/findByStatus", response_model=list[Pet], summary="Buscar pets por status",
            description="Lista todos os pets com um status específico")
def buscar_por_status(status: str = Query(..., description="Status para filtrar"), db: Session = Depends(get_db)):
    return pet_service.list_pets_by_status(db, status)


@router.get("/{pet_id}", response_model=Pet, summary="Buscar pet por ID",
            description="Retorna os detalhes de um pet específico")
def buscar_pet(pet_id: int, db: Session = Depends(get_db)):
    return pet_service.get_pet(db, pet_id)


@router.put("/{pet_id}", response_model=Pet, summary="Atualizar pet",
            description="Atualiza as informações de um pet existente")
def atualizar_pet(
    pet_id: int,
    name: str | None = Query(None, description="Nome do pet"),
    status: str | None = Query(None, description="Status do pet"),
    category_id: int | None = Query(None, description="ID da categoria do pet"),
    db: Session = Depends(get_db),
):
    return pet_service.update_pet(db, pet_id, name=name, status=status, category_id=category_id)


@router.delete("/{pet_id}", status_code=204, summary="Deletar pet",
               description="Remove um pet do catálogo")
def deletar_pet(pet_id: int, db: Session = Depends(get_db)):
    pet_service.delete_pet(db, pet_id)