from fastapi import APIRouter, Depends, HTTPException, Query
from app.schemas.schemas import Category
from app.security import require_roles
from app.database import get_db
from app.schemas.models import UserModel
from sqlalchemy.orm import Session
from app.services.category_service import (
    create_category,
    delete_category,
    get_category,
    list_categories,
    update_category,
)

router = APIRouter(prefix="/category", tags=["Category"])

@router.post("", status_code=201, response_model=Category)
def criar_categoria(
    name: str = Query(...),
    current_user: UserModel = Depends(require_roles(["admin"])),
    db: Session = Depends(get_db),
):
    created_category = create_category(db=db, name=name)
    return created_category

@router.get("/categories", response_model=list[Category])
def listar_categorias(db: Session = Depends(get_db)):
    return list_categories(db)

@router.get("/{id}", response_model=Category)
def buscar_categoria(id: int, db: Session = Depends(get_db)):
    categoria = get_category(db, id)
    if categoria is None:
        raise HTTPException(status_code=404, detail="Categoria não encontrada")
    return categoria

@router.put("/{id}", response_model=Category)
def atualizar_categoria(
    id: int,
    name: str = Query(...),
    current_user: UserModel = Depends(require_roles(["admin"])),
    db: Session = Depends(get_db),
):
    categoria = get_category(db, id)
    if categoria is None:
        raise HTTPException(status_code=404, detail="Categoria não encontrada")
    return update_category(db, id, name=name)



@router.delete("/{id}",status_code=204)
def deletar_categoria(
    id: int,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(require_roles(["admin"])),
):
    categoria = get_category(db, id)
    if categoria is None:
        raise HTTPException(status_code=404, detail="Categoria não encontrada")
    delete_category(db, id)
    