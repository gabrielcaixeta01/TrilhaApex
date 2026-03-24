from alembic.util import status
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.services import pet_service
from app.schemas.schemas import Pet

router = APIRouter(prefix="/pet", tags=["Pets"])


@router.post("", status_code=201, response_model=Pet)
def criar_pet(
    name: str = Query(..., example="Rex"),
    photoUrls: str | None = Query(None),
    status: str = Query("available"),
    category_id: int | None = Query(None),
    db: Session = Depends(get_db),
):
    created_pet = pet_service.create_pet(
        db, name, photoUrls, status, category_id
    )
    return created_pet


@router.get("/findByStatus", response_model=list[Pet])
def buscar_por_status(status: str = Query(...), db: Session = Depends(get_db)):
    return pet_service.list_pets_by_status(db, status)


@router.get("/{pet_id}", response_model=Pet)
def buscar_pet(pet_id: int, db: Session = Depends(get_db)):
    return pet_service.get_pet(db, pet_id)


@router.put("/{pet_id}", response_model=Pet)
def atualizar_pet(
    pet_id: int,
    name: str | None = Query(None),
    status: str | None = Query(None),
    category_id: int | None = Query(None),
    db: Session = Depends(get_db),
):
    return pet_service.update_pet(db, pet_id, name=name, status=status, category_id=category_id)


@router.delete("/{pet_id}", status_code=204)
def deletar_pet(pet_id: int, db: Session = Depends(get_db)):
    pet_service.delete_pet(db, pet_id)