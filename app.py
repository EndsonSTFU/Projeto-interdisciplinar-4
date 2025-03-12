from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from pymongo import MongoClient
import os

app = Flask(__name__)
app.secret_key = 'atendimento_psicologico_personalizado'

# 🔹 Conexão com MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["plataforma_agendamento"]

# 🔹 Função para verificar login do paciente
def check_login(email, senha):
    user = db.pacientes.find_one({"Email": email, "Senha": senha})
    return user

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
    events = list(db.horarios.find({}, {"_id": 0, "title": 1, "start": 1, "end": 1}))
    return jsonify(events)

# 🔹 Rota para adicionar um novo evento
@app.route('/add_event', methods=['POST'])
def add_event():
    data = request.get_json()
    db.horarios.insert_one({
        "title": data["title"],
        "start": data["start"],
        "end": data["end"]
    })
    return jsonify({'status': 'success'})

# 🔹 Iniciar a aplicação Flask
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))  # Render define a variável PORT automaticamente
    app.run(host='0.0.0.0', port=port, debug=True)
