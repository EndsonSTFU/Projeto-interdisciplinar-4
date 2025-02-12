package com.example.projetointerdisciplinar3.service

import androidx.lifecycle.ViewModel
import com.example.projetointerdisciplinar3.dao.HorarioDao
import com.example.projetointerdisciplinar3.model.Horario

class HorarioViewModel(private val horarioDao: HorarioDao) : ViewModel() {

    // Função para inserir um horário
    suspend fun inserirHorario(horario: Horario) {
        horarioDao.insert(horario)
    }

    // Função para atualizar um horário
    suspend fun atualizarHorario(horario: Horario) {
        horarioDao.update(horario)
    }

    // Função para deletar um horário por ID
    suspend fun deletarHorarioPorId(id: Int) {
        horarioDao.deleteById(id)
    }

    // Função para deletar todos os horários
    suspend fun deletarTodosHorarios() {
        horarioDao.deleteAll()
    }

    // Função para buscar um horário por ID
    suspend fun buscarHorarioPorId(id: Int): Horario? {
        return horarioDao.getById(id)
    }

    // Função para buscar horários por ID de paciente
    suspend fun buscarHorariosPorPacienteId(pacienteId: Int): List<Horario> {
        return horarioDao.getByPacienteId(pacienteId)
    }

    // Função para buscar horários por ID de colaborador
    suspend fun buscarHorariosPorColaboradorId(colaboradorId: Int): List<Horario> {
        return horarioDao.getByColaboradorId(colaboradorId)
    }

    // Função para buscar horários por ID de paciente e colaborador
    suspend fun buscarHorariosPorPacienteEColaborador(pacienteId: Int, colaboradorId: Int): List<Horario> {
        return horarioDao.getByPacienteIdAndColaboradorId(pacienteId, colaboradorId)
    }

    suspend fun buscarHorariosSemPacientes(): List<Horario> {
        return horarioDao.getWithoutPaciente()
    }

    // Função para buscar todos os horários
    suspend fun buscarTodosHorarios(): List<Horario> {
        return horarioDao.getAll()
    }
}
