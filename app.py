from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from datetime import datetime
import sqlite3
import os

app = Flask(__name__)
app.secret_key = 'atendimento_psicologico_personalizado'

# Função para verificar login do paciente
def check_login(email, senha):
    conn = sqlite3.connect('banco_de_dados.db')
    cursor = conn.cursor()
    cursor.execute('SELECT ID_pacientes FROM pacientes WHERE email=? AND senha=?', (email, senha))
    user = cursor.fetchone()
    conn.close()
    return user

# Rota inicial
@app.route('/')
def home():
    return render_template('login.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        senha = request.form.get('senha')

        if not email or not senha:
            flash('Todos os campos são obrigatórios.', 'danger')
            return render_template('login.html')

        user = check_login(email, senha)
        if user:
            session['user_id'] = user[0]
            return redirect(url_for('selecao_atendimento'))
        else:
            flash('Email ou senha inválidos', 'danger')

    return render_template('login.html')

@app.route('/telapaciente')
def telapaciente():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('telapaciente.html')

@app.route('/selecaoatendimento')
def selecao_atendimento():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('selecao_atendimento.html')

@app.route('/telapsicologo')
def telapsicologo():
    if 'user_id' not in session:
        return redirect(url_for('login_psicologo'))
    return render_template('telapsicologo.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('login'))

@app.route('/get_events')
def get_events():
    conn = sqlite3.connect('banco_de_dados.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute('SELECT title, start, end FROM horarios')
    events = cursor.fetchall()
    conn.close()

    formatted_events = [
        {
            'title': event['title'],
            'start': event['start'],
            'end': event['end']
        } 
        for event in events
    ]

    return jsonify(formatted_events)

@app.route('/add_event', methods=['POST'])
def add_event():
    data = request.get_json()
    title = data['title']
    start = data['start']
    end = data['end']
    
    conn = sqlite3.connect('banco_de_dados.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO horarios (title, start, end) VALUES (?, ?, ?)', (title, start, end))
    conn.commit()
    conn.close()

    return jsonify({'status': 'success'})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))  # Render define a variável PORT automaticamente
    app.run(host='0.0.0.0', port=port, debug=True)
