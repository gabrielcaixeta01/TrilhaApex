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

## Regras de negocio

- Um usuario pode ser cliente ou funcionario, mas, para isso, deve ter duas contas com emails diferentes.
- Cada cliente possui um unico endereco principal.
- O cliente pode logar e exigir um atendimento em diferentes lojas com a mesma conta.
- Um cliente pode ter nenhum ou varios pets.
- Um pet deve pertencer a um cliente responsavel.
- Um pet deve estar vinculado a uma categoria.
- Um pet pode possuir nenhuma ou varias tags.
- Um pet pode ter nenhum ou varios atendimentos ao longo do tempo.
- O pet exibe apenas o dono atual em seu cadastro.
- Um atendimento deve estar vinculado a um pet, a um cliente, a um funcionario e a uma loja.
- Um funcionario atende em apenas uma loja.
- Apenas um usuario com perfil "super_admin" pode criar, editar ou desativar lojas.
- O usuario com perfil "admin_loja" pode gerenciar operacoes da propria loja, mas nao cria novas lojas.
- Uma loja pode ter varios funcionarios e varios atendimentos.
- Uma categoria pode agrupar varios pets.
- Uma tag pode ser associada a varios pets.
- Um usuario deve ter identificacao unica por email.
- O sistema deve manter o historico dos atendimentos mesmo quando o pet ou o usuario forem desativados.
- Se uma categoria for deletada, todos os pets associados a ela tambem serao.
- Se uma loja for deletada, todos os funcionarios dela tambem serao.
- O funcionario pode nao estar associado a uma loja, como se fosse um periodo de alocacao dele.

## Gestao de lojas e perfis administrativos

Perfis de acesso sugeridos:

- super_admin: administra a rede toda e pode criar lojas.
- admin_loja: administra somente uma unidade especifica.
- funcionario: executa atendimentos e operacoes do dia a dia.
- cliente: solicita e acompanha atendimentos dos proprios pets.

Fluxo recomendado para criacao de lojas:

- Criar o primeiro usuario super_admin diretamente no banco, como bootstrap inicial.
- A partir desse primeiro acesso, novos usuarios administrativos devem ser criados pelo sistema.
- Toda nova loja deve ser criada por um super_admin.
- Apos criar a loja, um admin_loja pode ser vinculado a ela.

Regras de seguranca recomendadas:

- Endpoint de criacao de loja deve aceitar apenas perfil super_admin.
- Registrar auditoria de criacao e alteracao de loja (quem, quando e o que mudou).
- Preferir desativacao logica de loja em vez de exclusao fisica.

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

## Cardinalidades

### Relacoes entre entidades

| Relacao | Cardinalidade | Descricao |
|---------|---------------|-----------|
| Usuario (Cliente) → Pet | 1:N | Um cliente pode ter nenhum ou varios pets; um pet pertence a exatamente um cliente responsavel |
| Pet → Categoria | N:1 | Varios pets podem estar na mesma categoria; um pet esta vinculado a exatamente uma categoria |
| Pet ↔ Tag | N:M | Um pet pode ter nenhuma ou varias tags; uma tag pode estar associada a varios pets |
| Pet → Atendimento | 1:N | Um pet pode ter nenhum ou varios atendimentos; um atendimento vincula-se a exatamente um pet |
| Usuario (Cliente) → Atendimento | 1:N | Um cliente pode ter nenhum ou varios atendimentos; um atendimento vincula-se a exatamente um cliente |
| Usuario (Funcionario) → Atendimento | 1:N | Um funcionario pode realizar nenhum ou varios atendimentos; um atendimento vincula-se a exatamente um funcionario |
| Usuario (Funcionario) → Loja | N:1 (opcional) | Um funcionario atende em apenas uma loja (pode estar sem loja em periodo de alocacao); uma loja pode ter varios funcionarios |
| Loja → Atendimento | 1:N | Uma loja pode ter varios atendimentos; um atendimento vincula-se a exatamente uma loja |
| Usuario (Admin_Loja) → Loja | 1:1 | Um admin_loja gerencia exatamente uma loja; uma loja pode ter um admin_loja |

### Diagrama de relacionamento simplificado

```
Usuario
├── Cliente
│   ├── 1:N → Pet
│   │   ├── N:1 → Categoria
│   │   ├── N:M ← → Tag
│   │   └── 1:N → Atendimento
│   │       ├── 1:N → Funcionario
│   │       └── 1:N → Loja
│   │
│   └── 1:N → Atendimento
│
├── Funcionario
│   ├── N:1 → Loja (opcional)
│   └── 1:N → Atendimento
│
└── Admin_Loja
    └── 1:1 → Loja

Loja
├── 1:N → Atendimento
├── 1:N → Funcionario
└── 1:1 ← Admin_Loja
```

### Notas importantes sobre cardinalidades

- **Pet obrigatorio em Cliente**: Todo pet deve ter um cliente responsavel; a cardinalidade nao permite pets sem dono
- **Atendimento vinculado**: Um atendimento sempre requer: cliente, pet, funcionario e loja
- **Funcionario sem loja**: Um funcionario pode estar em periodo de alocacao sem estar vinculado a nenhuma loja (NULL permitido)
- **Categoria obrigatoria**: Um pet deve estar em exatamente uma categoria; se a categoria for deletada, seus pets tambem serao
- **Loja obrigatoria**: Uma loja deletada implica remocao de todos os seus funcionarios
- **Tags opcionais**: Um pet pode ter nenhuma ou varias tags; tags nao sao obrigatorias

