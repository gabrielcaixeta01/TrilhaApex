from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.security import require_roles
from app.services import pet_service
from app.schemas.schemas import Pet, PetStatus
from app.schemas.models import UserModel

router = APIRouter(prefix="/pet", tags=["CRUD de Pets"])


@router.post("", status_code=201, response_model=Pet)
def criar_pet(
    name: str = Query(...),
    photoUrls: str | None = Query(None),
    status: PetStatus = Query(...),
    category_id: int = Query(...),
    tag_id: int | None = Query(None),
    owner_id: int | None = Query(None),
    db: Session = Depends(get_db),
):
    
    created_pet = pet_service.create_pet(
        db=db,
        name=name,
        category_id=category_id,
        photoUrls=photoUrls,
        status=status,
        tag_id=tag_id,
        owner_id=owner_id,
    )
    return created_pet


@router.get("/findByStatus", response_model=list[Pet])
def buscar_por_status(status: PetStatus = Query(...), db: Session = Depends(get_db)):
    return pet_service.list_pets_by_status(db, status)


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
    status: PetStatus | None = Query(None),
    category_id: int = Query(...),
    tag_id: int | None = Query(None),
    owner_id: int | None = Query(None),
    photoUrls: str | None = Query(None),
    db: Session =  Depends(get_db),
):
    pet = pet_service.get_pet(db, pet_id)
    if pet is None:
        raise HTTPException(status_code=404, detail="Pet não encontrado")
    
    return pet_service.update_pet(
        db,
        pet_id,
        name=name,
        status=status,
        category_id=category_id,
        tag_id=tag_id,
        owner_id=owner_id,
        photoUrls=photoUrls
    )

@router.delete("/{pet_id}", status_code=204)
def deletar_pet(
    pet_id: int,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(require_roles(["admin", "user"])),
):
    pet = pet_service.get_pet(db, pet_id)
    if pet is None:
        raise HTTPException(status_code=404, detail="Pet não encontrado")
    if current_user.role != "admin" and pet.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Apenas admin ou o dono do pet pode deletar")

    pet_service.delete_pet(db, pet_id)