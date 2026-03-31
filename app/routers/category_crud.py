from fastapi import APIRouter, Depends, HTTPException
from app.schemas.schemas import CategoryCreate, CategoryResponse, CategoryUpdate, MessageResponse
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

router = APIRouter(prefix="/category", tags=["CRUD de Categorias"])

@router.get("", response_model=list[CategoryResponse])
def listar_categorias(db: Session = Depends(get_db)):
    return list_categories(db)


@router.post("", status_code=201, response_model=CategoryResponse)
def criar_categoria(
    payload: CategoryCreate,
    current_user: UserModel = Depends(require_roles(["admin"])),
    db: Session = Depends(get_db),
):
    created_category = create_category(db=db, name=payload.name)
    return created_category

@router.get("/{id}", response_model=CategoryResponse)
def buscar_categoria(id: int, db: Session = Depends(get_db)):
    categoria = get_category(db, id)
    if categoria is None:
        raise HTTPException(status_code=404, detail="Categoria não encontrada")
    return categoria

@router.put("/{id}", response_model=CategoryResponse)
def atualizar_categoria(
    id: int,
    payload: CategoryUpdate,
    current_user: UserModel = Depends(require_roles(["admin"])),
    db: Session = Depends(get_db),
):
    categoria = get_category(db, id)
    if categoria is None:
        raise HTTPException(status_code=404, detail="Categoria não encontrada")
    return update_category(db, id, name=payload.name)



@router.delete("/{id}", status_code=200, response_model=MessageResponse)
def deletar_categoria(
    id: int,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(require_roles(["admin"])),
) -> MessageResponse:
    categoria = get_category(db, id)
    if categoria is None:
        raise HTTPException(status_code=404, detail="Categoria não encontrada")
    delete_category(db, id)
    return {"message": "Categoria deletada com sucesso"}
    