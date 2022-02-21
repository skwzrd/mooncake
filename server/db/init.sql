CREATE TABLE "user" (
	"id"	INTEGER NOT NULL,
	"username"	TEXT NOT NULL,
	"email"	TEXT NOT NULL,
	"password"	TEXT NOT NULL,
	"salt"	TEXT NOT NULL,
	"date_joined"	TEXT NOT NULL,
	"active"	INTEGER NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT)
);

CREATE TABLE "no_account_user" (
	"id"	INTEGER NOT NULL,
	"username"	TEXT NOT NULL,
	"date_joined"	TEXT NOT NULL,
	"last_active"	TEXT NOT NULL,
	"active"	INTEGER NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT)
);

CREATE TABLE "stats" (
	"id"	INTEGER NOT NULL,
	"user_id"	INTEGER NOT NULL,
	"character_id"	INTEGER NOT NULL,
	"stat"	INTEGER NOT NULL DEFAULT 0,
  "last_studied"	TEXT DEFAULT NULL,
	PRIMARY KEY("id" AUTOINCREMENT),
  FOREIGN KEY("user_id") REFERENCES "user"("id")
);

CREATE TABLE "character" (
	"id"	INTEGER NOT NULL,
	"character"	TEXT NOT NULL,
	"pinyin"	TEXT NOT NULL,
	"english"	TEXT NOT NULL,
	"hsk"	INTEGER NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT)
);

INSERT INTO "main"."user" ("username", "email", "password", "salt", "date_joined", "active") VALUES ('admin', 'example@domain.com', 'pwd', 'salt', '2021-11-22 09:00:00', 1);
