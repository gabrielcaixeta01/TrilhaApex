from fastapi import HTTPException
from scripts.script2 import Category, Tag, Pet, _request
from app.schemas.models import PetSchema


def build_pet(payload: PetSchema):
	pet = Pet(
		category=Category(payload.category.id, payload.category.name),
		pet_id=payload.pet_id,
		name=payload.name,
		status=payload.status,
	)

	for url in payload.photoUrls:
		pet.add_photo_url(url)

	for tag in payload.tags:
		pet.add_tag(Tag(tag.id, tag.name))

	return pet


def create_pet(payload: PetSchema):
	pet = build_pet(payload)
	result = pet.criar()
	return result


def get_pet(pet_id):
	result = Pet.buscar(pet_id)
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

	result = _request("PUT", "/pet", json=pet.to_dict())
	return result


def delete_pet(pet_id):
	result = _request("DELETE", f"/pet/{pet_id}")
	return result


def list_pets_by_status(status):
	result = Pet.por_status(status)
	return result
