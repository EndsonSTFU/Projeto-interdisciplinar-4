package com.example.projetointerdisciplinar3.activity

import android.content.Intent
import android.os.Bundle
import android.widget.Button
import androidx.appcompat.app.AppCompatActivity
import android.widget.Toast
import com.example.projetointerdisciplinar3.MainActivity
import com.example.projetointerdisciplinar3.R
import com.example.projetointerdisciplinar3.SessionManager

class DashboardColaboradorActivity : AppCompatActivity() {

    private lateinit var registerScheduleButton: Button
    private lateinit var checkRequestsButton: Button
    private lateinit var patientNotesButton: Button
    private lateinit var logoutButton: Button
    private lateinit var sessionManager: SessionManager

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_dashboard_colaborador)

        sessionManager = SessionManager(this)

        registerScheduleButton = findViewById(R.id.registerScheduleButton)
        checkRequestsButton = findViewById(R.id.checkRequestsButton)
        patientNotesButton = findViewById(R.id.patientNotesButton)
        logoutButton = findViewById(R.id.logoutButton)

        registerScheduleButton.setOnClickListener {
            val intent = Intent(this, CadastrarHorarioActivity::class.java)
            startActivity(intent)
        }

        checkRequestsButton.setOnClickListener {
            val intent = Intent(this, DashboardColaboradorActivity::class.java)
            startActivity(intent)
        }

        patientNotesButton.setOnClickListener {
            val intent = Intent(this, SalvarAnotacaoActivity::class.java)
            startActivity(intent)
        }

        logoutButton.setOnClickListener {
            // Realizar logout
            sessionManager.logoutUser()
            Toast.makeText(this, "Logout realizado com sucesso!", Toast.LENGTH_SHORT).show()
            finish()
            startActivity(Intent(this, MainActivity::class.java))

        }
    }
}
