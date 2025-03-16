from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from datetime import datetime
from pymongo import MongoClient
from werkzeug.security import check_password_hash, generate_password_hash
import certifi
from bson import ObjectId
from bson import ObjectId
from bson.errors import InvalidId

app = Flask(__name__)
app.secret_key = 'atendimento_psicologico_personalizado'

client = MongoClient("mongodb+srv://jordao125:y3jcym4CfZMTBOyg@naps.ucftl.mongodb.net/",tls=True,tlsCAFile=certifi.where())
db = client["plataforma_agendamento"]

pacientes_col = db["pacientes"]
psicologos_col = db["psicologos"]
horarios_col = db["horarios"]
anotacoes_col = db["anotacoes"]
mensagens_col = db["mensagens_bot"]
pedagogos_col = db["pedagogo"]
enfermeiro_col = db["enfermeira"]

def check_login(email, senha):
    user = pacientes_col.find_one({"Email": email})
    if user and check_password_hash(user["Senha"], senha):
        return user
    return None

def check_psicologo_login(email, senha):
    user = psicologos_col.find_one({"Email": email})
    if user and check_password_hash(user["Senha"], senha):
        return user
    return None

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
            return redirect(url_for('telapaciente'))
        else:
            flash('Email ou senha inválidos', 'danger')

    return render_template('login.html')

@app.route('/telapaciente')
def telapaciente():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('telapaciente.html')

@app.route('/login_colaborador', methods=['GET', 'POST'])
def login_colaborador():
    if request.method == 'POST':
        email = request.form.get('email')
        senha = request.form.get('senha')

        if not email or not senha:
            flash('Todos os campos são obrigatórios.', 'danger')
            return render_template('login_colaborador.html')

        user = psicologos_col.find_one({"Email": email})
        if user and check_password_hash(user["Senha"], senha):
            session['user_id'] = str(user["_id"])
            session['psicologo_nome'] = user["Nome"]
            return redirect(url_for('telapsicologo'))
        else:
            flash('Email ou senha inválidos', 'danger')

    return render_template('login_colaborador.html')


@app.route('/telapsicologo')
def telapsicologo():
    if 'user_id' not in session:
        return redirect(url_for('login_colaborador'))
    return render_template('telapsicologo.html')

@app.route('/agendar_consulta')
def agendar_consulta():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    horarios = list(horarios_col.find({}, {"_id": 0}))
    return render_template('agendar_consulta.html', horarios=horarios)

@app.route('/agendar_horario', methods=['POST'])
def agendar_horario():
    if 'user_id' not in session:
        return jsonify({"status": "error", "message": "Usuário não autenticado"}), 401

    data = request.get_json()
    horario = data.get('horario')  # O horário que o paciente está tentando agendar

    if not horario:
        return jsonify({"status": "error", "message": "Horário não fornecido"}), 400

    # Verifica se o horário já está agendado
    horario_existente = horarios_col.find_one({"start": horario, "paciente_id": {"$ne": None}})
    if horario_existente:
        return jsonify({"status": "error", "message": "Desculpe, horário já reservado"}), 400

    # Busca o paciente no banco de dados
    paciente_id = session['user_id']
    paciente = pacientes_col.find_one({"_id": ObjectId(paciente_id)})

    if not paciente:
        return jsonify({"status": "error", "message": "Paciente não encontrado"}), 404

    # Atualiza o horário com o ID e nome do paciente
    horarios_col.update_one(
        {"start": horario},
        {"$set": {"paciente_id": paciente_id, "paciente_nome": paciente["Nome"]}}
    )

    return jsonify({"status": "success"})
@app.route('/verificadesabafo')
def verificadesabafo():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    try:
        mensagens = list(mensagens_col.find({}, {"_id": 0}))
        return render_template('verificadesabafo.html', mensagens=mensagens)
    except Exception as e:
        return f"Erro ao acessar o banco de dados: {e}", 500

    
