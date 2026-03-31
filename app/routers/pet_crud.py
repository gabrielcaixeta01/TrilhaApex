from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.security import require_roles
from app.services import pet_service
from app.schemas.schemas import MessageResponse, PetCreate, PetResponse, PetStatus, PetUpdate
from app.schemas.models import UserModel

router = APIRouter(prefix="/pet", tags=["CRUD de Pets"])


@router.get("", response_model=list[PetResponse])
def listar_pets(
    status: PetStatus | None = Query(None),
    db: Session = Depends(get_db),
) -> list[PetResponse]:
    return pet_service.list_pets(db, status)


@router.get("/all", response_model=list[PetResponse])
def listar_todos_pets(db: Session = Depends(get_db)) -> list[PetResponse]:
    return pet_service.list_pets(db)


@router.post("", status_code=201, response_model=PetResponse)
def criar_pet(
    payload: PetCreate,
    db: Session = Depends(get_db),
):

    try:
        created_pet = pet_service.create_pet(
            db=db,
            name=payload.name,
            category_id=payload.category_id,
            photoUrls=payload.photoUrls,
            status=payload.status,
            tag_ids=payload.tag_ids,
            owner_id=payload.owner_id,
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return created_pet


@router.get("/{pet_id}", response_model=PetResponse)
def buscar_pet(pet_id: int, db: Session = Depends(get_db)):
    pet = pet_service.get_pet(db, pet_id)
    if pet is None:
        raise HTTPException(status_code=404, detail="Pet não encontrado")
    return pet

@router.put("/{pet_id}", response_model=PetResponse)
def atualizar_pet(
    pet_id: int,
    payload: PetUpdate,
    db: Session =  Depends(get_db),
):
    pet = pet_service.get_pet(db, pet_id)
    if pet is None:
        raise HTTPException(status_code=404, detail="Pet não encontrado")
    
    try:
        return pet_service.update_pet(
            db,
            pet_id,
            name=payload.name,
            status=payload.status,
            category_id=payload.category_id,
            tag_ids=payload.tag_ids,
            owner_id=payload.owner_id,
            photoUrls=payload.photoUrls,
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

@router.delete("/{pet_id}", status_code=200, response_model=MessageResponse)
def deletar_pet(
    pet_id: int,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(require_roles(["admin", "user"])),
) -> MessageResponse:
    pet = pet_service.get_pet(db, pet_id)
    if pet is None:
        raise HTTPException(status_code=404, detail="Pet não encontrado")
    if current_user.role != "admin" and pet.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Apenas admin ou o dono do pet pode deletar")

    pet_service.delete_pet(db, pet_id)
    return {"message": "Pet deletado com sucesso"}