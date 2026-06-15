/**
 * @author     A. KHOUK
 * @date       12.06.2026
 * @version    1.01
 * @copyright  Copyright (c) 2026, A. KHOUK.
 * @license    This program is free software: you can redistribute it and/or modify
 *             it under the terms of the GNU General Public License as published by
 *             the Free Software Foundation, either version 3 of the License, or
 *             (at your option) any later version.
 */

package com.ibn3abad.jami3_al_adkar.ui

import android.content.Context
import androidx.lifecycle.ViewModel
import androidx.lifecycle.ViewModelProvider
import androidx.lifecycle.viewModelScope
import androidx.lifecycle.viewmodel.initializer
import androidx.lifecycle.viewmodel.viewModelFactory
import com.ibn3abad.jami3_al_adkar.Jami3AlAdkarApplication
import com.ibn3abad.jami3_al_adkar.data.repository.AdkarRepository
import com.ibn3abad.jami3_al_adkar.util.ReminderManager
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.launch
import java.text.SimpleDateFormat
import java.util.Date
import java.util.Locale

enum class AppLanguage(val nativeName: String, val isRtl: Boolean = false) {
    ARABIC("العربية", true),
    GERMAN("Deutsch"),
    ENGLISH("English"),
    FRENCH("Français"),
    SPANISH("Español"),
    URDU("اردو", true),
    FARISI("فارسی", true)
}

data class CategoryProgress(
    val categoryId: String,
    val completedCount: Int,
    val totalCount: Int
) {
    val percentage: Float = if (totalCount > 0) completedCount.toFloat() / totalCount else 0f
}

class ProfileViewModel(
    private val repository: AdkarRepository,
    private val applicationContext: Context
) : ViewModel() {
    private val sharedPrefs = applicationContext.getSharedPreferences("settings", Context.MODE_PRIVATE)
    private val reminderManager = ReminderManager(applicationContext)

    private val _language = MutableStateFlow(
        AppLanguage.valueOf(sharedPrefs.getString("language", AppLanguage.GERMAN.name) ?: AppLanguage.GERMAN.name)
    )
    val language: StateFlow<AppLanguage> = _language.asStateFlow()

    private val _morningTime = MutableStateFlow(sharedPrefs.getString("morning_time", "07:00") ?: "07:00")
    val morningTime: StateFlow<String> = _morningTime.asStateFlow()

    private val _eveningTime = MutableStateFlow(sharedPrefs.getString("evening_time", "18:00") ?: "18:00")
    val eveningTime: StateFlow<String> = _eveningTime.asStateFlow()

    private val _sleepTime = MutableStateFlow(sharedPrefs.getString("sleep_time", "21:00") ?: "21:00")
    val sleepTime: StateFlow<String> = _sleepTime.asStateFlow()

    private val _progress = MutableStateFlow<List<CategoryProgress>>(emptyList())
    val progress: StateFlow<List<CategoryProgress>> = _progress.asStateFlow()

    private val dateFormatter = SimpleDateFormat("yyyy-MM-dd", Locale.getDefault())

    init {
        // Schedule default reminders if not already set
        if (!sharedPrefs.contains("morning_time")) {
            setReminderTime("morning", "07:00", "Morning Adkar")
        }
        if (!sharedPrefs.contains("evening_time")) {
            setReminderTime("evening", "18:00", "Evening Adkar")
        }
        if (!sharedPrefs.contains("sleep_time")) {
            setReminderTime("sleep", "21:00", "Sleep Adkar")
        }
    }

    fun setLanguage(language: AppLanguage) {
        _language.value = language
        sharedPrefs.edit().putString("language", language.name).apply()
    }

    fun setReminderTime(categoryId: String, time: String, categoryName: String) {
        val parts = time.split(":")
        if (parts.size == 2) {
            val hour = parts[0].toIntOrNull() ?: return
            val minute = parts[1].toIntOrNull() ?: return
            
            sharedPrefs.edit().putString("${categoryId}_time", time).apply()
            when (categoryId) {
                "morning" -> _morningTime.value = time
                "evening" -> _eveningTime.value = time
                "sleep" -> _sleepTime.value = time
            }
            
            reminderManager.scheduleReminder(categoryId, categoryName, hour, minute)
        }
    }

    fun loadProgress() {
        viewModelScope.launch {
            val today = dateFormatter.format(Date())
            repository.getAllAdkarStream().collect { allAdkar ->
                val categories = allAdkar.groupBy { it.category }
                val progressList = categories.map { (categoryId, adkarList) ->
                    CategoryProgress(
                        categoryId = categoryId,
                        completedCount = adkarList.count { it.lastCompletedDate == today },
                        totalCount = adkarList.size
                    )
                }
                _progress.value = progressList
            }
        }
    }

    companion object {
        val Factory: ViewModelProvider.Factory = viewModelFactory {
            initializer {
                val application = (this[ViewModelProvider.AndroidViewModelFactory.APPLICATION_KEY] as Jami3AlAdkarApplication)
                ProfileViewModel(application.repository, application.applicationContext)
            }
        }
    }
}
