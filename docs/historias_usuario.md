# Histórias de Usuário - Petshop GC

## 1. Autenticação e Autorização

### 1.1 - Registrar novo usuario cliente
**Como** um visitante não autenticado
**Eu quero** me registrar no sistema como cliente
**Para que** eu possa agendar atendimentos para meus pets

**Critérios de Aceitação:**
- [ ] Deve permitir registrar com nome, email, senha e telefone
- [ ] Email deve ser único no sistema
- [ ] Senha deve ter mínimo 8 caracteres
- [ ] Após registro, devo ser redirecionado para login
- [ ] Deve validar format de email

### 1.2 - Registrar novo usuario funcionario
**Como** um super_admin
**Eu quero** registrar um novo funcionário no sistema
**Para que** ele possa realizar atendimentos em uma loja

**Critérios de Aceitação:**
- [ ] Apenas super_admin pode criar funcionários
- [ ] Deve solicitar: nome, email, senha, CPF, cargo, data_início, loja_id (opcional)
- [ ] Funcionário criado com perfil "funcionario"
- [ ] Email deve ser único no sistema
- [ ] Funcionário recebe email de confirmação com credenciais temporárias

### 1.3 - Fazer login no sistema
**Como** um usuário registrado
**Eu quero** fazer login com email e senha
**Para que** eu acesse minhas funcionalidades no sistema

**Critérios de Aceitação:**
- [ ] Deve validar email e senha
- [ ] Deve retornar token JWT válido
- [ ] Token deve conter perfil do usuário
- [ ] Mensagem de erro clara para credenciais inválidas
- [ ] Limite de tentativas falhadas para prevenir força bruta

### 1.4 - Atualizar senha
**Como** um usuário logado
**Eu quero** alterar minha senha
**Para que** eu mantenha minha conta segura

**Critérios de Aceitação:**
- [ ] Deve solicitar senha atual e nova senha
- [ ] Deve validar força da nova senha
- [ ] Nova senha não pode ser igual à anterior
- [ ] Sessão ativa não deve ser interrompida

---

## 2. Gestão de Usuários

### 2.1 - Visualizar perfil pessoal
**Como** um usuário logado
**Eu quero** visualizar meus dados de perfil
**Para que** eu verifique se minhas informações estão corretas

**Critérios de Aceitação:**
- [ ] Deve exibir nome, email, telefone e tipo de perfil
- [ ] Deve mostrar data de cadastro
- [ ] Dados não devem ser editáveis nesta tela
- [ ] Deve ter link para "Editar Perfil"

### 2.2 - Editar perfil pessoal
**Como** um usuário logado
**Eu quero** atualizar meus dados de perfil
**Para que** mantenha meus dados pessoais atualizados

**Critérios de Aceitação:**
- [ ] Deve permitir editar nome e telefone
- [ ] Email não deve ser editável
- [ ] Deve validar telefone em formato brasileiro
- [ ] Deve exigir confirmação antes de salvar
- [ ] Deve exibir mensagem de sucesso após atualização

### 2.3 - Listar usuarios por perfil (admin)
**Como** um super_admin ou admin_loja
**Eu quero** visualizar lista de usuários com seus respectivos perfis
**Para que** eu gerencie os usuários do sistema

**Critérios de Aceitação:**
- [ ] Super_admin deve ver todos os usuários do sistema
- [ ] Admin_loja deve ver apenas usuários da sua loja
- [ ] Deve exibir: nome, email, perfil, data_cadastro, status (ativo/inativo)
- [ ] Deve permitir filtrar por perfil
- [ ] Deve permitir ordenar por nome, email ou data de cadastro

### 2.4 - Desativar usuario
**Como** um super_admin
**Eu quero** desativar um usuário do sistema
**Para que** revogar seu acesso sem perder histórico

**Critérios de Aceitação:**
- [ ] Apenas super_admin pode desativar usuários
- [ ] Usuário desativado não pode fazer login
- [ ] Histórico de atendimentos do usuário permanece no sistema
- [ ] Desativação deve ser lógica (não deletar registro)
- [ ] Deve registrar quem desativou e quando

---

## 3. Gestão de Lojas

