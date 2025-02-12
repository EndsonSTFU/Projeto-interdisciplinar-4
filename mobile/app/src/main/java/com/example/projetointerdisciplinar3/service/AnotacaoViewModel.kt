package com.example.projetointerdisciplinar3.service

import androidx.lifecycle.ViewModel
import com.example.projetointerdisciplinar3.dao.AnotacaoDao
import com.example.projetointerdisciplinar3.model.Anotacao

class AnotacaoViewModel(private val anotacaoDao: AnotacaoDao) : ViewModel() {

    // Função para inserir uma anotação
    suspend fun inserirAnotacao(anotacao: Anotacao) {
        anotacaoDao.inserirAnotacao(anotacao)
    }

    // Função para atualizar uma anotação
    suspend fun atualizarAnotacao(anotacao: Anotacao) {
        anotacaoDao.atualizarAnotacao(anotacao)
    }

    // Função para deletar uma anotação
    suspend fun deletarAnotacao(anotacao: Anotacao) {
        anotacaoDao.deletarAnotacao(anotacao)
    }

    // Função para buscar anotações por ID de colaborador
    suspend fun buscarAnotacoesPorColaboradorId(colaboradorId: Int): List<Anotacao> {
        return anotacaoDao.buscarAnotacoesPorColaboradorId(colaboradorId)
    }

    // Função para buscar anotações por ID de paciente
    suspend fun buscarAnotacoesPorPacienteId(pacienteId: Int): List<Anotacao> {
        return anotacaoDao.buscarAnotacoesPorPacienteId(pacienteId)
    }

    // Função para buscar todas as anotações
    suspend fun buscarTodasAnotacoes(): List<Anotacao> {
        return anotacaoDao.buscarTodasAnotacoes()
    }
}
