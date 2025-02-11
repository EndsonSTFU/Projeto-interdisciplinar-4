from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from datetime import datetime
import sqlite3

app = Flask(__name__)
app.secret_key = 'atendimento_psicologico_personalizado'

def check_login(email, senha):
    conn = sqlite3.connect('banco_de_dados.db')
    cursor = conn.cursor()
    cursor.execute('SELECT ID_pacientes FROM pacientes WHERE email = ? AND senha = ?', (email, senha))
    user = cursor.fetchone()
    conn.close()
    return user

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

@app.route('/agendar_consulta')
def agendar_consulta():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    conn = sqlite3.connect('banco_de_dados.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute('SELECT title, start, end FROM horarios')
    horarios = cursor.fetchall()
    conn.close()

    return render_template('agendar_consulta.html', horarios=horarios)

@app.route('/get_events')
def get_events():
    conn = sqlite3.connect('banco_de_dados.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute('SELECT title, start, end FROM horarios')
    events = cursor.fetchall()
    conn.close()

    formatted_events = []
    for event in events:
        formatted_event = {
            'title': event['title'],
            'start': datetime.fromisoformat(event['start']).isoformat(),
            'end': datetime.fromisoformat(event['end']).isoformat()
        }
        formatted_events.append(formatted_event)

    return jsonify(formatted_events)

@app.route('/add_event', methods=['POST'])
def add_event():
    data = request.get_json()
    title = data['title']
    start = datetime.fromisoformat(data['start']).isoformat()
    end = datetime.fromisoformat(data['end']).isoformat()
    conn = sqlite3.connect('banco_de_dados.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO horarios (title, start, end) VALUES (?, ?, ?)', (title, start, end))
    conn.commit()
    conn.close()
    return jsonify({'status': 'success'})

if __name__ == '__main__':
    app.run(debug=True)
