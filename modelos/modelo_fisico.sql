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
	CONSTRAINT fk_clientes_usuario FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE
);

CREATE TABLE funcionarios (
	usuario_id INTEGER NOT NULL,
	matricula VARCHAR(20) NOT NULL UNIQUE,
	cargo VARCHAR(80) NOT NULL,
	salario DECIMAL(10,2) NOT NULL,
	data_contratacao DATE NOT NULL,
	CONSTRAINT fk_funcionarios_usuario FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE
);


CREATE TABLE lojas (
	id INTEGER PRIMARY KEY,
	nome VARCHAR(120) NOT NULL,
	cnpj VARCHAR(18) NOT NULL UNIQUE,
	telefone VARCHAR(20) NOT NULL,
	email VARCHAR(255) NOT NULL UNIQUE,
	ativo BOOLEAN NOT NULL DEFAULT TRUE,
	data_cadastro TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
	end_cep VARCHAR(9) NOT NULL,
	end_cidade VARCHAR(120) NOT NULL,
	end_estado CHAR(2) NOT NULL,
	end_rua VARCHAR(255) NOT NULL,
	end_bairro VARCHAR(120) NOT NULL,
	end_numero VARCHAR(20) NOT NULL,
);

CREATE TABLE atendimentos (
	id INTEGER PRIMARY KEY,
	valor_final DECIMAL(10,2) NOT NULL,
	data_atendimento TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
	forma_pagamento VARCHAR(20) NOT NULL,
	status VARCHAR(20) NOT NULL,
	online BOOLEAN NOT NULL DEFAULT FALSE,
	observacoes VARCHAR(500),
);

CREATE TABLE servicos (
	id INTEGER PRIMARY KEY,
	nome VARCHAR(120) NOT NULL,
	descricao VARCHAR(500),
	preco DECIMAL(10,2) NOT NULL,
);

CREATE TABLE atendimento_servicos (
	atendimento_id INTEGER NOT NULL,
	servico_id INTEGER NOT NULL,
	valor_cobrado DECIMAL(10,2) NOT NULL,
	obervacoes VARCHAR(500),
	PRIMARY KEY (atendimento_id, servico_id),
	CONSTRAINT fk_atendimento_servicos_atendimento FOREIGN KEY (atendimento_id) REFERENCES atendimentos(id) ON DELETE CASCADE,
	CONSTRAINT fk_atendimento_servicos_servico FOREIGN KEY (servico_id) REFERENCES servicos(id) ON DELETE CASCADE
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
	CONSTRAINT fk_pets_dono FOREIGN KEY (dono_id) REFERENCES clientes(usuario_id) ON DELETE CASCADE,
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

CREATE TABLE categorias (
	id INTEGER PRIMARY KEY,
	nome VARCHAR(80) NOT NULL UNIQUE,
	descricao VARCHAR(255)
);
