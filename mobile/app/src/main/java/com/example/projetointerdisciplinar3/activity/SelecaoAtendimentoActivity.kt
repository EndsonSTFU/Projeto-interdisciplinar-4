package com.example.projetointerdisciplinar3.activity

import android.content.Intent
import android.os.Bundle
import android.widget.Button
import androidx.appcompat.app.AppCompatActivity
import com.example.projetointerdisciplinar3.R

class SelecaoAtendimentoActivity : AppCompatActivity() {

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_selecao_atendimento)

        // Botões
        val psychologyButton: Button = findViewById(R.id.psychologyButton)
        val nursingButton: Button = findViewById(R.id.nursingButton)
        val pedagogicButton: Button = findViewById(R.id.pedagogicButton)
        val backButton: Button = findViewById(R.id.backButton)

        psychologyButton.setOnClickListener {
            val intent = Intent(this, SelecaoAtendimentoActivity::class.java)
            startActivity(intent)
        }

        nursingButton.setOnClickListener {
            val intent = Intent(this, SelecaoAtendimentoActivity::class.java)
            startActivity(intent)
        }

        pedagogicButton.setOnClickListener {
            val intent = Intent(this, SelecaoAtendimentoActivity::class.java)
            startActivity(intent)
        }

        backButton.setOnClickListener {
            val intent = Intent(this, DashboardPacienteActivity::class.java)
            startActivity(intent)
        }
    }
}