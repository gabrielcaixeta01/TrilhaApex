BEGIN TRANSACTION;
CREATE TABLE alembic_version (
	version_num VARCHAR(32) NOT NULL, 
	CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num)
);
INSERT INTO "alembic_version" VALUES('d1f3a9b6c2e4');
CREATE TABLE categories (
	id INTEGER NOT NULL, 
	name VARCHAR, 
	PRIMARY KEY (id)
);
INSERT INTO "categories" VALUES(9101,'Cachorro');
INSERT INTO "categories" VALUES(9102,'Gato');
INSERT INTO "categories" VALUES(9103,'Ave');
INSERT INTO "categories" VALUES(9104,'Roedor');
INSERT INTO "categories" VALUES(9105,'Peixe');
CREATE TABLE "orders" (
	id INTEGER NOT NULL, 
	"petId" INTEGER, 
	quantity INTEGER, 
	"shipDate" DATETIME, 
	status VARCHAR, 
	complete BOOLEAN, 
	owner_id INTEGER, 
	PRIMARY KEY (id), 
	CONSTRAINT fk_orders_owner_id_users FOREIGN KEY(owner_id) REFERENCES users (id), 
	FOREIGN KEY("petId") REFERENCES pets (id)
);
INSERT INTO "orders" VALUES(9401,9301,1,'2026-03-26 19:05:20.174938','placed',0,NULL);
INSERT INTO "orders" VALUES(9402,9302,2,'2026-03-27 19:05:20.174944','approved',0,NULL);
INSERT INTO "orders" VALUES(9403,9303,1,'2026-03-28 19:05:20.174947','delivered',1,NULL);
INSERT INTO "orders" VALUES(9404,9304,3,'2026-03-29 19:05:20.174948','placed',0,NULL);
INSERT INTO "orders" VALUES(9405,9305,1,'2026-03-30 19:05:20.174949','approved',0,NULL);
CREATE TABLE "pets" (
	id INTEGER NOT NULL, 
	name VARCHAR, 
	"photoUrls" VARCHAR, 
	status VARCHAR, 
	category_id INTEGER, 
	owner_id INTEGER, 
	tag_id INTEGER, 
	PRIMARY KEY (id), 
	CONSTRAINT fk_pets_owner_id_users FOREIGN KEY(owner_id) REFERENCES users (id), 
	CONSTRAINT fk_pets_tag_id_tags FOREIGN KEY(tag_id) REFERENCES tags (id), 
	FOREIGN KEY(category_id) REFERENCES categories (id)
);
INSERT INTO "pets" VALUES(9301,'Thor','https://pics.example/thor.jpg','available',9101,NULL,9201);
INSERT INTO "pets" VALUES(9302,'Luna','https://pics.example/luna.jpg','pending',9102,NULL,9202);
INSERT INTO "pets" VALUES(9303,'Pipoca','https://pics.example/pipoca.jpg','sold',9103,NULL,9203);
INSERT INTO "pets" VALUES(9304,'Nino','https://pics.example/nino.jpg','available',9104,NULL,9204);
INSERT INTO "pets" VALUES(9305,'Bidu','https://pics.example/bidu.jpg','pending',9105,NULL,9205);
INSERT INTO "pets" VALUES(9307,'Rex',NULL,'available',9101,9507,NULL);
CREATE TABLE tags (
	id INTEGER NOT NULL, 
	name VARCHAR, 
	PRIMARY KEY (id)
);
INSERT INTO "tags" VALUES(9201,'filhote');
INSERT INTO "tags" VALUES(9202,'vacinado');
INSERT INTO "tags" VALUES(9203,'castrado');
INSERT INTO "tags" VALUES(9204,'treinado');
INSERT INTO "tags" VALUES(9205,'adocao');
CREATE TABLE "users" (
	id INTEGER NOT NULL, 
	username VARCHAR, 
	"firstName" VARCHAR, 
	"lastName" VARCHAR, 
	email VARCHAR, 
	phone VARCHAR, 
	password_hash VARCHAR, 
	role VARCHAR DEFAULT 'user' NOT NULL, 
	user_active BOOLEAN DEFAULT 1 NOT NULL, 
	PRIMARY KEY (id)
);
INSERT INTO "users" VALUES(9501,'seed_admin','Ana','Silva','ana.silva@example.com','11911110001','pbkdf2_sha256$210000$556916b5a831cb8c2cd870a58b988251$0c66cb6eda736c9d5b427f1d1dbd0b27a1472a9351d840e57bf962245c8ce65e','admin',1);
INSERT INTO "users" VALUES(9502,'seed_user_1','Bruno','Souza','bruno.souza@example.com','11911110002','pbkdf2_sha256$210000$bc44462c8378da089f7d130e9ec5bf0b$abfdcf11776b6dba40c4285df20ad079d9625d0024b057b1bb72ce492ea1304d','user',1);
INSERT INTO "users" VALUES(9503,'seed_user_2','Carla','Mendes','carla.mendes@example.com','11911110003','pbkdf2_sha256$210000$203f9bc3c446d3b0eed7acc957ab152c$7d6cf0674e48b5d28a7008b302712a562aef2be247fd22138f668867b322313b','viewer',1);
INSERT INTO "users" VALUES(9504,'seed_user_3','Diego','Lima','diego.lima@example.com','11911110004','pbkdf2_sha256$210000$96bef32356d0acd67908bb0439d42c83$088a02beb134aa484cdba5a093379d175b6d0cd69b17b61c6023b3439f754beb','user',0);
INSERT INTO "users" VALUES(9505,'seed_user_4','Elisa','Costa','elisa.costa@example.com','11911110005','pbkdf2_sha256$210000$7258490f30ca8bd881f99c262918a796$adb8acb1a01f1c98b98ae242ee243b3f826722cd4f33d83511f805d101625fe6','user',1);
INSERT INTO "users" VALUES(9506,'gabriel','Gabriel','Romero','gabriel@gmil.com','1234567890','pbkdf2_sha256$210000$ec7afb9fbdaf26f797e71f2c4c85a915$8957198418d0c1994e3b1a8d9025575928c5d9ecc11020dd726b1a6c17f7503e','admin',1);
INSERT INTO "users" VALUES(9507,'teste','Gabriel','Romero','gabriel@gmil.com','123123123123','pbkdf2_sha256$210000$bf41b0a1baf4c2b4f3b84edcaf2449b3$4ae6b62ec8ed2f13a7e7cfbe37356e12888cba6427c614d4d769c22851d5d941','user',1);
CREATE INDEX ix_categories_id ON categories (id);
CREATE INDEX ix_categories_name ON categories (name);
CREATE INDEX ix_tags_id ON tags (id);
CREATE INDEX ix_tags_name ON tags (name);
CREATE INDEX ix_orders_id ON orders (id);
CREATE INDEX ix_orders_owner_id ON orders (owner_id);
CREATE UNIQUE INDEX ix_users_username ON users (username);
CREATE INDEX ix_users_id ON users (id);
CREATE INDEX ix_pets_owner_id ON pets (owner_id);
CREATE INDEX ix_pets_name ON pets (name);
CREATE INDEX ix_pets_id ON pets (id);
CREATE INDEX ix_pets_tag_id ON pets (tag_id);
COMMIT;