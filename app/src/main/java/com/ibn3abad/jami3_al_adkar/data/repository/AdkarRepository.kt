/**
 * @author     A. KHOUK
 * @date       12.06.2026
 * @version    1.02
 * @copyright  Copyright (c) 2026, A. KHOUK.
 * @license    This program is free software: you can redistribute it and/or modify
 *             it under the terms of the GNU General Public License as published by
 *             the Free Software Foundation, either version 3 of the License, or
 *             (at your option) any later version.
 */

package com.ibn3abad.jami3_al_adkar.data.repository

import com.ibn3abad.jami3_al_adkar.data.dao.AdkarDao
import com.ibn3abad.jami3_al_adkar.data.model.Adkar
import kotlinx.coroutines.flow.Flow

class AdkarRepository(private val adkarDao: AdkarDao) {
    fun getAllAdkarStream(): Flow<List<Adkar>> = adkarDao.getAllAdkar()

    fun getAdkarByCategoryStream(category: String): Flow<List<Adkar>> =
        adkarDao.getAdkarByCategory(category)

    suspend fun toggleFavorite(adkarId: Int, isFavorite: Boolean) {
        adkarDao.updateFavorite(adkarId, isFavorite)
    }

    suspend fun markAsCompleted(adkarId: Int, date: String) {
        adkarDao.updateLastCompletedDate(adkarId, date)
    }

    fun getFavoriteAdkarStream(): Flow<List<Adkar>> = adkarDao.getFavoriteAdkar()
}
