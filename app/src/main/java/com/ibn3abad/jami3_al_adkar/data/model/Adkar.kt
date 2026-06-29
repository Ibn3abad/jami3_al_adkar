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

package com.ibn3abad.jami3_al_adkar.data.model

import androidx.room.ColumnInfo
import androidx.room.Entity
import androidx.room.PrimaryKey

@Entity(tableName = "adkar")
data class Adkar(
    @PrimaryKey(autoGenerate = true)
    val id: Int = 0,
    @ColumnInfo(name = "category")
    val category: String,
    @ColumnInfo(name = "textArabic")
    val textArabic: String,
    @ColumnInfo(name = "transliteration")
    val transliteration: String,
    @ColumnInfo(name = "translationDe")
    val translationDe: String,
    @ColumnInfo(name = "translationEn")
    val translationEn: String = "",
    @ColumnInfo(name = "translationFr")
    val translationFr: String = "",
    @ColumnInfo(name = "translationEs")
    val translationEs: String = "",
    @ColumnInfo(name = "translationUr")
    val translationUr: String = "",
    @ColumnInfo(name = "translationFa")
    val translationFa: String = "",
    @ColumnInfo(name = "repetitions")
    val repetitions: Int,
    @ColumnInfo(name = "source")
    val source: String,
    @ColumnInfo(name = "sourceArabic")
    val sourceArabic: String = "",
    @ColumnInfo(name = "isFavorite")
    val isFavorite: Boolean = false,
    @ColumnInfo(name = "lastCompletedDate")
    val lastCompletedDate: String? = null
)
