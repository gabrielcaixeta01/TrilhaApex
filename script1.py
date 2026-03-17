import requests
import json

BASE_URL = "https://petstore.swagger.io/v2"

# funcao pra auxiliar nas chamadas
def _request(method, path, **kwargs):
    return requests.request(method, f"{BASE_URL}{path}", **kwargs).json()

# funcao pra nao repetir o json do usuario
def _usuario_payload(id, username, firstName, lastName, email, password, phone, userStatus):
    return {"id": id, "username": username, "firstName": firstName, "lastName": lastName,
            "email": email, "password": password, "phone": phone, "userStatus": userStatus}


# funcoes de pet

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


# funcoes da loja

def inventarioPets():
    return _request("GET", "/store/inventory")

def criarCompraPet(id, petId, quantidade, dataEntrega, status, completo):
    return _request("POST", "/store/order",
                    json={"id": id, "petId": petId, "quantity": quantidade,"shipDate": dataEntrega, "status": status, "complete": completo})

def buscarCompraPet(id):
    return _request("GET", f"/store/order/{id}")

def deletarCompraPet(id):
    return _request("DELETE", f"/store/order/{id}")


# funcoes do usuario

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
        "ok": True,
        "pet": {},
        "loja": {},
        "usuario": {},
    }

    pet_id = 12345
    order_id = 54321
    username = "gabriel_teste_main"

    try:
        criarPet(
            id=pet_id,
            categoria={"id": 1, "name": "Cachorro"},
            nome="Rex",
            fotoUrl=["https://example.com/photo1.jpg"],
            tags=[{"id": 1, "name": "Brinquedo"}],
            status="available",
        )
        pet = buscarPet(pet_id)
        pets_status = petsPorStatus("available")
        resultado["pet"] = {
            "consulta_pet_ok": pet.get("id") == pet_id,
            "pet_id": pet.get("id"),
            "pet_nome": pet.get("name"),
            "total_por_status": len(pets_status),
        }
    except Exception as e:
        resultado["ok"] = False
        resultado["pet"] = {"erro": str(e)}

    try:
        inventario = inventarioPets()
        criarCompraPet(
            id=order_id,
            petId=pet_id,
            quantidade=1,
            dataEntrega="2026-03-16T10:00:00.000Z",
            status="placed",
            completo=False,
        )
        pedido = buscarCompraPet(order_id)
        resultado["loja"] = {
            "consulta_inventario_ok": len(inventario) >= 0,
            "total_status_inventario": len(inventario),
            "consulta_pedido_ok": pedido.get("id") == order_id,
            "pedido_id": pedido.get("id"),
            "pedido_status": pedido.get("status"),
        }
    except Exception as e:
        resultado["ok"] = False
        resultado["loja"] = {"erro": str(e)}

    try:
        criarUsuario(
            id=1001,
            username=username,
            firstName="Gabriel",
            lastName="Romero",
            email="gabriel@email.com",
            password="123456",
            phone="11999999999",
            userStatus=1,
        )
        user = buscarUsuario(username)
        login_resp = login(username, "123456")
        resultado["usuario"] = {
            "consulta_usuario_ok": user.get("username") == username,
            "username": user.get("username"),
            "email": user.get("email"),
            "login_ok": login_resp.get("message") is not None,
            "login_message": login_resp.get("message"),
        }
    except Exception as e:
        resultado["ok"] = False
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

