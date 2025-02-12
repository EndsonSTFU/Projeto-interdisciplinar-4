package com.example.projetointerdisciplinar3.activity

import android.content.Intent
import android.os.Bundle
import android.widget.*
import androidx.appcompat.app.AppCompatActivity
import androidx.lifecycle.ViewModelProvider
import androidx.lifecycle.lifecycleScope
import com.example.projetointerdisciplinar3.MainActivity
import com.example.projetointerdisciplinar3.R
import com.example.projetointerdisciplinar3.factory.UsuarioViewModelFactory
import com.example.projetointerdisciplinar3.model.Tipo
import com.example.projetointerdisciplinar3.model.Usuario
import com.example.projetointerdisciplinar3.service.UsuarioViewModel
import kotlinx.coroutines.launch

class CadastroPacienteActivity : AppCompatActivity() {

    private lateinit var usuarioViewModel: UsuarioViewModel

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_cadastro_paciente)

        val etNome: EditText = findViewById(R.id.etNome)
        val etEmail: EditText = findViewById(R.id.etEmail)
        val etSenha: EditText = findViewById(R.id.etSenha)
        val etDataNascimento: EditText = findViewById(R.id.etDataNascimento)
        val btnCadastrar: Button = findViewById(R.id.btnCadastrar)
        val btnCadastrarColaborador: Button = findViewById(R.id.btnCadastroColaborador)
        val btnVoltar: Button = findViewById(R.id.backButton)

        val usuarioDao = com.example.projetointerdisciplinar3.AppDatabase.getInstance(applicationContext).usuarioDao()
        usuarioViewModel = ViewModelProvider(this, UsuarioViewModelFactory(usuarioDao))[UsuarioViewModel::class.java]

        btnCadastrar.setOnClickListener {
            val nome = etNome.text.toString()
            val email = etEmail.text.toString()
            val senha = etSenha.text.toString()
            val dataNascimento = etDataNascimento.text.toString()

            if (nome.isEmpty() || email.isEmpty() || senha.isEmpty() || dataNascimento.isEmpty()) {
                Toast.makeText(this, "Por favor, preencha todos os campos!", Toast.LENGTH_SHORT).show()
            } else {
                Toast.makeText(this, "Cadastro realizado com sucesso!", Toast.LENGTH_SHORT).show()
                val usuario = Usuario(nome, dataNascimento, email, senha, "matricula_paciente", Tipo.PACIENTE)

                lifecycleScope.launch {
                    try {
                        // Chama a função suspensa para cadastrar o usuário
                        usuarioViewModel.cadastrarUsuario(usuario)

                        // Caso o cadastro seja bem-sucedido, exibe o Toast e faz as ações
                        Toast.makeText(this@CadastroPacienteActivity, "Cadastro realizado com sucesso!", Toast.LENGTH_SHORT).show()

                        etNome.text.clear()
                        etEmail.text.clear()
                        etSenha.text.clear()
                        etDataNascimento.text.clear()

                        // Redireciona para a tela principal
                        startActivity(Intent(this@CadastroPacienteActivity, MainActivity::class.java))
                    } catch (e: Exception) {
                        // Caso haja erro no cadastro, exibe uma mensagem de erro
                        Toast.makeText(this@CadastroPacienteActivity, "Erro ao cadastrar usuário: ${e.message}", Toast.LENGTH_SHORT).show()
                    }
                }
            }
        }

        btnCadastrarColaborador.setOnClickListener {
            startActivity(Intent(this, CadastroColaboradorActivity::class.java))
        }

        btnVoltar.setOnClickListener {
            startActivity(Intent(this, MainActivity::class.java))
        }
    }
}