@app.route('/anotacoes_pacientes', methods=['GET', 'POST'])
def anotacoes_pacientes():
    if 'user_id' not in session:
        return redirect(url_for('login_colaborador'))

    pacientes = list(pacientes_col.find({}, {"_id": 1, "Nome": 1})) 

    if request.method == 'POST':
        paciente_id = request.form.get('paciente')
        anotacao = request.form.get('anotacao')

        if not paciente_id or not anotacao:
            flash('Todos os campos são obrigatórios.', 'danger')
            return render_template('anotacoes_pacientes.html', pacientes=pacientes)

        anotacoes_col.insert_one({
            "paciente_id": paciente_id,
            "anotacao": anotacao,
            "psicologo_nome": session.get('psicologo_nome', 'Psicólogo Desconhecido')
        })
        flash('Anotação salva com sucesso!', 'success')

    return render_template('anotacoes_pacientes.html', pacientes=pacientes)

@app.route('/salvar_anotacao/<string:id>', methods=['GET', 'POST'])
def salvar_anotacao(id):
    if 'user_id' not in session:
        return redirect(url_for('login_colaborador'))

    try:

        paciente_id = ObjectId(id)
    except:
        flash('ID do paciente inválido.', 'danger')
        return redirect(url_for('anotacoes_pacientes'))

    paciente = pacientes_col.find_one({"_id": paciente_id})
    if not paciente:
        flash('Paciente não encontrado.', 'danger')
        return redirect(url_for('anotacoes_pacientes'))

    if request.method == 'POST':
        anotacao = request.form.get('anotacao')

        if not anotacao:
            flash('A anotação não pode estar vazia.', 'danger')
            return render_template('salvar_anotacao.html', paciente=paciente, id=id)

        anotacoes_col.insert_one({
            "paciente_id": str(paciente_id), 
            "anotacao": anotacao,
            "psicologo_nome": session.get('psicologo_nome', 'Psicólogo Desconhecido')
        })
        flash('Anotação salva com sucesso!', 'success')
        return redirect(url_for('detalhes_paciente', paciente_id=str(paciente_id)))

    return render_template('salvar_anotacao.html', paciente=paciente, id=id)

@app.route('/detalhes_paciente/<string:paciente_id>', methods=['GET'])
def detalhes_paciente(paciente_id):
    if 'user_id' not in session:
        return redirect(url_for('login_colaborador'))

    try:
        paciente_id = ObjectId(paciente_id)
    except:
        flash('ID do paciente inválido.', 'danger')
        return redirect(url_for('anotacoes_pacientes'))

    paciente = pacientes_col.find_one({"_id": paciente_id})
    if not paciente:
        flash('Paciente não encontrado.', 'danger')
        return redirect(url_for('anotacoes_pacientes'))

    anotacoes = list(anotacoes_col.find({"paciente_id": str(paciente_id)}, {"_id": 0}))

    return render_template('detalhes_paciente.html', paciente=paciente, anotacoes=anotacoes, id=str(paciente_id))

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

        if pacientes_col.find_one({"Email": email}):
            flash('Email já cadastrado.', 'danger')
            return render_template('cadastro.html')

        senha_hash = generate_password_hash(senha)
        paciente = {
            "Nome": nome,
            "Email": email,
            "Senha": senha_hash,
            "DataNascimento": data_nascimento,
            "Matricula": matricula
        }
        pacientes_col.insert_one(paciente)
        flash('Cadastro realizado com sucesso!', 'success')
        return redirect(url_for('home'))

    return render_template('cadastro.html')

@app.route('/verificar_senha_psicologo', methods=['GET', 'POST'])
def verificar_senha_psicologo():
    if request.method == 'POST':
        senha_acesso = request.form.get('senha_acesso')       
        senha_acesso_correta = "atendiNAPS2024!"
        
        if senha_acesso == senha_acesso_correta:
            return redirect(url_for('cadastrocolaborador'))
        else:
            flash('Senha de acesso incorreta.', 'danger')
    
    return render_template('verificar_senha_psicologo.html')

@app.route('/cadastrocolaborador')
def cadastrocolaborador():
    return render_template('cadastrocolaborador.html')

