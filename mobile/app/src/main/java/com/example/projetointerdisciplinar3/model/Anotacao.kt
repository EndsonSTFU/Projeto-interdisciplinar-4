package com.example.projetointerdisciplinar3.model

import androidx.room.Entity
import androidx.room.PrimaryKey

@Entity(tableName = "anotacoes")
data class Anotacao(
    @PrimaryKey(autoGenerate = true)
    val id: Int = 0,
    val pacienteId: Int,
    val colaboradorId: Int,
    val data: String
)
