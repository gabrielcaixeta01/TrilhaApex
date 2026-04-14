# Guia de Integracao Frontend - API Petstore Apex

## 1. Visao Geral
Este documento descreve o contrato atual da API para consumo no frontend.

- Stack backend: FastAPI + SQLAlchemy
- Formato de resposta: JSON
- Ambiente local esperado:
  - API: `http://127.0.0.1:8000`
  - Swagger: `http://127.0.0.1:8000/docs`
- CORS liberado para:
  - `http://localhost:5173`
  - `http://127.0.0.1:5173`

## 2. Ponto importante (entrada de dados)
Atualmente, os endpoints de criacao e atualizacao recebem dados por **query params** (na URL), e nao por body JSON.

Exemplo (POST user):

```http
POST /user?name=Gabriel&email=gabriel@email.com&password=12345678&role=cliente
```

No frontend (axios), use `params`:

```ts
await api.post('/user', null, {
  params: {
    name: 'Gabriel',
    email: 'gabriel@email.com',
    password: '12345678',
    role: 'cliente',
  },
});
```

## 3. Convencao de respostas e erros

### 3.1 Sucesso
- `POST`: `201` + objeto criado
- `GET` lista: `200` + array de objetos
- `GET` por id: `200` + objeto
- `PUT`: `200` + objeto atualizado
- `DELETE`: `200` + `{ "message": "..." }`

### 3.2 Erros
- `400`: regra de negocio (ex.: duplicidade, campo obrigatorio de regra)
- `404`: recurso nao encontrado
- `422`: validacao de parametros do FastAPI (tipo invalido, parametro obrigatorio ausente)

Formato comum de erro:

```json
{
  "detail": "Mensagem de erro"
}
```

Formato de erro de validacao (422):

```json
{
  "detail": [
    {
      "loc": ["query", "name"],
      "msg": "Field required",
      "type": "missing"
    }
  ]
}
```

## 4. Contrato por recurso

## 4.1 Users
Prefixo: `/user`

### Endpoints
- `POST /user`
  - Query params:
    - `name` (string, obrigatorio)
    - `password` (string, obrigatorio, minimo 8)
    - `email` (string, obrigatorio)
    - `phone` (string, opcional)
    - `user_active` (boolean, opcional, default `true`)
    - `role` (string, opcional, default `cliente`)
  - Retorno: `201` + `User`

- `GET /user/users`
  - Retorno: `200` + `User[]`

- `GET /user/{user_id}`
  - Retorno: `200` + `User`

- `PUT /user/{user_id}`
  - Query params (todos opcionais):
    - `name`, `email`, `password`, `phone`, `role`, `user_active`
  - Retorno: `200` + `User`

- `DELETE /user/{user_id}`
  - Retorno: `200` + `{ "message": "Usuario deletado com sucesso" }`

### Shape de resposta `User`

```json
{
  "id": 1,
  "name": "Gabriel",
  "email": "gabriel@email.com",
  "password_hash": "12345678",
  "phone": "11999999999",
  "role": "cliente",
  "cpf": null,
  "cnpj": null,
  "active": true,
  "is_superuser": false,
  "created_at": "2026-04-14T19:30:00"
}
```

Observacao: atualmente `password_hash` esta sendo retornado no response.

## 4.2 Stores
Prefixo: `/store`

### Endpoints
- `POST /store`
  - Query params obrigatorios:
    - `name`, `cnpj`, `phone`, `email`, `cep`, `city`, `state`, `address`, `neighborhood`, `number`
  - Query params opcionais:
    - `active` (boolean, default `true`)
  - Retorno: `201` + `Store`

- `GET /store/stores`
  - Retorno: `200` + `Store[]`

- `GET /store/{store_id}`
  - Retorno: `200` + `Store`

- `PUT /store/{store_id}`
  - Query params: todos opcionais do recurso
  - Retorno: `200` + `Store`

- `DELETE /store/{store_id}`
  - Retorno: `200` + `{ "message": "Loja deletada com sucesso" }`

### Shape de resposta `Store`

