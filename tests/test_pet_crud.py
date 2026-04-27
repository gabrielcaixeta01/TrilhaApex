from app.database import SessionLocal
from app.schemas import models as models


def create_category_and_tag():
    import uuid
    unique_id = str(uuid.uuid4())[:8]
    db = SessionLocal()
    try:
        cat = models.Category(name=f"Cães-{unique_id}", description="Categoria para cães")
        tag = models.Tag(name=f"Vacinado-{unique_id}", description="Pet vacinado")
        db.add(cat)
        db.add(tag)
        db.commit()
        db.refresh(cat)
        db.refresh(tag)
        return cat, tag
    finally:
        db.close()


def register_client(client, email=None):
    import uuid
    if email is None:
        unique_id = str(uuid.uuid4())[:8]
        email = f"owner-{unique_id}@example.com"
    unique_id = str(uuid.uuid4())[:8]
    payload = {
        "name": "Owner",
        "email": email,
        "password": "ownerpass",
        "phone": "999",
        "profile_type": "cliente",
        "cpf": f"{unique_id[0:3]}.{unique_id[3:6]}.{unique_id[6:11]}-{unique_id[11:]}",
    }
    r = client.post("/auth/register", json=payload)
    assert r.status_code in (200, 201), r.text
    data = r.json()
    return data["access_token"], data["user"]["id"]


def test_pet_create_update_delete_owner_checks(client):
    cat, tag = create_category_and_tag()

    token_owner, owner_id = register_client(client)
    headers_owner = {"Authorization": f"Bearer {token_owner}"}

    # create pet as owner
    params = {
        "name": "Rex",
        "breed": "Vira-lata",
        "sex": "M",
        "size": "M",
        "weight": 12.5,
        "health_notes": "Healthy",
        "category_id": cat.id,
        "owner_id": owner_id,
        "tag_ids": [tag.id],
    }
    r = client.post("/pet", params=params, headers=headers_owner)
    assert r.status_code == 201
    pet = r.json()
    assert pet["owner_id"] == owner_id
    assert any(t["id"] == tag.id for t in pet["tags"])

    pet_id = pet["id"]

    # register another user
    token_other, other_id = register_client(client)
    headers_other = {"Authorization": f"Bearer {token_other}"}

    # other cannot update
    r_up = client.put(f"/pet/{pet_id}", params={"name": "Hack"}, headers=headers_other)
    assert r_up.status_code == 403

    # owner can update
    r_up2 = client.put(f"/pet/{pet_id}", params={"name": "Rexinho"}, headers=headers_owner)
    assert r_up2.status_code == 200
    assert r_up2.json()["name"] == "Rexinho"

    # other cannot delete
    r_del = client.delete(f"/pet/{pet_id}", headers=headers_other)
    assert r_del.status_code == 403

    # owner can delete
    r_del2 = client.delete(f"/pet/{pet_id}", headers=headers_owner)
    assert r_del2.status_code == 200
    assert r_del2.json()["message"]
