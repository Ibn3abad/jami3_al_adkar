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

package com.ibn3abad.jami3_al_adkar.receiver

import android.content.BroadcastReceiver
import android.content.Context
import android.content.Intent
import com.ibn3abad.jami3_al_adkar.util.ReminderManager

class BootReceiver : BroadcastReceiver() {
    override fun onReceive(context: Context, intent: Intent) {
        if (intent.action == Intent.ACTION_BOOT_COMPLETED) {
            val sharedPrefs = context.getSharedPreferences("settings", Context.MODE_PRIVATE)
            val reminderManager = ReminderManager(context)

            val morningTime = sharedPrefs.getString("morning_time", "07:00") ?: "07:00"
            val eveningTime = sharedPrefs.getString("evening_time", "18:00") ?: "18:00"
            val sleepTime = sharedPrefs.getString("sleep_time", "21:00") ?: "21:00"

            schedule(reminderManager, "morning", "Morning Adkar", morningTime)
            schedule(reminderManager, "evening", "Evening Adkar", eveningTime)
            schedule(reminderManager, "sleep", "Sleep Adkar", sleepTime)
        }
    }

    private fun schedule(reminderManager: ReminderManager, id: String, name: String, time: String) {
        val parts = time.split(":")
        if (parts.size == 2) {
            val hour = parts[0].toIntOrNull() ?: return
            val minute = parts[1].toIntOrNull() ?: return
            reminderManager.scheduleReminder(id, name, hour, minute)
        }
    }
}