```json
{
  "id": 1,
  "name": "Loja Centro",
  "cnpj": "12.345.678/0001-90",
  "phone": "1133334444",
  "email": "contato@loja.com",
  "cep": "01001-000",
  "city": "Sao Paulo",
  "state": "SP",
  "address": "Rua A",
  "neighborhood": "Centro",
  "number": "100",
  "active": true,
  "created_at": "2026-04-14T19:30:00"
}
```

## 4.3 Pets
Prefixo: `/pet`

### Endpoints
- `POST /pet`
  - Query params:
    - obrigatorio: `name`
    - opcionais no router: `breed`, `sex`, `size`, `weight`, `health_notes`, `category_id`, `owner_id`
  - Regra de negocio (service): `category_id` e `owner_id` sao obrigatorios
  - Retorno: `201` + `Pet`

- `GET /pet/pets`
  - Retorno: `200` + `Pet[]`

- `GET /pet/{pet_id}`
  - Retorno: `200` + `Pet`

- `PUT /pet/{pet_id}`
  - Query params todos opcionais
  - Retorno: `200` + `Pet`

- `DELETE /pet/{pet_id}`
  - Retorno: `200` + `{ "message": "Pet deletado com sucesso" }`

### Shape de resposta `Pet`

```json
{
  "id": 1,
  "name": "Rex",
  "breed": "SRD",
  "sex": "M",
  "size": "medio",
  "weight": 12.5,
  "health_notes": "Vacinado",
  "category_id": 1,
  "owner_id": 5
}
```

## 4.4 Services
Prefixo: `/service`

### Endpoints
- `POST /service`
  - Query params:
    - `name` (obrigatorio)
    - `description` (opcional)
    - `price` (obrigatorio na regra de negocio)
  - Retorno: `201` + `Service`

- `GET /service/services`
  - Retorno: `200` + `Service[]`

- `GET /service/{id}`
  - Retorno: `200` + `Service`

- `PUT /service/{id}`
  - Query params opcionais: `name`, `description`, `price`
  - Retorno: `200` + `Service`

- `DELETE /service/{id}`
  - Retorno: `200` + `{ "message": "Servico deletado com sucesso" }`

### Shape de resposta `Service`

```json
{
  "id": 1,
  "name": "Banho",
  "description": "Banho completo",
  "price": 79.9
}
```

## 4.5 Categories
Prefixo: `/category`

### Endpoints
- `POST /category`
  - Query params:
    - `name` (obrigatorio)
    - `description` (opcional)
  - Retorno: `201` + `Category`

- `GET /category/categories`
  - Retorno: `200` + `Category[]`

- `GET /category/{id}`
  - Retorno: `200` + `Category`

- `PUT /category/{id}`
  - Query params:
    - `name` (obrigatorio)
    - `description` (opcional)
  - Retorno: `200` + `Category`

- `DELETE /category/{id}`
  - Retorno: `200` + `{ "message": "Categoria deletada com sucesso" }`

### Shape de resposta `Category`

```json
{
  "id": 1,
  "name": "Canino",
  "description": "Pets caninos"
}
```

## 4.6 Tags
Prefixo: `/tag`

### Endpoints
- `POST /tag`
  - Query params:
    - `name` (obrigatorio)
  - Retorno: `201` + `Tag`

- `GET /tag/tags`
  - Retorno: `200` + `Tag[]`

- `GET /tag/{id}`
  - Retorno: `200` + `Tag`

- `PUT /tag/{id}`
  - Query params:
    - `name` (obrigatorio)
    - `description` (opcional)
  - Retorno: `200` + `Tag`

- `DELETE /tag/{id}`
  - Retorno: `200` + `{ "message": "Tag deletada com sucesso" }`

### Shape de resposta `Tag`

```json
{
  "id": 1,
  "name": "Urgente",
  "description": "Atendimento prioritario"
}
```

## 4.7 Appointments
Prefixo: `/appointment`

### Endpoints
- `POST /appointment`
  - Query params:
    - `service_at` (datetime, opcional)
    - `status` (string, opcional, default `agendado`)
    - `store_id` (int, obrigatorio)
    - `client_id` (int, obrigatorio)
    - `worker_id` (int, obrigatorio)
    - `payment_type` (string, obrigatorio na regra de negocio)
    - `observations` (string, opcional)
    - `online` (boolean, opcional, default `false`)
  - Retorno: `201` + `Appointment`

