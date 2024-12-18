package com.example.projetointerdisciplinar3.activity

import android.content.Intent
import android.os.Bundle
import android.widget.*
import androidx.appcompat.app.AppCompatActivity
import androidx.lifecycle.ViewModelProvider
import com.example.projetointerdisciplinar3.MainActivity
import com.example.projetointerdisciplinar3.R
import com.example.projetointerdisciplinar3.model.Tipo
import com.example.projetointerdisciplinar3.model.Usuario
import com.example.projetointerdisciplinar3.service.UsuarioViewModel
import com.example.projetointerdisciplinar3.factory.UsuarioViewModelFactory

class CadastroColaboradorActivity : AppCompatActivity() {

    private lateinit var usuarioViewModel: UsuarioViewModel

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_cadastro_colaborador)

        val etNome: EditText = findViewById(R.id.etNome)
        val etEmail: EditText = findViewById(R.id.etEmail)
        val etSenha: EditText = findViewById(R.id.etSenha)
        val etDataNascimento: EditText = findViewById(R.id.etDataNascimento)
        val etMatricula: EditText = findViewById(R.id.etMatricula)
        val radioGroup = findViewById<RadioGroup>(R.id.rgProfissao)
        val btnCadastrar = findViewById<Button>(R.id.btnCadastrar)
        val btnVoltar: Button = findViewById(R.id.backButton)

        val usuarioDao = com.example.projetointerdisciplinar3.AppDatabase.getInstance(applicationContext).usuarioDa()

        val factory = UsuarioViewModelFactory(usuarioDao)
        usuarioViewModel = ViewModelProvider(this, factory).get(UsuarioViewModel::class.java)

        btnCadastrar.setOnClickListener {
            val nome = etNome.text.toString()
            val email = etEmail.text.toString()
            val senha = etSenha.text.toString()
            val dataNascimento = etDataNascimento.text.toString()
            val matricula = etMatricula.text.toString()
            val selectedId = radioGroup.checkedRadioButtonId

            if (nome.isEmpty() || email.isEmpty() || senha.isEmpty() || dataNascimento.isEmpty() || matricula.isEmpty() || selectedId == -1) {
                Toast.makeText(this, "Por favor, preencha todos os campos!", Toast.LENGTH_SHORT).show()
            } else {
                val selectedRadioButton = findViewById<RadioButton>(selectedId)
                val selectedProfissao = selectedRadioButton.text.toString()

                val tipoUsuario = when (selectedProfissao) {
                    "Psicólogo" -> Tipo.PSICOLOGO
                    "Enfermeiro" -> Tipo.ENFERMEIRO
                    "Pedagogo" -> Tipo.PEDAGOGO
                    else -> {
                        Toast.makeText(this, "Profissão não selecionada corretamente", Toast.LENGTH_SHORT).show()
                        return@setOnClickListener
                    }
                }

                val usuario = Usuario(nome, dataNascimento, email, senha, matricula, tipoUsuario)

                usuarioViewModel.cadastrarUsuario(usuario,
                    onSuccess = {
                        Toast.makeText(this, "Cadastro realizado com sucesso!", Toast.LENGTH_SHORT).show()

                        etNome.text.clear()
                        etEmail.text.clear()
                        etSenha.text.clear()
                        etDataNascimento.text.clear()
                        etMatricula.text.clear()
                        radioGroup.clearCheck()

                        // Redireciona para a tela principal
                        startActivity(Intent(this, MainActivity::class.java))
                    },
                    onError = { message ->
                        // Caso haja erro, exibe a mensagem
                        Toast.makeText(this, message, Toast.LENGTH_SHORT).show()
                    }
                )
            }
        }

        btnVoltar.setOnClickListener {
            startActivity(Intent(this, CadastroPacienteActivity::class.java))
        }
    }
}
