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
                ID_anotacoes INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                ID_pacientes INTEGER NOT NULL,
                Anotacoes TEXT NOT NULL,
                FOREIGN KEY (ID_pacientes) REFERENCES pacientes(ID_pacientes)
            )
        ''')
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

def criacao_tabela_pedagogo():
    conn = get_db_connection()
    if conn is None:
        return
    try:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS pedagogo (
            ID_pedagogo INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            email VARCHAR NOT NULL,
            senha VARCHAR NOT NULL)''')
        conn.commit()
        print("Tabela 'pedagogo' criada com sucesso.")
    except sqlite3.Error as e:
        print(f"Erro ao criar a tabela 'pedagogo': {e}")
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

def check_psicologo_login(email, senha):
    conn = get_db_connection()
    if conn is None:
        return None
    try:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM psicologo WHERE Email = ? AND Senha = ?', (email, senha))
        user = cursor.fetchone()
        return user
    except sqlite3.Error as e:
        print(f"Erro ao verificar login: {e}")
        return None
    finally:
        conn.close()

def check_pedagogo_login(email, senha):
    conn = get_db_connection()
    if conn is None:
        return None
    try:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM pedagogo WHERE Email = ? AND Senha = ?', (email, senha))
        user = cursor.fetchone()
        return user
    except sqlite3.Error as e:
        print(f"Erro ao verificar login: {e}")
        return None
    finally:
        conn.close()

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

def insert_psicologo(email, senha):
    conn = get_db_connection()
    if conn is None:
        return
    try:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO psicologo (email, senha) 
            VALUES (?, ?)
        ''', (email, senha))
        conn.commit()
        print("Psicólogo inserido com sucesso.")
    except sqlite3.Error as e:
        print(f"Erro ao inserir psicólogo: {e}")
    finally:
        conn.close()

def insert_pedagogo(email, senha):
    conn = get_db_connection()
    if conn is None:
        return
    try:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO pedagogo (email, senha) 
            VALUES (?, ?)
        ''', (email, senha))
        conn.commit()
        print("Pedagogo inserido com sucesso.")
    except sqlite3.Error as e:
        print(f"Erro ao inserir pedagogo: {e}")
    finally:
        conn.close()

def test_psicologo():
    conn = get_db_connection()
    if conn is None:
        return
    try:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO psicologo (email, senha) 
            VALUES (?, ?)
        ''', ('fabio.psi@gmail.com', '1'))
        conn.commit()
        print("Psicólogo inserido com sucesso.")
    except sqlite3.Error as e:
        print(f"Erro ao inserir psicólogo: {e}")
    finally:
        conn.close()

def test_paciente():
    conn = get_db_connection()
    if conn is None:
        return
    try:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO pacientes (nome, Email, Senha, Data_Nascimento, Matricula)
            VALUES (?, ?, ?, ?, ?)
        ''', ('Jean Arruda', 'jeangui.arruda@gmail.com', 'jean2706', '2003-06-27', '131131131131'))
        conn.commit()

        cursor.execute('''
            INSERT INTO pacientes (nome, Email, Senha, Data_Nascimento, Matricula)
            VALUES (?, ?, ?, ?, ?)
        ''', ('José Bezerra', 'josebezerra@gmail.com', 'jose123456', '1990-06-27', '1234567890'))
        conn.commit()

        print("Paciente inserido com sucesso.")
    except sqlite3.Error as e:
        print(f"Erro ao inserir paciente: {e}")
    finally:
        conn.close()

def insert_horario(title, start):
    conn = get_db_connection()
    if conn is None:
        return
    try:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO horarios (title, start) 
            VALUES (?, ?)
        ''', (title, start))
        conn.commit()
        print("Horário inserido com sucesso.")
    except sqlite3.Error as e:
        print(f"Erro ao inserir horário: {e}")
    finally:
        conn.close()

def get_psicologo_by_id(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT email, senha FROM psicologo WHERE ID_psicologo = ?', (user_id,))
    user = cursor.fetchone()
    conn.close()
    return {'email': user[0], 'senha': user[1]} if user else None

def get_all_horarios():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM horarios')
    horarios = cursor.fetchall()
    conn.close()
    return [{'ID': h[0], 'title': h[1], 'start': h[2]} for h in horarios]

def get_paciente(paciente_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('SELECT nome, email, data_nascimento, matricula FROM pacientes WHERE ID_pacientes = ?', (paciente_id,))
    paciente = cursor.fetchone()
    conn.close()

    return {'nome': paciente[0], 'email': paciente[1], 'data_nascimento': paciente[2], 'matricula': paciente[3]}

def get_pacientes():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT ID_pacientes, nome FROM pacientes')
    pacientes = cursor.fetchall()
    conn.close()
    return [{'ID': p[0], 'nome': p[1]} for p in pacientes]

def get_paciente_anotacoes(paciente_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute('''
            SELECT anotacoes
            FROM anotacoes
            WHERE ID_pacientes = ?
        ''', (paciente_id,))
        anotacoes = cursor.fetchall()

        anotacoes_data = [a[0] for a in anotacoes]

        return {
            'anotacoes': anotacoes_data
        }
    
    except sqlite3.Error as e:
        print(f"Erro ao acessar o banco de dados: {e}")
        return {'error': 'Erro ao acessar o banco de dados'}

    finally:
        conn.close()

def save_anotacao(paciente_id, anotacao):
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute('INSERT INTO anotacoes (ID_pacientes, Anotacoes) VALUES (?, ?)', (paciente_id, anotacao))
        conn.commit()
    except sqlite3.Error as e:
        print(f"Erro ao salvar anotação: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    criacao_tabela_paciente()
    criacao_tabela_anotacoes()
    criacao_tabela_psicologo()
    criacao_tabela_horarios()
    criacao_tabela_pedagogo()
    test_psicologo()
    test_paciente()

    if os.path.exists('banco_de_dados.db'):
        print("Banco de dados e tabelas criados com sucesso!")
    else:
        print("Banco de dados não foi criado.")
