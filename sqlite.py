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

# Chamando as funções para verificar se as tabelas estão sendo criadas
if __name__ == "__main__":
    criacao_tabela_paciente()
    criacao_tabela_anotacoes()
    criacao_tabela_psicologo()

    # Verifica se o arquivo foi criado no diretório atual
    if os.path.exists('banco_de_dados.db'):
        print("Banco de dados criado com sucesso!")
    else:
        print("Banco de dados não foi criado.")
