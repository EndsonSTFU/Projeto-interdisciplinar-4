import sqlite3

def get_db_connection():
    conn = sqlite3.connect('banco_de_dados.db')
    conn.row_factory = sqlite3.Row
    return conn

def insert_paciente(nome, email, senha, data_nascimento, matricula):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO pacientes (nome, email, senha, data_nascimento, matricula)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (nome, email, senha, data_nascimento, matricula))
    conn.commit()
    conn.close()

def check_login(email, senha):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT * FROM pacientes WHERE email = ? AND senha = ?
    """, (email, senha))
    user = cursor.fetchone()
    conn.close()
    return user
