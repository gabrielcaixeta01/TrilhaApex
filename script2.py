import requests
import json

def _request(method, path, **kwargs):
    return requests.request(method, f"https://petstore.swagger.io/v2{path}", **kwargs).json()


class Category:
    def __init__(self, category_id, name):
        self.category_id = category_id
        self.name = name

    def to_dict(self):
        return {"id": self.category_id, "name": self.name}


class Tag:
    def __init__(self, tag_id, name):
        self.tag_id = tag_id
        self.name = name

    def to_dict(self):
        return {"id": self.tag_id, "name": self.name}


class Pet:
    def __init__(self, category, pet_id, name, status):
        self.pet_id = pet_id
        self.name = name
        self.status = status
        self.category = category
        self.photo_urls = []
        self.tags = []

    def add_photo_url(self, photo_url):
        self.photo_urls.append(photo_url)

    def add_tag(self, tag):
        self.tags.append(tag)

    def to_dict(self):
        return {
            "id": self.pet_id,
            "category": self.category.to_dict(),
            "name": self.name,
            "photoUrls": self.photo_urls,
            "tags": [t.to_dict() for t in self.tags],
            "status": self.status,
        }

    def criar(self):
        return _request("POST", "/pet", json=self.to_dict())

    def atualizar(self):
        return _request("PUT", "/pet", json=self.to_dict())

    def upload_imagem(self, metadata, file_path):
        with open(file_path, "rb") as f:
            return _request("POST", f"/pet/{self.pet_id}/uploadImage",
                            files={"file": f}, data={"additionalMetadata": metadata})

    def buscar(pet_id):
        return _request("GET", f"/pet/{pet_id}")

    def deletar(pet_id):
        return _request("DELETE", f"/pet/{pet_id}")

    def por_status(status):
        return _request("GET", "/pet/findByStatus", params={"status": status})


class Order:
    def __init__(self, order_id, pet_id, quantity, ship_date, status, complete):
        self.order_id = order_id
        self.pet_id = pet_id
        self.quantity = quantity
        self.ship_date = ship_date
        self.status = status
        self.complete = complete

    def to_dict(self):
        return {
            "id": self.order_id,
            "petId": self.pet_id,
            "quantity": self.quantity,
            "shipDate": self.ship_date,
            "status": self.status,
            "complete": self.complete,
        }

    def criar(self):
        return _request("POST", "/store/order", json=self.to_dict())

    def buscar(order_id):
        return _request("GET", f"/store/order/{order_id}")

    def deletar(order_id):
        return _request("DELETE", f"/store/order/{order_id}")

    def inventario():
        return _request("GET", "/store/inventory")


class User:
    def __init__(self, user_id, username, first_name, last_name, email, password, phone, user_status):
        self.user_id = user_id
        self.username = username
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password
        self.phone = phone
        self.user_status = user_status

    def to_dict(self):
        return {
            "id": self.user_id,
            "username": self.username,
            "firstName": self.first_name,
            "lastName": self.last_name,
            "email": self.email,
            "password": self.password,
            "phone": self.phone,
            "userStatus": self.user_status,
        }

    def criar(self):
        return _request("POST", "/user", json=self.to_dict())

    def atualizar(self, **dados):
        atual = User.buscar(self.username)
        atual.update(dados)
        atual["username"] = self.username
        return _request("PUT", f"/user/{self.username}", json=atual)

    def buscar(username):
        return _request("GET", f"/user/{username}")

    def deletar(username):
        return _request("DELETE", f"/user/{username}")

    def login(username, password):
        return _request("GET", "/user/login", params={"username": username, "password": password})

    def logout():
        return _request("GET", "/user/logout")

    def criar_lista(users):
        return _request("POST", "/user/createWithArray", json=[user.to_dict() for user in users])

    def criar_lista_desejo(users):
        return _request("POST", "/user/createWithList", json=[user.to_dict() for user in users])


def main():
    resultado = {
        "api_base": "https://petstore.swagger.io/v2",
        "ok": True,
        "pet": {},
        "loja": {},
        "usuario": {},
    }

    pet_id = 12345
    order_id = 54321
    username = "gabriel_teste_main"

    try:
        pet = Pet(
            category=Category(1, "Cachorro"),
            pet_id=pet_id,
            name="Rex",
            status="available",
        )
        pet.add_photo_url("https://example.com/photo1.jpg")
        pet.add_tag(Tag(1, "Brinquedo"))
        pet.criar()

        encontrado = Pet.buscar(pet_id)
        por_status = Pet.por_status("available")
        resultado["pet"] = {
            "consulta_pet_ok": encontrado.get("id") == pet_id,
            "pet_id": encontrado.get("id"),
            "pet_nome": encontrado.get("name"),
            "total_por_status": len(por_status),
        }
    except Exception as e:
        resultado["ok"] = False
        resultado["pet"] = {"erro": str(e)}

    try:
        inventario = Order.inventario()
        pedido = Order(order_id, pet_id, 1, "2026-03-16T10:00:00.000Z", "placed", False)
        pedido.criar()
        pedido_encontrado = Order.buscar(order_id)
        resultado["loja"] = {
            "consulta_inventario_ok": len(inventario) >= 0,
            "total_status_inventario": len(inventario),
            "consulta_pedido_ok": pedido_encontrado.get("id") == order_id,
            "pedido_id": pedido_encontrado.get("id"),
            "pedido_status": pedido_encontrado.get("status"),
        }
    except Exception as e:
        resultado["ok"] = False
        resultado["loja"] = {"erro": str(e)}

    try:
        usuario = User(1001, username, "Gabriel", "Romero", "gabriel@email.com", "123456", "11999999999", 1)
        usuario.criar()
        user_encontrado = User.buscar(username)
        login_resp = User.login(username, "123456")
        resultado["usuario"] = {
            "consulta_usuario_ok": user_encontrado.get("username") == username,
            "username": user_encontrado.get("username"),
            "email": user_encontrado.get("email"),
            "login_ok": login_resp.get("message") is not None,
            "login_message": login_resp.get("message"),
        }
    except Exception as e:
        resultado["ok"] = False
        resultado["usuario"] = {"erro": str(e)}

    try:
        Order.deletar(order_id)
        Pet.deletar(pet_id)
        User.deletar(username)
        User.logout()
    except Exception:
        pass

    with open("resultado_script2.json", "w", encoding="utf-8") as arquivo:
        json.dump(resultado, arquivo, ensure_ascii=False, indent=2)

    print("Arquivo JSON salvo: resultado_script2.json")

if __name__ == "__main__":
    main()







