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

package com.ibn3abad.jami3_al_adkar.ui.theme

import android.os.Build
import androidx.compose.foundation.isSystemInDarkTheme
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.darkColorScheme
import androidx.compose.material3.dynamicDarkColorScheme
import androidx.compose.material3.dynamicLightColorScheme
import androidx.compose.material3.lightColorScheme
import androidx.compose.runtime.Composable
import androidx.compose.ui.platform.LocalContext

private val DarkColorScheme = darkColorScheme(
    primary = PurpleDeep,         // Dunkles Violett als Hauptfarbe für Buttons etc.
    secondary = PurplePrimary,    // Helles Violett nur als Akzent
    tertiary = Pink80,
    background = Black,           // Tiefschwarzer Hintergrund
    surface = DarkGrey800,        // Sehr dunkles Grau für Oberflächen
    onPrimary = White,
    onSecondary = White,
    onBackground = White,
    onSurface = White,
    primaryContainer = PurpleDeep,
    onPrimaryContainer = White,
    surfaceVariant = DarkGrey700, // Dunkles Grau für Karten
    onSurfaceVariant = White,
    outline = PurplePrimary       // Linien/Ränder im hellen Violett
)

private val LightColorScheme = lightColorScheme(
    primary = Purple40,
    secondary = PurpleGrey40,
    tertiary = Pink40,
    background = White,
    surface = White,
    onBackground = Black,
    onSurface = Black
)

@Composable
fun Jami3_al_adkarTheme(
    darkTheme: Boolean = isSystemInDarkTheme(),
    dynamicColor: Boolean = false,
    content: @Composable () -> Unit
) {
    val colorScheme = when {
        dynamicColor && Build.VERSION.SDK_INT >= Build.VERSION_CODES.S -> {
            val context = LocalContext.current
            if (darkTheme) dynamicDarkColorScheme(context) else dynamicLightColorScheme(context)
        }

        darkTheme -> DarkColorScheme
        else -> LightColorScheme
    }

    MaterialTheme(
        colorScheme = colorScheme,
        typography = Typography,
        content = content
    )
}