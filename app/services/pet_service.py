from fastapi import HTTPException
from scripts.script2 import Category, Tag, Pet
from app.schemas.models import PetSchema


def build_pet(payload: PetSchema):
	pet = Pet(
		category=Category(payload.category.id, payload.category.name),
		pet_id=payload.id,
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
	atual = Pet.buscar(pet_id)
	result = atual.atualizar(
		Category(payload.category.id, payload.category.name),
		name = payload.name,
		photoUrls = payload.photoUrls,
		tags = [Tag(tag.id, tag.name) for tag in payload.tags],
		status = payload.status
	)
	return result


def delete_pet(pet_id):
	alvo = Pet.buscar(pet_id)
	result = alvo.deletar(pet_id)
	return result


def list_pets_by_status(status):
	result = Pet.por_status(status)
	return result
