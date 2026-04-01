## Entidades principais

- Usuario
- Pet
- Categoria
- Tag
- Loja
- Servico ou Atendimento

### Usuario

Representa qualquer pessoa com acesso ao sistema, seja cliente ou funcionario.

Tipos de perfil aceitos no sistema:

- cliente
- funcionario
- admin_loja
- super_admin

- id
- nome
- email
- senha_hash
- telefone
- tipo_perfil
- data_cadastro
- ativo

#### Cliente

Extensao de Usuario para quem contrata os servicos.

- cpf ou cnpj
- data_nascimento ou data_abertura, conforme o tipo de cliente
- endereco

#### Funcionario

Extensao de Usuario para quem realiza os atendimentos.

- cpf
- cargo
- data_inicio
- salario ou faixa_salarial, se fizer sentido no negocio
- loja_id (pode ser nulo em periodo de alocacao)

#### Admin de Loja

Extensao de Usuario para perfil administrativo de uma unidade especifica.

- cpf
- cargo = admin_loja
- data_inicio
- loja_id (obrigatorio)

#### Super Admin

Extensao de Usuario para perfil administrativo de rede.

- cpf
- cargo = super_admin
- data_inicio
- escopo = rede
- criado_via_bootstrap (indica se foi usuario inicial criado direto no banco)

### Pet

Representa o animal cadastrado no sistema.

- id
- nome
- especie
- raca
- sexo
- data_nascimento
- porte
- peso
- observacoes_saude
- categoria_id
- usuario_id
- ativo

O pet deve mostrar apenas o dono atual no cadastro.

### Categoria

Classifica o pet por tipo ou grupo de atendimento.

- id
- nome
- descricao

### Tag

Usada para marcar caracteristicas importantes do pet.

- id
- nome
- descricao

Exemplos:

- idoso
- agressivo
- alergico
- precisa_sedacao
- primeiro_atendimento

Por enquanto, as tags servem apenas como informacao complementar e nao alteram regras de negocio.

### Loja

Representa uma unidade fisica da franquia.

- id
- nome
- cnpj
- telefone
- email
- cep
- endereco
- cidade
- estado
- ativo

### Servico / Atendimento

Representa o registro de um atendimento realizado na loja.

- id
- tipo_servico
- descricao
- data_hora
- status
- valor
- desconto
- forma_pagamento
- observacoes
- loja_id
- pet_id
- cliente_id
- funcionario_id

O atendimento nao tera etapas internas; apenas o status do processo sera acompanhado.