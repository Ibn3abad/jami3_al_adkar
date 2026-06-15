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

import android.app.TimePickerDialog
import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.activity.enableEdgeToEdge
import androidx.core.splashscreen.SplashScreen.Companion.installSplashScreen
import androidx.compose.foundation.ExperimentalFoundationApi
import androidx.compose.foundation.combinedClickable
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.verticalScroll
import androidx.compose.foundation.background
import androidx.compose.foundation.Image
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.filled.ArrowBack
import androidx.compose.material.icons.automirrored.filled.Login
import androidx.compose.material.icons.automirrored.filled.Logout
import androidx.compose.material.icons.filled.AccessTime
import androidx.compose.material.icons.filled.Bedtime
import androidx.compose.material.icons.filled.Favorite
import androidx.compose.material.icons.filled.FavoriteBorder
import androidx.compose.material.icons.filled.NightsStay
import androidx.compose.material.icons.filled.WbSunny
import androidx.compose.material3.Button
import androidx.compose.material3.Card
import androidx.compose.material3.CardDefaults
import androidx.compose.material3.CircularProgressIndicator
import androidx.compose.material3.ExperimentalMaterial3Api
import androidx.compose.material3.Icon
import androidx.compose.material3.IconButton
import androidx.compose.material3.LinearProgressIndicator
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.OutlinedButton
import androidx.compose.material3.Scaffold
import androidx.compose.material3.Text
import androidx.compose.material3.TopAppBar
import androidx.compose.material3.adaptive.navigationsuite.NavigationSuiteScaffold
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.collectAsState
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableIntStateOf
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.saveable.listSaver
import androidx.compose.runtime.saveable.rememberSaveable
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.alpha
import androidx.compose.ui.draw.drawBehind
import androidx.compose.ui.graphics.Brush
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.vector.ImageVector
import androidx.compose.ui.layout.ContentScale
import androidx.compose.ui.res.painterResource
import androidx.compose.ui.res.stringResource
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.tooling.preview.Preview
import androidx.compose.ui.tooling.preview.PreviewScreenSizes
import androidx.compose.ui.unit.dp
import androidx.compose.ui.platform.LocalContext
import androidx.lifecycle.viewmodel.compose.viewModel
import com.ibn3abad.jami3_al_adkar.ui.AdkarUiState
import com.ibn3abad.jami3_al_adkar.ui.AdkarViewModel
import com.ibn3abad.jami3_al_adkar.ui.AppLanguage
import com.ibn3abad.jami3_al_adkar.ui.ProfileViewModel
import com.ibn3abad.jami3_al_adkar.ui.theme.Jami3_al_adkarTheme

class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        val splashScreen = installSplashScreen()
        super.onCreate(savedInstanceState)
        
        val startTime = System.currentTimeMillis()
        splashScreen.setKeepOnScreenCondition {
            System.currentTimeMillis() - startTime < 1000
        }

        enableEdgeToEdge()
        setContent {
            val profileViewModel: ProfileViewModel = viewModel(factory = ProfileViewModel.Factory)
            val language by profileViewModel.language.collectAsState()
            
            Jami3_al_adkarTheme {
                Jami3_al_adkarApp(profileViewModel, language)
            }
        }
    }
}

val DestinationSaver = listSaver<Any, Any>(
    save = {
        when (it) {
            is AppDestinations -> listOf("ENUM", it.name)
            is AdkarDetailsDestination -> listOf("DETAILS", it.categoryId, it.categoryNameResId)
            else -> emptyList()
        }
    },
    restore = {
        val list = it as List<*>
        if (list.size >= 2 && list[0] == "ENUM") {
            AppDestinations.valueOf(list[1] as String)
        } else if (list.size >= 3 && list[0] == "DETAILS") {
            AdkarDetailsDestination(list[1] as String, list[2] as Int)
        } else {
            null
        }
    }
)

