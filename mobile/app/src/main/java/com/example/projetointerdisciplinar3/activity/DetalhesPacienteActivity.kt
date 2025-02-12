package com.example.projetointerdisciplinar3.activity

import android.content.Intent
import android.os.Bundle
import android.widget.Button
import android.widget.TableRow
import android.widget.TextView
import androidx.appcompat.app.AppCompatActivity
import androidx.lifecycle.ViewModelProvider
import androidx.lifecycle.lifecycleScope
import com.example.projetointerdisciplinar3.AppDatabase
import com.example.projetointerdisciplinar3.R
import com.example.projetointerdisciplinar3.factory.UsuarioViewModelFactory
import com.example.projetointerdisciplinar3.model.Usuario
import com.example.projetointerdisciplinar3.model.Anotacao
import com.example.projetointerdisciplinar3.service.UsuarioViewModel
import kotlinx.coroutines.launch

class DetalhesPacienteActivity : AppCompatActivity() {

    private lateinit var paciente: Usuario
    private lateinit var anotacoes: List<Anotacao>
    private lateinit var usuarioViewModel: UsuarioViewModel

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_detalhes_paciente)

        val pacienteId = intent.getIntExtra("pacienteId", -1)
        val usuarioDao = AppDatabase.getInstance(applicationContext).usuarioDao()
        usuarioViewModel = ViewModelProvider(this, UsuarioViewModelFactory(usuarioDao))[UsuarioViewModel::class.java]

        lifecycleScope.launch {
            val usuario = usuarioViewModel.buscarUsuarioPorId(pacienteId)
            if (usuario != null) {
                paciente = usuario
            }
        }

        // Preencher as informações do paciente
        val nomeTextView = findViewById<TextView>(R.id.tvNome)
        val emailTextView = findViewById<TextView>(R.id.tvEmail)
        val dataNascimentoTextView = findViewById<TextView>(R.id.tvDataNascimento)
        val matriculaTextView = findViewById<TextView>(R.id.tvMatricula)

        nomeTextView.text = "Nome: ${paciente.nome}"
        emailTextView.text = "Email: ${paciente.email}"
        dataNascimentoTextView.text = "Data de Nascimento: ${paciente.dataNascimento}"
        matriculaTextView.text = "Matrícula: ${paciente.matricula}"

        // Adicionar as anotações na tabela
        val tableLayout = findViewById<android.widget.TableLayout>(R.id.tableAnotacoes)

        for (anotacao in anotacoes) {
            val tableRow = TableRow(this)

            val anotacaoTextView = TextView(this)
            anotacaoTextView.text = anotacao.data
            anotacaoTextView.setPadding(16, 16, 16, 16)
            anotacaoTextView.setBackgroundColor(resources.getColor(R.color.white))

            anotacaoTextView.setOnClickListener {
                onAnotacaoClick(anotacao)
            }

            tableRow.addView(anotacaoTextView)
            tableLayout.addView(tableRow)
        }

        val voltarButton = findViewById<Button>(R.id.btnVoltar)
        voltarButton.setOnClickListener {
            finish()
        }

        val adicionarAnotacaoButton = findViewById<Button>(R.id.btnAdicionarAnotacao)
        adicionarAnotacaoButton.setOnClickListener {
            val intent = Intent(this, SalvarAnotacaoActivity::class.java)
            intent.putExtra("pacienteNome", paciente.nome)
            startActivity(intent)
        }
    }

    private fun onAnotacaoClick(anotacao: Anotacao) {
        val intent = Intent(this, DetalhesAnotacaoActivity::class.java)
        intent.putExtra("anotacaoId", anotacao.id)
        startActivity(intent)
    }
}
