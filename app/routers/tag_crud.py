from fastapi import APIRouter, Depends, HTTPException, Query
from app.schemas.schemas import Tag
from app.database import get_db
from sqlalchemy.orm import Session
from app.services.tag_service import (
    create_tag,
    delete_tag,
    get_tag,
    list_tags,
    update_tag,
)

router = APIRouter(prefix="/tag", tags=["Tag"])

@router.post("", status_code=201, response_model=Tag)
def criar_tag(
    name: str = Query(...),
    db: Session = Depends(get_db),
):
    created_tag = create_tag(db=db, name=name)
    return created_tag

@router.get("/tags", response_model=list[Tag])
def listar_tags(db: Session = Depends(get_db)):
    return list_tags(db)

@router.get("/{id}", response_model=Tag)
def buscar_tag(id: int, db: Session = Depends(get_db)):
    tag = get_tag(db, id)
    if tag is None:
        raise HTTPException(status_code=404, detail="Tag não encontrada")
    return tag

@router.put("/{id}", response_model=Tag)
def atualizar_tag(
    id: int,
    name: str = Query(...),
    db: Session = Depends(get_db),
):
    tag = get_tag(db, id)
    if tag is None:
        raise HTTPException(status_code=404, detail="Tag não encontrada")
    return update_tag(db, id, name=name)



@router.delete("/{id}",status_code=204)
def deletar_tag(
    id: int,
    db: Session = Depends(get_db),
):
    tag = get_tag(db, id)
    if tag is None:
        raise HTTPException(status_code=404, detail="Tag não encontrada")
    delete_tag(db, id)
    