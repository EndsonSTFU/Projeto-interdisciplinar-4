package com.example.projetointerdisciplinar3.factory

import androidx.lifecycle.ViewModel
import androidx.lifecycle.ViewModelProvider
import com.example.projetointerdisciplinar3.dao.HorarioDao
import com.example.projetointerdisciplinar3.service.HorarioViewModel

class HorarioViewModelFactory(private val horarioDao: HorarioDao) : ViewModelProvider.Factory {
    override fun <T : ViewModel> create(modelClass: Class<T>): T {
        if (modelClass.isAssignableFrom(HorarioViewModel::class.java)) {
            @Suppress("UNCHECKED_CAST")
            return HorarioViewModel(horarioDao) as T
        }
        throw IllegalArgumentException("Unknown ViewModel class")
    }
}
