from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.services import pet_service
from app.schemas.schemas import Pet

router = APIRouter(prefix="/pet", tags=["CRUD de Pets"])


@router.post("", status_code=201, response_model=Pet)
def criar_pet(
    name: str = Query(...),
    breed: str | None = Query(None),
    sex: str | None = Query(None),
    size: str | None = Query(None),
    weight: float | None = Query(None),
    health_notes: str | None = Query(None),
    category_id: int | None = Query(None),
    owner_id: int | None = Query(None),
    db: Session = Depends(get_db),
):
    created_pet = pet_service.create_pet(
        db=db,
        name=name,
        breed=breed,
        sex=sex,
        size=size,
        weight=weight,
        health_notes=health_notes,
        category_id=category_id,
        owner_id=owner_id,
    )
    return created_pet


@router.get("/{pet_id}", response_model=Pet)
def buscar_pet(pet_id: int, db: Session = Depends(get_db)):
    pet = pet_service.get_pet(db, pet_id)
    if pet is None:
        raise HTTPException(status_code=404, detail="Pet não encontrado")
    return pet

@router.put("/{pet_id}", response_model=Pet)
def atualizar_pet(
    pet_id: int,
    name: str | None = Query(None),
    breed: str | None = Query(None),
    sex: str | None = Query(None),
    size: str | None = Query(None),
    weight: float | None = Query(None),
    health_notes: str | None = Query(None),
    category_id: int | None = Query(None),
    owner_id: int | None = Query(None),
    db: Session =  Depends(get_db),
):
    pet = pet_service.get_pet(db, pet_id)
    if pet is None:
        raise HTTPException(status_code=404, detail="Pet não encontrado")
        
    updated_pet = pet_service.update_pet(
        db=db,
        pet_id=pet_id,
        name=name,
        breed=breed,
        sex=sex,
        size=size,
        weight=weight,
        health_notes=health_notes,
        category_id=category_id,
        owner_id=owner_id
    )
    return updated_pet

@router.delete("/{pet_id}", status_code=200, response_model=dict)
def deletar_pet(pet_id: int, db: Session = Depends(get_db)):

    pet = pet_service.get_pet(db, pet_id)

    if pet is None:
        raise HTTPException(status_code=404, detail="Pet não encontrado")

    pet_service.delete_pet(db, pet_id)
    return {"message": "Pet deletado com sucesso"}