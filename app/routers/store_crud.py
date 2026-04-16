from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.schemas import Store
from app.services import store_service

router = APIRouter(prefix="/store", tags=["CRUD de Lojas"])


@router.post("", status_code=201, response_model=Store)
def create_store(
	name: str = Query(...),
	cnpj: str = Query(...),
	phone: str = Query(...),
	email: str = Query(...),
	zip_code: str | None = Query(None),
	cep: str = Query(...),
	city: str = Query(...),
	state: str = Query(...),
	street: str | None = Query(None),
	address: str = Query(...),
	neighborhood: str = Query(...),
	number: str = Query(...),
	active: bool = Query(True),
	db: Session = Depends(get_db),
) -> Store:
	effective_zip_code = zip_code if zip_code is not None else cep
	effective_street = street if street is not None else address

	return store_service.create_store(
		db=db,
		name=name,
		cnpj=cnpj,
		phone=phone,
		email=email,
		zip_code=effective_zip_code,
		city=city,
		state=state,
		street=effective_street,
		neighborhood=neighborhood,
		number=number,
		active=active,
	)


@router.get("/stores", response_model=list[Store])
def list_stores(db: Session = Depends(get_db)) -> list[Store]:
	return store_service.list_stores(db)


@router.get("/{store_id}", response_model=Store)
def get_store(store_id: int, db: Session = Depends(get_db)) -> Store:
	return store_service.get_store(db, store_id)


@router.put("/{store_id}", response_model=Store)
def update_store(
	store_id: int,
	name: str | None = Query(None),
	cnpj: str | None = Query(None),
	phone: str | None = Query(None),
	email: str | None = Query(None),
	zip_code: str | None = Query(None),
	cep: str | None = Query(None),
	city: str | None = Query(None),
	state: str | None = Query(None),
	street: str | None = Query(None),
	address: str | None = Query(None),
	neighborhood: str | None = Query(None),
	number: str | None = Query(None),
	active: bool | None = Query(None),
	db: Session = Depends(get_db),
) -> Store:
	effective_zip_code = zip_code if zip_code is not None else cep
	effective_street = street if street is not None else address

	updated_store = store_service.update_store(
		db=db,
		store_id=store_id,
		name=name,
		cnpj=cnpj,
		phone=phone,
		email=email,
		zip_code=effective_zip_code,
		city=city,
		state=state,
		street=effective_street,
		neighborhood=neighborhood,
		number=number,
		active=active,
	)
	return updated_store


@router.delete("/{store_id}", status_code=200, response_model=dict)
def delete_store(store_id: int, db: Session = Depends(get_db)) -> dict:
	store_service.delete_store(db, store_id)
	return {"message": "Loja deletada com sucesso"}