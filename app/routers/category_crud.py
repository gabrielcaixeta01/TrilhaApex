from fastapi import APIRouter, Depends, HTTPException, Query
from app.schemas.schemas import Category
from app.database import get_db
from sqlalchemy.orm import Session
from app.services.category_service import (
    create_category,
    delete_category,
    get_category,
    list_categories,
    update_category,
)

router = APIRouter(prefix="/category", tags=["CRUD de Categorias"])

@router.post("", status_code=201, response_model=Category)
def criar_categoria(
    name: str = Query(...),
    description: str | None = Query(None),
    db: Session = Depends(get_db),
):
    created_category = create_category(db=db, name=name, description=description)
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
    description: str | None = Query(None),
    db: Session = Depends(get_db),
):
    categoria = get_category(db, id)
    if categoria is None:
        raise HTTPException(status_code=404, detail="Categoria não encontrada")
    return update_category(db, id, name=name, description=description)



@router.delete("/{id}", status_code=200, response_model=dict)
def deletar_categoria( id: int, db: Session = Depends(get_db)) -> dict:
    categoria = get_category(db, id)
    if categoria is None:
        raise HTTPException(status_code=404, detail="Categoria não encontrada")
    delete_category(db, id)
    return {"message": "Categoria deletada com sucesso"}