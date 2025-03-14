from pymongo import MongoClient
from bson import ObjectId
from werkzeug.security import generate_password_hash


# Conexão com MongoDB
client = MongoClient("mongodb+srv://jordao125:y3jcym4CfZMTBOyg@naps.ucftl.mongodb.net/")
db = client["plataforma_agendamento"]

# Coleções
pacientes_collection = db["pacientes"]
psicologos_collection = db["psicologos"]
horarios_collection = db["horarios"]


# 🔹 Classe Login Paciente
class Paciente:
    def __init__(self, nome, email, senha):
        self.nome = nome
        self.email = email
        self.senha = generate_password_hash(senha)  # Senha segura com hash    

    def salvar(self):
        paciente_id = pacientes_collection.insert_one({
            "Nome": self.nome,
            "Email": self.email,
            "Senha": self.senha
        }).inserted_id
        return str(paciente_id)
    
    def inserir_paciente(self, nome, email, senha, data_nascimento, matricula):
        if pacientes_collection.find_one({"Email": email}):
            return {"status": "error", "message": "Email já cadastrado"}

        senha_hash = generate_password_hash(senha)  # Criptografando a senha
        paciente = {
            "Nome": nome,
            "Email": email,
            "Senha": senha_hash,
            "DataNascimento": data_nascimento,
            "Matricula": matricula
        }
        pacientes_collection.insert_one(paciente)
        return {"status": "success", "message": "Cadastro realizado com sucesso!"}

    @staticmethod
    def buscar_por_email(email):
        return pacientes_collection.find_one({"Email": email})
  

# 🔹 Classe Psicólogo
class Psicologo:
    def __init__(self, nome, email, especialidade):
        self.nome = nome
        self.email = email
        self.especialidade = especialidade

    def salvar(self):
        psicologo_id = psicologos_collection.insert_one({
            "Nome": self.nome,
            "Email": self.email,
            "Especialidade": self.especialidade
        }).inserted_id
        return str(psicologo_id)

    @staticmethod
    def buscar_por_email(email):
        return psicologos_collection.find_one({"Email": email})


# 🔹 Classe Horário
class Horario:
    def __init__(self, psicologo_email, paciente_email, data_inicio, data_fim):
        self.psicologo_email = psicologo_email
        self.paciente_email = paciente_email
        self.data_inicio = data_inicio
        self.data_fim = data_fim

    def salvar(self):
        horario_id = horarios_collection.insert_one({
            "Psicologo": self.psicologo_email,
            "Paciente": self.paciente_email,
            "Start": self.data_inicio,
            "End": self.data_fim
        }).inserted_id
        return str(horario_id)

    @staticmethod
    def listar_horarios():
        return list(horarios_collection.find({}, {"_id": 0}))


# 🔹 Testando a conexão com o banco de dados
if __name__ == "__main__":
    print("Testando conexão com o banco de dados...")
    try:
        # Listando as coleções do banco de dados
        print("Coleções no banco de dados:", db.list_collection_names())
    except Exception as e:
        print("Erro ao conectar ao MongoDB Atlas:", e)

# 🔹 Criando dados iniciais
if __name__ == "__main__":
    print("Inserindo dados de exemplo...")

    # Criando um paciente
    paciente1 = Paciente("João da Silva", "joao@email.com", "123456")
    paciente_id = paciente1.salvar()
    print(f"Paciente criado com ID: {paciente_id}")

    # Criando um psicólogo
    psicologo1 = Psicologo("Dra. Ana", "ana@psicologa.com", "Terapia Cognitiva")
    psicologo_id = psicologo1.salvar()
    print(f"Psicólogo criado com ID: {psicologo_id}")

    # Criando um horário de atendimento
    horario1 = Horario("ana@psicologa.com", "joao@email.com", "2025-03-15T10:00:00", "2025-03-15T11:00:00")
    horario_id = horario1.salvar()
    print(f"Horário criado com ID: {horario_id}")

    # Listando horários agendados
    print("Lista de horários agendados:")
    print(Horario.listar_horarios())