@PreviewScreenSizes
@Composable
fun Jami3_al_adkarApp(
    profileViewModel: ProfileViewModel = viewModel(),
    language: AppLanguage = AppLanguage.GERMAN
) {
    var currentDestination by rememberSaveable(stateSaver = DestinationSaver) { 
        mutableStateOf<Any>(AppDestinations.HOME) 
    }

    Box(
        modifier = Modifier.fillMaxSize()
    ) {
        // Background Image
        Image(
            painter = painterResource(id = R.drawable.app_background),
            contentDescription = null,
            modifier = Modifier.fillMaxSize(),
            contentScale = ContentScale.Crop
        )

        NavigationSuiteScaffold(
            modifier = Modifier.fillMaxSize(),
            containerColor = Color.Transparent, // Make scaffold transparent to see background
            navigationSuiteItems = {
                AppDestinations.entries.forEach { destination ->
                    item(
                        icon = {
                            Icon(
                                painterResource(destination.icon),
                                contentDescription = null // We'll handle label below
                            )
                        },
                        label = { 
                            Text(localizedString(destination.labelResId, language)) 
                        },
                        selected = (currentDestination is AppDestinations) && destination == currentDestination,
                        onClick = { currentDestination = destination }
                    )
                }
            }
        ) {
            Scaffold(
                modifier = Modifier.fillMaxSize(),
                containerColor = Color.Transparent // Make internal scaffold transparent
            ) { innerPadding ->
                when (val dest = currentDestination) {
                    AppDestinations.HOME -> AdkarHome(
                        language = language,
                        modifier = Modifier.padding(innerPadding),
                        onCategoryClick = { category ->
                            currentDestination = AdkarDetailsDestination(
                                category.id, 
                                category.titleResId
                            )
                        }
                    )

                    is AdkarDetailsDestination -> AdkarDetailsScreen(
                        categoryId = dest.categoryId,
                        categoryNameResId = dest.categoryNameResId,
                        language = language,
                        modifier = Modifier.padding(innerPadding),
                        onBack = { currentDestination = AppDestinations.HOME }
                    )

                    AppDestinations.PROFILE -> ProfileScreen(
                        profileViewModel = profileViewModel,
                        language = language,
                        modifier = Modifier.padding(innerPadding)
                    )

                    AppDestinations.FAVORITES -> FavoritesScreen(
                        language = language,
                        modifier = Modifier.padding(innerPadding)
                    )

                    else -> {
                        val label = (dest as? AppDestinations)?.let { 
                            localizedString(it.labelResId, language)
                        } ?: stringResource(R.string.app_name)
                        
                        Greeting(
                            name = label,
                            language = language,
                            modifier = Modifier.padding(innerPadding)
                        )
                    }
                }
            }
        }
    }
}

data class AdkarDetailsDestination(
    val categoryId: String, 
    val categoryNameResId: Int
)

