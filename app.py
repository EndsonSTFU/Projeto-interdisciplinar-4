from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from datetime import datetime
<<<<<<< HEAD
import sqlite
import sqlite3


=======
import sqlite3

>>>>>>> 7a963580531f4730819175fb12116f251e786879
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

@app.route('/telapaciente')
def telapaciente():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('telapaciente.html')

@app.route('/login_psicologo', methods=['GET', 'POST'])
def login_psicologo():
    if request.method == 'POST':
        email = request.form.get('email')
        senha = request.form.get('senha')

        if not email or not senha:
            flash('Todos os campos são obrigatórios.', 'danger')
            return render_template('login_psicologo.html')

        user = sqlite.check_psicologo_login(email, senha)
        if user:
            session['user_id'] = user['ID_psicologo']
            return redirect(url_for('telapsicologo'))
        else:
            flash('Email ou senha inválidos', 'danger')

    return render_template('login_psicologo.html')

@app.route('/telapsicologo')
def telapsicologo():
    if 'user_id' not in session:
        return redirect(url_for('login_psicologo'))
    return render_template('telapsicologo.html')


@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login_psicologo'))

    user_id = session['user_id']
    
    user = sqlite.get_psicologo_by_id(user_id)
    if user is None:
        flash('Usuário não encontrado.', 'danger')
        return redirect(url_for('login_psicologo'))
    
    horarios = sqlite.get_all_horarios()

    return render_template('dashboard.html', email=user['email'], senha=user['senha'], horarios=horarios)

@app.route('/agendar_consulta', methods=['GET', 'POST'])
def agendar_consulta():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        title = request.form.get('title')
        start = request.form.get('start')

        if not title or not start:
            flash('Todos os campos são obrigatórios.', 'danger')
            return render_template('agendar_consulta.html')
        
        try:
            sqlite.insert_horario(title, start)
            flash('Consulta agendada com sucesso!', 'success')
            return redirect(url_for('agendar_consulta'))
        except Exception as e:
            flash(f'Ocorreu um erro: {e}', 'danger')
            return render_template('agendar_consulta.html')
    
    return render_template('agendar_consulta.html')

@app.route('/anotacoes_pacientes', methods=['GET', 'POST'])
def anotacoes_pacientes():
    if 'user_id' not in session:
        return redirect(url_for('login_psicologo'))

    if request.method == 'POST':
        paciente_id = request.form.get('paciente')
        anotacao = request.form.get('anotacao')

        if not paciente_id or not anotacao:
            flash('Todos os campos são obrigatórios.', 'danger')
            return render_template('anotacoes_pacientes.html', pacientes=sqlite.get_pacientes())

        sqlite.save_anotacao(paciente_id, anotacao)
        flash('Anotação salva com sucesso!', 'success')

    return render_template('anotacoes_pacientes.html', pacientes=sqlite.get_pacientes())

@app.route('/salvar_anotacao/<int:id>', methods=['GET', 'POST'])
def salvar_anotacao(id):
    if 'user_id' not in session:
        return redirect(url_for('login_psicologo'))

    paciente = sqlite.get_paciente(id)
    if request.method == 'POST':
        anotacao = request.form.get('anotacao')

        if not anotacao:
            flash('Todos os campos são obrigatórios.', 'danger')
            return render_template('salvar_anotacao.html', paciente=paciente, id=id)

        sqlite.save_anotacao(id, anotacao)
        flash('Anotação salva com sucesso!', 'success')
        return redirect(url_for('anotacoes_pacientes'))

    return render_template('salvar_anotacao.html', paciente=paciente, id=id)

@app.route('/detalhes_paciente/<int:id>', methods=['GET'])
def detalhes_paciente(id):
    if 'user_id' not in session:
        return redirect(url_for('login_psicologo'))

    paciente = sqlite.get_paciente(id)

    if not paciente:
        flash('Paciente não encontrado.', 'danger')
        return redirect(url_for('dashboard'))

    anotacoes = sqlite.get_paciente_anotacoes(id)
    anotacoes = anotacoes['anotacoes']
    return render_template('detalhes_paciente.html', paciente=paciente, anotacoes=anotacoes, id=id)


@app.route('/logout', methods=['GET', 'POST'])
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

@app.route('/cadastro_psicologo', methods=['GET', 'POST'])
def cadastro_psicologo():
    if request.method == 'POST':
        email = request.form.get('email')
        senha = request.form.get('senha')
        if not email or not senha:
            flash('Todos os campos são obrigatórios.', 'danger')
            return render_template('cadastro_psicologo.html')
        sqlite.insert_psicologo(email, senha) 
        flash('Cadastro realizado com sucesso!', 'success')
        return redirect(url_for('login_psicologo'))
    return render_template('cadastro_psicologo.html')

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
