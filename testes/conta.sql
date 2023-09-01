CREATE TABLE "conta" (
	"id"	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	"numero"	INTEGER NOT NULL,
	"saldo"	REAL NOT NULL,
	"id_cliente"	INTEGER NOT NULL,
	FOREIGN KEY("id_cliente") REFERENCES "cliente"("id")
)