@OptIn(ExperimentalMaterial3Api::class, ExperimentalFoundationApi::class)
@Composable
fun AdkarDetailsScreen(
    categoryId: String,
    categoryNameResId: Int,
    language: AppLanguage,
    modifier: Modifier = Modifier,
    onBack: () -> Unit,
    viewModel: AdkarViewModel = viewModel(factory = AdkarViewModel.Factory)
) {
    val uiState by viewModel.uiState.collectAsState()

    // Load data when the screen is first shown
    LaunchedEffect(categoryId) {
        viewModel.loadAdkarByCategory(categoryId)
    }

    Column(modifier = modifier.fillMaxSize()) {
        TopAppBar(
            title = { Text(localizedString(categoryNameResId, language)) },
            navigationIcon = {
                IconButton(onClick = onBack) {
                    Icon(
                        imageVector = Icons.AutoMirrored.Filled.ArrowBack,
                        contentDescription = localizedString(R.string.back, language)
                    )
                }
            }
        )

        when (val state = uiState) {
            is AdkarUiState.Loading -> {
                Box(
                    modifier = Modifier.fillMaxSize(),
                    contentAlignment = Alignment.Center
                ) {
                    CircularProgressIndicator()
                }
            }

            is AdkarUiState.Empty -> {
                Box(
                    modifier = Modifier.fillMaxSize(),
                    contentAlignment = Alignment.Center
                ) {
                    Text(localizedString(R.string.no_adkar_found, language))
                }
            }

            is AdkarUiState.Success -> {
                val adkarList = state.adkarList
                var currentIndex by remember(categoryId) { mutableIntStateOf(0) }
                
                // Safety check: reset if index is out of bounds (e.g. after list shrinks)
                if (currentIndex >= adkarList.size) {
                    currentIndex = 0
                }
                
                var currentRepetitionCount by remember(currentIndex, categoryId) { mutableIntStateOf(0) }
                val currentAdkar = adkarList[currentIndex]

                Column(
                    modifier = Modifier
                        .fillMaxSize()
                        .padding(16.dp),
                    horizontalAlignment = Alignment.CenterHorizontally
                ) {
                    Text(
                        text = localizedString(R.string.dhikr_count_label, language, currentIndex + 1, adkarList.size),
                        style = MaterialTheme.typography.labelLarge,
                        modifier = Modifier.padding(bottom = 8.dp)
                    )

                    Card(
                        modifier = Modifier
                            .weight(1f)
                            .fillMaxWidth()
                            .combinedClickable(
                                onClick = {
                                    if (currentRepetitionCount < currentAdkar.repetitions) {
                                        currentRepetitionCount++
                                        if (currentRepetitionCount == currentAdkar.repetitions) {
                                            viewModel.markAsCompleted(currentAdkar)
                                        }
                                    } else if (currentIndex < adkarList.size - 1) {
                                        currentIndex++
                                    }
                                },
                                onLongClick = {
                                    viewModel.toggleFavorite(currentAdkar)
                                }
                            ),
                        elevation = CardDefaults.cardElevation(defaultElevation = 4.dp),
                        colors = CardDefaults.cardColors(
                            containerColor = MaterialTheme.colorScheme.surface.copy(alpha = 0.8f)
                        )
                    ) {
                        Column(
                            modifier = Modifier
                                .padding(24.dp)
                                .fillMaxSize(),
                            horizontalAlignment = Alignment.CenterHorizontally
                        ) {
                            Column(
                                modifier = Modifier
                                    .weight(1f)
                                    .verticalScroll(rememberScrollState()),
                                horizontalAlignment = Alignment.CenterHorizontally,
                                verticalArrangement = Arrangement.Center
                            ) {
                                Box(modifier = Modifier.fillMaxWidth()) {
                                    if (currentAdkar.isFavorite) {
                                        Icon(
                                            imageVector = Icons.Default.Favorite,
                                            contentDescription = null,
                                            tint = MaterialTheme.colorScheme.primary,
                                            modifier = Modifier.align(Alignment.TopEnd)
                                        )
                                    } else {
                                        Icon(
                                            imageVector = Icons.Default.FavoriteBorder,
                                            contentDescription = null,
                                            tint = MaterialTheme.colorScheme.outline,
                                            modifier = Modifier.align(Alignment.TopEnd)
                                        )
                                    }

                                    Text(
                                        text = currentAdkar.textArabic,
                                        style = MaterialTheme.typography.headlineSmall,
                                        textAlign = TextAlign.Center,
                                        fontWeight = FontWeight.Bold,
                                        modifier = Modifier
                                            .padding(bottom = 16.dp, top = 24.dp)
                                            .align(Alignment.Center)
                                    )
                                }

                                if (!language.isRtl) {
                                    Text(
                                        text = currentAdkar.transliteration,
                                        style = MaterialTheme.typography.bodyMedium,
                                        textAlign = TextAlign.Center,
                                        modifier = Modifier.padding(bottom = 16.dp)
                                    )

                                    val translation = when (language) {
                                        AppLanguage.GERMAN -> currentAdkar.translationDe
                                        AppLanguage.ENGLISH -> currentAdkar.translationEn
                                        AppLanguage.FRENCH -> currentAdkar.translationFr
                                        AppLanguage.SPANISH -> currentAdkar.translationEs
                                        AppLanguage.URDU -> currentAdkar.translationUr
                                        AppLanguage.FARISI -> currentAdkar.translationFa
                                        else -> currentAdkar.translationEn
                                    }

                                    if (translation.isNotEmpty()) {
                                        Text(
                                            text = translation,
                                            style = MaterialTheme.typography.bodyLarge,
                                            textAlign = TextAlign.Center,
                                            modifier = Modifier.padding(bottom = 16.dp)
                                        )
                                    }
                                }
                            }

                            Spacer(modifier = Modifier.size(16.dp))

                            // Repetition Counter UI
                            Column(
                                horizontalAlignment = Alignment.CenterHorizontally,
                                modifier = Modifier.padding(bottom = 16.dp)
                            ) {
                                Text(
                                    text = "$currentRepetitionCount / ${currentAdkar.repetitions}",
                                    style = MaterialTheme.typography.displaySmall,
                                    color = if (currentRepetitionCount == currentAdkar.repetitions) 
                                        MaterialTheme.colorScheme.primary 
                                    else 
                                        MaterialTheme.colorScheme.onSurface,
                                    fontWeight = FontWeight.ExtraBold
                                )
                                Text(
                                    text = if (currentRepetitionCount < currentAdkar.repetitions) {
                                        localizedString(R.string.tap_to_count, language)
                                    } else if (currentIndex < adkarList.size - 1) {
                                        localizedString(R.string.done_next, language)
                                    } else {
                                        localizedString(R.string.all_adkar_read, language)
                                    },
                                    style = MaterialTheme.typography.labelMedium,
                                    color = MaterialTheme.colorScheme.outline
                                )
                            }

                            val sourceVal = if (language.isRtl) currentAdkar.sourceArabic else currentAdkar.source
                            Text(
                                text = localizedString(R.string.source_label, language, sourceVal),
                                style = MaterialTheme.typography.bodySmall,
                                textAlign = TextAlign.Center,
                                color = MaterialTheme.colorScheme.outline
                            )
                        }
                    }

                    Spacer(modifier = Modifier.size(16.dp))

                    Row(
                        modifier = Modifier.fillMaxWidth(),
                        horizontalArrangement = Arrangement.SpaceEvenly
                    ) {
                        Button(
                            onClick = { 
                                if (currentIndex > 0) {
                                    currentIndex--
                                }
                            },
                            enabled = currentIndex > 0,
                            modifier = Modifier.weight(1f).padding(end = 8.dp)
                        ) {
                            Text(localizedString(R.string.previous, language))
                        }
                        Button(
                            onClick = {
                                if (currentIndex < adkarList.size - 1) {
                                    currentIndex++
                                }
                            },
                            enabled = currentIndex < adkarList.size - 1,
                            modifier = Modifier.weight(1f).padding(start = 8.dp)
                        ) {
                            Text(localizedString(R.string.next, language))
                        }
                    }
                }
            }
        }
    }
}

