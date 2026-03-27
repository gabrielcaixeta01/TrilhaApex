from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.schemas.models import Tag


def create_tag(db: Session, name: str):
    exists = db.query(Tag).filter(Tag.name == name).first()

    if exists:
        raise HTTPException(status_code=400, detail="Tag já existe")
    
    db_tag = Tag(name=name)
    db.add(db_tag)
    db.commit()
    db.refresh(db_tag)
    return db_tag

def get_tag(db: Session, tag_id: int):
    tag = db.query(Tag).filter(Tag.id == tag_id).first()
    if not tag:
        return None
    return tag

def update_tag(db: Session, tag_id: int, name: str):
    tag = db.query(Tag).filter(Tag.id == tag_id).first()
    if not tag:
        return None

    tag.name = name

    db.commit()
    db.refresh(tag)
    return tag


def delete_tag(db: Session, tag_id: int):
    tag = db.query(Tag).filter(Tag.id == tag_id).first()
    if tag:
        db.delete(tag)
        db.commit()
    return tag

def list_tags(db: Session):
    return db.query(Tag).all()