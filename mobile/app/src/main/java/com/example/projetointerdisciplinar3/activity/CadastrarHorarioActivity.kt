package com.example.projetointerdisciplinar3.activity

import android.os.Bundle
import android.view.View
import android.widget.Button
import android.widget.EditText
import android.widget.Toast
import androidx.appcompat.app.AppCompatActivity
import androidx.lifecycle.ViewModelProvider
import androidx.lifecycle.lifecycleScope
import com.example.projetointerdisciplinar3.AppDatabase
import com.example.projetointerdisciplinar3.R
import com.example.projetointerdisciplinar3.SessionManager
import com.example.projetointerdisciplinar3.factory.HorarioViewModelFactory
import com.example.projetointerdisciplinar3.model.Horario
import com.example.projetointerdisciplinar3.service.HorarioViewModel
import kotlinx.coroutines.launch

class CadastrarHorarioActivity : AppCompatActivity() {

    private lateinit var etTitulo: EditText
    private lateinit var etInicio: EditText
    private lateinit var etFim: EditText
    private lateinit var btnCadastrar: Button
    private lateinit var backButton: Button

    private lateinit var horarioViewModel: HorarioViewModel
    private lateinit var sessionManager: SessionManager

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_cadastrar_horario)

        etTitulo = findViewById(R.id.etTitulo)
        etInicio = findViewById(R.id.etInicio)
        etFim = findViewById(R.id.etFim)
        btnCadastrar = findViewById(R.id.btnCadastrar)
        backButton = findViewById(R.id.backButton)

        val horarioDao = AppDatabase.getInstance(applicationContext).horarioDao()
        horarioViewModel = ViewModelProvider(this, HorarioViewModelFactory(horarioDao))[HorarioViewModel::class.java]

        sessionManager = SessionManager(this)

        btnCadastrar.setOnClickListener {
            cadastrarHorario()
        }

        backButton.setOnClickListener {
            finish()
        }
    }

    private fun cadastrarHorario() {
        val titulo = etTitulo.text.toString().trim()
        val inicio = etInicio.text.toString().trim()
        val fim = etFim.text.toString().trim()

        if (titulo.isEmpty() || inicio.isEmpty() || fim.isEmpty()) {
            Toast.makeText(this, "Por favor, preencha todos os campos.", Toast.LENGTH_SHORT).show()
        } else {
            val horarioNovo = Horario(
                title = titulo,
                start = inicio,
                end = fim,
                pacienteId = null,
                colaboradorId = sessionManager.getUserId(),
            )

            lifecycleScope.launch {
                horarioViewModel.inserirHorario(horarioNovo)
            }
            Toast.makeText(this, "Horário cadastrado com sucesso!", Toast.LENGTH_SHORT).show()

            etTitulo.text.clear()
            etInicio.text.clear()
            etFim.text.clear()
        }
    }
}
