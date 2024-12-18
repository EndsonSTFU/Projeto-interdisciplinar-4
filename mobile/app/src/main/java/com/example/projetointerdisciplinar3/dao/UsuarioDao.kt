package com.example.projetointerdisciplinar3.dao

import androidx.room.Dao
import androidx.room.Insert
import androidx.room.Query
import androidx.room.Update
import androidx.room.Delete
import com.example.projetointerdisciplinar3.model.Usuario
import com.example.projetointerdisciplinar3.model.Tipo

@Dao
interface UsuarioDao {

    @Insert
    suspend fun inserirUsuario(usuario: Usuario)

    @Update
    suspend fun atualizarUsuario(usuario: Usuario)

    @Delete
    suspend fun deletarUsuario(usuario: Usuario)

    @Query("SELECT * FROM usuarios WHERE email = :email AND senha = :senha")
    suspend fun autenticarUsuario(email: String, senha: String): Usuario?

    @Query("SELECT * FROM usuarios WHERE id = :id")
    suspend fun buscarUsuarioPorId(id: Int): Usuario?

    @Query("SELECT * FROM usuarios WHERE nome= :nome")
    suspend fun buscarUsuarioPorNome(nome: String): Usuario

    @Query("SELECT * FROM usuarios WHERE tipo = :tipo")
    suspend fun buscarUsuariosPorTipo(tipo: Tipo): List<Usuario>

    @Query("SELECT * FROM usuarios")
    suspend fun buscarTodosUsuarios(): List<Usuario>
}
