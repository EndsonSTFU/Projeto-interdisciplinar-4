package com.example.projetointerdisciplinar3.activity

import android.os.Bundle
import android.widget.Button
import android.widget.TableLayout
import android.widget.TableRow
import android.widget.TextView
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

class AgendarHorarioActivity : AppCompatActivity() {

    private lateinit var backButton: Button
    private lateinit var tableLayout: TableLayout
    private lateinit var horarioViewModel: HorarioViewModel

    private lateinit var horariosLivres: List<Horario>
    private lateinit var sessionManager: SessionManager

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_agendar_horario)
        sessionManager = SessionManager(this)

        backButton = findViewById(R.id.backButton)
        tableLayout = findViewById(R.id.tableLayout)

        val horarioDao = AppDatabase.getInstance(applicationContext).horarioDao()
        horarioViewModel = ViewModelProvider(this, HorarioViewModelFactory(horarioDao))[HorarioViewModel::class.java]

        lifecycleScope.launch {
            horariosLivres = horarioViewModel.buscarHorariosSemPacientes()

            // Verifique se a lista está sendo preenchida corretamente
            if (horariosLivres.isNotEmpty()) {
                preencherTabelaComHorarios()
            } else {
                Toast.makeText(this@AgendarHorarioActivity, "Não há horários disponíveis", Toast.LENGTH_SHORT).show()
            }
        }

        backButton.setOnClickListener {
            finish()
        }
    }

    private fun preencherTabelaComHorarios() {
        // Limpar a tabela antes de adicionar novas linhas
        tableLayout.removeAllViews()

        // Adicionar o cabeçalho novamente
        val headerRow = TableRow(this)

        val tituloHeader = TextView(this).apply {
            text = "Título"
            setPadding(12, 12, 12, 12)
            gravity = android.view.Gravity.CENTER
        }

        val inicioHeader = TextView(this).apply {
            text = "Início"
            setPadding(12, 12, 12, 12)
            gravity = android.view.Gravity.CENTER
        }

        val fimHeader = TextView(this).apply {
            text = "Fim"
            setPadding(12, 12, 12, 12)
            gravity = android.view.Gravity.CENTER
        }

        val acaoHeader = TextView(this).apply {
            text = "Ação"
            setPadding(12, 12, 12, 12)
            gravity = android.view.Gravity.CENTER
        }

        headerRow.apply {
            addView(tituloHeader)
            addView(inicioHeader)
            addView(fimHeader)
            addView(acaoHeader)
        }

        tableLayout.addView(headerRow)

        // Adicionar uma linha para cada horário livre
        for (horario in horariosLivres) {
            val tableRow = TableRow(this)

            val tituloTextView = TextView(this).apply {
                text = horario.title
                setPadding(12, 12, 12, 12)
                gravity = android.view.Gravity.CENTER
            }

            val inicioTextView = TextView(this).apply {
                text = horario.start
                setPadding(12, 12, 12, 12)
                gravity = android.view.Gravity.CENTER
            }

            val fimTextView = TextView(this).apply {
                text = horario.end
                setPadding(12, 12, 12, 12)
                gravity = android.view.Gravity.CENTER
            }

            val agendarButton = Button(this).apply {
                text = "Agendar"
                setPadding(8, 8, 8, 8)
                setBackgroundColor(resources.getColor(R.color.black))
                setTextColor(resources.getColor(R.color.white))
                gravity = android.view.Gravity.CENTER

                setOnClickListener {
                    Toast.makeText(
                        this@AgendarHorarioActivity,
                        "Agendamento para ${horario.title} realizado!",
                        Toast.LENGTH_SHORT
                    ).show()

                    horario.pacienteId = sessionManager.getUserId()
                    lifecycleScope.launch {
                        horarioViewModel.atualizarHorario(horario)
                    }
                }
            }

            tableRow.apply {
                addView(tituloTextView)
                addView(inicioTextView)
                addView(fimTextView)
                addView(agendarButton)
            }

            tableLayout.addView(tableRow)
        }
    }
}
