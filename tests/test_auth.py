def test_register_login_me_logout(client):
    import uuid
    unique_id = str(uuid.uuid4())[:8]
    register_payload = {
        "name": "Test Client",
        "email": f"testclient-{unique_id}@example.com",
        "password": "secret123",
        "phone": "123456789",
        "profile_type": "cliente",
        "cpf": f"{unique_id[0:3]}.{unique_id[3:6]}.{unique_id[6:11]}-{unique_id[11:]}",
    }

    r = client.post("/auth/register", json=register_payload)
    assert r.status_code == 201
    data = r.json()
    assert "access_token" in data
    token = data["access_token"]

    headers = {"Authorization": f"Bearer {token}"}
    r_me = client.get("/auth/me", headers=headers)
    assert r_me.status_code == 200
    me = r_me.json()
    assert me["email"] == register_payload["email"]

    # logout (no auth required)
    r_logout = client.post("/auth/logout")
    assert r_logout.status_code == 200

    # login
    login_payload = {"email": register_payload["email"], "password": register_payload["password"]}
    r_login = client.post("/auth/login", json=login_payload)
    assert r_login.status_code == 200
    assert "access_token" in r_login.json()
