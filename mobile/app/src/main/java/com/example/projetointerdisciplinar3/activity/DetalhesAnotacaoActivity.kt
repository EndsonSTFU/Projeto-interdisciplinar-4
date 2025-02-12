package com.example.projetointerdisciplinar3.activity

import android.os.Bundle
import android.widget.Button
import android.widget.TextView
import androidx.appcompat.app.AppCompatActivity
import com.example.projetointerdisciplinar3.R

class DetalhesAnotacaoActivity : AppCompatActivity() {

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_detalhes_anotacao)

        val tvDataAnotacao: TextView = findViewById(R.id.tvDataAnotacao)
        val tvColaborador: TextView = findViewById(R.id.tvColaborador)
        val btnVoltar: Button = findViewById(R.id.btnVoltar)

        val dataAnotacao = intent.getStringExtra("DATA_ANOTACAO")
        val colaborador = intent.getStringExtra("COLABORADOR")

        tvDataAnotacao.text = dataAnotacao
        tvColaborador.text = colaborador

        btnVoltar.setOnClickListener {
            finish()
        }
    }
}
