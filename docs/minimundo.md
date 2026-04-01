# Petshop GC - Mini Mundo

## Visao geral

O sistema representa a operacao de uma rede de petshops focada em cuidados e atendimento a animais domesticos. O objetivo e registrar clientes, funcionarios, pets, atendimentos, servicos executados e o historico de relacionamento entre esses elementos.

O sistema deve permitir:

- cadastro e gestao de unidades da rede;
- cadastro de usuarios com perfis diferentes;
- cadastro de pets vinculados a seus donos;
- registro de servicos prestados em cada atendimento;
- consulta de historico dos atendimentos realizados.

## Contexto do negocio

- A Petshop GC e uma franquia nacional, atuando somente no Brasil.
- Existem diversas unidades fisicas espalhadas pelo pais, aproximadamente 100 lojas.
- A empresa atende animais domesticos de pequeno e medio porte, como caes, gatos, aves, coelhos e roedores de pequeno porte.
- A Petshop GC nao realiza venda de animais; o foco e apenas em cuidados, manutencao e atendimento.
- O cliente pode agendar atendimentos pelo site ou aplicativo.
- Quando o atendimento ocorrer presencialmente, o funcionario responsavel deve registrar o servico no sistema para manter o historico.

## Objetivos do sistema

- Controlar quais servicos foram feitos, em qual unidade e por qual funcionario.
- Garantir que cada pet tenha um responsavel cadastrado.
- Manter o historico de atendimentos por pet, cliente, funcionario e unidade.
- Organizar os tipos de servico oferecidos pela rede.
- Permitir evolucao futura do modelo sem quebrar a estrutura do banco.

## Entidades principais

- Usuario
- Pet
- Categoria
- Tag
- Loja
- Servico ou Atendimento

## Entidades e atributos

### Usuario

Representa qualquer pessoa com acesso ao sistema, seja cliente ou funcionario.

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
- loja_id

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

## Regras de negocio

- Um usuario pode ser cliente ou funcionario, dependendo do perfil.
- Cada cliente possui um unico endereco principal.
- Um cliente pode ter nenhum ou varios pets.
- Um pet deve pertencer a um cliente responsavel.
- Um pet deve estar vinculado a uma categoria.
- Um pet pode possuir nenhuma ou varias tags.
- Um pet pode ter nenhum ou varios atendimentos ao longo do tempo.
- O pet exibe apenas o dono atual em seu cadastro.
- Um atendimento deve estar vinculado a um pet, a um cliente, a um funcionario e a uma loja.
- Um funcionario atende em apenas uma loja.
- Uma loja pode ter varios funcionarios e varios atendimentos.
- Uma categoria pode agrupar varios pets.
- Uma tag pode ser associada a varios pets.
- Um usuario deve ter identificacao unica por email.
- O sistema deve manter o historico dos atendimentos mesmo quando o pet ou o usuario forem desativados.

## Tipos de serviço prestados

Essas acoes podem virar tipos de servico no futuro:

- banho
- tosa
- cuidados/higiene de unha, ouvidos e/ou olhos
- consulta veterinaria
- vacinacao
- avaliacao de comportamento
- hospedagem temporaria
- adestramento basico