### 3.1 - Criar nova loja
**Como** um super_admin
**Eu quero** criar uma nova unidade da Petshop GC
**Para que** expandir a rede de atendimento

**Critérios de Aceitação:**
- [ ] Apenas super_admin pode criar lojas
- [ ] Deve solicitar: nome, endereço, telefone, email e cep
- [ ] Loja deve ter identificador único
- [ ] Deve registrar data de criação e quem criou
- [ ] Após criar, deve permitir vincular admin_loja

### 3.2 - Editar dados da loja
**Como** um super_admin ou admin_loja
**Eu quero** atualizar informações de uma loja
**Para que** manter dados atualizados

**Critérios de Aceitação:**
- [ ] Super_admin pode editar qualquer loja
- [ ] Admin_loja pode editar apenas sua própria loja
- [ ] Deve permitir editar: nome, telefone, email, endereço
- [ ] Deve registrar alterações para auditoria
- [ ] Deve validar novos dados antes de salvar

### 3.3 - Listar todas as lojas
**Como** um super_admin
**Eu quero** visualizar todas as unidades de petshops da rede
**Para que** gerenciar a operação da rede

**Critérios de Aceitação:**
- [ ] Deve exibir: nome, endereço, telefone, email, data_criação
- [ ] Deve exibir quantidade de funcionários por loja
- [ ] Deve permitir filtrar por status (ativa/inativa)
- [ ] Deve permitir ordenar por nome ou data
- [ ] Deve ter link para editar e visualizar detalhes

### 3.4 - Vincular admin_loja a uma loja
**Como** um super_admin
**Eu quero** designar um admin_loja para gerenciar uma unidade
**Para que** cada loja tenha um responsável administrativo

**Critérios de Aceitação:**
- [ ] Apenas super_admin pode fazer essa ação
- [ ] Deve validar se o usuário tem perfil admin_loja
- [ ] Cada loja deve ter apenas um admin_loja ativo
- [ ] Se desvincular, novo admin_loja pode ser atribuído
- [ ] Deve registrar mudanças para auditoria

---

## 4. Gestão de Pets

### 4.1 - Cadastrar novo pet
**Como** um cliente
**Eu quero** registrar um novo pet em minha conta
**Para que** agendar atendimentos para ele

**Critérios de Aceitação:**
- [ ] Deve solicitar: nome, espécie, raça, sexo, data_nascimento, porte, peso
- [ ] Deve permitir selecionar categoria pré-existente
- [ ] Deve permitir adicionar tags
- [ ] Peso e data de nascimento devem ser validados
- [ ] Após salvar, deve exibir confiração com dados do pet

### 4.2 - Editar dados do pet
**Como** um cliente
**Eu quero** atualizar informações do meu pet
**Para que** manter dados sempre corretos

**Critérios de Aceitação:**
- [ ] Apenas o dono do pet pode editar
- [ ] Deve permitir editar: peso, observações de saúde, tags, categoria
- [ ] Não deve permitir alterar espécie ou data de nascimento
- [ ] Deve validar dados antes de salvar
- [ ] Deve exibir mensagem de sucesso

### 4.3 - Listar meus pets
**Como** um cliente
**Eu quero** visualizar todos os meus pets cadastrados
**Para que** escolher qual pet agendar atendimento

**Critérios de Aceitação:**
- [ ] Deve exibir apenas pets do cliente logado
- [ ] Deve mostrar: nome, espécie, raça, porte, data_nascimento
- [ ] Deve exibir tags associadas
- [ ] Deve exibir última data de atendimento
- [ ] Deve permitir clicar em um pet para ver detalhes

### 4.4 - Visualizar detalhes do pet
**Como** um cliente
**Eu quero** ver informações completas de um pet
**Para que** revisar histórico e características

**Critérios de Aceitação:**
- [ ] Deve exibir todos os dados cadastrados
- [ ] Deve exibir histórico de atendimentos (últimos 5)
- [ ] Deve exibir categoria do pet
- [ ] Deve exibir todas as tags
- [ ] Deve ter link para editar pet

### 4.5 - Listar todos os pets (admin)
**Como** um super_admin ou admin_loja
**Eu quero** visualizar todos os pets cadastrados no sistema
**Para que** gerenciar o catálogo

