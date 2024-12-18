package com.example.projetointerdisciplinar3.service

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.example.projetointerdisciplinar3.dao.UsuarioDao
import com.example.projetointerdisciplinar3.model.Usuario
import kotlinx.coroutines.launch

class UsuarioViewModel(private val usuarioDao: UsuarioDao) : ViewModel() {

    fun cadastrarUsuario(usuario: Usuario, onSuccess: () -> Unit, onError: (String) -> Unit) {
        viewModelScope.launch {
            try {
                usuarioDao.inserirUsuario(usuario)
                onSuccess()
            } catch (e: Exception) {
                onError(e.message ?: "Erro ao criar o usuário")
            }
        }
    }

    fun autenticarUsuario(email: String, senha: String, onResult: (Usuario?) -> Unit) {
        viewModelScope.launch {
            val usuario = usuarioDao.autenticarUsuario(email, senha)
            onResult(usuario)
        }
    }
}
