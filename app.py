from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
import sqlite

app = Flask(__name__)
app.secret_key = 'atendimento_psicologico_personalizado'

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

        user = sqlite.check_login(email, senha)
        if user:
            session['user_id'] = user['ID_pacientes']
            return redirect(url_for('telapaciente'))
        else:
            flash('Email ou senha inválidos', 'danger')

    return render_template('login.html')

@app.route('/login_psicologo', methods=['GET', 'POST'])
def login_psicologo():
    if request.method == 'POST':
        email = request.form.get('email')
        senha = request.form.get('senha')

        if not email or not senha:
            flash('Todos os campos são obrigatórios.', 'danger')
            return render_template('login_psicologo')

        user = sqlite.check_login(email, senha)
        if user:
            session['user_id'] = user['ID_psicologo']
            return redirect(url_for('telapsicologo'))
        else:
            flash('Email ou senha inválidos', 'danger')

    return render_template('login_psicologo.html')

@app.route('/telapaciente')
def telapaciente():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('telapaciente.html')

@app.route('/agendar_consulta')
def agendar_consulta():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('agendar_consulta.html')

@app.route('/logout', methods=['POST'])
def logout():
    session.pop('user_id', None)
    return redirect(url_for('login'))

@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        nome = request.form.get('nome')
        email = request.form.get('email')
        senha = request.form.get('senha')
        data_nascimento = request.form.get('data_nascimento')
        matricula = request.form.get('matricula')

        if not nome or not email or not senha or not data_nascimento or not matricula:
            flash('Todos os campos são obrigatórios.', 'danger')
            return render_template('cadastro.html')

        sqlite.insert_paciente(nome, email, senha, data_nascimento, matricula)
        flash('Cadastro realizado com sucesso!', 'success')
        return redirect(url_for('home'))

    return render_template('cadastro.html')

@app.route('/anotacao_paciente', methods=['GET', 'POST'])
def anotacao_paciente():
    if request.method == 'POST':
        nome_paciente = request.form.get('nome_paciente')
        anotacao_paciente = request.form.get('anotacao_paciente')

        if not nome_paciente or not anotacao_paciente:
            flash('Todos os campos são obrigatórios.', 'danger')
            return render_template('anotacao_paciente.html')

        sqlite.insert_anotacao(nome_paciente, anotacao_paciente)
        return redirect(url_for('home'))

    return render_template('anotacao_paciente.html')

@app.route('/cadastrarhorario')
def cadastrarhorario():
    if 'user_id' not in session:
        return redirect(url_for('login_psicologo'))
    return render_template('cadastrarhorario.html')

@app.route('/get_events')
def get_events():
    conn = sqlite.get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM horarios')
    events = cursor.fetchall()
    conn.close()
    return jsonify([{
        'title': event['title'],
        'start': event['start'],
        'end': event['end']
    } for event in events])

@app.route('/add_event', methods=['POST'])
def add_event():
    data = request.get_json()
    title = data['title']
    start = data['start']
    end = data['end']
    conn = sqlite.get_db_connection()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO horarios (title, start, end) VALUES (?, ?, ?)', (title, start, end))
    conn.commit()
    conn.close()
    return jsonify({'status': 'success'})

if __name__ == '__main__':
    app.run(debug=True)
