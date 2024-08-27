from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite

app = Flask(__name__)
app.secret_key = 'sua_chave_secreta'

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
            session['user_id'] = user['id']
            return redirect(url_for('telapaciente'))
        else:
            flash('Email ou senha inválidos', 'danger')

    return render_template('login.html')

@app.route('/login_psicologo')
def login_psicologo():
    if request.method == 'POST':
        email = request.form.get('email')
        senha = request.form.get('senha')
        if not email or not senha:
            flash('Todos os campos são obrigatórios.', 'danger')
            return render_template('login_psicologo')
        user = sqlite.check_login(email, senha)
        if user:
            session['user_id'] = user['user']
            return redirect(url_for('telapsicologo'))
        else:
            flash('Email ou senha inválidos', 'danger')          
            
    return render_template('login_psicologo.html')

#testando
@app.route('/telapsicologo', methods=['GET', 'POST'])
def telapsicologo_login():
    """if request.method == 'POST':
        email = request.form.get('email')
        senha = request.form.get('senha')
        
        if not email or not senha:
            flash('Todos os campos são obrigatórios.', 'danger')    
            return render_template('login.html')

        user = sqlite.check_login(email, senha)
        if user:
            session['user_id'] = user['id']
            return redirect(url_for('telapsicologo'))
        else:
            flash('Email ou senha inválidos', 'danger')"""

    return render_template('telapsicologo.html')
#testando
@app.route('/telapaciente')
def telapaciente():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('telapaciente.html')

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
        #cpf = request.form.get('cpf')
        matricula = request.form.get('matricula')

        if not nome or not email or not senha or not data_nascimento or not matricula:
            flash('Todos os campos são obrigatórios.', 'danger')
            return render_template('cadastro.html')

        sqlite.insert_paciente(nome, email, senha, data_nascimento, matricula)
        return redirect(url_for('home'))

    return render_template('cadastro.html')

@app.route('/anotacao_paciente', methods=['GET', 'POST'])
def anotacao_paciente():
    # Sobre esta função: É só uma base para pode registrar as anotações
    # Vai ser necessário adaptar de acordo com a página que será criada
    if request.method == 'POST':
        nome_paciente = request.form.get('nome_paciente')
        anotacao_paciente = request.form.get('anotacao_paciente')

        if not nome_paciente or not anotacao_paciente:
            flash('Todos os campos são obrigatórios.', 'danger')
            return render_template('anotacao_paciente.html')

        sqlite.insert_anotacao(nome_paciente, anotacao_paciente)
        return redirect(url_for('home'))

    return render_template('anotacao_paciente.html')

if __name__ == '__main__':
    app.run(debug=True)
