from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from pymongo import MongoClient
from werkzeug.security import check_password_hash
import os
from mongo import Paciente, Psicologo, Horario


app = Flask(__name__)
app.secret_key = 'atendimento_psicologico_personalizado'

# 🔹 Conexão com MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["plataforma_agendamento"]


# 🔹 Função para verificar login do paciente
def check_login(email, senha):
    user = db.pacientes.find_one({"Email": email})
    if user and check_password_hash(user["Senha"], senha):
        return user
    return None


# 🔹 Rota inicial
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
            session['user_id'] = str(user["_id"])
            return redirect(url_for('selecao_atendimento'))
        else:
            flash('Email ou senha inválidos', 'danger')

    return render_template('login.html')

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

        paciente = Paciente(db)
        resultado = paciente.inserir_paciente(nome, email, senha, data_nascimento, matricula)

        flash(resultado["message"], 'success' if resultado["status"] == "success" else 'danger')
        
        if resultado["status"] == "success":
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
        psicologos_col.insert_one({'email': email, 'senha': senha})
        flash('Cadastro realizado com sucesso!', 'success')
        return redirect(url_for('login_psicologo'))
    return render_template('cadastro_psicologo.html')

@app.route('/agendar_consulta', methods=['GET', 'POST'])
def agendar_consulta():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        title = request.form.get('title')
        start = request.form.get('start')
        end = request.form.get('end')
        if not title or not start or not end:
            flash('Todos os campos são obrigatórios.', 'danger')
        else:
            agendamentos_col.insert_one({
                'title': title,
                'start': start,
                'end': end
            })
            flash('Consulta agendada com sucesso!', 'success')
            return redirect(url_for('agendar_consulta'))
    horarios = list(agendamentos_col.find({}, {'_id': 0}))
    return render_template('agendar_consulta.html', horarios=horarios)


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
        return redirect(url_for('login'))
    return render_template('telapsicologo.html')


@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('login'))


# 🔹 Rota para buscar eventos agendados
@app.route('/get_events')
def get_events():
    events = list(db.horarios.find({}, {"_id": 0, "title": 1, "start": 1, "end": 1, "Psicologo": 1, "Paciente": 1}))
    return jsonify(events)


# 🔹 Rota para adicionar um novo evento
@app.route('/add_event', methods=['POST'])
def add_event():
    if 'user_id' not in session:
        return jsonify({'status': 'error', 'message': 'Usuário não autenticado'}), 401

    data = request.get_json()
    paciente = db.pacientes.find_one({"_id": session['user_id']})

    if not paciente:
        return jsonify({'status': 'error', 'message': 'Paciente não encontrado'}), 404

    if not all(key in data for key in ["title", "start", "end", "psicologo_email"]):
        return jsonify({'status': 'error', 'message': 'Dados incompletos'}), 400

    db.horarios.insert_one({
        "title": data["title"],
        "start": data["start"],
        "end": data["end"],
        "Psicologo": data["psicologo_email"],
        "Paciente": paciente["Email"]
    })
    return jsonify({'status': 'success'})


# 🔹 Iniciar a aplicação Flask
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))  # Render define a variável PORT automaticamente
    app.run(host='0.0.0.0', port=port, debug=True)
