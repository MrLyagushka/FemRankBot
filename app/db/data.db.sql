BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS "group_data" (
	"id"	INTEGER,
	"type"	TEXT,
	"status"	TEXT,
	"full_name"	TEXT,
	"on_off"	INTEGER
);
COMMIT;
