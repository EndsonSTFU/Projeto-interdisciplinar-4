import sqlite3
import os

db_path = 'banco_de_dados.db'


if os.path.exists(db_path):
    os.remove(db_path)


banco = sqlite3.connect(db_path)

cursor = banco.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS pacientes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        email TEXT NOT NULL UNIQUE,
        senha TEXT NOT NULL,
        data_nascimento TEXT NOT NULL,
        cpf TEXT NOT NULL UNIQUE,
        matricula INTEGER NOT NULL UNIQUE
    )
""")


cursor.execute("""
    INSERT INTO pacientes (nome, email, senha, data_nascimento, cpf, matricula)
    VALUES ('Creuza', 'Creuza_123@gmail.com', 'senha123', '1984-07-23', '12345678900', 123456)
""")


banco.commit()


cursor.execute("SELECT * FROM pacientes")
for row in cursor.fetchall():
    print(row)


banco.close()