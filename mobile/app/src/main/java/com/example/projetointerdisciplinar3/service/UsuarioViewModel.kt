package com.example.projetointerdisciplinar3.service

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.example.projetointerdisciplinar3.dao.UsuarioDao
import com.example.projetointerdisciplinar3.model.Usuario
import com.example.projetointerdisciplinar3.model.Tipo
import kotlinx.coroutines.launch

class UsuarioViewModel(private val usuarioDao: UsuarioDao) : ViewModel() {

    // Função suspensa para cadastrar um usuário
    suspend fun cadastrarUsuario(usuario: Usuario) {
        try {
            usuarioDao.inserirUsuario(usuario)
        } catch (e: Exception) {
            throw Exception(e.message ?: "Erro ao criar o usuário")
        }
    }

    // Função suspensa para autenticar um usuário
    suspend fun autenticarUsuario(email: String, senha: String): Usuario? {
        return try {
            usuarioDao.autenticarUsuario(email, senha)
        } catch (e: Exception) {
            null
        }
    }

    // Função suspensa para buscar usuário por ID
    suspend fun buscarUsuarioPorId(id: Int): Usuario? {
        return try {
            usuarioDao.buscarUsuarioPorId(id)
        } catch (e: Exception) {
            null
        }
    }

    // Função suspensa para buscar usuário por nome
    suspend fun buscarUsuarioPorNome(nome: String): Usuario? {
        return try {
            usuarioDao.buscarUsuarioPorNome(nome)
        } catch (e: Exception) {
            null
        }
    }

    // Função suspensa para buscar usuários por tipo
    suspend fun buscarUsuariosPorTipo(tipo: Tipo): List<Usuario> {
        return try {
            usuarioDao.buscarUsuariosPorTipo(tipo)
        } catch (e: Exception) {
            emptyList()
        }
    }

    // Função suspensa para buscar todos os usuários
    suspend fun buscarTodosUsuarios(): List<Usuario> {
        return try {
            usuarioDao.buscarTodosUsuarios()
        } catch (e: Exception) {
            emptyList()
        }
    }

    // Função suspensa para atualizar um usuário
    suspend fun atualizarUsuario(usuario: Usuario) {
        try {
            usuarioDao.atualizarUsuario(usuario)
        } catch (e: Exception) {
            throw Exception(e.message ?: "Erro ao atualizar o usuário")
        }
    }

    // Função suspensa para deletar um usuário
    suspend fun deletarUsuario(usuario: Usuario) {
        try {
            usuarioDao.deletarUsuario(usuario)
        } catch (e: Exception) {
            throw Exception(e.message ?: "Erro ao deletar o usuário")
        }
    }
}
