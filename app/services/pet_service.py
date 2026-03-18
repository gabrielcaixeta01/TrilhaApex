from fastapi import HTTPException
from scripts.script2 import Category, Tag, Pet, _request
from app.schemas.pet import PetCreateSchema, PetUpdateSchema


def build_pet(pet_id: int, payload: PetCreateSchema | PetUpdateSchema) -> Pet:
	pet = Pet(
		category=Category(payload.category.id, payload.category.name),
		pet_id=pet_id,
		name=payload.name,
		status=payload.status,
	)

	for url in payload.photoUrls:
		pet.add_photo_url(url)

	for tag in payload.tags:
		pet.add_tag(Tag(tag.id, tag.name))

	return pet


def create_pet(pet_id: int, payload: PetCreateSchema) -> dict:
	pet = build_pet(pet_id, payload)
	result = pet.criar()

	if not isinstance(result, dict) or result.get("id") is None:
		raise HTTPException(status_code=502, detail="Falha ao criar pet na API externa")

	return result


def get_pet(pet_id):
	result = Pet.buscar(pet_id)

	if isinstance(result, dict) and result.get("code") == 1:
		raise HTTPException(status_code=404, detail="Pet nao encontrado")

	return result


def update_pet(pet_id: int, payload: PetUpdateSchema) -> dict:
	pet = build_pet(pet_id, payload)
	result = pet.atualizar()

	if isinstance(result, dict) and result.get("code") == 1:
		raise HTTPException(status_code=404, detail="Pet nao encontrado")

	return result


def delete_pet(pet_id):
	result = _request("DELETE", f"/pet/{pet_id}")

	if isinstance(result, dict) and result.get("code") == 1:
		raise HTTPException(status_code=404, detail="Pet nao encontrado")


def list_pets_by_status(status):
	result = Pet.por_status(status)

	if not isinstance(result, list):
		raise HTTPException(status_code=502, detail="Falha ao listar pets por status")

	return result
