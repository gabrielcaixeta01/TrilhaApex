from app.database import SessionLocal
from app.schemas import models as models
import pytest


def register_user(client, email, profile_type="cliente", is_superuser=False):
    import uuid
    unique_id = str(uuid.uuid4())[:8]
    cpf = f"{unique_id[0:3]}.{unique_id[3:6]}.{unique_id[6:11]}-{unique_id[11:]}"
    
    payload = {
        "name": "User",
        "email": email,
        "password": "pass1234",
        "phone": "000",
        "profile_type": profile_type,
        "is_superuser": is_superuser,
    }

    if profile_type == "cliente":
        payload["cpf"] = cpf

    if profile_type == "funcionario":
        db = SessionLocal()
        try:
            store = models.Store(
                name=f"Store-{unique_id}",
                cnpj=f"11.111.111/0001-{unique_id}",
                phone="999",
                email=f"store-{unique_id}@example.com",
                cep="00000-000",
                city="City",
                state="ST",
                street="Street",
                neighborhood="Neigh",
                number="1",
            )
            db.add(store)
            db.commit()
            db.refresh(store)
            store_id = store.id
        finally:
            db.close()

        payload.update({
            "employee_code": f"EMP-{unique_id}",
            "job_title": "Tester",
            "salary": 1000.0,
            "store_id": store_id,
            "cnpj": cpf,
        })

    if profile_type != "funcionario":
        for k in ["employee_code", "job_title", "salary", "hired_at", "store_id", "cnpj"]:
            payload.pop(k, None)

    r = client.post("/auth/register", json=payload)
    assert r.status_code in (200, 201), r.text
    data = r.json()
    return data["access_token"], data["user"]["id"]


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


def test_auth_invalid_token(client):
    """Test authentication with invalid/missing token"""
    # without token
    r_no_token = client.get("/auth/me")
    assert r_no_token.status_code == 401
    
    # with invalid token
    headers_invalid = {"Authorization": "Bearer invalid_token_xyz"}
    r_invalid = client.get("/auth/me", headers=headers_invalid)
    assert r_invalid.status_code == 401
    
    # malformed authorization header
    headers_malformed = {"Authorization": "InvalidFormat token"}
    r_malformed = client.get("/auth/me", headers=headers_malformed)
    assert r_malformed.status_code == 401


def test_appointment_full_crud(client):
    """Test full CRUD operations on appointments"""
    import uuid
    from datetime import datetime, timedelta
    unique_id = str(uuid.uuid4())[:8]
    
    # register client, employee, and create category/tag
    token_client, client_id = register_user(client, f"cli-apt-{unique_id}@example.com", "cliente")
    token_emp, emp_id = register_user(client, f"emp-apt-{unique_id}@example.com", "funcionario")
    cat, tag = create_category_and_tag()
    
    headers_client = {"Authorization": f"Bearer {token_client}"}
    headers_emp = {"Authorization": f"Bearer {token_emp}"}
    
    # create a service
    service_params = {"name": f"Service-{unique_id}", "price": 100.0}
    r_service = client.post("/service", params=service_params, headers=headers_emp)
    assert r_service.status_code == 201
    service_id = r_service.json()["id"]
    
    # create pet for appointment
    pet_params = {
        "name": f"Pet-{unique_id}",
        "breed": "Labrador",
        "sex": "M",
        "size": "G",
        "weight": 30.0,
        "health_notes": "Healthy",
        "category_id": cat.id,
        "owner_id": client_id,
        "tag_ids": [tag.id],
    }
    r_pet = client.post("/pet", params=pet_params, headers=headers_client)
    assert r_pet.status_code == 201, f"Pet creation failed: {r_pet.text}"
    pet_id = r_pet.json()["id"]
    
    # get employee's store_id from the DB
    from app.database import SessionLocal
    from app.services.user_service import get_user
    db = SessionLocal()
    emp_user = get_user(db, emp_id)
    store_id = emp_user.employee_profile.store_id if emp_user.employee_profile else None
    db.close()
    
    assert store_id is not None, "Employee must have a store_id"
    
    # CREATE appointment
    apt_params = {
        "payment_method": "pix",
        "store_id": store_id,
        "client_id": client_id,
        "employee_id": emp_id,
        "pet_id": pet_id,
        "service_ids": [service_id],
    }
    r_create = client.post("/appointment", params=apt_params, headers=headers_client)
    assert r_create.status_code == 201, f"Appointment creation failed with {r_create.status_code}: {r_create.text}"
    apt = r_create.json()
    apt_id = apt["id"]
    assert apt["online"] == True  # client appointments are always online
    
    # LIST appointments
    r_list = client.get("/appointment/appointments")
    assert r_list.status_code == 200
    apts = r_list.json()
    assert len(apts) > 0
    assert any(a["id"] == apt_id for a in apts)
    
    # GET specific appointment
    r_get = client.get(f"/appointment/{apt_id}")
    assert r_get.status_code == 200
    apt_retrieved = r_get.json()
    assert apt_retrieved["id"] == apt_id
    
    # UPDATE appointment (only employee or owner can update)
    update_params = {"status": "em andamento"}
    r_update = client.put(f"/appointment/{apt_id}", params=update_params, headers=headers_emp)
    assert r_update.status_code == 200, f"Update failed with {r_update.status_code}: {r_update.text}"
    apt_updated = r_update.json()
    assert apt_updated["status"] == "em andamento"
    
    # DELETE appointment
    r_delete = client.delete(f"/appointment/{apt_id}", headers=headers_emp)
    assert r_delete.status_code == 200
    
    # verify deleted
    r_get_deleted = client.get(f"/appointment/{apt_id}")
    assert r_get_deleted.status_code == 404


