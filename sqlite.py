import sqlite3
import os

def get_db_connection():
    try:
        conn = sqlite3.connect('banco_de_dados.db')  
        conn.row_factory = sqlite3.Row
        return conn
    except sqlite3.Error as e:
        return None

def criacao_tabela_paciente():
    conn = get_db_connection()
    if conn is None:
        return
    try:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS pacientes (
            ID_pacientes INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            Nome VARCHAR NOT NULL,
            Email VARCHAR NOT NULL,
            Senha VARCHAR NOT NULL,
            Data_Nascimento DATE,
            Matricula INTEGER NOT NULL)''')
        conn.commit()
    except sqlite3.Error as e:
        print(f"Erro ao criar a tabela 'pacientes': {e}")
    finally:
        conn.close()

def criacao_tabela_anotacoes():
    conn = get_db_connection()
    if conn is None:
        return
    try:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS anotacoes (
            ID_Anotacoes INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            Anotacoes VARCHAR NOT NULL)''')
        conn.commit()
        print("Tabela 'anotacoes' criada com sucesso.")
    except sqlite3.Error as e:
        print(f"Erro ao criar a tabela 'anotacoes': {e}")
    finally:
        conn.close()

def criacao_tabela_psicologo():
    conn = get_db_connection()
    if conn is None:
        return
    try:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS psicologo (
            ID_psicologo INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            email VARCHAR NOT NULL,
            senha VARCHAR NOT NULL)''')
        conn.commit()
        print("Tabela 'psicologo' criada com sucesso.")
    except sqlite3.Error as e:
        print(f"Erro ao criar a tabela 'psicologo': {e}")
    finally:
        conn.close()

def criacao_tabela_horarios():
    conn = get_db_connection()
    if conn is None:
        return
    try:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS horarios (
            ID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            start TEXT NOT NULL,
            end TEXT NOT NULL)''')
        conn.commit()
        print("Tabela 'horarios' criada com sucesso.")
    except sqlite3.Error as e:
        print(f"Erro ao criar a tabela 'horarios': {e}")
    finally:
        conn.close()

def insert_paciente(nome, email, senha, data_nascimento, matricula):
    conn = get_db_connection()
    if conn is None:
        return
    try:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO pacientes (Nome, Email, Senha, Data_Nascimento, Matricula) 
            VALUES (?, ?, ?, ?, ?)''', (nome, email, senha, data_nascimento, matricula))
        conn.commit()
    except sqlite3.Error as e:
        print(f"Erro ao inserir paciente: {e}")
    finally:
        conn.close()

def insert_psicologo(email,senha):
    conn = get_db_connection()
    if conn is None:
        return
    try:
        cursor = conn.cursor()
        cursor.execute('''INSERT INTO psicologo (email, senha)
                       VALUES(?,?)''', (email, senha))
        conn.commit()
    except sqlite3.Error as e:
        print(f"Erro ao inserir paciente: {e}")
    finally:
        conn.close()

def check_login(email, senha):
    conn = get_db_connection()
    if conn is None:
        return None
    try:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM pacientes WHERE Email = ? AND Senha = ?', (email, senha))
        user = cursor.fetchone()
        return user
    except sqlite3.Error as e:
        print(f"Erro ao verificar login: {e}")
        return None
    finally:
        conn.close()

def check_login_psicologo(email, senha):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM psicologo WHERE email = ? AND senha = ?', (email, senha))
    user = cursor.fetchone()
    conn.close()
    return user

def insert_event(title, start, end):
    conn = get_db_connection()
    if conn is None:
        return
    try:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO horarios (title, start, end) 
            VALUES (?, ?, ?)''', (title, start, end))
        conn.commit()
    except sqlite3.Error as e:
        print(f"Erro ao inserir evento: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    criacao_tabela_paciente()
    criacao_tabela_anotacoes()
    criacao_tabela_psicologo()
    criacao_tabela_horarios()

    if os.path.exists('banco_de_dados.db'):
        print("Banco de dados e tabelas criados com sucesso!")
    else:
        print("Banco de dados não foi criado.")
