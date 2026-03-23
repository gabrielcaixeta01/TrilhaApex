"""
GUIA RÁPIDO - Como testar a API

Este arquivo mostra exemplos de requisições para testar a API
"""

# ============ INSTALAÇÃO E EXECUÇÃO ============

# 1. Instalar dependências
# pip install -r requirements.txt

# 2. Executar servidor
# uvicorn app.main:app --reload

# 3. Acessar documentação interativa
# http://localhost:8000/docs

# ============ TESTES COM CURL ============

# Criar um pet
curl -X POST "http://localhost:8000/pet" \
  -H "Content-Type: application/json" \
  -d '{
    "pet_id": 1,
    "name": "Fluffy",
    "status": "available",
    "photoUrls": ["http://example.com/photo.jpg"]
  }'

# Buscar um pet
curl -X GET "http://localhost:8000/pet/1"

# Listar pets por status
curl -X GET "http://localhost:8000/pet/findByStatus?status=available"

# Atualizar um pet
curl -X PUT "http://localhost:8000/pet/1" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "name=Fluffy%20Updated&status=available"

# Deletar um pet
curl -X DELETE "http://localhost:8000/pet/1"

# ============ TESTES COM PYTHON ============

import requests

BASE_URL = "http://localhost:8000"

# Criar pet
response = requests.post(
    f"{BASE_URL}/pet",
    json={
        "pet_id": 1,
        "name": "Rex",
        "status": "available",
        "photoUrls": ["url1", "url2"]
    }
)
print(response.json())

# Buscar pet
response = requests.get(f"{BASE_URL}/pet/1")
print(response.json())

# Listar por status
response = requests.get(f"{BASE_URL}/pet/findByStatus?status=available")
print(response.json())

# Atualizar
response = requests.put(
    f"{BASE_URL}/pet/1",
    params={
        "name": "Rex Updated",
        "status": "pending"
    }
)
print(response.json())

# Deletar
response = requests.delete(f"{BASE_URL}/pet/1")
print(response.status_code)

# ============ CRIAR USUÁRIO ============

# POST /user
response = requests.post(
    f"{BASE_URL}/user",
    json={
        "id": 1,
        "username": "gabriel",
        "password": "senha123",
        "firstName": "Gabriel",
        "lastName": "Romero",
        "email": "gabriel@example.com",
        "phone": "123456789",
        "userStatus": 1
    }
)
print(response.json())

# Buscar usuário
response = requests.get(f"{BASE_URL}/user/gabriel")
print(response.json())

# Login
response = requests.post(
    f"{BASE_URL}/user/login",
    params={
        "username": "gabriel",
        "password": "senha123"
    }
)
print(response.json())

# ============ CRIAR PEDIDO ============

from datetime import datetime

# POST /store/order
response = requests.post(
    f"{BASE_URL}/store/order",
    json={
        "order_id": 1,
        "petId": 1,
        "quantity": 2,
        "shipDate": datetime.now().isoformat(),
        "status": "placed",
        "complete": False
    }
)
print(response.json())

# Buscar pedido
response = requests.get(f"{BASE_URL}/store/order/1")
print(response.json())

# Listar inventário
response = requests.get(f"{BASE_URL}/store/inventory")
print(response.json())

# ============ ACESSAR SWAGGER ============

# Abrir no navegador:
# http://localhost:8000/docs
# ou
# http://localhost:8000/redoc

# Lá você pode:
# ✅ Ver todos os endpoints
# ✅ Ver documentação de cada um
# ✅ Testar os endpoints interativamente
# ✅ Ver exemplos de request/response
