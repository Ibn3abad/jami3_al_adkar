/**
 * @author     A. KHOUK
 * @date       12.06.2026
 * @version    4.05
 * @copyright  Copyright (c) 2026, A. KHOUK.
 * @license    This program is free software: you can redistribute it and/or modify
 *             it under the terms of the GNU General Public License as published by
 *             the Free Software Foundation, either version 3 of the License, or
 *             (at your option) any later version.
 */

package com.ibn3abad.jami3_al_adkar.ui

import androidx.lifecycle.ViewModel
import androidx.lifecycle.ViewModelProvider
import androidx.lifecycle.viewModelScope
import androidx.lifecycle.viewmodel.initializer
import androidx.lifecycle.viewmodel.viewModelFactory
import com.ibn3abad.jami3_al_adkar.Jami3AlAdkarApplication
import com.ibn3abad.jami3_al_adkar.data.model.Adkar
import com.ibn3abad.jami3_al_adkar.data.repository.AdkarRepository
import kotlinx.coroutines.Job
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.launch
import java.text.SimpleDateFormat
import java.util.Date
import java.util.Locale

class AdkarViewModel(private val repository: AdkarRepository) : ViewModel() {
    private val dateFormatter = SimpleDateFormat("yyyy-MM-dd", Locale.getDefault())

    private val _uiState = MutableStateFlow<AdkarUiState>(AdkarUiState.Loading)
    val uiState: StateFlow<AdkarUiState> = _uiState.asStateFlow()

    private var loadJob: Job? = null

    fun loadAdkarByCategory(category: String) {
        loadJob?.cancel()
        _uiState.value = AdkarUiState.Loading
        loadJob = viewModelScope.launch {
            repository.getAdkarByCategoryStream(category).collect { adkarList ->
                if (adkarList.isEmpty()) {
                    _uiState.value = AdkarUiState.Empty
                } else {
                    _uiState.value = AdkarUiState.Success(adkarList)
                }
            }
        }
    }

    fun loadFavorites() {
        loadJob?.cancel()
        _uiState.value = AdkarUiState.Loading
        loadJob = viewModelScope.launch {
            repository.getFavoriteAdkarStream().collect { adkarList ->
                if (adkarList.isEmpty()) {
                    _uiState.value = AdkarUiState.Empty
                } else {
                    _uiState.value = AdkarUiState.Success(adkarList)
                }
            }
        }
    }

    fun toggleFavorite(adkar: Adkar) {
        viewModelScope.launch {
            repository.toggleFavorite(adkar.id, !adkar.isFavorite)
        }
    }

    fun markAsCompleted(adkar: Adkar) {
        viewModelScope.launch {
            val today = dateFormatter.format(Date())
            repository.markAsCompleted(adkar.id, today)
        }
    }

    companion object {
        val Factory: ViewModelProvider.Factory = viewModelFactory {
            initializer {
                val application = (this[ViewModelProvider.AndroidViewModelFactory.APPLICATION_KEY] as Jami3AlAdkarApplication)
                AdkarViewModel(application.repository)
            }
        }
    }
}

sealed interface AdkarUiState {
    data class Success(val adkarList: List<Adkar>) : AdkarUiState
    object Loading : AdkarUiState
    object Empty : AdkarUiState
}
