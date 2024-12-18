package com.example.projetointerdisciplinar3.activity

import android.content.Intent
import android.os.Bundle
import android.widget.Button
import androidx.appcompat.app.AppCompatActivity
import android.widget.Toast
import com.example.projetointerdisciplinar3.MainActivity
import com.example.projetointerdisciplinar3.R

class DashboardPacienteActivity : AppCompatActivity() {

    private lateinit var requestAppointmentButton: Button
    private lateinit var viewOtherAppointmentsButton: Button
    private lateinit var cancelAppointmentButton: Button
    private lateinit var logoutButton: Button

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_dashboard_paciente)

        requestAppointmentButton = findViewById(R.id.requestAppointmentButton)
        viewOtherAppointmentsButton = findViewById(R.id.viewOtherAppointmentsButton)
        cancelAppointmentButton = findViewById(R.id.cancelAppointmentButton)
        logoutButton = findViewById(R.id.logoutButton)

        requestAppointmentButton.setOnClickListener {
            val intent = Intent(this, DashboardPacienteActivity::class.java)
            startActivity(intent)
        }

        viewOtherAppointmentsButton.setOnClickListener {
            val intent = Intent(this, SelecaoAtendimentoActivity::class.java)
            startActivity(intent)
        }

        cancelAppointmentButton.setOnClickListener {
            val intent = Intent(this, DashboardPacienteActivity::class.java)
            startActivity(intent)
        }

        logoutButton.setOnClickListener {
            Toast.makeText(this, "Logout realizado com sucesso!", Toast.LENGTH_SHORT).show()
            finish()
            startActivity(Intent(this, MainActivity::class.java))
        }
    }
}
