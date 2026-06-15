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

import android.app.NotificationChannel
import android.app.NotificationManager
import android.app.PendingIntent
import android.content.BroadcastReceiver
import android.content.Context
import android.content.Intent
import android.os.Build
import androidx.core.app.NotificationCompat
import com.ibn3abad.jami3_al_adkar.MainActivity
import com.ibn3abad.jami3_al_adkar.R

class ReminderReceiver : BroadcastReceiver() {
    override fun onReceive(context: Context, intent: Intent) {
        val categoryId = intent.getStringExtra("category_id") ?: return
        
        val sharedPrefs = context.getSharedPreferences("settings", Context.MODE_PRIVATE)
        val langStr = sharedPrefs.getString("language", "GERMAN") ?: "GERMAN"
        
        // Simple mapping for notification titles
        val title = when (categoryId) {
            "morning" -> context.getString(R.string.morning_reminder)
            "evening" -> context.getString(R.string.evening_reminder)
            "sleep" -> context.getString(R.string.sleep_reminder)
            else -> "Adkar"
        }

        showNotification(context, categoryId, title)
    }

    private fun showNotification(context: Context, categoryId: String, categoryName: String) {
        val notificationManager = context.getSystemService(Context.NOTIFICATION_SERVICE) as NotificationManager
        val channelId = "adkar_reminders"

        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
            val channel = NotificationChannel(
                channelId,
                "Adkar Reminders",
                NotificationManager.IMPORTANCE_DEFAULT
            )
            notificationManager.createNotificationChannel(channel)
        }

        val intent = Intent(context, MainActivity::class.java).apply {
            flags = Intent.FLAG_ACTIVITY_NEW_TASK or Intent.FLAG_ACTIVITY_CLEAR_TASK
        }
        val pendingIntent = PendingIntent.getActivity(
            context, 0, intent,
            PendingIntent.FLAG_UPDATE_CURRENT or PendingIntent.FLAG_IMMUTABLE
        )

        val notification = NotificationCompat.Builder(context, channelId)
            .setSmallIcon(R.drawable.ic_launcher_foreground) // Use a proper icon if available
            .setContentTitle(categoryName)
            .setContentText(context.getString(R.string.notification_body))
            .setPriority(NotificationCompat.PRIORITY_DEFAULT)
            .setContentIntent(pendingIntent)
            .setAutoCancel(true)
            .build()

        notificationManager.notify(categoryId.hashCode(), notification)
    }
}
