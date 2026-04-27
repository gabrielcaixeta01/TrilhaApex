from app.database import SessionLocal
from app.schemas import models as models


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

    # ensure required fields for cliente
    if profile_type == "cliente":
        payload["cpf"] = cpf

    # ensure required store exists and employee fields for funcionario
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

    # ensure cliente payload doesn't carry employee fields
    if profile_type != "funcionario":
        for k in ["employee_code", "job_title", "salary", "hired_at", "store_id", "cnpj"]:
            payload.pop(k, None)

    r = client.post("/auth/register", json=payload)
    assert r.status_code in (200, 201), r.text
    data = r.json()
    return data["access_token"], data["user"]["id"]


def test_tag_service_category_permissions(client):
    import uuid
    unique_id_cli = str(uuid.uuid4())[:8]
    unique_id_emp = str(uuid.uuid4())[:8]
    
    # cliente cannot create tag/service/category
    token_client, _ = register_user(client, f"cli-{unique_id_cli}@example.com", "cliente")
    headers_client = {"Authorization": f"Bearer {token_client}"}

    r_tag = client.post("/tag", params={"name": f"T1-{unique_id_cli}"}, headers=headers_client)
    assert r_tag.status_code == 403

    r_service = client.post("/service", params={"name": f"S1-{unique_id_cli}", "price": 10.0}, headers=headers_client)
    assert r_service.status_code == 403

    r_cat = client.post("/category", params={"name": f"C1-{unique_id_cli}"}, headers=headers_client)
    assert r_cat.status_code == 403

    # funcionario can create
    token_emp, _ = register_user(client, f"emp-{unique_id_emp}@example.com", "funcionario")
    headers_emp = {"Authorization": f"Bearer {token_emp}"}

    r_tag2 = client.post("/tag", params={"name": f"T2-{unique_id_emp}"}, headers=headers_emp)
    assert r_tag2.status_code == 201

    r_service2 = client.post("/service", params={"name": f"S2-{unique_id_emp}", "price": 20.0}, headers=headers_emp)
    assert r_service2.status_code == 201

    r_cat2 = client.post("/category", params={"name": f"C2-{unique_id_emp}"}, headers=headers_emp)
    assert r_cat2.status_code == 201

    # cliente cannot delete tag
    tag_id = r_tag2.json()["id"]
    r_del = client.delete(f"/tag/{tag_id}", headers=headers_client)
    assert r_del.status_code == 403

    # funcionario can delete
    r_del2 = client.delete(f"/tag/{tag_id}", headers=headers_emp)
    assert r_del2.status_code == 200


def test_store_creation_superuser_only(client):
    import uuid
    unique_id = str(uuid.uuid4())[:8]
    
    # funcionario cannot create store
    token_emp, _ = register_user(client, f"emp2-{unique_id}@example.com", "funcionario")
    headers_emp = {"Authorization": f"Bearer {token_emp}"}

    store_params = {
        "name": f"Loja Teste-{unique_id}",
        "cnpj": f"00.000.000/0001-{unique_id[:2]}",
        "phone": "123",
        "email": f"loja-{unique_id}@example.com",
        "cep": "00000-000",
        "city": "Cidade",
        "state": "ST",
        "street": "Rua Teste",
        "neighborhood": "Bairro",
        "number": "1",
    }

    r_emp_store = client.post("/store", params=store_params, headers=headers_emp)
    assert r_emp_store.status_code == 403

    # superuser can create store
    unique_id2 = str(uuid.uuid4())[:8]
    token_sup, _ = register_user(client, f"sup-{unique_id2}@example.com", "funcionario", True)
    headers_sup = {"Authorization": f"Bearer {token_sup}"}

    r_sup_store = client.post("/store", params=store_params, headers=headers_sup)
    assert r_sup_store.status_code == 201


def test_appointment_client_restriction(client):
    import uuid
    unique_id_a = str(uuid.uuid4())[:8]
    unique_id_b = str(uuid.uuid4())[:8]
    
    # register two clients
    token_a, id_a = register_user(client, f"a-{unique_id_a}@example.com", "cliente")
    token_b, id_b = register_user(client, f"b-{unique_id_b}@example.com", "cliente")
    headers_a = {"Authorization": f"Bearer {token_a}"}

    # try to create appointment as A for client B -> should be 403
    params = {
        "payment_method": "cash",
        "store_id": 1,
        "client_id": id_b,
        "employee_id": 1,
        "pet_id": 1,
        "service_ids": [1],
    }
    r = client.post("/appointment", params=params, headers=headers_a)
    assert r.status_code == 403
