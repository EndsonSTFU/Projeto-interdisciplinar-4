package com.example.projetointerdisciplinar3.model

import androidx.room.Entity
import androidx.room.PrimaryKey

@Entity(tableName = "usuarios")
open class Usuario(
    @PrimaryKey(autoGenerate = true)
    val id: Int = 0,
    val nome: String,
    val dataNascimento: String,
    val email: String,
    val senha: String,
    val matricula: String,
    val tipo: Tipo
) {
    constructor(nome: String, dataNascimento: String, email: String, senha: String, matricula: String, tipo: Tipo) :
            this(0, nome, dataNascimento, email, senha, matricula, tipo)
}
