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

package com.ibn3abad.jami3_al_adkar.data.dao

import androidx.room.Dao
import androidx.room.Insert
import androidx.room.OnConflictStrategy
import androidx.room.Query
import com.ibn3abad.jami3_al_adkar.data.model.Adkar
import kotlinx.coroutines.flow.Flow

@Dao
interface AdkarDao {
    @Query("SELECT * FROM adkar ORDER BY id ASC")
    fun getAllAdkar(): Flow<List<Adkar>>

    @Query("SELECT * FROM adkar WHERE category = :category ORDER BY id ASC")
    fun getAdkarByCategory(category: String): Flow<List<Adkar>>

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun insertAll(adkarList: List<Adkar>)

    @Query("UPDATE adkar SET isFavorite = :isFavorite WHERE id = :adkarId")
    suspend fun updateFavorite(adkarId: Int, isFavorite: Boolean)

    @Query("UPDATE adkar SET lastCompletedDate = :date WHERE id = :adkarId")
    suspend fun updateLastCompletedDate(adkarId: Int, date: String)

    @Query("SELECT * FROM adkar WHERE isFavorite = 1 ORDER BY id ASC")
    fun getFavoriteAdkar(): Flow<List<Adkar>>
}
