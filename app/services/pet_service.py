from fastapi import HTTPException
from scripts.script2 import Category, Tag, Pet
from app.schemas.models import PetSchema


def create_pet(name, payload: PetSchema):
	pet = Pet(
		category=Category(payload.category.id, payload.category.name),
		pet_id=payload.pet_id,
		name=name,
		status=payload.status,
	)

	for url in payload.photoUrls:
		pet.add_photo_url(url)

	for tag in payload.tags:
		pet.add_tag(Tag(tag.id, tag.name))

	result = pet.criar()

	if not result:
		raise HTTPException(status_code=400, detail="Failed to create pet")
	
	return result


def get_pet(pet_id):
	result = Pet.buscar(pet_id)

	if not result:
		raise HTTPException(status_code=404, detail="Pet not found")
	
	return result


def update_pet(pet_id, payload: PetSchema):
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

	result = pet.atualizar()

	if not result:
		raise HTTPException(status_code=400, detail="Failed to update pet")
	
	return result


def delete_pet(pet_id):
	result = Pet.deletar(pet_id)
	if not result:
		raise HTTPException(status_code=400, detail="Failed to delete pet")
	
	return result


def list_pets_by_status(status):
	result = Pet.por_status(status)

	if not result:
		raise HTTPException(status_code=404, detail="No pets found with the given status")
	
	return result
