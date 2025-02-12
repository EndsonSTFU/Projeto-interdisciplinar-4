package com.example.projetointerdisciplinar3.factory

import androidx.lifecycle.ViewModel
import androidx.lifecycle.ViewModelProvider
import com.example.projetointerdisciplinar3.dao.AnotacaoDao
import com.example.projetointerdisciplinar3.service.AnotacaoViewModel

class AnotacaoViewModelFactory(private val anotacaoDao: AnotacaoDao) : ViewModelProvider.Factory {
    override fun <T : ViewModel> create(modelClass: Class<T>): T {
        if (modelClass.isAssignableFrom(AnotacaoViewModel::class.java)) {
            @Suppress("UNCHECKED_CAST")
            return AnotacaoViewModel(anotacaoDao) as T
        }
        throw IllegalArgumentException("Unknown ViewModel class")
    }
}
