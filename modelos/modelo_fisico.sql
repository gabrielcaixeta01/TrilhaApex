BEGIN TRANSACTION;

CREATE TABLE users (
	id INTEGER NOT NULL,
	username VARCHAR NOT NULL,
	"firstName" VARCHAR,
	"lastName" VARCHAR,
	email VARCHAR,
	phone VARCHAR,
	password_hash VARCHAR,
	role VARCHAR NOT NULL DEFAULT 'user',
	user_active BOOLEAN NOT NULL DEFAULT 1,
	PRIMARY KEY (id)
);

CREATE TABLE categories (
	id INTEGER NOT NULL,
	name VARCHAR,
	PRIMARY KEY (id)
);

CREATE TABLE tags (
	id INTEGER NOT NULL,
	name VARCHAR,
	PRIMARY KEY (id)
);

CREATE TABLE pets (
	id INTEGER NOT NULL,
	name VARCHAR NOT NULL,
	"photoUrls" VARCHAR,
	status VARCHAR NOT NULL,
	category_id INTEGER NOT NULL,
	owner_id INTEGER,
	PRIMARY KEY (id),
	FOREIGN KEY (category_id) REFERENCES categories (id),
	CONSTRAINT fk_pets_owner_id_users FOREIGN KEY (owner_id) REFERENCES users (id)
);

CREATE TABLE orders (
	id INTEGER NOT NULL,
	"petId" INTEGER NOT NULL,
	quantity INTEGER,
	"shipDate" DATETIME,
	status VARCHAR,
	complete BOOLEAN,
	owner_id INTEGER NOT NULL,
	PRIMARY KEY (id),
	FOREIGN KEY ("petId") REFERENCES pets (id),
	CONSTRAINT fk_orders_owner_id_users FOREIGN KEY (owner_id) REFERENCES users (id)
);

CREATE TABLE pet_tags (
	pet_id INTEGER NOT NULL,
	tag_id INTEGER NOT NULL,
	PRIMARY KEY (pet_id, tag_id),
	FOREIGN KEY (pet_id) REFERENCES pets (id),
	FOREIGN KEY (tag_id) REFERENCES tags (id)
);

CREATE UNIQUE INDEX ix_users_username ON users (username);
CREATE UNIQUE INDEX ix_categories_name ON categories (name);
CREATE UNIQUE INDEX ix_tags_name ON tags (name);

CREATE INDEX ix_users_id ON users (id);
CREATE INDEX ix_categories_id ON categories (id);
CREATE INDEX ix_tags_id ON tags (id);
CREATE INDEX ix_pets_id ON pets (id);
CREATE INDEX ix_pets_name ON pets (name);
CREATE INDEX ix_pets_owner_id ON pets (owner_id);
CREATE INDEX ix_orders_id ON orders (id);
CREATE INDEX ix_orders_owner_id ON orders (owner_id);

COMMIT;