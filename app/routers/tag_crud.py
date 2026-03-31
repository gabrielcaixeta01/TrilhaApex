from fastapi import APIRouter, Depends, HTTPException
from app.schemas.schemas import MessageResponse, TagCreate, TagResponse, TagUpdate
from app.database import get_db
from sqlalchemy.orm import Session
from app.services.tag_service import (
    create_tag,
    delete_tag,
    get_tag,
    list_tags,
    update_tag,
)

router = APIRouter(prefix="/tag", tags=["CRUD de Tags"])

@router.get("", response_model=list[TagResponse])
def listar_tags(db: Session = Depends(get_db)):
    return list_tags(db)


@router.post("", status_code=201, response_model=TagResponse)
def criar_tag(
    payload: TagCreate,
    db: Session = Depends(get_db),
):
    created_tag = create_tag(db=db, name=payload.name)
    return created_tag

@router.get("/{id}", response_model=TagResponse)
def buscar_tag(id: int, db: Session = Depends(get_db)):
    tag = get_tag(db, id)
    if tag is None:
        raise HTTPException(status_code=404, detail="Tag não encontrada")
    return tag

@router.put("/{id}", response_model=TagResponse)
def atualizar_tag(
    id: int,
    payload: TagUpdate,
    db: Session = Depends(get_db),
):
    tag = get_tag(db, id)
    if tag is None:
        raise HTTPException(status_code=404, detail="Tag não encontrada")
    return update_tag(db, id, name=payload.name)



@router.delete("/{id}", status_code=200, response_model=MessageResponse)
def deletar_tag(
    id: int,
    db: Session = Depends(get_db),
) -> MessageResponse:
    tag = get_tag(db, id)
    if tag is None:
        raise HTTPException(status_code=404, detail="Tag não encontrada")
    delete_tag(db, id)
    return {"message": "Tag deletada com sucesso"}
    