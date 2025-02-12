package com.example.projetointerdisciplinar3

import android.content.Context
import android.content.SharedPreferences

class SessionManager(context: Context) {
    private val sharedPreferences: SharedPreferences =
        context.getSharedPreferences(PREF_NAME, Context.MODE_PRIVATE)

    companion object {
        private const val PREF_NAME = "UserSession"
        private const val KEY_USER_ID = "user_id"
        private const val KEY_USER_EMAIL = "user_email"
        private const val KEY_USER_TIPO = "user_tipo"
        private const val KEY_USER_MATRICULA = "user_matricula"
        private const val KEY_LOGGED_IN = "logged_in"
    }

    fun saveUserSession(userId: Int, userEmail: String, userTipo: String, userMatricula: String) {
        val editor = sharedPreferences.edit()
        editor.putInt(KEY_USER_ID, userId)
        editor.putString(KEY_USER_EMAIL, userEmail)
        editor.putString(KEY_USER_TIPO, userTipo)
        editor.putString(KEY_USER_MATRICULA, userMatricula)
        editor.putBoolean(KEY_LOGGED_IN, true)
        editor.apply()
    }

    fun getUserId(): Int {
        return sharedPreferences.getInt(KEY_USER_ID, -1)
    }

    fun getUserEmail(): String? {
        return sharedPreferences.getString(KEY_USER_EMAIL, null)
    }

    fun getUserTipo(): String? {
        return sharedPreferences.getString(KEY_USER_TIPO, null)
    }

    fun getUserMatricula(): String? {
        return sharedPreferences.getString(KEY_USER_MATRICULA, null)
    }

    fun isLoggedIn(): Boolean {
        return sharedPreferences.getBoolean(KEY_LOGGED_IN, false)
    }

    fun logoutUser() {
        val editor = sharedPreferences.edit()
        editor.clear()
        editor.apply()
    }
}