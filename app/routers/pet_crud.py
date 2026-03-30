from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.security import require_roles
from app.services import pet_service
from app.schemas.schemas import Pet, PetStatus
from app.schemas.models import UserModel

router = APIRouter(prefix="/pet", tags=["CRUD de Pets"])


def _parse_tag_ids(tag_ids_raw: list[str] | None) -> list[int] | None:
    if tag_ids_raw is None:
        return None

    parsed: list[int] = []
    for item in tag_ids_raw:
        parts = [part.strip() for part in item.split(",") if part.strip()]
        for part in parts:
            if not part.isdigit():
                raise HTTPException(
                    status_code=422,
                    detail=f"tag_ids inválido: '{part}'. Use inteiros, ex: 1,2,3",
                )
            parsed.append(int(part))
    return parsed


@router.post("", status_code=201, response_model=Pet)
def criar_pet(
    name: str = Query(...),
    photoUrls: str | None = Query(None),
    status: PetStatus = Query(...),
    category_id: int = Query(...),
    tag_ids: list[str] | None = Query(None),
    owner_id: int | None = Query(None),
    db: Session = Depends(get_db),
):
    tag_ids_parsed = _parse_tag_ids(tag_ids)

    try:
        created_pet = pet_service.create_pet(
            db=db,
            name=name,
            category_id=category_id,
            photoUrls=photoUrls,
            status=status,
            tag_ids=tag_ids_parsed,
            owner_id=owner_id,
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
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
    category_id: int | None = Query(None),
    tag_ids: list[str] | None = Query(None),
    owner_id: int | None = Query(None),
    photoUrls: str | None = Query(None),
    db: Session =  Depends(get_db),
):
    pet = pet_service.get_pet(db, pet_id)
    if pet is None:
        raise HTTPException(status_code=404, detail="Pet não encontrado")

    tag_ids_parsed = _parse_tag_ids(tag_ids)
    
    try:
        return pet_service.update_pet(
            db,
            pet_id,
            name=name,
            status=status,
            category_id=category_id,
            tag_ids=tag_ids_parsed,
            owner_id=owner_id,
            photoUrls=photoUrls
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

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