@app.route('/cadastro_psicologo', methods=['GET', 'POST'])
def cadastro_psicologo():
    if request.method == 'POST':
        nome = request.form.get('nome')
        especialidade = request.form.get('especialidade')
        email = request.form.get('email')
        senha = request.form.get('senha')

        if not nome or not especialidade or not email or not senha:
            flash('Todos os campos são obrigatórios.', 'danger')
            return render_template('cadastro_psicologo.html')

        if psicologos_col.find_one({"Email": email}):
            flash('Email já cadastrado.', 'danger')
            return render_template('cadastro_psicologo.html')

        senha_hash = generate_password_hash(senha)
        psicologo = {
            "Nome": nome,
            "Especialidade": especialidade,
            "Email": email,
            "Senha": senha_hash
        }
        psicologos_col.insert_one(psicologo)
        flash('Cadastro realizado com sucesso!', 'success')
        return redirect(url_for('login_colaborador'))
    return render_template('cadastro_psicologo.html')

@app.route('/cadastro_pedagogo', methods=['GET', 'POST'])
def cadastro_pedagogo():
    if request.method == 'POST':
        nome = request.form.get('nome')
        especialidade = request.form.get('especialidade')
        email = request.form.get('email')
        senha = request.form.get('senha')

        if not nome or not especialidade or not email or not senha:
            flash('Todos os campos são obrigatórios.', 'danger')
            return render_template('cadastro_pedagogo.html')

        if pedagogos_col.find_one({"Email": email}):
            flash('Email já cadastrado.', 'danger')
            return render_template('cadastro_pedagogo.html')

        senha_hash = generate_password_hash(senha)
        pedagogo = {
            "Nome": nome,
            "Especialidade": especialidade,
            "Email": email,
            "Senha": senha_hash
        }
        pedagogos_col.insert_one(pedagogo)
        flash('Cadastro realizado com sucesso!', 'success')
        return redirect(url_for('login_colaborador'))
    return render_template('cadastro_pedagogo.html')

@app.route('/cadastro_enfermeira', methods=['GET', 'POST'])
def cadastro_enfermeira():
    if request.method == 'POST':
        nome = request.form.get('nome')
        especialidade = request.form.get('especialidade')
        email = request.form.get('email')
        senha = request.form.get('senha')

        if not nome or not especialidade or not email or not senha:
            flash('Todos os campos são obrigatórios.', 'danger')
            return render_template('cadastro_enfermeira.html')

        if enfermeiro_col.find_one({"Email": email}):
            flash('Email já cadastrado.', 'danger')
            return render_template('cadastro_enfermeira.html')

        senha_hash = generate_password_hash(senha)
        enfermeira = {
            "Nome": nome,
            "Especialidade": especialidade,
            "Email": email,
            "Senha": senha_hash
        }
        enfermeiro_col.insert_one(enfermeira)

        flash('Cadastro realizado com sucesso!', 'success')
        return redirect(url_for('login_colaborador'))
    return render_template('cadastro_enfermeira.html')

@app.route('/cadastrarhorario')
def cadastrarhorario():
    if 'user_id' not in session:
        return redirect(url_for('login_colaborador'))
    return render_template('cadastrarhorario.html')


@app.route('/get_events')
def get_events():
    eventos = list(horarios_col.find({}, {"_id": 0}))
    return jsonify(eventos)

@app.route('/add_event', methods=['POST'])
def add_event():
    if 'user_id' not in session:
        return jsonify({"status": "error", "message": "Usuário não autenticado"}), 401

    data = request.get_json()
    title = data.get('title')
    start = data.get('start')
    end = data.get('end')

    if not title or not start or not end:
        return jsonify({"status": "error", "message": "Dados incompletos"}), 400


    psicologo_nome = session.get('psicologo_nome', 'Psicólogo Desconhecido')


    horarios_col.insert_one({
        "title": title,
        "start": start,
        "end": end,
        "psicologo_nome": psicologo_nome
    })

    return jsonify({"status": "success"})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)