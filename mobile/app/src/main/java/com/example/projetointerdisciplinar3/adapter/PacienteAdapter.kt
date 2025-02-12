package com.example.projetointerdisciplinar3.adapter

import android.content.Intent
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.Button
import android.widget.TextView
import androidx.recyclerview.widget.RecyclerView
import com.example.projetointerdisciplinar3.R
import com.example.projetointerdisciplinar3.activity.DetalhesPacienteActivity
import com.example.projetointerdisciplinar3.model.Usuario

class PacienteAdapter(private val pacientes: List<Usuario>) : RecyclerView.Adapter<PacienteAdapter.PacienteViewHolder>() {

    override fun onCreateViewHolder(parent: ViewGroup, viewType: Int): PacienteViewHolder {
        val view = LayoutInflater.from(parent.context).inflate(R.layout.item_paciente, parent, false)
        return PacienteViewHolder(view)
    }

    override fun onBindViewHolder(holder: PacienteViewHolder, position: Int) {
        val paciente = pacientes[position]
        holder.nomeTextView.text = paciente.nome
        holder.detalhesButton.setOnClickListener {
            val intent = Intent(holder.itemView.context, DetalhesPacienteActivity::class.java)
            intent.putExtra("ID", paciente.id)
            holder.itemView.context.startActivity(intent)
        }
    }

    override fun getItemCount(): Int = pacientes.size

    class PacienteViewHolder(itemView: View) : RecyclerView.ViewHolder(itemView) {
        val nomeTextView: TextView = itemView.findViewById(R.id.nomePaciente)
        val detalhesButton: Button = itemView.findViewById(R.id.detalhesPacienteButton)
    }
}
