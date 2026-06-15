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

package com.ibn3abad.jami3_al_adkar

import android.app.Application
import com.ibn3abad.jami3_al_adkar.data.AdkarDatabase
import com.ibn3abad.jami3_al_adkar.data.repository.AdkarRepository

class Jami3AlAdkarApplication : Application() {
    val database: AdkarDatabase by lazy { AdkarDatabase.getDatabase(this) }
    val repository: AdkarRepository by lazy { AdkarRepository(database.adkarDao()) }
}
