package com.example.projetointerdisciplinar3.activity

import android.content.Intent
import android.os.Bundle
import android.widget.Button
import androidx.appcompat.app.AppCompatActivity
import androidx.lifecycle.ViewModelProvider
import androidx.lifecycle.lifecycleScope
import androidx.recyclerview.widget.LinearLayoutManager
import androidx.recyclerview.widget.RecyclerView
import com.example.projetointerdisciplinar3.AppDatabase
import com.example.projetointerdisciplinar3.R
import com.example.projetointerdisciplinar3.SessionManager
import com.example.projetointerdisciplinar3.model.Usuario
import com.example.projetointerdisciplinar3.adapter.PacienteAdapter
import com.example.projetointerdisciplinar3.factory.AnotacaoViewModelFactory
import com.example.projetointerdisciplinar3.factory.HorarioViewModelFactory
import com.example.projetointerdisciplinar3.factory.UsuarioViewModelFactory
import com.example.projetointerdisciplinar3.model.Tipo
import com.example.projetointerdisciplinar3.service.AnotacaoViewModel
import com.example.projetointerdisciplinar3.service.HorarioViewModel
import com.example.projetointerdisciplinar3.service.UsuarioViewModel
import kotlinx.coroutines.launch

class AnotacoesPacientesActivity : AppCompatActivity() {

    private lateinit var recyclerView: RecyclerView
    private lateinit var adapter: PacienteAdapter
    private lateinit var btnVoltar: Button

    private lateinit var anotacaoViewModel: AnotacaoViewModel
    private lateinit var usuarioViewModel: UsuarioViewModel
    private lateinit var sessionManager: SessionManager

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_anotacoes_pacientes)

        // Inicializar RecyclerView
        recyclerView = findViewById(R.id.pacienteRecyclerView)
        recyclerView.layoutManager = LinearLayoutManager(this)

        recyclerView.adapter = adapter

        val usuarioDao = AppDatabase.getInstance(applicationContext).usuarioDao()
        val anotacaoDao = AppDatabase.getInstance(applicationContext).anotacaoDao()

        usuarioViewModel = ViewModelProvider(this, UsuarioViewModelFactory(usuarioDao))[UsuarioViewModel::class.java]
        anotacaoViewModel = ViewModelProvider(this, AnotacaoViewModelFactory(anotacaoDao))[AnotacaoViewModel::class.java]

        // Botão Voltar
        btnVoltar = findViewById(R.id.btnVoltar)
        btnVoltar.setOnClickListener {
            finish()
        }

        sessionManager = SessionManager(this)

        if (sessionManager.isLoggedIn()) {
            navigateToDashboard()
            return
        }

        lifecycleScope.launch {
            val pacientes = getPacientes()
            adapter = PacienteAdapter(pacientes)
            recyclerView.adapter = adapter
        }
    }

    private suspend fun getPacientes(): List<Usuario> {
        val anotacoes = anotacaoViewModel.buscarAnotacoesPorColaboradorId(sessionManager.getUserId())

        val pacientes = mutableListOf<Usuario>()

        for (anotacao in anotacoes) {
            val usuario = usuarioViewModel.buscarUsuarioPorId(anotacao.pacienteId)
            if (usuario != null) {
                pacientes.add(usuario)
            }
        }
        return pacientes
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
