import sqlite3

def get_db_connection():
    conn = sqlite3.connect('banco_de_dados.db')
    conn.row_factory = sqlite3.Row
    return conn

def criacao_tabelas():
    conn = get_db_connection()
    cursor = conn.cursor()
    


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
#criar método de cadastro do psicólogo
def insert_psicologo(nome, email, senha):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
                   INSERT INTO psicicólogo (nome, email, senha)
                   VALUES (waldemar, waldemar.neto@ufrpe.br, 123456789)""",(nome, email, senha))
    conn.commit()
    conn.close()
    
