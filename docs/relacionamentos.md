# Relacionamentos do banco

## Usuário

- Um usuário pode ter nenhum ou N pets.
- Um usuário pode ter nenhum ou N orders.
- Um usuário deve ter um nome de usuário e um cargo

## Pet

- Um pet deve pertencer a uma categoria.
- Um pet pode pertencer a nenhum ou um usuário.
- Um pet pode ter nenhuma ou N tags.
- Um pet pode estar em nenhum ou um pedido.
- Um pet deve ter um nome e um status ao ser criado.

## Categoria

- Uma categoria pode ter nenhum ou N pets.
- Uma categoria deve ter um nome ao ser criada.

## Tag

- Uma tag pode estar associada a nenhum ou N pets.
- Uma tag deve ter um nome ao ser criada.

## Order

- Um pedido deve estar associado a um pet.
- Um pedido deve estar associado a um usuário (owner).
- Um usuário pode ter nenhum ou N orders.
- Um pet pode aparecer em nenhum ou N orders.