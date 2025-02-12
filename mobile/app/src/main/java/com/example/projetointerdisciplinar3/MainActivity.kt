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
import androidx.lifecycle.lifecycleScope
import com.example.projetointerdisciplinar3.activity.CadastroPacienteActivity
import com.example.projetointerdisciplinar3.activity.DashboardPacienteActivity
import com.example.projetointerdisciplinar3.activity.DashboardColaboradorActivity
import com.example.projetointerdisciplinar3.database.DatabaseInitializer
import com.example.projetointerdisciplinar3.factory.AnotacaoViewModelFactory
import com.example.projetointerdisciplinar3.factory.HorarioViewModelFactory
import com.example.projetointerdisciplinar3.factory.UsuarioViewModelFactory
import com.example.projetointerdisciplinar3.model.Tipo
import com.example.projetointerdisciplinar3.service.AnotacaoViewModel
import com.example.projetointerdisciplinar3.service.HorarioViewModel
import com.example.projetointerdisciplinar3.service.UsuarioViewModel
import kotlinx.coroutines.launch

class MainActivity : AppCompatActivity() {
    private lateinit var usuarioViewModel: UsuarioViewModel
    private lateinit var anotacaoViewModel: AnotacaoViewModel
    private lateinit var horarioViewModel: HorarioViewModel

    private lateinit var sessionManager: SessionManager

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_login)

        lifecycleScope.launch {
            val dbInitializer = DatabaseInitializer(this@MainActivity)
            dbInitializer.populateDatabase()
        }

        ViewCompat.setOnApplyWindowInsetsListener(findViewById(R.id.main)) { v, insets ->
            val systemBars = insets.getInsets(WindowInsetsCompat.Type.systemBars())
            v.setPadding(systemBars.left, systemBars.top, systemBars.right, systemBars.bottom)
            insets
        }

        sessionManager = SessionManager(this)

        if (sessionManager.isLoggedIn()) {
            navigateToDashboard()
            return
        }

        val emailInput = findViewById<EditText>(R.id.emailInput)
        val passwordInput = findViewById<EditText>(R.id.passwordInput)
        val loginButton = findViewById<Button>(R.id.loginButton)
        val registerButton = findViewById<Button>(R.id.registerButton)
        val errorMessage = findViewById<TextView>(R.id.errorMessage)

        val usuarioDao = AppDatabase.getInstance(applicationContext).usuarioDao()
        val horarioDao = AppDatabase.getInstance(applicationContext).horarioDao()
        val anotacaoDao = AppDatabase.getInstance(applicationContext).anotacaoDao()

        usuarioViewModel = ViewModelProvider(this, UsuarioViewModelFactory(usuarioDao))[UsuarioViewModel::class.java]
        horarioViewModel = ViewModelProvider(this, HorarioViewModelFactory(horarioDao))[HorarioViewModel::class.java]
        anotacaoViewModel = ViewModelProvider(this, AnotacaoViewModelFactory(anotacaoDao))[AnotacaoViewModel::class.java]

        loginButton.setOnClickListener {
            val email = emailInput.text.toString()
            val password = passwordInput.text.toString()

            if (email.isEmpty() || password.isEmpty()) {
                errorMessage.text = "Preencha todos os campos"
                errorMessage.visibility = TextView.VISIBLE
                return@setOnClickListener
            }

            lifecycleScope.launch {
                val usuario = usuarioViewModel.autenticarUsuario(email, password)
                if (usuario != null) {
                    errorMessage.visibility = TextView.GONE
                    sessionManager.saveUserSession(
                        usuario.id,
                        usuario.email,
                        usuario.tipo.toString(),
                        usuario.matricula
                    )

                    navigateToDashboard()
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

    private fun navigateToDashboard() {
        val userType = sessionManager.getUserTipo()
        val dashboardIntent = if (userType?.let { Tipo.valueOf(it.uppercase()) } == Tipo.PACIENTE) {
            Intent(this, DashboardPacienteActivity::class.java)
        } else {
            Intent(this, DashboardColaboradorActivity::class.java)
        }
        startActivity(dashboardIntent)
        finish()
    }
}
