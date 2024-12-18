package com.example.projetointerdisciplinar3

import android.content.Context

class SessaoManager(context: Context) {
    private val preferences = context.getSharedPreferences("sessao_prefs", Context.MODE_PRIVATE)

    fun salvarSessaoUsuario(idUsuario: Int) {
        preferences.edit()
            .putInt("id_usuario", idUsuario)
            .apply()
    }

    fun obterIdUsuarioLogado(): Int? {
        val id = preferences.getInt("id_usuario", -1)
        return if (id != -1) id else null
    }

    fun limparSessao() {
        preferences.edit()
            .remove("id_usuario")
            .apply()
    }
}
