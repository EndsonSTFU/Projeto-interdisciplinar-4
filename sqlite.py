import sqlite3
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Caminho do SQLite dentro do container
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DB_PATH = os.path.join(BASE_DIR, "banco_de_dados.db")
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{DB_PATH}"
db = SQLAlchemy(app)

# Função para conectar ao banco de dados
def get_db_connection():
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        return conn
    except sqlite3.Error as e:
        print(f"Erro ao conectar ao banco de dados: {e}")
        return None

# Função para criar a tabela de pacientes
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

# Função para criar a tabela de anotações
def criacao_tabela_anotacoes():
    conn = get_db_connection()
    if conn is None:
        return
    try:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS anotacoes (
            ID_anotacao INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            ID_paciente INTEGER NOT NULL,
            ID_psicologo INTEGER NOT NULL,
            Texto TEXT NOT NULL,
            Data DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(ID_paciente) REFERENCES pacientes(ID_pacientes),
            FOREIGN KEY(ID_psicologo) REFERENCES psicologos(ID_psicologos))''')
        conn.commit()
    except sqlite3.Error as e:
        print(f"Erro ao criar a tabela 'anotacoes': {e}")
    finally:
        conn.close()

# Função para criar a tabela de psicólogos
def criacao_tabela_psicologo():
    conn = get_db_connection()
    if conn is None:
        return
    try:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS psicologos (
            ID_psicologos INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            Nome VARCHAR NOT NULL,
            Email VARCHAR NOT NULL,
            Senha VARCHAR NOT NULL)''')
        conn.commit()
    except sqlite3.Error as e:
        print(f"Erro ao criar a tabela 'psicologos': {e}")
    finally:
        conn.close()

# Função para criar a tabela de horários
def criacao_tabela_horarios():
    conn = get_db_connection()
    if conn is None:
        return
    try:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS horarios (
            ID_horario INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            ID_psicologo INTEGER NOT NULL,
            Data_Horario DATETIME NOT NULL,
            Disponivel BOOLEAN NOT NULL DEFAULT 1,
            FOREIGN KEY(ID_psicologo) REFERENCES psicologos(ID_psicologos))''')
        conn.commit()
    except sqlite3.Error as e:
        print(f"Erro ao criar a tabela 'horarios': {e}")
    finally:
        conn.close()

# Função para criar a tabela de pedagogos
def criacao_tabela_pedagogo():
    conn = get_db_connection()
    if conn is None:
        return
    try:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS pedagogos (
            ID_pedagogo INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            Nome VARCHAR NOT NULL,
            Email VARCHAR NOT NULL,
            Senha VARCHAR NOT NULL)''')
        conn.commit()
    except sqlite3.Error as e:
        print(f"Erro ao criar a tabela 'pedagogos': {e}")
    finally:
        conn.close()

# Verifica se as tabelas foram criadas corretamente
if __name__ == "__main__":
    criacao_tabela_paciente()
    criacao_tabela_anotacoes()
    criacao_tabela_psicologo()
    criacao_tabela_horarios()
    criacao_tabela_pedagogo()

    if os.path.exists(DB_PATH):
        print("Banco de dados e tabelas criados com sucesso!")
    else:
        print("Banco de dados não foi criado.")

    # Inicia o servidor Flask
    app.run(host='0.0.0.0', port=5000)

# Rota principal do Flask
@app.route('/')
def home():
    return "Plataforma de Agendamento Online!"
