from sqlalchemy.orm import Session
from app.schemas.models import Service


def create_service(db: Session, petId: int, quantity: int | None, shipDate, status: str, complete: bool, owner_id: int):
    db_service = Service(petId=petId, quantity=quantity, shipDate=shipDate, status=status, complete=complete, owner_id=owner_id)
    db.add(db_service)
    db.commit()
    db.refresh(db_service)
    return db_service


def get_service(db: Session, service_id: int):
    service = db.query(service).filter(service.id == service_id).first()
    if not service:
        return None
    return service

def update_service(db: Session, service_id: int):
    service = db.query(service).filter(service.id == service_id).first()
    if not service:
        return None
    # Atualize os campos do serviço conforme necessário
    db.commit()

def delete_service(db: Session, service_id: int):
    service = db.query(service).filter(service.id == service_id).first()
    if service:
        db.delete(service)
        db.commit()


