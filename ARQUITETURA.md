# Arquitetura do Projeto - Petstore da Apex

## 📋 Visão Geral

Projeto de API RESTful construído com **FastAPI** e arquitetura em camadas, sem dependências externas desnecessárias.

### Características
✅ **Sem Pydantic** - Type hints nativos do Python  
✅ **Sem SQLAlchemy** - Pronto para integração futura com banco de dados  
✅ **Documentação automática** - Swagger gerado pelo FastAPI  
✅ **Arquitetura em camadas** - Separação clara de responsabilidades  

---

## 🏗️ Estrutura do Projeto

```
app/
├── main.py              # Aplicação FastAPI principal
├── database.py          # Configuração de banco (futuro)
├── models.py            # Modelos SQLAlchemy (futuro)
├── routers/             # Endpoints organizados por recurso
│   ├── pet_crud.py      # Operações de Pets
│   ├── order_crud.py    # Operações de Pedidos
│   └── user_crud.py     # Operações de Usuários
├── services/            # Lógica de negócio
│   ├── pet_service.py
│   ├── order_service.py
│   └── user_service.py
└── schemas/
    └── models.py        # Modelos de dados com type hints

scripts/
├── script1.py           # Script auxiliar
├── script2.py           # Integração com Pet, Order, User
└── *.json              # Arquivos de dados
```

---

## 🔄 Fluxo de Dados

```
Cliente HTTP
    ↓
FastAPI Application (main.py)
    ↓
Router (routers/) - Define endpoints
    ↓
Service (services/) - Lógica de negócio
    ↓
Scripts (scripts/script2.py) - Manipulação de dados
    ↓
Modelos (schemas/models.py) - Estruturas de dados
```

---

## 📦 Type Hints Nativos

Ao invés de Pydantic, usamos type hints nativos do Python que o FastAPI entende:

### Exemplo: Criar um Pet

```python
@router.post("/pet", status_code=201)
def criar_pet(
    pet_id: int,
    name: str,
    status: Literal["available", "pending", "sold"] = "available",
    photoUrls: list[str] | None = None
) -> dict:
    """Criar um novo pet"""
    return create_pet(
        pet_id=pet_id,
        name=name,
        status=status,
        photoUrls=photoUrls
    )
```

**O que FastAPI faz automaticamente:**
- ✅ Gera documentação Swagger
- ✅ Valida tipos de entrada
- ✅ Converte JSON para Python
- ✅ Serializa resposta para JSON

---

## 🎯 Camadas da Aplicação

### 1️⃣ Router (app/routers/)
**Responsabilidade:** Definir endpoints HTTP

```python
# Exemplo: pet_crud.py
@router.post("", status_code=201)
def criar_pet(pet_id: int, name: str, ...) -> dict:
    return create_pet(pet_id, name, ...)
```

- Define a rota e método HTTP
- Especifica parâmetros e tipos
- Documenta via docstring
- Chama service

### 2️⃣ Service (app/services/)
**Responsabilidade:** Lógica de negócio

```python
# Exemplo: pet_service.py
def create_pet(pet_id: int, name: str, ...) -> dict:
    """Lógica para criar pet"""
    # Validações
    # Chamadas a scripts
    # Tratamento de erros
    # Retorna resultado
    return result
```

- Valida dados
- Implementa lógica
- Trata erros
- Retorna resultado

### 3️⃣ Modelos (app/schemas/models.py)
**Responsabilidade:** Estruturas de dados

```python
class Pet:
    id: int
    name: str
    photoUrls: list[str]
    status: str
    category: Category | None
    tags: list[Tag]
```

- Define estrutura de dados
- Type hints para documentação

### 4️⃣ Scripts (scripts/script2.py)
**Responsabilidade:** Manipulação de dados

- Criação e atualização de registros
- Persistência de dados
- Consultas

---

## 🚀 Endpoints Disponíveis

### Pets
```
POST   /pet                    Criar pet
GET    /pet/{pet_id}          Buscar pet
GET    /pet/findByStatus      Listar por status
PUT    /pet/{pet_id}          Atualizar pet
DELETE /pet/{pet_id}          Deletar pet
```

### Pedidos
```
POST   /store/order            Criar pedido
GET    /store/order/{id}       Buscar pedido
DELETE /store/order/{id}       Deletar pedido
GET    /store/inventory        Listar inventário
```

### Usuários
```
POST   /user                   Criar usuário
GET    /user/{username}        Buscar usuário
PUT    /user/{username}        Atualizar usuário
DELETE /user/{username}        Deletar usuário
POST   /user/login             Login
POST   /user/logout            Logout
POST   /user/createWithList    Criar múltiplos
```

---

## 💻 Executar a Aplicação

```bash
# Instalar dependências
pip install -r requirements.txt

# Executar servidor
uvicorn app.main:app --reload

# Acessar documentação
http://localhost:8000/docs
```

---

## 🔮 Futuro

Quando necessário banco de dados:

1. **Descomentar database.py** - Configuração SQLAlchemy
2. **Descomentar models.py** - Modelos ORM
3. **Atualizar services** - Para usar DB em vez de scripts
4. **Adicionar migrações** - Alembic setup

---

## 📝 Notas

- **Type hints** são entendidos nativamente pelo FastAPI
- **Swagger** é gerado automaticamente baseado nos types
- **Validação** é feita pelo FastAPI automaticamente
- **Serialização** JSON é automática

---

**Desenvolvido conforme os requisitos do projeto:**
✅ Endpoints documentados com Swagger  
✅ Arquitetura em camadas  
✅ Sem dependências desnecessárias
