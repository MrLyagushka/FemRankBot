BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS "mark" (
	"id"	INTEGER,
	"p_id"	INTEGER,
	"user_id"	INTEGER,
	"author_id"	INTEGER,
	"mark"	INTEGER,
	PRIMARY KEY("id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "photo" (
	"id"	INTEGER,
	"user_id"	INTEGER,
	"file_id"	TEXT,
	"media_group_id"	INTEGER,
	"caption"	TEXT,
	"BLOB"	BLOB,
	PRIMARY KEY("id" AUTOINCREMENT)
);
CREATE UNIQUE INDEX IF NOT EXISTS "idx_unique_mark" ON "mark" (
	"p_id",
	"user_id",
	"author_id"
);
CREATE UNIQUE INDEX IF NOT EXISTS "idx_unique_photo" ON "photo" (
	"user_id",
	"file_id",
	"media_group_id"
);
COMMIT;
