from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('banco_de_dados.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def home():
    return render_template('login.html')

@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        senha = request.form['senha']
        data_nascimento = request.form['data_nascimento']
        cpf = request.form['cpf']
        matricula = request.form['matricula']

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO pacientes (nome, email, senha, data_nascimento, cpf, matricula)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (nome, email, senha, data_nascimento, cpf, matricula))
        conn.commit()
        conn.close()
        return redirect(url_for('home'))

    return render_template('cadastro.html')

if __name__ == '__main__':
    app.run(debug=True)

