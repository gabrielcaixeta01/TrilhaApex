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