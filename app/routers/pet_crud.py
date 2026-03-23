from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.services import pet_service

router = APIRouter(prefix="/pet", tags=["Pets"])


@router.post("", status_code=201, response_model=dict)
def criar_pet(
    pet_id: int,
    name: str,
    category_id: int | None = None,
    category_name: str | None = None,
    photoUrls: list[str] | None = None,
    status: str = "available",
    tags: list[dict] | None = None,
    db: Session = Depends(get_db),
):
    return pet_service.create_pet(
        db, pet_id, name, category_id, category_name, photoUrls, status, tags
    )


@router.get("/{pet_id}", response_model=dict)
def buscar_pet(pet_id: int, db: Session = Depends(get_db)):
    return pet_service.get_pet(db, pet_id)


@router.put("/{pet_id}", response_model=dict)
def atualizar_pet(
    pet_id: int,
    name: str | None = None,
    status: str | None = None,
    db: Session = Depends(get_db),
):
    return pet_service.update_pet(db, pet_id, name=name, status=status)


@router.delete("/{pet_id}", status_code=204)
def deletar_pet(pet_id: int, db: Session = Depends(get_db)):
    pet_service.delete_pet(db, pet_id)


@router.get("/findByStatus", response_model=list[dict])
def buscar_por_status(status: str, db: Session = Depends(get_db)):
    return pet_service.list_pets_by_status(db, status)