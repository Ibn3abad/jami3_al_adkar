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

package com.ibn3abad.jami3_al_adkar.data.model

import androidx.room.Entity
import androidx.room.PrimaryKey

@Entity(tableName = "adkar")
data class Adkar(
    @PrimaryKey(autoGenerate = true)
    val id: Int = 0,
    val category: String,
    val textArabic: String,
    val transliteration: String,
    val translationDe: String,
    val translationEn: String = "",
    val translationFr: String = "",
    val translationEs: String = "",
    val translationUr: String = "",
    val translationFa: String = "",
    val repetitions: Int,
    val source: String,
    val sourceArabic: String = "",
    val isFavorite: Boolean = false,
    val lastCompletedDate: String? = null
)