@Composable
fun AdkarHome(
    language: AppLanguage,
    modifier: Modifier = Modifier,
    onCategoryClick: (AdkarCategory) -> Unit = {}
) {
    val categories = listOf(
        AdkarCategory("Adhkar_Sabah", R.string.cat_morning, Icons.Default.WbSunny),
        AdkarCategory("Adhkar_Masae", R.string.cat_evening, Icons.Default.NightsStay),
        AdkarCategory("Adhkar_Nawm", R.string.cat_sleep, Icons.Default.Bedtime),
        AdkarCategory("Adhkar_Dukhoul", R.string.cat_entering, Icons.AutoMirrored.Filled.Login),
        AdkarCategory("Adhkar_Khorouj", R.string.cat_leaving, Icons.AutoMirrored.Filled.Logout)
    )

    LazyColumn(
        modifier = modifier
            .fillMaxSize()
            .padding(16.dp),
        verticalArrangement = Arrangement.spacedBy(12.dp)
    ) {
        item {
            Text(
                text = localizedString(R.string.choose_your_adkar, language),
                style = MaterialTheme.typography.headlineMedium,
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(bottom = 16.dp),
                textAlign = TextAlign.Center,
                fontWeight = FontWeight.Bold
            )
        }
        items(categories) { category ->
            AdkarCategoryCard(
                category = category, 
                language = language,
                onClick = { onCategoryClick(category) }
            )
        }
    }
}

