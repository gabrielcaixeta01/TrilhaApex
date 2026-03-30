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
INSERT INTO "categories" VALUES(1,'Cachorro');
INSERT INTO "categories" VALUES(2,'Gato');
INSERT INTO "categories" VALUES(3,'Ave');
INSERT INTO "categories" VALUES(4,'Roedor');
INSERT INTO "categories" VALUES(5,'Peixe');
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
INSERT INTO "orders" VALUES(1,1,1,'2026-03-21 10:00:00.000000','placed',0,1);
INSERT INTO "orders" VALUES(2,2,2,'2026-03-22 10:00:00.000000','approved',0,2);
INSERT INTO "orders" VALUES(3,3,1,'2026-03-23 10:00:00.000000','delivered',1,3);
INSERT INTO "orders" VALUES(4,4,3,'2026-03-24 10:00:00.000000','placed',0,4);
INSERT INTO "orders" VALUES(5,5,1,'2026-03-25 10:00:00.000000','approved',0,5);
INSERT INTO "orders" VALUES(6,6,2,'2026-03-26 10:00:00.000000','placed',0,6);
INSERT INTO "orders" VALUES(7,7,1,'2026-03-27 10:00:00.000000','delivered',1,7);
INSERT INTO "orders" VALUES(8,8,4,'2026-03-28 10:00:00.000000','approved',0,8);
INSERT INTO "orders" VALUES(9,9,2,'2026-03-29 10:00:00.000000','placed',0,9);
INSERT INTO "orders" VALUES(10,10,1,'2026-03-30 10:00:00.000000','approved',0,10);
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
INSERT INTO "pets" VALUES(1,'Thor','https://pics.example/thor.jpg','available',1,1,1);
INSERT INTO "pets" VALUES(2,'Luna','https://pics.example/luna.jpg','pending',2,2,2);
INSERT INTO "pets" VALUES(3,'Pipoca','https://pics.example/pipoca.jpg','sold',3,3,3);
INSERT INTO "pets" VALUES(4,'Nino','https://pics.example/nino.jpg','available',4,4,4);
INSERT INTO "pets" VALUES(5,'Bidu','https://pics.example/bidu.jpg','pending',5,5,5);
INSERT INTO "pets" VALUES(6,'Mel','https://pics.example/mel.jpg','available',1,6,6);
INSERT INTO "pets" VALUES(7,'Fred','https://pics.example/fred.jpg','pending',2,7,7);
INSERT INTO "pets" VALUES(8,'Nina','https://pics.example/nina.jpg','sold',3,8,8);
INSERT INTO "pets" VALUES(9,'Bob','https://pics.example/bob.jpg','available',4,9,9);
INSERT INTO "pets" VALUES(10,'Lilo','https://pics.example/lilo.jpg','pending',5,10,10);
CREATE TABLE tags (
	id INTEGER NOT NULL, 
	name VARCHAR, 
	PRIMARY KEY (id)
);
INSERT INTO "tags" VALUES(1,'filhote');
INSERT INTO "tags" VALUES(2,'vacinado');
INSERT INTO "tags" VALUES(3,'castrado');
INSERT INTO "tags" VALUES(4,'treinado');
INSERT INTO "tags" VALUES(5,'adocao');
INSERT INTO "tags" VALUES(6,'sociavel');
INSERT INTO "tags" VALUES(7,'porte-pequeno');
INSERT INTO "tags" VALUES(8,'porte-medio');
INSERT INTO "tags" VALUES(9,'porte-grande');
INSERT INTO "tags" VALUES(10,'especial');
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
INSERT INTO "users" VALUES(1,'seed_admin','Ana','Silva','ana.silva@example.com','11911110001','pbkdf2_sha256$210000$556916b5a831cb8c2cd870a58b988251$0c66cb6eda736c9d5b427f1d1dbd0b27a1472a9351d840e57bf962245c8ce65e','admin',1);
INSERT INTO "users" VALUES(2,'seed_user_1','Bruno','Souza','bruno.souza@example.com','11911110002','pbkdf2_sha256$210000$bc44462c8378da089f7d130e9ec5bf0b$abfdcf11776b6dba40c4285df20ad079d9625d0024b057b1bb72ce492ea1304d','user',1);
INSERT INTO "users" VALUES(3,'seed_user_2','Carla','Mendes','carla.mendes@example.com','11911110003','pbkdf2_sha256$210000$203f9bc3c446d3b0eed7acc957ab152c$7d6cf0674e48b5d28a7008b302712a562aef2be247fd22138f668867b322313b','viewer',1);
INSERT INTO "users" VALUES(4,'seed_user_3','Diego','Lima','diego.lima@example.com','11911110004','pbkdf2_sha256$210000$96bef32356d0acd67908bb0439d42c83$088a02beb134aa484cdba5a093379d175b6d0cd69b17b61c6023b3439f754beb','user',0);
INSERT INTO "users" VALUES(5,'seed_user_4','Elisa','Costa','elisa.costa@example.com','11911110005','pbkdf2_sha256$210000$7258490f30ca8bd881f99c262918a796$adb8acb1a01f1c98b98ae242ee243b3f826722cd4f33d83511f805d101625fe6','user',1);
INSERT INTO "users" VALUES(6,'seed_user_5','Felipe','Almeida','felipe.almeida@example.com','11911110006','pbkdf2_sha256$210000$ec7afb9fbdaf26f797e71f2c4c85a915$8957198418d0c1994e3b1a8d9025575928c5d9ecc11020dd726b1a6c17f7503e','user',1);
INSERT INTO "users" VALUES(7,'seed_user_6','Giovana','Ramos','giovana.ramos@example.com','11911110007','pbkdf2_sha256$210000$bf41b0a1baf4c2b4f3b84edcaf2449b3$4ae6b62ec8ed2f13a7e7cfbe37356e12888cba6427c614d4d769c22851d5d941','viewer',1);
INSERT INTO "users" VALUES(8,'seed_user_7','Henrique','Pereira','henrique.pereira@example.com','11911110008','pbkdf2_sha256$210000$9f5f5aa52f2b4dfbb2eebf8f36adf8d1$677f80d8a4f5ab8fa0ad3f6f9bf6f40c8d98fb74f14584f49f4dfe4db17ea69a','user',1);
INSERT INTO "users" VALUES(9,'seed_user_8','Isabela','Nunes','isabela.nunes@example.com','11911110009','pbkdf2_sha256$210000$3a4cd32f0f6cb84f062cf9b3e9e743f0$96890a486f64e9553ca4f5f67d3f0e4c795f14f7f9d14543c71f8459f549ec20','user',0);
INSERT INTO "users" VALUES(10,'seed_user_9','Joao','Oliveira','joao.oliveira@example.com','11911110010','pbkdf2_sha256$210000$5a2a1b88c52cd887b623f9dd2d7f30b4$8f38518880d6f52b6d07c3f5ce24699afb7fbbf48810b117cb7159b4de2a9f0e','user',1);
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