def test_pet_listing_private(client):
    """Test that clients only see their own pets"""
    import uuid
    unique_id_a = str(uuid.uuid4())[:8]
    unique_id_b = str(uuid.uuid4())[:8]
    
    # register two clients
    token_a, id_a = register_user(client, f"client-a-{unique_id_a}@example.com", "cliente")
    token_b, id_b = register_user(client, f"client-b-{unique_id_b}@example.com", "cliente")
    headers_a = {"Authorization": f"Bearer {token_a}"}
    headers_b = {"Authorization": f"Bearer {token_b}"}
    
    cat, tag = create_category_and_tag()
    
    # client A creates a pet
    pet_a_params = {
        "name": f"Pet-A-{unique_id_a}",
        "breed": "Poodle",
        "sex": "F",
        "size": "P",
        "weight": 5.0,
        "health_notes": "Healthy",
        "category_id": cat.id,
        "owner_id": id_a,
        "tag_ids": [tag.id],
    }
    r_pet_a = client.post("/pet", params=pet_a_params, headers=headers_a)
    assert r_pet_a.status_code == 201
    pet_a_id = r_pet_a.json()["id"]
    
    # client B creates a pet
    pet_b_params = {
        "name": f"Pet-B-{unique_id_b}",
        "breed": "Bulldog",
        "sex": "M",
        "size": "M",
        "weight": 15.0,
        "health_notes": "Athletic",
        "category_id": cat.id,
        "owner_id": id_b,
        "tag_ids": [tag.id],
    }
    r_pet_b = client.post("/pet", params=pet_b_params, headers=headers_b)
    assert r_pet_b.status_code == 201
    pet_b_id = r_pet_b.json()["id"]
    
    # both clients can list all pets (public listing)
    # but they can only edit/delete their own
    r_list_a = client.get("/pet/pets")
    assert r_list_a.status_code == 200
    pets = r_list_a.json()
    assert any(p["id"] == pet_a_id for p in pets)
    assert any(p["id"] == pet_b_id for p in pets)
    
    # client A tries to update client B's pet -> should fail
    r_update_fail = client.put(
        f"/pet/{pet_b_id}",
        params={"name": "Hacked"},
        headers=headers_a
    )
    assert r_update_fail.status_code == 403
    
    # client A tries to delete client B's pet -> should fail
    r_delete_fail = client.delete(f"/pet/{pet_b_id}", headers=headers_a)
    assert r_delete_fail.status_code == 403
    
    # client A can update their own pet
    r_update_own = client.put(
        f"/pet/{pet_a_id}",
        params={"name": f"Pet-A-Updated-{unique_id_a}"},
        headers=headers_a
    )
    assert r_update_own.status_code == 200
    assert r_update_own.json()["name"] == f"Pet-A-Updated-{unique_id_a}"
    
    # client A can delete their own pet
    r_delete_own = client.delete(f"/pet/{pet_a_id}", headers=headers_a)
    assert r_delete_own.status_code == 200