@Composable
fun AdkarCategoryCard(category: AdkarCategory, language: AppLanguage, onClick: () -> Unit) {
    Card(
        onClick = onClick,
        modifier = Modifier.fillMaxWidth(),
        colors = CardDefaults.cardColors(
            containerColor = MaterialTheme.colorScheme.surfaceVariant.copy(alpha = 0.7f)
        )
    ) {
        Row(
            modifier = Modifier
                .padding(20.dp)
                .fillMaxWidth(),
            verticalAlignment = Alignment.CenterVertically,
            horizontalArrangement = if (language.isRtl) Arrangement.End else Arrangement.Start
        ) {
            if (!language.isRtl) {
                Icon(
                    imageVector = category.icon,
                    contentDescription = null,
                    modifier = Modifier.size(32.dp),
                    tint = MaterialTheme.colorScheme.primary
                )
                Spacer(modifier = Modifier.width(16.dp))
            }
            
            Column(
                horizontalAlignment = if (language.isRtl) Alignment.End else Alignment.Start,
                modifier = Modifier.weight(1f)
            ) {
                Text(
                    text = localizedString(category.titleResId, AppLanguage.ARABIC),
                    style = MaterialTheme.typography.titleLarge,
                    fontWeight = FontWeight.Bold
                )
                if (language != AppLanguage.ARABIC) {
                    Text(
                        text = localizedString(category.titleResId, language),
                        style = MaterialTheme.typography.bodyMedium,
                        color = MaterialTheme.colorScheme.onSurfaceVariant
                    )
                }
            }
            
            if (language.isRtl) {
                Spacer(modifier = Modifier.width(16.dp))
                Icon(
                    imageVector = category.icon,
                    contentDescription = null,
                    modifier = Modifier.size(32.dp),
                    tint = MaterialTheme.colorScheme.primary
                )
            }
        }
    }
}

@OptIn(androidx.compose.foundation.layout.ExperimentalLayoutApi::class)
@Composable
fun ProfileScreen(
    profileViewModel: ProfileViewModel,
    language: AppLanguage,
    modifier: Modifier = Modifier
) {
    val progress by profileViewModel.progress.collectAsState()
    val morningTime by profileViewModel.morningTime.collectAsState()
    val eveningTime by profileViewModel.eveningTime.collectAsState()
    val sleepTime by profileViewModel.sleepTime.collectAsState()
    val context = LocalContext.current

    LaunchedEffect(Unit) {
        profileViewModel.loadProgress()
    }

    fun showTimePicker(categoryId: String, currentVal: String, label: String) {
        val parts = currentVal.split(":")
        val hour = parts[0].toInt()
        val minute = parts[1].toInt()

        TimePickerDialog(context, { _, h, m ->
            val newTime = String.format("%02d:%02d", h, m)
            profileViewModel.setReminderTime(categoryId, newTime, label)
        }, hour, minute, true).show()
    }

    Column(
        modifier = modifier
            .fillMaxSize()
            .verticalScroll(rememberScrollState())
            .padding(24.dp),
        horizontalAlignment = if (language.isRtl) Alignment.End else Alignment.Start
    ) {
        Text(
            text = localizedString(R.string.settings_progress, language),
            style = MaterialTheme.typography.headlineMedium,
            fontWeight = FontWeight.Bold,
            modifier = Modifier.padding(bottom = 24.dp)
        )

        Text(
            text = localizedString(R.string.today_progress, language),
            style = MaterialTheme.typography.titleLarge,
            modifier = Modifier.padding(bottom = 16.dp)
        )

        progress.forEach { catProgress ->
            val baseResId = when (catProgress.categoryId) {
                "Adhkar_Sabah" -> R.string.cat_morning
                "Adhkar_Masae" -> R.string.cat_evening
                "Adhkar_Nawm" -> R.string.cat_sleep
                "Adhkar_Dukhoul" -> R.string.cat_entering
                "Adhkar_Khorouj" -> R.string.cat_leaving
                else -> -1
            }

            Column(modifier = Modifier.fillMaxWidth().padding(bottom = 12.dp)) {
                Row(
                    modifier = Modifier.fillMaxWidth(),
                    horizontalArrangement = Arrangement.SpaceBetween
                ) {
                    Text(
                        text = if (baseResId != -1) localizedString(baseResId, language) else catProgress.categoryId,
                        style = MaterialTheme.typography.bodyMedium
                    )
                    Text(
                        text = "${(catProgress.percentage * 100).toInt()}%",
                        style = MaterialTheme.typography.bodySmall
                    )
                }
                LinearProgressIndicator(
                    progress = { catProgress.percentage },
                    modifier = Modifier.fillMaxWidth().padding(top = 4.dp),
                )
            }
        }

        Spacer(modifier = Modifier.size(24.dp))

        // Reminders Section
        Text(
            text = localizedString(R.string.reminders, language),
            style = MaterialTheme.typography.titleLarge,
            modifier = Modifier.padding(bottom = 16.dp)
        )

    val morningLabel = localizedString(R.string.morning_reminder, language)
    val eveningLabel = localizedString(R.string.evening_reminder, language)
    val sleepLabel = localizedString(R.string.sleep_reminder, language)

    ReminderRow(
        label = morningLabel,
        time = morningTime,
        onClick = { showTimePicker("morning", morningTime, morningLabel) },
        language = language
    )
    ReminderRow(
        label = eveningLabel,
        time = eveningTime,
        onClick = { showTimePicker("evening", eveningTime, eveningLabel) },
        language = language
    )
    ReminderRow(
        label = sleepLabel,
        time = sleepTime,
        onClick = { showTimePicker("sleep", sleepTime, sleepLabel) },
        language = language
    )

        Spacer(modifier = Modifier.size(24.dp))

        Text(
            text = localizedString(R.string.language, language),
            style = MaterialTheme.typography.titleLarge,
            modifier = Modifier.padding(bottom = 16.dp)
        )

        androidx.compose.foundation.layout.FlowRow(
            modifier = Modifier.fillMaxWidth(),
            horizontalArrangement = Arrangement.spacedBy(8.dp),
            verticalArrangement = Arrangement.spacedBy(8.dp)
        ) {
            AppLanguage.entries.forEach { lang ->
                Button(
                    onClick = { profileViewModel.setLanguage(lang) },
                    enabled = language != lang,
                    modifier = Modifier.padding(bottom = 4.dp)
                ) {
                    Text(lang.nativeName)
                }
            }
        }
    }
}

