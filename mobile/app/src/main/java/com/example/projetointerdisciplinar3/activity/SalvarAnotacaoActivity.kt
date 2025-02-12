package com.example.projetointerdisciplinar3.activity

import android.os.Bundle
import android.view.View
import android.widget.Button
import android.widget.EditText
import android.widget.TextView
import androidx.appcompat.app.AppCompatActivity
import androidx.lifecycle.ViewModelProvider
import androidx.lifecycle.lifecycleScope
import com.example.projetointerdisciplinar3.AppDatabase
import com.example.projetointerdisciplinar3.R
import com.example.projetointerdisciplinar3.SessionManager
import com.example.projetointerdisciplinar3.factory.AnotacaoViewModelFactory
import com.example.projetointerdisciplinar3.factory.UsuarioViewModelFactory
import com.example.projetointerdisciplinar3.model.Anotacao
import com.example.projetointerdisciplinar3.service.AnotacaoViewModel
import com.example.projetointerdisciplinar3.service.UsuarioViewModel
import kotlinx.coroutines.launch

class SalvarAnotacaoActivity : AppCompatActivity() {

    private lateinit var pacienteEditText: EditText
    private lateinit var anotacaoEditText: EditText
    private lateinit var saveButton: Button
    private lateinit var backButton: Button
    private lateinit var flashMessageContainer: View
    private lateinit var flashMessageText: TextView

    private lateinit var sessionManager: SessionManager
    private lateinit var anotacaoViewModel: AnotacaoViewModel
    private lateinit var usuarioViewModel: UsuarioViewModel

    private var pacienteNomePreenchido = false // Flag para garantir que o nome não será reatribuído

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_salvar_anotacao)

        pacienteEditText = findViewById(R.id.paciente)
        anotacaoEditText = findViewById(R.id.anotacao)
        saveButton = findViewById(R.id.saveButton)
        backButton = findViewById(R.id.backButton)
        flashMessageContainer = findViewById(R.id.flashMessagesContainer)
        flashMessageText = findViewById(R.id.flashMessage)

        sessionManager = SessionManager(this)

        val usuarioDao = AppDatabase.getInstance(applicationContext).usuarioDao()
        val anotacaoDao = AppDatabase.getInstance(applicationContext).anotacaoDao()
        usuarioViewModel = ViewModelProvider(this, UsuarioViewModelFactory(usuarioDao))[UsuarioViewModel::class.java]
        anotacaoViewModel = ViewModelProvider(this, AnotacaoViewModelFactory(anotacaoDao))[AnotacaoViewModel::class.java]

        val colaboradorId = sessionManager.getUserId()

        // Verifique se o nome do paciente foi passado e preencha uma única vez
        val pacienteNome = intent.getStringExtra("pacienteNome") ?: ""
        if (pacienteNome.isNotEmpty() && !pacienteNomePreenchido) {
            pacienteEditText.setText(pacienteNome)
            pacienteNomePreenchido = true // Marcar que o nome já foi preenchido
        }

        saveButton.setOnClickListener {
            val anotacaoText = anotacaoEditText.text.toString().trim()
            val pacienteText = pacienteEditText.text.toString().trim()

            if (anotacaoText.isNotEmpty()) {
                lifecycleScope.launch {
                    val paciente = usuarioViewModel.buscarUsuarioPorNome(pacienteText)
                    val pacienteId = paciente?.id ?: return@launch

                    if (pacienteId > 0) {
                        val anotacao = Anotacao(
                            pacienteId = pacienteId,
                            colaboradorId = colaboradorId,
                            data = anotacaoText
                        )

                        anotacaoViewModel.inserirAnotacao(anotacao)
                        showFlashMessage("Anotação salva com sucesso!", "success")
                    } else {
                        showFlashMessage("Paciente não encontrado!", "danger")
                    }
                }
            } else {
                showFlashMessage("A anotação não pode estar vazia!", "danger")
            }
        }

        backButton.setOnClickListener {
            finish()
        }
    }

    private fun showFlashMessage(message: String, type: String) {
        flashMessageContainer.visibility = View.VISIBLE
        flashMessageText.text = message

        // Ajustar cor com base no tipo de mensagem (sucesso ou erro)
        if (type == "success") {
            flashMessageContainer.setBackgroundColor(resources.getColor(R.color.green)) // Fundo verde
        } else {
            flashMessageContainer.setBackgroundColor(resources.getColor(R.color.red)) // Fundo vermelho
        }

        // Esconde a mensagem após 3 segundos
        flashMessageContainer.postDelayed({
            flashMessageContainer.visibility = View.GONE
        }, 3000)
    }
}