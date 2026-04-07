BEGIN TRANSACTION;

CREATE TABLE lojas (
	id INTEGER PRIMARY KEY,
	nome VARCHAR(120) NOT NULL,
	cnpj VARCHAR(18) NOT NULL UNIQUE,
	telefone VARCHAR(20),
	email VARCHAR(255),
	cep VARCHAR(9),
	endereco VARCHAR(255),
	cidade VARCHAR(120),
	estado CHAR(2),
	ativo BOOLEAN NOT NULL DEFAULT TRUE,
	data_cadastro TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE usuarios (
	id INTEGER PRIMARY KEY,
	nome VARCHAR(120) NOT NULL,
	email VARCHAR(255) NOT NULL UNIQUE,
	senha_hash VARCHAR(255) NOT NULL,
	telefone VARCHAR(20),
	perfil VARCHAR(20) NOT NULL,
	cpf VARCHAR(14),
	cnpj VARCHAR(18),
	tipo_cliente VARCHAR(20),
	data_nascimento DATE,
	endereco VARCHAR(255),
	cargo VARCHAR(80),
	data_inicio DATE,
	loja_id INTEGER,
	ativo BOOLEAN NOT NULL DEFAULT TRUE,
	data_cadastro TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
	CONSTRAINT ck_usuarios_perfil CHECK (perfil IN ('cliente', 'funcionario', 'admin_loja', 'super_admin')),
	CONSTRAINT fk_usuarios_loja FOREIGN KEY (loja_id) REFERENCES lojas(id) ON DELETE CASCADE,
	CONSTRAINT ck_usuario_loja_por_perfil CHECK (
		(perfil = 'funcionario')
		OR (perfil = 'admin_loja' AND loja_id IS NOT NULL)
		OR (perfil IN ('cliente', 'super_admin') AND loja_id IS NULL)
	),
	CONSTRAINT ck_cliente_documento CHECK (
		perfil <> 'cliente'
		OR (
			(cpf IS NOT NULL AND cnpj IS NULL)
			OR (cpf IS NULL AND cnpj IS NOT NULL)
		)
	)
);

CREATE TABLE categorias (
	id INTEGER PRIMARY KEY,
	nome VARCHAR(80) NOT NULL UNIQUE,
	descricao VARCHAR(255)
);

CREATE TABLE tags (
	id INTEGER PRIMARY KEY,
	nome VARCHAR(80) NOT NULL UNIQUE,
	descricao VARCHAR(255)
);

CREATE TABLE pets (
	id INTEGER PRIMARY KEY,
	nome VARCHAR(120) NOT NULL,
	especie VARCHAR(60),
	raca VARCHAR(80),
	sexo VARCHAR(20),
	data_nascimento DATE,
	porte VARCHAR(20),
	peso DECIMAL(6,2),
	observacoes_saude VARCHAR(500),
	categoria_id INTEGER NOT NULL,
	dono_id INTEGER NOT NULL,
	ativo BOOLEAN NOT NULL DEFAULT TRUE,
	CONSTRAINT fk_pets_categoria FOREIGN KEY (categoria_id) REFERENCES categorias(id) ON DELETE CASCADE,
	CONSTRAINT fk_pets_dono FOREIGN KEY (dono_id) REFERENCES usuarios(id)
);

CREATE TABLE pet_tags (
	pet_id INTEGER NOT NULL,
	tag_id INTEGER NOT NULL,
	PRIMARY KEY (pet_id, tag_id),
	CONSTRAINT fk_pet_tags_pet FOREIGN KEY (pet_id) REFERENCES pets(id) ON DELETE CASCADE,
	CONSTRAINT fk_pet_tags_tag FOREIGN KEY (tag_id) REFERENCES tags(id) ON DELETE CASCADE
);

CREATE TABLE atendimentos (
	id INTEGER PRIMARY KEY,
	tipo_servico VARCHAR(80) NOT NULL,
	descricao VARCHAR(500),
	data_hora TIMESTAMP NOT NULL,
	status VARCHAR(30) NOT NULL,
	valor DECIMAL(10,2),
	desconto DECIMAL(10,2) DEFAULT 0,
	forma_pagamento VARCHAR(40),
	observacoes VARCHAR(500),
	loja_id INTEGER NOT NULL,
	pet_id INTEGER NOT NULL,
	cliente_id INTEGER NOT NULL,
	funcionario_id INTEGER NOT NULL,
	CONSTRAINT fk_atendimentos_loja FOREIGN KEY (loja_id) REFERENCES lojas(id),
	CONSTRAINT fk_atendimentos_pet FOREIGN KEY (pet_id) REFERENCES pets(id),
	CONSTRAINT fk_atendimentos_cliente FOREIGN KEY (cliente_id) REFERENCES usuarios(id),
	CONSTRAINT fk_atendimentos_funcionario FOREIGN KEY (funcionario_id) REFERENCES usuarios(id)
);

CREATE UNIQUE INDEX ux_admin_loja_por_loja ON usuarios(loja_id) WHERE perfil = 'admin_loja';
CREATE INDEX ix_usuarios_perfil ON usuarios(perfil);
CREATE INDEX ix_pets_dono_id ON pets(dono_id);
CREATE INDEX ix_pets_categoria_id ON pets(categoria_id);
CREATE INDEX ix_atendimentos_pet_id ON atendimentos(pet_id);
CREATE INDEX ix_atendimentos_loja_id ON atendimentos(loja_id);
CREATE INDEX ix_atendimentos_cliente_id ON atendimentos(cliente_id);
CREATE INDEX ix_atendimentos_funcionario_id ON atendimentos(funcionario_id);

COMMIT;

