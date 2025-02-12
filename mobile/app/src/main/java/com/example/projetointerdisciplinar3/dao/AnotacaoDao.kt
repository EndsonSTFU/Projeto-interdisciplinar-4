package com.example.projetointerdisciplinar3.dao

import androidx.room.Dao
import androidx.room.Insert
import androidx.room.Query
import androidx.room.Update
import androidx.room.Delete
import com.example.projetointerdisciplinar3.model.Anotacao

@Dao
interface AnotacaoDao {

    @Insert
    suspend fun inserirAnotacao(anotacao: Anotacao)

    @Query("DELETE FROM anotacoes")
    suspend fun clearAllAnotacoes()

    @Update
    suspend fun atualizarAnotacao(anotacao: Anotacao)

    @Delete
    suspend fun deletarAnotacao(anotacao: Anotacao)

    @Query("SELECT * FROM anotacoes WHERE id = :id")
    suspend fun buscarAnotacaoPorId(id: Int): Anotacao?

    @Query("SELECT * FROM anotacoes WHERE colaboradorId = :colaboradorId")
    suspend fun buscarAnotacoesPorColaboradorId(colaboradorId: Int): List<Anotacao>

    @Query("SELECT * FROM anotacoes WHERE pacienteId = :pacienteId")
    suspend fun buscarAnotacoesPorPacienteId(pacienteId: Int): List<Anotacao>

    @Query("SELECT * FROM anotacoes")
    suspend fun buscarTodasAnotacoes(): List<Anotacao>
}
