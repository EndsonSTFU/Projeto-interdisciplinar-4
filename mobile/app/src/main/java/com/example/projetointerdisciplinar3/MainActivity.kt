package com.example.projetointerdisciplinar3

import android.content.Intent
import android.os.Bundle
import android.widget.Button
import android.widget.EditText
import android.widget.TextView
import androidx.appcompat.app.AppCompatActivity
import androidx.core.view.ViewCompat
import androidx.core.view.WindowInsetsCompat
import androidx.lifecycle.ViewModelProvider
import com.example.projetointerdisciplinar3.activity.CadastroPacienteActivity
import com.example.projetointerdisciplinar3.activity.DashboardPacienteActivity
import com.example.projetointerdisciplinar3.activity.DashboardColaboradorActivity
import com.example.projetointerdisciplinar3.factory.UsuarioViewModelFactory
import com.example.projetointerdisciplinar3.model.Tipo
import com.example.projetointerdisciplinar3.service.UsuarioViewModel

class MainActivity : AppCompatActivity() {
    private lateinit var usuarioViewModel: UsuarioViewModel

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_login)

        ViewCompat.setOnApplyWindowInsetsListener(findViewById(R.id.main)) { v, insets ->
            val systemBars = insets.getInsets(WindowInsetsCompat.Type.systemBars())
            v.setPadding(systemBars.left, systemBars.top, systemBars.right, systemBars.bottom)
            insets
        }

        val emailInput = findViewById<EditText>(R.id.emailInput)
        val passwordInput = findViewById<EditText>(R.id.passwordInput)
        val loginButton = findViewById<Button>(R.id.loginButton)
        val registerButton = findViewById<Button>(R.id.registerButton)
        val errorMessage = findViewById<TextView>(R.id.errorMessage)

        val usuarioDao = AppDatabase.getInstance(applicationContext).usuarioDa()
        val factory = UsuarioViewModelFactory(usuarioDao)
        usuarioViewModel = ViewModelProvider(this, factory).get(UsuarioViewModel::class.java)

        loginButton.setOnClickListener {
            val email = emailInput.text.toString()
            val password = passwordInput.text.toString()

            if (email.isEmpty() || password.isEmpty()) {
                errorMessage.text = "Preencha todos os campos"
                errorMessage.visibility = TextView.VISIBLE
                return@setOnClickListener
            }

            usuarioViewModel.autenticarUsuario(email, password) { usuario ->
                if (usuario != null) {
                    errorMessage.visibility = TextView.GONE

                    when (usuario.tipo) {
                        Tipo.PACIENTE -> {
                            startActivity(Intent(this, DashboardPacienteActivity::class.java))
                        } else -> {
                            startActivity(Intent(this, DashboardColaboradorActivity::class.java))
                        }
                    }
                    finish()
                } else {
                    errorMessage.text = "Credenciais inválidas"
                    errorMessage.visibility = TextView.VISIBLE
                }
            }
        }

        registerButton.setOnClickListener {
            startActivity(Intent(this, CadastroPacienteActivity::class.java))
        }
    }
}
