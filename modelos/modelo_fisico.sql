CREATE TABLE usuarios (
	id INTEGER PRIMARY KEY,
	nome VARCHAR(120) NOT NULL,
	email VARCHAR(255) NOT NULL UNIQUE,
	senha_hash VARCHAR(255) NOT NULL,
	telefone VARCHAR(20) NOT NULL,
	tipo_perfil VARCHAR(20) NOT NULL,
	cpf VARCHAR(14),
	cnpj VARCHAR(18),
	ativo BOOLEAN NOT NULL DEFAULT TRUE,
	is_superuser BOOLEAN NOT NULL DEFAULT FALSE,
	data_cadastro TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE clientes (
	usuario_id INTEGER NOT NULL,
	tipo_cliente VARCHAR(20) NOT NULL,
	end_cep VARCHAR(9) NOT NULL,
	end_estado CHAR(2) NOT NULL,
	end_cidade VARCHAR(120) NOT NULL,
	PRIMARY KEY (usuario_id),
	CONSTRAINT fk_clientes_usuario FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE
);

CREATE TABLE lojas (
	id INTEGER PRIMARY KEY,
	nome VARCHAR(120) NOT NULL,
	cnpj VARCHAR(18) NOT NULL UNIQUE,
	telefone VARCHAR(20) NOT NULL,
	email VARCHAR(255) NOT NULL UNIQUE,
	ativo BOOLEAN NOT NULL DEFAULT TRUE,
	data_cadastro TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
	end_cep VARCHAR(9) NOT NULL,
	end_cidade VARCHAR(120) NOT NULL,
	end_estado CHAR(2) NOT NULL,
	end_rua VARCHAR(255) NOT NULL,
	end_bairro VARCHAR(120) NOT NULL,
	end_numero VARCHAR(20) NOT NULL
);

CREATE TABLE funcionarios (
	usuario_id INTEGER NOT NULL,
	matricula VARCHAR(20) NOT NULL UNIQUE,
	cargo VARCHAR(80) NOT NULL,
	salario DECIMAL(10,2) NOT NULL,
	data_contratacao DATE NOT NULL,
	loja_id INTEGER NOT NULL,
	CONSTRAINT fk_funcionarios_loja FOREIGN KEY (loja_id) REFERENCES lojas(id) ON DELETE CASCADE,
	CONSTRAINT fk_funcionarios_usuario FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE
);

CREATE TABLE atendimentos (
	id INTEGER PRIMARY KEY,
	valor_final DECIMAL(10,2) NOT NULL,
	data_atendimento TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
	forma_pagamento VARCHAR(20) NOT NULL,
	status VARCHAR(20) NOT NULL,
	online BOOLEAN NOT NULL DEFAULT FALSE,
	observacoes VARCHAR(500),
	loja_id INTEGER NOT NULL,
	cliente_id INTEGER NOT NULL,
	funcionario_id INTEGER NOT NULL,
	CONSTRAINT fk_atendimentos_loja FOREIGN KEY (loja_id) REFERENCES lojas(id) ON DELETE CASCADE,
	CONSTRAINT fk_atendimentos_cliente FOREIGN KEY (cliente_id) REFERENCES clientes(usuario_id),
	CONSTRAINT fk_atendimentos_funcionario FOREIGN KEY (funcionario_id) REFERENCES funcionarios(usuario_id)
);

CREATE TABLE servicos (
	id INTEGER PRIMARY KEY,
	nome VARCHAR(120) NOT NULL,
	descricao VARCHAR(500),
	preco DECIMAL(10,2) NOT NULL
);

CREATE TABLE atendimento_servicos (
	atendimento_id INTEGER NOT NULL,
	servico_id INTEGER NOT NULL,
	valor_cobrado DECIMAL(10,2) NOT NULL,
	observacoes VARCHAR(500),
	PRIMARY KEY (atendimento_id, servico_id),
	CONSTRAINT fk_atendimento_servicos_atendimento FOREIGN KEY (atendimento_id) REFERENCES atendimentos(id) ON DELETE CASCADE,
	CONSTRAINT fk_atendimento_servicos_servico FOREIGN KEY (servico_id) REFERENCES servicos(id) ON DELETE CASCADE
);

CREATE TABLE categorias (
	id INTEGER PRIMARY KEY,
	nome VARCHAR(80) NOT NULL UNIQUE,
	descricao VARCHAR(255)
);

CREATE TABLE pets (
	id INTEGER PRIMARY KEY,
	nome VARCHAR(120),
	raca VARCHAR(80),
	sexo VARCHAR(20),
	porte VARCHAR(20),
	peso DECIMAL(6,2),
	observacoes_saude VARCHAR(500),
	categoria_id INTEGER NOT NULL,
	dono_id INTEGER NOT NULL,
	CONSTRAINT fk_pets_categoria FOREIGN KEY (categoria_id) REFERENCES categorias(id) ON DELETE CASCADE,
	CONSTRAINT fk_pets_dono FOREIGN KEY (dono_id) REFERENCES clientes(usuario_id) ON DELETE CASCADE
);

CREATE TABLE tags (
	id INTEGER PRIMARY KEY,
	nome VARCHAR(80) NOT NULL UNIQUE,
	descricao VARCHAR(255)
);

CREATE TABLE pet_tags (
	pet_id INTEGER NOT NULL,
	tag_id INTEGER NOT NULL,
	PRIMARY KEY (pet_id, tag_id),
	CONSTRAINT fk_pet_tags_pet FOREIGN KEY (pet_id) REFERENCES pets(id) ON DELETE CASCADE,
	CONSTRAINT fk_pet_tags_tag FOREIGN KEY (tag_id) REFERENCES tags(id) ON DELETE CASCADE
);

-- Mantem valor_final em sincronia com a soma dos itens do atendimento
CREATE TRIGGER tr_atendimento_servicos_ai
AFTER INSERT ON atendimento_servicos
BEGIN
	UPDATE atendimentos
	SET valor_final = COALESCE((
		SELECT SUM(valor_cobrado)
		FROM atendimento_servicos
		WHERE atendimento_id = NEW.atendimento_id
	), 0)
	WHERE id = NEW.atendimento_id;
END;

CREATE TRIGGER tr_atendimento_servicos_au
AFTER UPDATE ON atendimento_servicos
BEGIN
	UPDATE atendimentos
	SET valor_final = COALESCE((
		SELECT SUM(valor_cobrado)
		FROM atendimento_servicos
		WHERE atendimento_id = NEW.atendimento_id
	), 0)
	WHERE id = NEW.atendimento_id;

	UPDATE atendimentos
	SET valor_final = COALESCE((
		SELECT SUM(valor_cobrado)
		FROM atendimento_servicos
		WHERE atendimento_id = OLD.atendimento_id
	), 0)
	WHERE id = OLD.atendimento_id;
END;

CREATE TRIGGER tr_atendimento_servicos_ad
AFTER DELETE ON atendimento_servicos
BEGIN
	UPDATE atendimentos
	SET valor_final = COALESCE((
		SELECT SUM(valor_cobrado)
		FROM atendimento_servicos
		WHERE atendimento_id = OLD.atendimento_id
	), 0)
	WHERE id = OLD.atendimento_id;
END;


-- ==========================================
-- DADOS DE EXEMPLO (SEED)
-- Pelo menos 5 registros por tabela
-- ==========================================

INSERT INTO usuarios (id, nome, email, senha_hash, telefone, tipo_perfil, cpf, cnpj, ativo, is_superuser, data_cadastro) VALUES
	(1, 'Ana Paula', 'ana.paula@exemplo.com', 'hash_ana_123', '11990001111', 'cliente', '111.111.111-11', NULL, TRUE, FALSE, '2026-01-10 09:00:00'),
	(2, 'Bruno Lima', 'bruno.lima@exemplo.com', 'hash_bruno_123', '11990002222', 'cliente', '222.222.222-22', NULL, TRUE, FALSE, '2026-01-11 09:10:00'),
	(3, 'Carla Souza', 'carla.souza@exemplo.com', 'hash_carla_123', '11990003333', 'cliente', '333.333.333-33', NULL, TRUE, FALSE, '2026-01-12 09:20:00'),
	(4, 'Diego Martins', 'diego.martins@exemplo.com', 'hash_diego_123', '11990004444', 'cliente', '444.444.444-44', NULL, TRUE, FALSE, '2026-01-13 09:30:00'),
	(5, 'Elisa Rocha', 'elisa.rocha@exemplo.com', 'hash_elisa_123', '11990005555', 'cliente', '555.555.555-55', NULL, TRUE, FALSE, '2026-01-14 09:40:00'),
	(6, 'Fabio Costa', 'fabio.costa@exemplo.com', 'hash_fabio_123', '11991111111', 'funcionario', '666.666.666-66', NULL, TRUE, FALSE, '2026-01-15 10:00:00'),
	(7, 'Gabriela Nunes', 'gabriela.nunes@exemplo.com', 'hash_gabi_123', '11992222222', 'funcionario', '777.777.777-77', NULL, TRUE, FALSE, '2026-01-16 10:10:00'),
	(8, 'Heitor Alves', 'heitor.alves@exemplo.com', 'hash_heitor_123', '11993333333', 'funcionario', '888.888.888-88', NULL, TRUE, FALSE, '2026-01-17 10:20:00'),
	(9, 'Isabela Melo', 'isabela.melo@exemplo.com', 'hash_isabela_123', '11994444444', 'funcionario', '999.999.999-99', NULL, TRUE, FALSE, '2026-01-18 10:30:00'),
	(10, 'Joao Pedro', 'joao.pedro@exemplo.com', 'hash_joao_123', '11995555555', 'funcionario', '000.000.000-00', NULL, TRUE, FALSE, '2026-01-19 10:40:00');

INSERT INTO clientes (usuario_id, tipo_cliente, end_cep, end_estado, end_cidade) VALUES
	(1, 'pessoa_fisica', '01001-000', 'SP', 'Sao Paulo'),
	(2, 'pessoa_fisica', '20040-020', 'RJ', 'Rio de Janeiro'),
	(3, 'pessoa_fisica', '30110-040', 'MG', 'Belo Horizonte'),
	(4, 'pessoa_fisica', '80010-000', 'PR', 'Curitiba'),
	(5, 'pessoa_fisica', '40020-000', 'BA', 'Salvador');

INSERT INTO lojas (id, nome, cnpj, telefone, email, ativo, data_cadastro, end_cep, end_cidade, end_estado, end_rua, end_bairro, end_numero) VALUES
	(1, 'Petshop GC Paulista', '10.000.000/0001-01', '1130001001', 'paulista@petshopgc.com', TRUE, '2026-01-01 08:00:00', '01310-100', 'Sao Paulo', 'SP', 'Av Paulista', 'Bela Vista', '1000'),
	(2, 'Petshop GC Centro RJ', '10.000.000/0001-02', '2130002002', 'centrorj@petshopgc.com', TRUE, '2026-01-01 08:10:00', '20031-170', 'Rio de Janeiro', 'RJ', 'Rua Primeiro de Marco', 'Centro', '200'),
	(3, 'Petshop GC Savassi', '10.000.000/0001-03', '3130003003', 'savassi@petshopgc.com', TRUE, '2026-01-01 08:20:00', '30140-070', 'Belo Horizonte', 'MG', 'Rua Pernambuco', 'Savassi', '300'),
	(4, 'Petshop GC Batel', '10.000.000/0001-04', '4130004004', 'batel@petshopgc.com', TRUE, '2026-01-01 08:30:00', '80420-090', 'Curitiba', 'PR', 'Av do Batel', 'Batel', '400'),
	(5, 'Petshop GC Barra', '10.000.000/0001-05', '7130005005', 'barra@petshopgc.com', TRUE, '2026-01-01 08:40:00', '40140-110', 'Salvador', 'BA', 'Av Oceanica', 'Barra', '500');

INSERT INTO funcionarios (usuario_id, matricula, cargo, salario, data_contratacao, loja_id) VALUES
	(6, 'FUNC-0001', 'banhista', 2200.00, '2026-01-20', 1),
	(7, 'FUNC-0002', 'tosador', 2600.00, '2026-01-21', 2),
	(8, 'FUNC-0003', 'veterinario', 5500.00, '2026-01-22', 3),
	(9, 'FUNC-0004', 'recepcionista', 2100.00, '2026-01-23', 4),
	(10, 'FUNC-0005', 'adestrador', 3200.00, '2026-01-24', 5);

INSERT INTO categorias (id, nome, descricao) VALUES
	(1, 'Canino', 'Pets do tipo cao'),
	(2, 'Felino', 'Pets do tipo gato'),
	(3, 'Ave', 'Aves domesticas'),
	(4, 'Coelho', 'Coelhos de companhia'),
	(5, 'Roedor', 'Roedores de pequeno porte');

INSERT INTO pets (id, nome, raca, sexo, porte, peso, observacoes_saude, categoria_id, dono_id) VALUES
	(1, 'Thor', 'Labrador', 'macho', 'grande', 28.50, 'Sem restricoes', 1, 1),
	(2, 'Luna', 'Siamês', 'femea', 'pequeno', 4.20, 'Alergia leve', 2, 2),
	(3, 'Pipoca', 'Calopsita', 'femea', 'pequeno', 0.09, 'Acompanha crescimento de bico', 3, 3),
	(4, 'Nino', 'Mini Lop', 'macho', 'medio', 1.80, 'Sensivel a ruido', 4, 4),
	(5, 'Bolt', 'Porquinho-da-india', 'macho', 'pequeno', 1.10, 'Dieta controlada', 5, 5);

INSERT INTO tags (id, nome, descricao) VALUES
	(1, 'idoso', 'Pet com idade avancada'),
	(2, 'alergico', 'Pet com historico de alergia'),
	(3, 'agressivo', 'Pet com comportamento reativo'),
	(4, 'precisa_sedacao', 'Pet pode demandar sedacao em procedimentos'),
	(5, 'primeiro_atendimento', 'Primeiro atendimento do pet na rede');

INSERT INTO pet_tags (pet_id, tag_id) VALUES
	(1, 1),
	(2, 2),
	(3, 5),
	(4, 4),
	(5, 3);

INSERT INTO servicos (id, nome, descricao, preco) VALUES
	(1, 'Banho', 'Banho completo com secagem', 80.00),
	(2, 'Tosa', 'Tosa higienica e estetica', 95.00),
	(3, 'Consulta Veterinaria', 'Consulta clinica geral', 180.00),
	(4, 'Vacinacao', 'Aplicacao de vacina conforme protocolo', 140.00),
	(5, 'Adestramento Basico', 'Sessao inicial de comandos basicos', 220.00);

INSERT INTO atendimentos (id, valor_final, data_atendimento, forma_pagamento, status, online, observacoes, loja_id, cliente_id, funcionario_id) VALUES
	(1, 80.00, '2026-02-01 10:00:00', 'pix', 'concluido', FALSE, 'Atendimento tranquilo', 1, 1, 6),
	(2, 95.00, '2026-02-02 11:00:00', 'cartao_credito', 'concluido', FALSE, 'Tosa com tesoura', 2, 2, 7),
	(3, 180.00, '2026-02-03 15:30:00', 'cartao_debito', 'concluido', TRUE, 'Consulta por teleorientacao', 3, 3, 8),
	(4, 140.00, '2026-02-04 09:15:00', 'dinheiro', 'concluido', FALSE, 'Vacinacao anual', 4, 4, 9),
	(5, 220.00, '2026-02-05 16:45:00', 'pix', 'agendado', FALSE, 'Primeira sessao de adestramento', 5, 5, 10);

INSERT INTO atendimento_servicos (atendimento_id, servico_id, valor_cobrado, observacoes) VALUES
	(1, 1, 80.00, 'Banho completo realizado'),
	(2, 2, 95.00, 'Tosa finalizada com sucesso'),
	(3, 3, 180.00, 'Consulta clinica registrada'),
	(4, 4, 140.00, 'Vacina aplicada sem intercorrencias'),
	(5, 5, 220.00, 'Sessao inicial concluida');

