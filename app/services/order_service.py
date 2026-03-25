from sqlalchemy import func
from sqlalchemy.orm import Session
from app.schemas.models import Order, Pet


def create_order(db: Session, petId: int, quantity: int | None, shipDate, status: str, complete: bool, owner_id: int | None = None):
    db_order = Order(petId=petId, quantity=quantity, shipDate=shipDate, status=status, complete=complete, owner_id=owner_id)
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order


def get_order(db: Session, order_id: int):
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        return None
    return order


def delete_order(db: Session, order_id: int):
    order = db.query(Order).filter(Order.id == order_id).first()
    if order:
        db.delete(order)
        db.commit()


def list_inventory(db: Session):
    rows = db.query(Pet.status, func.count(Pet.id)).group_by(Pet.status).all()
    return {status: count for status, count in rows}

