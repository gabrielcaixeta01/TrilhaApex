from fastapi import HTTPException
from scripts.script2 import Category, Tag, Pet
from app.schemas.models import PetSchema


def build_pet(id, payload: PetSchema) -> Pet:
	pet = Pet(
		category=Category(payload.category.id, payload.category.name),
		pet_id=id,
		name=payload.name,
		status=payload.status,
	)

	for url in payload.photoUrls:
		pet.add_photo_url(url)

	for tag in payload.tags:
		pet.add_tag(Tag(tag.id, tag.name))

	return pet


def create_pet(payload: PetSchema) -> dict:
	pet = build_pet(payload.id, payload)
	result = pet.criar()

	if not isinstance(result, dict) or result.get("id") is None:
		raise HTTPException(status_code=502, detail="Falha ao criar pet na API externa")

	return result


def get_pet(pet_id):
	result = Pet.buscar(pet_id)

	if isinstance(result, dict) and result.get("code") == 1:
		raise HTTPException(status_code=404, detail="Pet nao encontrado")

	return result


def update_pet(id: int, payload: PetSchema) -> dict:
	pet = build_pet(id, payload)
	result = pet.atualizar()

	if isinstance(result, dict) and result.get("code") == 1:
		raise HTTPException(status_code=404, detail="Pet nao encontrado")

	return result


def delete_pet(pet_id):
	pet = Pet()
	result = pet.deletar(pet_id)

	if isinstance(result, dict) and result.get("code") == 1:
		raise HTTPException(status_code=404, detail="Pet nao encontrado")
	
	return result


def list_pets_by_status(status):
	result = Pet.por_status(status)

	if not isinstance(result, list):
		raise HTTPException(status_code=502, detail="Falha ao listar pets por status")

	return result