- `GET /appointment/appointments`
  - Retorno: `200` + `Appointment[]`

- `GET /appointment/{id}`
  - Retorno: `200` + `Appointment`

- `PUT /appointment/{id}`
  - Query params: todos opcionais
  - Retorno: `200` + `Appointment`

- `DELETE /appointment/{id}`
  - Retorno: `200` + `{ "message": "Atendimento deletado com sucesso" }`

### Shape de resposta `Appointment`

```json
{
  "id": 1,
  "value_final": 120,
  "service_at": "2026-04-14T20:00:00",
  "payment_type": "pix",
  "status": "agendado",
  "online": false,
  "observations": "Cliente prefere horario da tarde",
  "store_id": 1,
  "client_id": 5,
  "worker_id": 7
}
```

## 5. Tipos recomendados no frontend (TypeScript)

```ts
export type ApiError = {
  detail: string | Array<{
    loc: (string | number)[];
    msg: string;
    type: string;
  }>;
};

export interface User {
  id: number;
  name: string;
  email: string;
  password_hash: string;
  phone: string;
  role: string;
  cpf: string | null;
  cnpj: string | null;
  active: boolean;
  is_superuser: boolean;
  created_at: string;
}

export interface Store {
  id: number;
  name: string;
  cnpj: string;
  phone: string;
  email: string;
  cep: string;
  city: string;
  state: string;
  address: string;
  neighborhood: string;
  number: string;
  active: boolean;
  created_at: string;
}

export interface Pet {
  id: number;
  name: string;
  breed: string | null;
  sex: string | null;
  size: string | null;
  weight: number | null;
  health_notes: string | null;
  category_id: number;
  owner_id: number;
}

export interface Service {
  id: number;
  name: string;
  description: string | null;
  price: number;
}

export interface Category {
  id: number;
  name: string;
  description: string | null;
}

export interface Tag {
  id: number;
  name: string;
  description: string | null;
}

export interface Appointment {
  id: number;
  value_final: number;
  service_at: string;
  payment_type: string;
  status: string;
  online: boolean;
  observations: string | null;
  store_id: number;
  client_id: number;
  worker_id: number;
}
```

## 6. Exemplo de client HTTP (axios)

```ts
import axios from 'axios';

export const api = axios.create({
  baseURL: 'http://127.0.0.1:8000',
});

export async function listUsers() {
  const { data } = await api.get('/user/users');
  return data;
}

export async function createUser(payload: {
  name: string;
  email: string;
  password: string;
  phone?: string;
  role?: string;
}) {
  const { data } = await api.post('/user', null, { params: payload });
  return data;
}

export async function updateUser(userId: number, payload: Partial<{
  name: string;
  email: string;
  password: string;
  phone: string;
  role: string;
  user_active: boolean;
}>) {
  const { data } = await api.put(`/user/${userId}`, null, { params: payload });
  return data;
}
```

## 7. Checklist de integracao no frontend

- Configurar `baseURL` para `http://127.0.0.1:8000`.
- Enviar dados de POST/PUT via `params`.
- Tratar erros `400`, `404`, `422` lendo `error.response.data.detail`.
- Tipar campos de data/hora como `string` (ISO).
- Tipar campos decimais como `number` no front.
- Usar `/docs` para validar rapidamente qualquer contrato durante desenvolvimento.

## 8. Fontes do contrato (backend)

- `app/main.py`
- `app/routers/user_crud.py`
- `app/routers/store_crud.py`
- `app/routers/pet_crud.py`
- `app/routers/service_crud.py`
- `app/routers/category_crud.py`
- `app/routers/tag_crud.py`
- `app/routers/appointment_crud.py`
- `app/schemas/schemas.py`
- `app/services/user_service.py`
- `app/services/store_service.py`
- `app/services/pet_service.py`
- `app/services/service_service.py`
- `app/services/category_service.py`
- `app/services/tag_service.py`
- `app/services/appointment_service.py`
