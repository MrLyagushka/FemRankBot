BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS "group_data" (
	"id"	INTEGER,
	"type"	TEXT,
	"status"	TEXT,
	"full_name"	TEXT,
	"on_off"	INTEGER
);
CREATE TABLE IF NOT EXISTS "users" (
	"user_id"	INTEGER,
	"username"	TEXT,
	"first_name"	TEXT,
	"last_name"	TEXT
);
COMMIT;