**Critérios de Aceitação:**
- [ ] Super_admin vê todos os pets
- [ ] Admin_loja vê apenas pets que tiveram atendimento em sua loja
- [ ] Deve permitir filtrar por categoria
- [ ] Deve permitir buscar por nome
- [ ] Deve exibir: nome, dono, categoria, porte

### 4.6 - Deletar pet
**Como** um cliente
**Eu quero** remover um pet do meu cadastro
**Para que** não apareça mais em minha lista

**Critérios de Aceitação:**
- [ ] Apenas o dono ou admin pode deletar
- [ ] Deve exibir confirmação antes de deletar
- [ ] Histórico de atendimentos deve ser preservado
- [ ] Pet não deve desaparecer, apenas desativado logicamente
- [ ] Mensagem de confirmação após exclusão

---

## 5. Gestão de Categorias e Tags

### 5.1 - Criar categoria de pet
**Como** um super_admin
**Eu quero** criar uma nova categoria de pet
**Para que** organizar os tipos de animais atendidos

**Critérios de Aceitação:**
- [ ] Apenas super_admin pode criar
- [ ] Deve solicitar: nome e descrição
- [ ] Nome deve ser único
- [ ] Deve validar comprimento mínimo de descrição
- [ ] Categoria criada deve estar ativa por padrão

### 5.2 - Editar categoria
**Como** um super_admin
**Eu quero** atualizar informações de uma categoria
**Para que** manter nomes e descrições atualizadas

**Critérios de Aceitação:**
- [ ] Apenas super_admin pode editar
- [ ] Deve permitir editar nome e descrição
- [ ] Deve validar que nome permanece único
- [ ] Deve registrar alterações

### 5.3 - Listar categorias
**Como** um usuário do sistema
**Eu quero** visualizar todas as categorias disponíveis
**Para que** filtrar ou selecionar ao cadastrar pet

**Critérios de Aceitação:**
- [ ] Deve exibir apenas categorias ativas
- [ ] Deve exibir: nome, descrição, quantidade de pets
- [ ] Deve permitir ordenar por nome

### 5.4 - Criar tag
**Como** um super_admin
**Eu quero** criar uma nova tag para marcar pets
**Para que** identificar características especiais

**Critérios de Aceitação:**
- [ ] Apenas super_admin pode criar
- [ ] Deve solicitar: nome e descrição
- [ ] Nome deve ser único
- [ ] Tag criada deve estar ativa por padrão

### 5.5 - Editar tag
**Como** um super_admin
**Eu quero** atualizar uma tag existente
**Para que** manter informações precisas

**Critérios de Aceitação:**
- [ ] Apenas super_admin pode editar
- [ ] Deve permitir editar nome e descrição
- [ ] Nome deve permanecer único após edição

### 5.6 - Listar tags
**Como** um usuário do sistema
**Eu quero** visualizar todas as tags disponíveis
**Para que** usar ao cadastrar ou editar pet

**Critérios de Aceitação:**
- [ ] Deve exibir apenas tags ativas
- [ ] Deve exibir: nome, descrição, quantidade de pets com a tag
- [ ] Deve permitir ordenar por nome

---

## 6. Gestão de Atendimentos

### 6.1 - Registrar atendimento
**Como** um funcionário
**Eu quero** registrar um atendimento realizado
**Para que** manter histórico de serviços prestados

**Critérios de Aceitação:**
- [ ] Deve solicitar: pet, cliente, tipo de serviço, data/hora, observações
- [ ] Funcionário deve estar vinculado à loja
- [ ] Pet deve pertencer ao cliente informado
- [ ] Deve associar automaticamente loja do funcionário
- [ ] Deve registrar data/hora de criação do atendimento
- [ ] Deve exibir confirmação com número do atendimento

### 6.2 - Listar atendimentos do meu pet
**Como** um cliente
**Eu quero** visualizar histórico de atendimentos do meu pet
**Para que** acompanhar cuidados realizados

