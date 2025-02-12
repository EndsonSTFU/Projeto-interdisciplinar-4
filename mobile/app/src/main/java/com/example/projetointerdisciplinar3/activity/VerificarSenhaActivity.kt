package com.example.projetointerdisciplinar3.activity

import android.content.Intent
import android.os.Bundle
import android.view.View
import android.widget.Button
import android.widget.EditText
import android.widget.LinearLayout
import android.widget.TextView
import androidx.appcompat.app.AppCompatActivity
import androidx.lifecycle.ViewModelProvider
import androidx.lifecycle.lifecycleScope
import com.example.projetointerdisciplinar3.AppDatabase
import com.example.projetointerdisciplinar3.MainActivity
import com.example.projetointerdisciplinar3.R
import com.example.projetointerdisciplinar3.SessionManager
import com.example.projetointerdisciplinar3.factory.AnotacaoViewModelFactory
import com.example.projetointerdisciplinar3.factory.HorarioViewModelFactory
import com.example.projetointerdisciplinar3.factory.UsuarioViewModelFactory
import com.example.projetointerdisciplinar3.model.Tipo
import com.example.projetointerdisciplinar3.service.AnotacaoViewModel
import com.example.projetointerdisciplinar3.service.HorarioViewModel
import com.example.projetointerdisciplinar3.service.UsuarioViewModel
import kotlinx.coroutines.launch

class VerificarSenhaActivity : AppCompatActivity() {

    private lateinit var senhaAcessoEditText: EditText
    private lateinit var btnVerificar: Button
    private lateinit var messagesContainer: LinearLayout
    private lateinit var senhaTextView: TextView
    private lateinit var mensagemTextView: TextView
    private lateinit var usuarioViewModel: UsuarioViewModel
    private lateinit var sessionManager: SessionManager

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_verificar_senha)
        senhaAcessoEditText = findViewById(R.id.senhaAcesso)
        btnVerificar = findViewById(R.id.btnVerificar)
        messagesContainer = findViewById(R.id.messagesContainer)
        senhaTextView = findViewById(R.id.senhaAcesso)
        mensagemTextView = findViewById(R.id.messagesContainer)

        sessionManager = SessionManager(this)
        val usuarioDao = AppDatabase.getInstance(applicationContext).usuarioDao()
        usuarioViewModel = ViewModelProvider(this, UsuarioViewModelFactory(usuarioDao))[UsuarioViewModel::class.java]

        if (!sessionManager.isLoggedIn()) {
            // Se não estiver logado, redireciona para a tela de login
            startActivity(Intent(this, MainActivity::class.java))
            finish()
        } else {
            // Caso o usuário esteja logado, você pode usar as informações do usuário
            val userId = sessionManager.getUserId()
            val userEmail = sessionManager.getUserEmail()
            val userTipo = sessionManager.getUserTipo()
            val userMatricula = sessionManager.getUserMatricula()

            btnVerificar.setOnClickListener {
                verificarSenha(userEmail, userTipo)
            }
        }
    }

    private fun verificarSenha(userEmail: String?, userTipo: String?) {
        val senha = senhaAcessoEditText.text.toString()

        if (userEmail != null) {
            lifecycleScope.launch {
                try {
                    val usuario = usuarioViewModel.autenticarUsuario(userEmail, senha)

                    if (usuario != null) {
                        when (usuario.tipo) {
                            Tipo.PACIENTE -> {
                                exibirMensagem("Você não é um colaborador.", R.color.red)
                            }
                            else -> {
                                exibirMensagem("Você é um colaborador!", R.color.green)
                            }
                        }
                    } else {
                        exibirMensagem("Senha incorreta. Tente novamente.", R.color.red)
                    }

                } catch (e: Exception) {
                    exibirMensagem("Erro ao autenticar usuário. Tente novamente.", R.color.red)
                }
            }
        }
    }

    private fun exibirMensagem(mensagem: String, cor: Int) {
        val mensagemTextView = TextView(this)
        mensagemTextView.text = mensagem
        mensagemTextView.setTextColor(resources.getColor(cor, null))
        mensagemTextView.visibility = View.VISIBLE
        messagesContainer.removeAllViews()
        messagesContainer.addView(mensagemTextView)
    }
}
