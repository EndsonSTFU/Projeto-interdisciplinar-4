package com.example.projetointerdisciplinar3.dao

import androidx.room.Dao
import androidx.room.Insert
import androidx.room.Query
import androidx.room.Update
import com.example.projetointerdisciplinar3.model.Horario

@Dao
interface HorarioDao {

    @Insert
    suspend fun insert(horario: Horario)

    @Query("DELETE FROM horarios")
    suspend fun clearAllHorarios()

    @Update
    suspend fun update(horario: Horario)

    @Query("SELECT * FROM horarios WHERE id = :id")
    suspend fun getById(id: Int): Horario?

    @Query("SELECT * FROM horarios WHERE pacienteId = :pacienteId")
    suspend fun getByPacienteId(pacienteId: Int): List<Horario>

    @Query("SELECT * FROM horarios WHERE colaboradorId = :colaboradorId")
    suspend fun getByColaboradorId(colaboradorId: Int): List<Horario>

    @Query("SELECT * FROM horarios WHERE pacienteId = :pacienteId AND colaboradorId = :colaboradorId")
    suspend fun getByPacienteIdAndColaboradorId(pacienteId: Int, colaboradorId: Int): List<Horario>

    @Query("SELECT * FROM horarios")
    suspend fun getAll(): List<Horario>

    @Query("SELECT * FROM horarios WHERE pacienteId IS NULL")
    suspend fun getWithoutPaciente(): List<Horario>

    @Query("DELETE FROM horarios WHERE id = :id")
    suspend fun deleteById(id: Int)

    @Query("DELETE FROM horarios")
    suspend fun deleteAll()
}