**Critérios de Aceitação:**
- [ ] Deve exibir apenas atendimentos dos pets do cliente
- [ ] Deve mostrar: data, tipo_serviço, loja, funcionário, observações
- [ ] Deve permitir filtrar por data
- [ ] Deve permitir filtrar por tipo de serviço
- [ ] Deve ordenar por data (mais recente primeiro)

### 6.3 - Listar atendimentos da loja
**Como** um admin_loja
**Eu quero** ver todos os atendimentos realizados em minha loja
**Para que** gerenciar operações

**Critérios de Aceitação:**
- [ ] Apenas atendimentos da loja do admin
- [ ] Deve exibir: data, cliente, pet, funcionário, tipo_serviço
- [ ] Deve permitir filtrar por data
- [ ] Deve permitir filtrar por funcionário
- [ ] Deve permitir filtrar por cliente

### 6.4 - Visualizar detalhes do atendimento
**Como** um cliente, funcionário ou admin
**Eu quero** ver informações completas de um atendimento
**Para que** revisar dados do serviço realizado

**Critérios de Aceitação:**
- [ ] Cliente vê apenas atendimentos de seus pets
- [ ] Funcionário vê apenas atendimentos de sua loja
- [ ] Admin_loja vê atendimentos de sua loja
- [ ] Super_admin vê todos
- [ ] Deve exibir: pet, cliente, funcionário, loja, data/hora, tipo_serviço, observações

### 6.5 - Editar atendimento
**Como** um funcionário ou admin_loja
**Eu quero** corrigir informações de um atendimento
**Para que** manter dados precisos

**Critérios de Aceitação:**
- [ ] Apenas o funcionário que criou ou admin_loja pode editar
- [ ] Deve permitir editar: tipo_serviço, observações
- [ ] Não deve permitir alterar: pet, cliente, data, funcionário, loja
- [ ] Deve registrar alterações para auditoria
- [ ] Deve exibir confirmação

---

## 7. Analytics e Relatórios

### 7.1 - Relatório de atendimentos por período
**Como** um admin_loja ou super_admin
**Eu quero** gerar relatório de atendimentos em um período
**Para que** analisar volume e performance

**Critérios de Aceitação:**
- [ ] Deve permitir selecionar data inicial e final
- [ ] Deve exibir: total de atendimentos, quantidade por serviço
- [ ] Deve exibir: cliente com mais atendimentos, pet com mais atendimentos
- [ ] Admin_loja vê datos apenas de sua loja
- [ ] Super_admin pode filtrar por loja
- [ ] Deve permitir exportar em CSV

### 7.2 - Relatório de funcionarios por loja
**Como** um admin_loja
**Eu quero** visualizar número de atendimentos por funcionário
**Para que** avaliar produtividade

**Critérios de Aceitação:**
- [ ] Deve exibir: nome do funcionário, quantidade de atendimentos, período
- [ ] Deve permitir filtrar por período
- [ ] Deve ordenar por quantidade de atendimentos
- [ ] Deve permitir exportar em CSV

---

## 8. Notificações e Alertas

### 8.1 - Confirmar registro com email
**Como** um novo usuário
**Eu quero** receber email de confirmação após me registrar
**Para que** validar meu endereço de email

**Critérios de Aceitação:**
- [ ] Email deve ser enviado para o endereço fornecido
- [ ] Email deve conter link único de confirmação
- [ ] Link deve expirar em 24 horas
- [ ] Conta não pode realizar ações até confirmar email
- [ ] Link já utilizado não deve funcionar novamente

---

## Priorização

**P0 (Critical):**
- 1.3 - Fazer login
- 2.1 - Visualizar perfil pessoal
- 4.1 - Cadastrar novo pet
- 6.1 - Registrar atendimento

**P1 (High):**
- 1.1 - Registrar novo usuario cliente
- 1.2 - Registrar novo usuario funcionario
- 3.1 - Criar nova loja
- 4.3 - Listar meus pets
- 6.2 - Listar atendimentos do meu pet

**P2 (Medium):**
- 2.2 - Editar perfil pessoal
- 2.3 - Listar usuarios por perfil
- 3.2 - Editar dados da loja
- 4.2 - Editar dados do pet
- 5.1 - Criar categoria de pet
- 7.1 - Relatório de atendimentos

**P3 (Low):**
- Demais histórias
