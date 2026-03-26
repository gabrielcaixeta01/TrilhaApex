# PostgreSQL em producao

Este projeto usa SQLite por padrao no ambiente local e PostgreSQL em producao via variavel `DATABASE_URL`.

## 1) Provisionar banco PostgreSQL

Voce pode usar um provedor gerenciado (Render, Railway, Neon, Supabase, RDS) ou um servidor proprio.

Requisitos minimos:
- Banco criado (ex: `petstore`)
- Usuario com permissao de leitura e escrita
- URL de conexao

Formato recomendado da URL:
- `postgresql+psycopg://usuario:senha@host:5432/petstore`

Tambem funciona URL no formato de provedor:
- `postgres://usuario:senha@host:5432/petstore`

## 2) Configurar variavel de ambiente

No deploy (servidor/plataforma), defina:
- `DATABASE_URL=<url_do_postgres>`

Localmente, se quiser simular producao, crie um arquivo `.env` com:

```env
DATABASE_URL=postgresql+psycopg://usuario:senha@localhost:5432/petstore
```

## 3) Rodar migrations no PostgreSQL

Com o ambiente virtual ativo:

```bash
alembic upgrade head
```

Isso aplica todas as migrations da pasta `alembic/versions` no banco apontado por `DATABASE_URL`.

## 4) Seed opcional

Para popular dados iniciais:

```bash
python scripts/seed_db.py
```

## 5) Subir a API

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

## 6) Checklist para producao

- Nao usar SQLite em producao
- Definir `DATABASE_URL` no ambiente de deploy
- Executar `alembic upgrade head` antes de iniciar a API
- Restringir acesso do banco por rede/IP
- Usar senha forte no usuario do banco
