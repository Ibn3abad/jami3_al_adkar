# 📿 Jami3 Al Adkar — جامع الأذكار


An open-source Android app for daily Islamic remembrances (أذكار), built with Jetpack Compose and Room.

---

## Features

- **5 Adhkar categories** — Morning, Evening, Before Sleep, Entering the Home, Leaving the Home
- **Tap-to-count** — tap a card to count each repetition; the app tracks when all repetitions are done
- **Favorites** — long-press any dhikr to save it; view all favorites in a dedicated screen
- **Daily progress** — track completion per category for the current day
- **Scheduled reminders** — set custom reminder times for Morning, Evening and Sleep adhkar, persisted across reboots
- **6 languages** — Arabic, German, English, French, Spanish, Urdu, Persian (Farsi)
- **Full RTL support** — layout and text direction adapt automatically for Arabic, Urdu and Farsi
- **Transliteration** — Latin-script pronunciation guide shown alongside Arabic text
- **Source references** — each dhikr shows its hadith source (e.g. Sahih al-Bukhari, Hisn al-Muslim)
- **Pre-populated SQLite database** — all adhkar are shipped as an asset DB; no network required

---

## Screenshots

> _(coming soon)_

---

## Tech Stack

| Layer | Library |
|---|---|
| UI | Jetpack Compose + Material 3 |
| Navigation | `NavigationSuiteScaffold` (adaptive: bottom bar / side rail) |
| State | `ViewModel` + `StateFlow` |
| Database | Room (pre-populated via `createFromAsset`) |
| Reminders | `AlarmManager` + `BroadcastReceiver` + `BootReceiver` |
| Build | Kotlin 2.2 · KSP · Gradle version catalog |

- **Min SDK:** Android 7.0 (API 24)
- **Target SDK:** API 36
- **Language:** Kotlin

---

## Project Structure

```
app/src/main/
├── assets/
│   └── adkar.db                  # Pre-populated SQLite database
├── java/com/ibn3abad/jami3_al_adkar/
│   ├── MainActivity.kt           # UI, composables, navigation
│   ├── Jami3AlAdkarApplication.kt
│   ├── data/
│   │   ├── AdkarDatabase.kt      # Room database (createFromAsset)
│   │   ├── model/Adkar.kt        # Entity
│   │   ├── dao/AdkarDao.kt       # DAO queries
│   │   └── repository/AdkarRepository.kt
│   ├── ui/
│   │   ├── AdkarViewModel.kt
│   │   ├── ProfileViewModel.kt
│   │   └── theme/
│   ├── receiver/
│   │   ├── ReminderReceiver.kt
│   │   └── BootReceiver.kt
│   └── util/
│       └── ReminderManager.kt    # AlarmManager scheduling
```

---

## Getting Started

### Prerequisites

- Android Studio Meerkat or newer
- JDK 11+

### Build

```bash
git clone https://github.com/Ibn3abad/jami3_al_adkar.git
cd jami3_al_adkar
./gradlew assembleDebug
```

The APK will be at `app/build/outputs/apk/debug/app-debug.apk`.

---

## Adding or Editing Adhkar

All adhkar live in `app/src/main/assets/adkar.db`. To modify the content:

1. Open the DB with any SQLite editor (e.g. [DB Browser for SQLite](https://sqlitebrowser.org/))
2. Edit the `adkar` table
3. Replace the file in `assets/`
4. Increment `version` in `@Database(version = ...)` in `AdkarDatabase.kt`

Each row has the following columns:

| Column | Description |
|---|---|
| `id` | Unique integer (e.g. 101 = Sabah #1, 201 = Masae #1) |
| `category` | `Adhkar_Sabah`, `Adhkar_Masae`, `Adhkar_Nawm`, `Adhkar_Dukhoul`, `Adhkar_Khorouj` |
| `textArabic` | Arabic text |
| `transliteration` | Latin-script pronunciation |
| `translationDe/En/Fr/Es/Ur/Fa` | Translations |
| `repetitions` | How many times to recite |
| `source` | Hadith source (Latin) |
| `sourceArabic` | Hadith source (Arabic) |
| `isFavorite` | 0 / 1 |
| `lastCompletedDate` | ISO date string or NULL |

---

## License

This project is free software, distributed under the **GNU General Public License v3.0** — see [`LICENSE`](LICENSE) for details.

---

## Author

**A. KHOUK** · 2026
