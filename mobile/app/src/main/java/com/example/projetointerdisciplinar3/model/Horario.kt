package com.example.projetointerdisciplinar3.model

import androidx.room.Entity
import androidx.room.PrimaryKey

@Entity(tableName = "horarios")
data class Horario(
    @PrimaryKey(autoGenerate = true)
    val id: Int = 0,
    val title: String,
    val start: String,
    val end: String,
    var pacienteId: Int? = null,
    val colaboradorId: Int
)