@Composable
fun ReminderRow(label: String, time: String, onClick: () -> Unit, language: AppLanguage) {
    Row(
        modifier = Modifier
            .fillMaxWidth()
            .padding(vertical = 8.dp),
        horizontalArrangement = if (language.isRtl) Arrangement.End else Arrangement.Start,
        verticalAlignment = Alignment.CenterVertically
    ) {
        if (!language.isRtl) {
            Text(text = label, modifier = Modifier.weight(1f))
            OutlinedButton(onClick = onClick) {
                Icon(Icons.Default.AccessTime, contentDescription = null, modifier = Modifier.size(18.dp))
                Spacer(Modifier.width(8.dp))
                Text(text = time)
            }
        } else {
            OutlinedButton(onClick = onClick) {
                Text(text = time)
                Spacer(Modifier.width(8.dp))
                Icon(Icons.Default.AccessTime, contentDescription = null, modifier = Modifier.size(18.dp))
            }
            Spacer(Modifier.width(16.dp))
            Text(text = label, modifier = Modifier.weight(1f), textAlign = TextAlign.End)
        }
    }
}

data class AdkarCategory(
    val id: String,
    val titleResId: Int,
    val icon: ImageVector
)

enum class AppDestinations(
    val labelResId: Int,
    val icon: Int,
) {
    HOME(R.string.dest_home, R.drawable.ic_home),
    FAVORITES(R.string.dest_favorites, R.drawable.ic_favorite),
    PROFILE(R.string.dest_profile, R.drawable.ic_account_box),
}

