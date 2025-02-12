package com.example.projetointerdisciplinar3.database

import android.content.Context
import androidx.room.Room
import com.example.projetointerdisciplinar3.dao.AnotacaoDao
import com.example.projetointerdisciplinar3.dao.HorarioDao
import com.example.projetointerdisciplinar3.dao.UsuarioDao
import com.example.projetointerdisciplinar3.AppDatabase
import com.example.projetointerdisciplinar3.model.Anotacao
import com.example.projetointerdisciplinar3.model.Horario
import com.example.projetointerdisciplinar3.model.Tipo
import com.example.projetointerdisciplinar3.model.Usuario

class DatabaseInitializer(private val context: Context) {

    suspend fun populateDatabase() {
        // Criação de instâncias de DAOs
        val db = Room.databaseBuilder(context, AppDatabase::class.java, "app_database")
            .fallbackToDestructiveMigration()
            .build()

        val usuarioDao = db.usuarioDao()
        val anotacaoDao = db.anotacaoDao()
        val horarioDao = db.horarioDao()

        // Limpar todas as tabelas antes de inserir novos dados
        usuarioDao.clearAllUsuarios()  // Supondo que você tenha um método clearAllUsuarios() no seu UsuarioDao
        anotacaoDao.clearAllAnotacoes()  // Supondo que você tenha um método clearAllAnotacoes() no seu AnotacaoDao
        horarioDao.clearAllHorarios()  // Supondo que você tenha um método clearAllHorarios() no seu HorarioDao

        // Criação de usuários
        val usuario1 = Usuario(
            nome = "João Silva",
            dataNascimento = "1990-06-15",
            email = "joao@example.com",
            senha = "senha123",
            matricula = "12345",
            tipo = Tipo.PACIENTE
        )

        val usuario2 = Usuario(
            nome = "Maria Oliveira",
            dataNascimento = "1985-08-22",
            email = "maria@example.com",
            senha = "senha456",
            matricula = "67890",
            tipo = Tipo.PSICOLOGO
        )

        val usuario3 = Usuario(
            nome = "Carlos Pereira",
            dataNascimento = "1992-02-10",
            email = "carlos@example.com",
            senha = "senha789",
            matricula = "11223",
            tipo = Tipo.PEDAGOGO
        )

        // Inserir usuários no banco de dados
        usuarioDao.inserirUsuario(usuario1)
        usuarioDao.inserirUsuario(usuario2)
        usuarioDao.inserirUsuario(usuario3)

        // Criação de anotações
        val anotacao1 = Anotacao(
            pacienteId = usuario1.id,
            colaboradorId = usuario2.id,
            data = "2025-02-10"
        )

        val anotacao2 = Anotacao(
            pacienteId = usuario1.id,
            colaboradorId = usuario3.id,
            data = "2025-02-11"
        )

        // Inserir anotações no banco de dados
        anotacaoDao.inserirAnotacao(anotacao1)
        anotacaoDao.inserirAnotacao(anotacao2)

        // Criação de horários
        val horario1 = Horario(
            title = "Consulta com Psicólogo",
            start = "2025-02-11 10:00",
            end = "2025-02-11 11:00",
            pacienteId = usuario1.id,
            colaboradorId = usuario2.id
        )

        val horario2 = Horario(
            title = "Consulta com Pedagogo",
            start = "2025-02-11 14:00",
            end = "2025-02-11 15:00",
            pacienteId = usuario1.id,
            colaboradorId = usuario3.id
        )

        val horario3 = Horario(
            title = "Consulta com Psicólogo",
            start = "2025-02-11 15:00",
            end = "2025-02-11 15:30",
            pacienteId = null,  // Permitido como null
            colaboradorId = usuario3.id
        )

        val horario4 = Horario(
            title = "Consulta com Pedagogo",
            start = "2025-02-11 14:00",
            end = "2025-02-11 15:00",
            pacienteId = null,  // Permitido como null
            colaboradorId = usuario3.id
        )

        // Inserir horários no banco de dados
        horarioDao.insert(horario1)
        horarioDao.insert(horario2)
        horarioDao.insert(horario3)  // Agora será inserido corretamente
        horarioDao.insert(horario4)  // Agora será inserido corretamente
    }
}
