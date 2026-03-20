from fastapi import HTTPException
from scripts.script2 import Category, Tag, Pet
from app.schemas.models import PetCreateSchema


def create_pet(pet_id, name, payload: PetCreateSchema):
	pet = Pet(
		category=Category(payload.category.id, payload.category.name),
		pet_id=pet_id,
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


def update_pet(pet_id, updates: dict):
	atual = Pet.buscar(pet_id)

	if not atual or (isinstance(atual, dict) and atual.get("code") == 1):
		raise HTTPException(status_code=404, detail="Pet not found")

	category_data = atual.get("category") or {}
	pet = Pet(
		category=Category(category_data.get("id", 0), category_data.get("name", "")),
		pet_id=pet_id,
		name=atual.get("name", ""),
		status=atual.get("status", "available"),
	)

	for url in atual.get("photoUrls", []):
		pet.add_photo_url(url)

	for tag in atual.get("tags", []):
		pet.add_tag(Tag(tag.get("id", 0), tag.get("name", "")))

	filtered_updates = {k: v for k, v in updates.items() if v is not None}
	if not filtered_updates:
		return atual

	category_id = filtered_updates.pop("category_id", None)
	category_name = filtered_updates.pop("category_name", None)
	if category_id is not None or category_name is not None:
		new_category = atual.get("category", {}).copy() if isinstance(atual.get("category"), dict) else {}
		if category_id is not None:
			new_category["id"] = category_id
		if category_name is not None:
			new_category["name"] = category_name
		filtered_updates["category"] = new_category

	result = pet.atualizar(**filtered_updates)

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
