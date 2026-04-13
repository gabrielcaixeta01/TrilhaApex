from fastapi import APIRouter, Depends, Query
from app.schemas.schemas import Tag
from app.database import get_db
from sqlalchemy.orm import Session
from app.services import tag_service

router = APIRouter(prefix="/tag", tags=["CRUD de Tags"])

@router.post("", status_code=201, response_model=Tag)
def criar_tag(
    name: str = Query(...),
    db: Session = Depends(get_db),
):
    created_tag = tag_service.create_tag(db=db, name=name)
    return created_tag


@router.get("/tags", response_model=list[Tag])
def listar_tags(db: Session = Depends(get_db)):
    return tag_service.list_tags(db)


@router.get("/{id}", response_model=Tag)
def buscar_tag(id: int, db: Session = Depends(get_db)):
    return tag_service.get_tag(db, id)
@router.put("/{id}", response_model=Tag)
def atualizar_tag(
    id: int,
    name: str = Query(...),
    description: str | None = Query(None),
    db: Session = Depends(get_db),
):
    updated_tag = tag_service.update_tag(db=db, tag_id=id, name=name, description=description)
    return updated_tag



@router.delete("/{id}", status_code=200, response_model=dict)
def deletar_tag( id: int, db: Session = Depends(get_db)) -> dict:
    tag_service.delete_tag(db, id)
    return {"message": "Tag deletada com sucesso"}