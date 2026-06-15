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

package com.ibn3abad.jami3_al_adkar.data

import android.content.Context
import androidx.room.Database
import androidx.room.Room
import androidx.room.RoomDatabase
import com.ibn3abad.jami3_al_adkar.data.dao.AdkarDao
import com.ibn3abad.jami3_al_adkar.data.model.Adkar

@Database(entities = [Adkar::class], version = 9, exportSchema = false)
abstract class AdkarDatabase : RoomDatabase() {
    abstract fun adkarDao(): AdkarDao

    companion object {
        @Volatile
        private var Instance: AdkarDatabase? = null

        fun getDatabase(context: Context): AdkarDatabase {
            return Instance ?: synchronized(this) {
                Room.databaseBuilder(context, AdkarDatabase::class.java, "adkar_database")
                    .createFromAsset("adkar.db")
                    .fallbackToDestructiveMigration()
                    .build()
                    .also { Instance = it }
            }
        }
    }
}