@Composable
fun FavoritesScreen(
    language: AppLanguage,
    modifier: Modifier = Modifier,
    viewModel: AdkarViewModel = viewModel(factory = AdkarViewModel.Factory)
) {
    val uiState by viewModel.uiState.collectAsState()

    LaunchedEffect(Unit) {
        viewModel.loadFavorites()
    }

    Column(
        modifier = modifier
            .fillMaxSize()
            .padding(16.dp)
    ) {
        Text(
            text = localizedString(R.string.favorites, language),
            style = MaterialTheme.typography.headlineMedium,
            fontWeight = FontWeight.Bold,
            modifier = Modifier
                .fillMaxWidth()
                .padding(bottom = 16.dp),
            textAlign = TextAlign.Center
        )

        when (val state = uiState) {
            is AdkarUiState.Loading -> {
                Box(modifier = Modifier.fillMaxSize(), contentAlignment = Alignment.Center) {
                    CircularProgressIndicator()
                }
            }

            is AdkarUiState.Empty -> {
                Box(modifier = Modifier.fillMaxSize(), contentAlignment = Alignment.Center) {
                    Text(
                        text = localizedString(R.string.no_favorites_yet, language),
                        style = MaterialTheme.typography.bodyLarge,
                        color = MaterialTheme.colorScheme.outline
                    )
                }
            }

            is AdkarUiState.Success -> {
                LazyColumn(
                    verticalArrangement = Arrangement.spacedBy(12.dp)
                ) {
                    items(state.adkarList) { adkar ->
                        Card(
                            modifier = Modifier.fillMaxWidth(),
                            onClick = { /* Could navigate to details or just show here */ },
                            colors = CardDefaults.cardColors(
                                containerColor = MaterialTheme.colorScheme.surfaceVariant.copy(alpha = 0.7f)
                            )
                        ) {
                            Column(modifier = Modifier.padding(16.dp)) {
                                Text(
                                    text = adkar.textArabic,
                                    style = MaterialTheme.typography.titleMedium,
                                    fontWeight = FontWeight.Bold,
                                    textAlign = TextAlign.End,
                                    modifier = Modifier.fillMaxWidth()
                                )
                                if (!language.isRtl) {
                                    Spacer(modifier = Modifier.size(8.dp))
                                    val translation = when (language) {
                                        AppLanguage.GERMAN -> adkar.translationDe
                                        AppLanguage.ENGLISH -> adkar.translationEn
                                        AppLanguage.FRENCH -> adkar.translationFr
                                        AppLanguage.SPANISH -> adkar.translationEs
                                        AppLanguage.URDU -> adkar.translationUr
                                        AppLanguage.FARISI -> adkar.translationFa
                                        else -> adkar.translationEn
                                    }
                                    if (translation.isNotEmpty()) {
                                        Text(
                                            text = translation,
                                            style = MaterialTheme.typography.bodyMedium
                                        )
                                    }
                                }
                                Row(
                                    modifier = Modifier.fillMaxWidth(),
                                    horizontalArrangement = Arrangement.End
                                ) {
                                    IconButton(onClick = { viewModel.toggleFavorite(adkar) }) {
                                        Icon(
                                            imageVector = Icons.Default.Favorite,
                                            contentDescription = null,
                                            tint = MaterialTheme.colorScheme.primary
                                        )
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
    }
}

@Composable
fun Greeting(name: String, language: AppLanguage, modifier: Modifier = Modifier) {
    Column(
        modifier = modifier.fillMaxSize(),
        verticalArrangement = Arrangement.Center,
        horizontalAlignment = Alignment.CenterHorizontally
    ) {
        Text(text = localizedString(R.string.welcome_to, language, name))
    }
}

@Composable
fun localizedString(baseResId: Int, language: AppLanguage, vararg formatArgs: Any): String {
    val context = LocalContext.current
    val baseName = try {
        context.resources.getResourceEntryName(baseResId)
    } catch (e: Exception) {
        ""
    }
    
    if (baseName.isEmpty()) return ""

    val suffix = when (language) {
        AppLanguage.ARABIC -> "_ar"
        AppLanguage.GERMAN -> "_de"
        AppLanguage.FRENCH -> "_fr"
        AppLanguage.SPANISH -> "_es"
        AppLanguage.URDU -> "_ur"
        AppLanguage.FARISI -> "_fa"
        else -> "" // English/Default
    }

    val resId = if (suffix.isEmpty()) baseResId
    else context.resources.getIdentifier(baseName + suffix, "string", context.packageName)

    return if (resId != 0) stringResource(resId, *formatArgs) else stringResource(baseResId, *formatArgs)
}

@Preview(showBackground = true)
@Composable
fun GreetingPreview() {
    Jami3_al_adkarTheme {
        Greeting("الأذكار", AppLanguage.ARABIC)
    }
}
