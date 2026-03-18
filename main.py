from fastapi import FastAPI, HTTPException, Response
from pydantic import BaseModel
from scripts.script2 import Category, Tag, Pet, _request

app = FastAPI(title="CRUD Pets - Petstore")


class CategoryIn(BaseModel):
    id: int
    name: str


class TagIn(BaseModel):
    id: int
    name: str


class PetIn(BaseModel):
    category: CategoryIn
    name: str
    photoUrls: list[str] = []
    tags: list[TagIn] = []
    status: str = "available"


class PetOut(PetIn):
    id: int


@app.get("/")
def raiz():
    return {"mensagem": "API no ar. Use /docs para testar o CRUD de pets."}


def _build_pet(pet_id: int, payload: PetIn) -> Pet:
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


# CREATE
@app.post("/pets/{pet_id}", response_model=PetOut, status_code=201)
def criar_pet(pet_id: int, payload: PetIn):
    pet = _build_pet(pet_id, payload)
    result = pet.criar()
    if not isinstance(result, dict) or result.get("id") is None:
        raise HTTPException(status_code=502, detail="Falha ao criar pet na API externa")
    return result


# READ ONE
@app.get("/pets/{pet_id}", response_model=PetOut)
def buscar_pet(pet_id: int):
    result = Pet.buscar(pet_id)
    if isinstance(result, dict) and result.get("code") == 1:
        raise HTTPException(status_code=404, detail="Pet não encontrado")
    return result


# UPDATE
@app.put("/pets/{pet_id}", response_model=PetOut)
def atualizar_pet(pet_id: int, payload: PetIn):
    pet = _build_pet(pet_id, payload)
    result = pet.atualizar()
    if isinstance(result, dict) and result.get("code") == 1:
        raise HTTPException(status_code=404, detail="Pet não encontrado")
    return result


# DELETE
@app.delete("/pets/{pet_id}", status_code=204)
def deletar_pet(pet_id: int):
    result = _request("DELETE", f"/pet/{pet_id}")
    if isinstance(result, dict) and result.get("code") == 1:
        raise HTTPException(status_code=404, detail="Pet não encontrado")
    return Response(status_code=204)


@app.get("/pets/status/{status}")
def buscar_por_status(status: str):
    return Pet.por_status(status)