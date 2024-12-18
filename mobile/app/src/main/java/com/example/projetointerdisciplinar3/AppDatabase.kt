package com.example.projetointerdisciplinar3

import android.content.Context
import androidx.room.Database
import androidx.room.Room
import androidx.room.RoomDatabase
import com.example.projetointerdisciplinar3.dao.AnotacaoDao
import com.example.projetointerdisciplinar3.dao.HorarioDao
import com.example.projetointerdisciplinar3.dao.UsuarioDao
import com.example.projetointerdisciplinar3.model.Anotacao
import com.example.projetointerdisciplinar3.model.Horario
import com.example.projetointerdisciplinar3.model.Usuario

@Database(entities = [Usuario::class, Horario::class, Anotacao::class], version = 1)
abstract class AppDatabase : RoomDatabase() {
    abstract fun usuarioDa(): UsuarioDao
    abstract fun horarioDao(): HorarioDao
    abstract fun anotacaoDao(): AnotacaoDao

    companion object {
        @Volatile
        private var INSTANCE: AppDatabase? = null

        fun getInstance(context: Context): AppDatabase {
            return INSTANCE ?: synchronized(this) {
                val instance = Room.databaseBuilder(
                    context.applicationContext,
                    AppDatabase::class.java,
                    "app_database"
                )
                    .fallbackToDestructiveMigration()
                    .build()
                INSTANCE = instance
                instance
            }
        }
    }
}
