import requests
import json

BASE_URL = "https://petstore.swagger.io/v2"

def _request(method, path, **kwargs):
    return requests.request(method, f"{BASE_URL}{path}", **kwargs).json()

def _usuario_payload(id, username, firstName, lastName, email, password, phone, userStatus):
    return {"id": id, "username": username, "firstName": firstName, "lastName": lastName,
            "email": email, "password": password, "phone": phone, "userStatus": userStatus}



def criarPet(id, categoria, nome, fotoUrl, tags, status):
    return _request("POST", "/pet", json={"id": id, "category": categoria, "name": nome,
                                          "photoUrls": fotoUrl, "tags": tags, "status": status})

def imagemPet(id, metadata, file_path):
    with open(file_path, "rb") as f:
        return _request("POST", f"/pet/{id}/uploadImage",
                        files={"file": f}, data={"additionalMetadata": metadata})

def buscarPet(id):
    return _request("GET", f"/pet/{id}")

def petsPorStatus(status):
    return _request("GET", "/pet/findByStatus", params={"status": status})

def atualizarPet(id, categoria, nome, fotoUrl, tags, status):
    return _request("PUT", "/pet", json={"id": id, "category": categoria, "name": nome,
                                         "photoUrls": fotoUrl, "tags": tags, "status": status})

def deletarPet(id):
    return _request("DELETE", f"/pet/{id}")



def inventarioPets():
    return _request("GET", "/store/inventory")

def criarCompraPet(id, petId, quantidade, dataEntrega, status, completo):
    return _request("POST", "/store/order",
                    json={"id": id, "petId": petId, "quantity": quantidade,"shipDate": dataEntrega, "status": status, "complete": completo})

def buscarCompraPet(id):
    return _request("GET", f"/store/order/{id}")

def deletarCompraPet(id):
    return _request("DELETE", f"/store/order/{id}")



def criarListaDesejo(id, username, firstName, lastName, email, password, phone, userStatus):
    return _request("POST", "/user/createWithList",
                    json=[_usuario_payload(id, username, firstName, lastName, email, password, phone, userStatus)])

def buscarUsuario(username):
    return _request("GET", f"/user/{username}")

def atualizarUsuario(username, **dados):
    usuario = buscarUsuario(username)
    usuario.update(dados)
    usuario["username"] = username
    return _request("PUT", f"/user/{username}", json=usuario)

def deletarUsuario(username):
    return _request("DELETE", f"/user/{username}")

def login(username, password):
    return _request("GET", "/user/login", params={"username": username, "password": password})

def logout():
    return _request("GET", "/user/logout")

def criarListaUsuarios(id, username, firstName, lastName, email, password, phone, userStatus):
    return _request("POST", "/user/createWithArray",
                    json=[_usuario_payload(id, username, firstName, lastName, email, password, phone, userStatus)])

def criarUsuario(id, username, firstName, lastName, email, password, phone, userStatus):
    return _request("POST", "/user",
                    json=_usuario_payload(id, username, firstName, lastName, email, password, phone, userStatus))




def main():
    resultado = {
        "api_base": BASE_URL,
        "pet": {},
        "loja": {},
        "usuario": {},
    }

    pet_id = 12345
    order_id = 54321
    username = "gabriel_teste_main"

    try:
        pet_payload = {
            "id": pet_id,
            "category": {"id": 1, "name": "Cachorro"},
            "name": "Rex",
            "photoUrls": ["https://example.com/photo1.jpg"],
            "tags": [{"id": 1, "name": "Brinquedo"}],
            "status": "available",
        }
        criarPet(
            id=pet_id,
            categoria=pet_payload["category"],
            nome=pet_payload["name"],
            fotoUrl=pet_payload["photoUrls"],
            tags=pet_payload["tags"],
            status=pet_payload["status"],
        )
        pets_status = petsPorStatus("available")
        resultado["pet"] = {
            "pet_enviado": pet_payload,
            "total_por_status": len(pets_status),
        }
    except Exception as e:
        resultado["pet"] = {"erro": str(e)}

    try:
        inventario = inventarioPets()
        pedido_payload = {
            "id": order_id,
            "petId": pet_id,
            "quantity": 1,
            "shipDate": "2026-03-16T10:00:00.000Z",
            "status": "placed",
            "complete": False,
        }
        criarCompraPet(
            id=order_id,
            petId=pet_id,
            quantidade=pedido_payload["quantity"],
            dataEntrega=pedido_payload["shipDate"],
            status=pedido_payload["status"],
            completo=pedido_payload["complete"],
        )
        resultado["loja"] = {
            "pedido_enviado": pedido_payload,
            "inventario": inventario,
            "total_status_inventario": len(inventario),
        }
    except Exception as e:
        resultado["loja"] = {"erro": str(e)}

    try:
        usuario_payload = _usuario_payload(
            1001,
            username,
            "Gabriel",
            "Romero",
            "gabriel@email.com",
            "123456",
            "11999999999",
            1,
        )
        criarUsuario(
            id=usuario_payload["id"],
            username=usuario_payload["username"],
            firstName=usuario_payload["firstName"],
            lastName=usuario_payload["lastName"],
            email=usuario_payload["email"],
            password=usuario_payload["password"],
            phone=usuario_payload["phone"],
            userStatus=usuario_payload["userStatus"],
        )
        login_resp = login(username, "123456")
        resultado["usuario"] = {
            "usuario_enviado": usuario_payload,
            "login_retorno": login_resp,
        }
    except Exception as e:
        resultado["usuario"] = {"erro": str(e)}

    try:
        deletarCompraPet(order_id)
        deletarPet(pet_id)
        deletarUsuario(username)
        logout()
    except Exception:
        pass

    with open("script1.json", "w", encoding="utf-8") as arquivo:
        json.dump(resultado, arquivo, ensure_ascii=False, indent=2)

    print("Arquivo JSON salvo: script1.json")

if __name__ == "__main__":
    main()

