#!/usr/bin/env python3
"""
@author     A. KHOUK
@date       12.06.2026
@version    1.01
@copyright  Copyright (c) 2026, A. KHOUK.
@license    This program is free software: you can redistribute it and/or modify
            it under the terms of the GNU General Public License as published by
            the Free Software Foundation, either version 3 of the License, or
            (at your option) any later version.
────────────────────────────────────────────────────────────────────────

generate_adkar_db.py
--------------------
Generates adkar.db for the jami3_al_adkar Android app.

The schema matches the Room @Database(version = 9) definition exactly:
  - id INTEGER NOT NULL PRIMARY KEY  (no AUTOINCREMENT, no DEFAULT)
  - all TEXT/INTEGER columns without DEFAULT clauses
  - room_master_table with the correct identity hash

Usage:
    python3 generate_adkar_db.py
    # outputs: adkar.db  →  copy to app/src/main/assets/adkar.db

To add more adhkar: just extend the ADKAR list below.
Category IDs used:
  101-1xx  Adhkar_Sabah   (Morning)
  201-2xx  Adhkar_Masae   (Evening)
  301-3xx  Adhkar_Nawm    (Sleep)
  401-4xx  Adhkar_Khorouj (Leaving home)
  501-5xx  Adhkar_Dukhoul (Entering home)
"""

import sqlite3
import struct
import os

OUTPUT_FILE = "adkar.db"

# Room identity hash for version 9 of AdkarDatabase
# (taken from the crash log: Expected identity hash: 9898b877d94a5411ec912820e8de18b2)
ROOM_IDENTITY_HASH = "9898b877d94a5411ec912820e8de18b2"
ROOM_DB_VERSION = 12

# ---------------------------------------------------------------------------
# Data
# ---------------------------------------------------------------------------

ADKAR = [
    # ── Adhkar_Sabah (Morning) ──────────────────────────────────────────────
    {
        "id": 101,
        "category": "Adhkar_Sabah",
        "textArabic": "أَصْبَحْنَا وَأَصْبَحَ الْمُلْكُ لِلَّهِ، وَالْحَمْدُ لِلَّهِ، لَا إِلَهَ إِلَّا اللهُ وَحْدَهُ لَا شَرِيكَ لَهُ، لَهُ الْمُلْكُ وَلَهُ الْحَمْدُ وَهُوَ عَلَى كُلِّ شَيْءٍ قَدِيرٌ",
        "transliteration": "Asbahna wa asbahal-mulku lillah, wal-hamdulillah. La ilaha illallahu wahdahu la sharika lah, lahul-mulku wa lahul-hamdu wa Huwa 'ala kulli shay'in Qadir.",
        "translationDe": "Wir haben den Morgen erreicht, und die Herrschaft gehört Allah, und alles Lob gebührt Allah. Es gibt keinen Gott außer Allah allein, Er hat keinen Partner. Ihm gehört die Herrschaft und Ihm gebührt das Lob, und Er hat Macht über alle Dinge.",
        "translationEn": "We have reached the morning and at this very time unto Allah belongs all sovereignty, and all praise is for Allah. None has the right to be worshipped but Allah alone, without partner, to Him belongs all sovereignty and praise and He is over all things omnipotent.",
        "translationFr": "Nous sommes au matin et la royauté appartient à Allah. Louange à Allah. Il n'y a d'autre divinité qu'Allah, Seul, sans associé. À Lui la royauté, à Lui la louange et Il est Capable de toute chose.",
        "translationEs": "Hemos llegado a la mañana y la soberanía pertenece a Alá, y toda alabanza es para Alá. No hay más dios que Alá solo, sin socio, suya es la soberanía y suya es la alabanza y Él tiene poder sobre todas las cosas.",
        "translationUr": "ہم نے صبح کی اور اللہ کے لیے تمام بادشاہت ہے، اور تمام تعریف اللہ کے لیے ہے۔ اللہ کے سوا کوئی معبود نہیں وہ اکیلا ہے اس کا کوئی شریک نہیں، اسی کے لیے بادشاہت ہے اور اسی کے لیے تعریف ہے اور وہ ہر چیز پر قادر ہے۔",
        "translationFa": "ما به صبح رسیدیم و پادشاهی از آن خداست و حمد مخصوص خداست. معبودی جز خدای یگانه نیست، شریکی ندارد، فرمانروایی و ستایش از آن اوست و او بر هر چیزی تواناست.",
        "repetitions": 1,
        "source": "Sahih Muslim / Hisn al-Muslim",
        "sourceArabic": "صحيح مسلم / حصن المسلم",
    },
    {
        "id": 102,
        "category": "Adhkar_Sabah",
        "textArabic": "اللَّهُمَّ أَنْتَ رَبِّي لَا إِلَهَ إِلَّا أَنْتَ، خَلَقْتَنِي وَأَنَا عَبْدُكَ، وَأَنَا عَلَى عَهْدِكَ وَوَعْدِكَ مَا اسْتَطَعْتُ، أَعُوذُ بِكَ مِنْ شَرِّ مَا صَنَعْتُ، أَبُوءُ لَكَ بِنِعْمَتِكَ عَلَيَّ، وَأَبُوءُ بِذَنْبِي فَاغْفِرْ لِي فَإِنَّهُ لَا يَغْفِرُ الذُّنُوبَ إِلَّا أَنْتَ",
        "transliteration": "Allahumma Anta Rabbi, la ilaha illa Anta, khalaqtani wa ana 'abduka, wa ana 'ala 'ahdika wa wa'dika mastata'tu. A'udhu bika min sharri ma sana'tu, abu'u laka bi-ni'matika 'alayya, wa abu'u bi-dhambi, faghfir li, fa-innahu la yaghfiru-dhunuba illa Anta.",
        "translationDe": "(Sayyidul-Istighfar) O Allah, Du bist mein Herr. Es gibt keinen Gott außer Dir. Du hast mich erschaffen und ich bin Dein Diener. Und ich halte Dein Versprechen und Deinen Bund ein, so gut ich kann. Ich suche Zuflucht bei Dir vor dem Übel dessen, was ich getan habe. Ich erkenne Deine Gnade gegenüber mir an und ich erkenne meine Sünde an. So vergib mir, denn niemand vergibt die Sünden außer Dir.",
        "translationEn": "O Allah, You are my Lord, none has the right to be worshipped except You, You created me and I am Your servant and I abide by Your covenant and promise as best I can, I take refuge in You from the evil of which I have committed. I acknowledge Your favor upon me and I acknowledge my sin, so forgive me, for verily none can forgive sin except You.",
        "translationFr": "Ô Allah, Tu es mon Seigneur, il n'y a de divinité que Toi. Tu m'as créé et je suis Ton serviteur. Je suis fidèle à Ton pacte et à Ta promesse autant que je le puis. Je cherche refuge auprès de Toi contre le mal de ce que j'ai fait. Je reconnais Tes bienfaits envers moi et je reconnais mon péché. Pardonne-moi, car nul ne pardonne les péchés sinon Toi.",
        "translationEs": "¡Oh Alá! Tú eres mi Señor, no hay más dios que Tú, Tú me creaste y yo soy Tu siervo y me adhiero a Tu pacto y promesa lo mejor que puedo, me refugio en Ti del mal que he cometido. Reconozco Tu favor sobre mí y reconozco mi pecado, así que perdóname, porque verdaderamente nadie puede perdonar el pecado excepto Tú.",
        "translationUr": "اے اللہ! تو میرا رب ہے، تیرے سوا کوئی معبود نہیں، تو نے مجھے پیدا کیا اور میں تیرا بندہ ہوں اور میں اپنی استطاعت کے مطابق تیرے عہد اور وعدے پر قائم ہوں، میں نے جو برائی کی ہے اس کے شر سے تیری پناہ مانگتا ہوں، میں تیرے ان احسانات کا اعتراف کرتا ہوں جو مجھ پر ہیں اور میں اپنے گناہوں کا اعتراف کرتا ہوں، پس مجھے بخش دے، کیونکہ تیرے سوا کوئی گناہوں کو معاف نہیں کر سکتا۔",
        "translationFa": "خداوندا، تو پروردگار منی، معبودی جز تو نیست، مرا آفریدی و من بنده تو هستم و تا آنجا که بتوانم بر عهد و پیمان تو پایبندم، از شر آنچه انجام داده‌ام به تو پناه می‌برم. به نعمت تو بر خودم و به گناهم اعتراف می‌کنم، پس مرا ببخش که جز تو کسی گناهان را نمی‌بخشد.",
        "repetitions": 1,
        "source": "Sahih Al-Bukhari / Hisn al-Muslim",
        "sourceArabic": "صحيح البخاري / حصن المسلم",
    },
    {
        "id": 103,
        "category": "Adhkar_Sabah",
        "textArabic": "بِسْمِ اللَّهِ الَّذِي لَا يَضُرُّ مَعَ اسْمِهِ شَيْءٌ فِي الْأَرْضِ وَلَا فِي السَّمَاءِ وَهُوَ السَّمِيعُ الْعَلِيمُ",
        "transliteration": "Bismillahil-ladhi la yadurru ma'as-mihi shay'un fil-ardi wa la fis-sama'i wa Huwas-Sami'ul-'Alim.",
        "translationDe": "Im Namen Allahs, mit Dessen Namen nichts Schaden nehmen kann, weder auf der Erde noch im Himmel, und Er ist der Allhörende, der Allwissende.",
        "translationEn": "In the name of Allah, with whose name nothing can cause harm in the earth nor in the heavens, and He is the All-Hearing, the All-Knowing.",
        "translationFr": "Au nom d'Allah, tel qu'en compagnie de Son nom rien ne peut nuire sur terre ni au ciel, et Il est l'Audient, l'Omniscient.",
        "translationEs": "En el nombre de Alá, con cuyo nombre nada puede causar daño en la tierra ni en los cielos, y Él es el que todo lo oye, el que todo lo sabe.",
        "translationUr": "اللہ کے نام کے ساتھ جس کے نام کے ساتھ زمین و آسمان میں کوئی چیز نقصان نہیں پہنچا سکتی، اور وہ سننے والا، جاننے والا ہے۔",
        "translationFa": "به نام خداوندی که با نام او هیچ چیز در زمین و آسمان گزندی نمی‌رساند و او شنوا و داناست.",
        "repetitions": 3,
        "source": "Jami' at-Tirmidhi & Abu Dawud / Hisn al-Muslim",
        "sourceArabic": "جامع الترمذي وأبو داود / حصن المسلم",
    },
    {
        "id": 104,
        "category": "Adhkar_Sabah",
        "textArabic": "سُبْحَانَ اللهِ وَبِحَمْدِهِ",
        "transliteration": "Subhanallahi wa bi-hamdihi.",
        "translationDe": "Preis sei Allah und Lob sei Ihm.",
        "translationEn": "Glory is to Allah and praise is to Him.",
        "translationFr": "Gloire et louange à Allah.",
        "translationEs": "Gloria sea a Alá y la alabanza sea a Él.",
        "translationUr": "اللہ پاک ہے اپنی تعریفوں کے ساتھ۔",
        "translationFa": "پاک و منزه است خداوند و حمد از آن اوست.",
        "repetitions": 100,
        "source": "Sahih Muslim & Sahih Al-Bukhari",
        "sourceArabic": "صحيح مسلم وصحيح البخاري",
    },
    {
        "id": 105,
        "category": "Adhkar_Sabah",
        "textArabic": "سُبْحَانَ اللهِ وَبِحَمْدِهِ: عَدَدَ خَلْقِهِ، وَرِضَا نَفْسِهِ، وَزِنَةَ عَرْشِهِ، وَمِدَادَ كَلِمَاتِهِ",
        "transliteration": "Subhanallahi wa bi-hamdihi: 'Adada khalqihi, wa rida nafsihi, wa zinata 'arshihi, wa midada kalimatih.",
        "translationDe": "Preis sei Allah und Lob sei Ihm, entsprechend der Anzahl Seiner Schöpfung, Seiner Selbstzufriedenheit, dem Gewicht Seines Throns und der Menge der Tinte Seiner Worte.",
        "translationEn": "Glory is to Allah and praise is to Him, by the multitude of His creation, by His Pleasure, by the weight of His Throne, and by the extent of His Words.",
        "translationFr": "Gloire et louange à Allah, autant de fois qu'il y a de créatures, autant qu'Il Lui plaît, autant que pèse Son Trône et autant qu'il faudrait d'encre pour écrire Ses paroles.",
        "translationEs": "Gloria sea a Alá y alabanza sea a Él, por la multitud de Su creación, por Su Placer, por el peso de Su Trono y por la extensión de Su Palabra.",
        "translationUr": "اللہ پاک ہے اور اپنی تعریفوں کے ساتھ: اپنی مخلوق کی تعداد کے برابر، اپنی ذات کی خوشنودی کے برابر، اپنے عرش کے وزن کے برابر اور اپنے کلمات کی سیاہی کے برابر۔",
        "translationFa": "پاک و منزه است خداوند و حمد از آن اوست به تعداد آفریدگانش و خشنودی ذاتش و سنگینی عرشش و جوهر کلماتش.",
        "repetitions": 3,
        "source": "Sahih Muslim / Hisn al-Muslim",
        "sourceArabic": "صحيح مسلم / حصن المسلم",
    },
    {
        "id": 106,
        "category": "Adhkar_Sabah",
        "textArabic": "رَضِيتُ بِاللَّهِ رَبَّاً، وَبِالْإِسْلَامِ دِيناً، وَبِمُحَمَّدٍ صلى الله عليه وسلم نَبِيَّاً",
        "transliteration": "Raditu billahi Rabban, wa bil-Islami dinan, wa bi-Muhammadin (ﷺ) nabiyya.",
        "translationDe": "Ich bin zufrieden mit Allah als Herrn, mit dem Islam als Religion und mit Muhammad (ﷺ) als Propheten.",
        "translationEn": "I am pleased with Allah as my Lord, with Islam as my religion and with Muhammad (ﷺ) as my Prophet.",
        "translationFr": "Je suis satisfait d'Allah comme Seigneur, de l'Islam comme religion et de Muhammad (ﷺ) comme Prophète.",
        "translationEs": "Estoy complacido con Alá como mi Señor, con el Islam como mi religión y con Muhammad (ﷺ) como mi Profeta.",
        "translationUr": "میں اللہ کے رب ہونے، اسلام کے دین ہونے اور محمد (صلی اللہ علیہ وآلہ وسلم) کے نبی ہونے پر راضی ہوں۔",
        "translationFa": "خشنودم که الله پروردگار من است و اسلام دین من و محمد (ص) پیامبر من است.",
        "repetitions": 3,
        "source": "Jami' at-Tirmidhi & Abu Dawud / Hisn al-Muslim",
        "sourceArabic": "جامع الترمذي وأبو داود / حصن المسلم",
    },
    {
        "id": 107,
        "category": "Adhkar_Sabah",
        "textArabic": "حَسْبِيَ اللَّهُ لَا إِلَهَ إِلَّا هُوَ عَلَيْهِ تَوَكَّلْتُ وَهُوَ رَبُّ الْعَرْشِ الْعَظِيمِ",
        "transliteration": "Hasbiyallahu la ilaha illa Huwa, 'alayhi tawakkaltu wa Huwa Rabbul-'Arshil-'Adhim.",
        "translationDe": "Allah genügt mir. Es gibt keinen Gott außer Ihm. Auf Ihn vertraue ich, und Er ist der Herr des gewaltigen Throns.",
        "translationEn": "Allah is sufficient for me. There is no God but Him. In Him I put my trust, and He is the Lord of the Mighty Throne.",
        "translationFr": "Allah me suffit. Il n'y a de divinité que Lui. En Lui je place ma confiance, et Il est le Seigneur du Trône immense.",
        "translationEs": "Alá me basta. No hay más dios que Él. En Él he puesto mi confianza, y Él es el Señor del Trono Majestuoso.",
        "translationUr": "مجھے اللہ کافی ہے، اس کے سوا کوئی معبود نہیں، اسی پر میں نے بھروسہ کیا اور وہ عرش عظیم کا رب ہے۔",
        "translationFa": "خداوند برای من کافی است، معبودی جز او نیست، بر او توکل کردم و او پروردگار عرش بزرگ است.",
        "repetitions": 7,
        "source": "Abu Dawud / Hisn al-Muslim",
        "sourceArabic": "أبو داود / حصن المسلم",
    },
    {
        "id": 108,
        "category": "Adhkar_Sabah",
        "textArabic": "اللَّهُمَّ بِكَ أَصْبَحْنَا، وَبِكَ أَمْسَيْنَا، وَبِكَ نَحْيَا، وَبِكَ نَمُوتُ وَإِلَيْكَ النُّشُورُ",
        "transliteration": "Allahumma bika asbahna, wa bika amsayna, wa bika nahya, wa bika namutu wa ilaykan-nushur.",
        "translationDe": "O Allah, durch Dich haben wir den Morgen erreicht und durch Dich erreichen wir den Abend. Durch Dich leben wir und durch Dich sterben wir und zu Dir ist die Auferstehung.",
        "translationEn": "O Allah, by You we enter the morning and by You we enter the evening, by You we live and by You we die, and to You is the Final Return.",
        "translationFr": "Ô Allah, par Toi nous sommes au matin et par Toi nous sommes au soir. Par Toi nous vivons et par Toi nous mourons et vers Toi est la résurrection.",
        "translationEs": "¡Oh Alá! Por Ti entramos en la mañana y por Ti entramos en la tarde, por Ti vivimos y por Ti morimos, y hacia Ti es el Retorno Final.",
        "translationUr": "اے اللہ! تیری ہی توفیق سے ہم نے صبح کی اور تیری ہی توفیق سے ہم نے شام کی، اور تیری ہی مرضی سے ہم جیتے ہیں اور تیری ہی مرضی سے ہم مریں گے اور تیری ہی طرف لوٹ کر جانا ہے۔",
        "translationFa": "خداوندا، به تو صبح کردیم و به تو شب کردیم، به تو زنده می‌شویم و به تو می‌میریم و رستاخیز به سوی توست.",
        "repetitions": 1,
        "source": "Jami' at-Tirmidhi / Hisn al-Muslim",
        "sourceArabic": "جامع الترمذي / حصن المسلم",
    },
    {
        "id": 109,
        "category": "Adhkar_Sabah",
        "textArabic": "أَعُوذُ بِكَلِمَاتِ اللَّهِ التَّامَّاتِ مِنْ شَرِّ مَا خَلَقَ",
        "transliteration": "A'udhu bi-kalimatil-lahit-tammati min sharri ma khalaq.",
        "translationDe": "Ich suche Zuflucht bei den vollkommenen Worten Allahs vor dem Übel dessen, was Er erschaffen hat.",
        "translationEn": "I seek refuge in the perfect words of Allah from the evil of what He has created.",
        "translationFr": "Je cherche refuge auprès des paroles parfaites d'Allah contre le mal de ce qu'Il a créé.",
        "translationEs": "Busco refugio en las palabras perfectas de Alá contra el mal de lo que Él ha creado.",
        "translationUr": "میں اللہ کے کامل کلمات کے ذریعے ہر اس چیز کے شر سے پناہ مانگتا ہوں جو اس نے پیدا کی۔",
        "translationFa": "پناه می‌برم به کلمات کامل خدا از شر آنچه آفریده است.",
        "repetitions": 3,
        "source": "Sahih Muslim / Hisn al-Muslim",
        "sourceArabic": "صحيح مسلم / حصن المسلم",
    },
    {
        "id": 110,
        "category": "Adhkar_Sabah",
        "textArabic": "اللَّهُمَّ إِنِّي أَسْأَلُكَ عِلْمًا نَافِعًا، وَرِزْقًا طَيِّبًا، وَعَمَلًا مُتَقَبَّلًا",
        "transliteration": "Allahumma inni as'aluka 'ilman nafi'an, wa rizqan tayyiban, wa 'amalan mutaqabbala.",
        "translationDe": "O Allah, ich bitte Dich um nützliches Wissen, eine gute Versorgung und Taten, die von Dir angenommen werden.",
        "translationEn": "O Allah, I ask You for beneficial knowledge, goodly provision and acceptable deeds.",
        "translationFr": "Ô Allah, je Te demande un savoir utile, une subsistance bonne et une œuvre agréée.",
        "translationEs": "¡Oh Alá! Te pido conocimiento beneficioso, provisión buena y obras aceptables.",
        "translationUr": "اے اللہ! میں تجھ سے نفع بخش علم، پاکیزہ رزق اور قبول ہونے والے عمل کا سوال کرتا ہوں۔",
        "translationFa": "خداوندا، از تو دانشی سودمند، روزی‌ای پاک و عملی پذیرفته شده درخواست می‌کنم.",
        "repetitions": 1,
        "source": "Sunan Ibn Majah / Hisn al-Muslim",
        "sourceArabic": "سنن ابن ماجه / حصن المسلم",
    },
    # ── Adhkar_Masae (Evening) ──────────────────────────────────────────────
    {
        "id": 201,
        "category": "Adhkar_Masae",
        "textArabic": "أَمْسَيْنَا وَأَمْسَى الْمُلْكُ لِلَّهِ، وَالْحَمْدُ لِلَّهِ، لَا إِلَهَ إِلَّا اللهُ وَحْدَهُ لَا شَرِيكَ لَهُ، لَهُ الْمُلْكُ وَلَهُ الْحَمْدُ وَهُوَ عَلَى كُلِّ شَيْءٍ قَدِيرٌ",
        "transliteration": "Amsayna wa amsayal-mulku lillah, wal-hamdulillah. La ilaha illallahu wahdahu la sharika lah, lahul-mulku wa lahul-hamdu wa Huwa 'ala kulli shay'in Qadir.",
        "translationDe": "Wir haben den Abend erreicht, und die Herrschaft gehört Allah, und alles Lob gebührt Allah. Es gibt keinen Gott außer Allah allein, Er hat keinen Partner. Ihm gehört die Herrschaft und Ihm gebührt das Lob, und Er hat Macht über alle Dinge.",
        "translationEn": "We have reached the evening and at this very time unto Allah belongs all sovereignty, and all praise is for Allah. None has the right to be worshipped but Allah alone, without partner, to Him belongs all sovereignty and praise and He is over all things omnipotent.",
        "translationFr": "Nous sommes au soir et la royauté appartient à Allah. Louange à Allah. Il n'y a d'autre divinité qu'Allah, Seul, sans associé. À Lui la royauté, à Lui la louange et Il est Capable de toute chose.",
        "translationEs": "Hemos llegado a la tarde y la soberanía pertenece a Alá, y toda alabanza es para Alá. No hay más dios que Alá solo, sin socio, suya es la soberanía y suya es la alabanza y Él tiene poder sobre todas las cosas.",
        "translationUr": "ہم نے شام کی اور اللہ کے لیے تمام بادشاہت ہے، اور تمام تعریف اللہ کے لیے ہے۔ اللہ کے سوا کوئی معبود نہیں وہ اکیلا ہے اس کا کوئی شریک نہیں، اسی کے لیے بادشاہت ہے اور اسی کے لیے تعریف ہے اور وہ ہر چیز پر قادر ہے۔",
        "translationFa": "ما به شب رسیدیم و پادشاهی از آن خداست و حمد مخصوص خداست. معبودی جز خدای یگانه نیست، شریکی ندارد، فرمانروایی و ستایش از آن اوست و او بر هر چیزی تواناست.",
        "repetitions": 1,
        "source": "Sahih Muslim / Hisn al-Muslim",
        "sourceArabic": "صحيح مسلم / حصن المسلم",
    },
    {
        "id": 202,
        "category": "Adhkar_Masae",
        "textArabic": "اللَّهُمَّ أَنْتَ رَبِّي لَا إِلَهَ إِلَّا أَنْتَ، خَلَقْتَنِي وَأَنَا عَبْدُكَ، وَأَنَا عَلَى عَهْدِكَ وَوَعْدِكَ مَا اسْتَطَعْتُ، أَعُوذُ بِكَ مِنْ شَرِّ مَا صَنَعْتُ، أَبُوءُ لَكَ بِنِعْمَتِكَ عَلَيَّ، وَأَبُوءُ بِذَنْبِي فَاغْفِرْ لِي فَإِنَّهُ لَا يَغْفِرُ الذُّنُوبَ إِلَّا أَنْتَ",
        "transliteration": "Allahumma Anta Rabbi, la ilaha illa Anta, khalaqtani wa ana 'abduka, wa ana 'ala 'ahdika wa wa'dika mastata'tu. A'udhu bika min sharri ma sana'tu, abu'u laka bi-ni'matika 'alayya, wa abu'u bi-dhambi, faghfir li, fa-innahu la yaghfiru-dhunuba illa Anta.",
        "translationDe": "(Sayyidul-Istighfar) O Allah, Du bist mein Herr. Es gibt keinen Gott außer Dir. Du hast mich erschaffen und ich bin Dein Diener. Und ich halte Dein Versprechen und Deinen Bund ein, so gut ich kann. Ich suche Zuflucht bei Dir vor dem Übel dessen, was ich getan habe. Ich erkenne Deine Gnade gegenüber mir an und ich erkenne meine Sünde an. So vergib mir, denn niemand vergibt die Sünden außer Dir.",
        "translationEn": "O Allah, You are my Lord, none has the right to be worshipped except You, You created me and I am Your servant and I abide by Your covenant and promise as best I can, I take refuge in You from the evil of which I have committed. I acknowledge Your favor upon me and I acknowledge my sin, so forgive me, for verily none can forgive sin except You.",
        "translationFr": "Ô Allah, Tu es mon Seigneur, il n'y a de divinité que Toi. Tu m'as créé et je suis Ton serviteur. Je suis fidèle à Ton pacte et à Ta promesse autant que je le puis. Je cherche refuge auprès de Toi contre le mal de ce que j'ai fait. Je reconnais Tes bienfaits envers moi et je reconnais mon péché. Pardonne-moi, car nul ne pardonne les péchés sinon Toi.",
        "translationEs": "¡Oh Alá! Tú eres mi Señor, no hay más dios que Tú, Tú me creaste y yo soy Tu siervo y me adhiero a Tu pacto y promesa lo mejor que puedo, me refugio en Ti del mal que he cometido. Reconozco Tu favor sobre mí y reconozco mi pecado, así que perdóname, porque verdaderamente nadie puede perdonar el pecado excepto Tú.",
        "translationUr": "اے اللہ! تو میرا رب ہے، تیرے سوا کوئی معبود نہیں، تو نے مجھے پیدا کیا اور میں تیرا بندہ ہوں اور میں اپنی استطاعت کے مطابق تیرے عہد اور وعدے پر قائم ہوں، میں نے جو برائی کی ہے اس کے شر سے تیری پناہ مانگتا ہوں، میں تیرے ان احسانات کا اعتراف کرتا ہوں جو مجھ پر ہیں اور میں اپنے گناہوں کا اعتراف کرتا ہوں، پس مجھے بخش دے، کیونکہ تیرے سوا کوئی گناہوں کو معاف نہیں کر سکتا۔",
        "translationFa": "خداوندا، تو پروردگار منی، معبودی جز تو نیست، مرا آفریدی و من بنده تو هستم و تا آنجا که بتوانم بر عهد و پیمان تو پایبندم، از شر آنچه انجام داده‌ام به تو پناه می‌برم. به نعمت تو بر خودم و به گناهم اعتراف می‌کنم، پس مرا ببخش که جز تو کسی گناهان را نمی‌بخشد.",
        "repetitions": 1,
        "source": "Sahih Al-Bukhari / Hisn al-Muslim",
        "sourceArabic": "صحيح البخاري / حصن المسلم",
    },
    {
        "id": 203,
        "category": "Adhkar_Masae",
        "textArabic": "اللَّهُمَّ بِكَ أَمْسَيْنَا، وَبِكَ أَصْبَحْنَا، وَبِكَ نَحْيَا، وَبِكَ نَمُوتُ وَإِلَيْكَ الْمَصِيرُ",
        "transliteration": "Allahumma bika amsayna, wa bika asbahna, wa bika nahya, wa bika namutu wa ilaykal-masir.",
        "translationDe": "O Allah, durch Dich haben wir den Abend erreicht und durch Dich erreichen wir den Morgen. Durch Dich leben wir und durch Dich sterben wir und zu Dir ist die Rückkehr.",
        "translationEn": "O Allah, by You we enter the evening and by You we enter the morning, by You we live and by You we die, and to You is the Return.",
        "translationFr": "Ô Allah, par Toi nous sommes au soir et par Toi nous sommes au matin. Par Toi nous vivons et par Toi nous mourons et vers Toi est le retour.",
        "translationEs": "¡Oh Alá! Por Ti entramos en la tarde y por Ti entramos en la mañana, por Ti vivimos y por Ti morimos, y hacia Ti es el Retorno.",
        "translationUr": "اے اللہ! تیری ہی توفیق سے ہم نے شام کی اور تیری ہی توفیق سے ہم نے صبح کی، اور تیری ہی مرضی سے ہم جیتے ہیں اور تیری ہی مرضی سے ہم مریں گے اور تیری ہی طرف لوٹ کر جانا ہے۔",
        "translationFa": "خداوندا، به تو شب کردیم و به تو صبح کردیم، به تو زنده می‌شویم و به تو می‌میریم و بازگشت به سوی توست.",
        "repetitions": 1,
        "source": "Jami' at-Tirmidhi / Hisn al-Muslim",
        "sourceArabic": "جامع الترمذي / حصن المسلم",
    },
    {
        "id": 204,
        "category": "Adhkar_Masae",
        "textArabic": "أَعُوذُ بِكَلِمَاتِ اللَّهِ التَّامَّاتِ مِنْ شَرِّ مَا خَلَقَ",
        "transliteration": "A'udhu bi-kalimatil-lahit-tammati min sharri ma khalaq.",
        "translationDe": "Ich suche Zuflucht bei den vollkommenen Worten Allahs vor dem Übel dessen, was Er erschaffen hat.",
        "translationEn": "I seek refuge in the perfect words of Allah from the evil of what He has created.",
        "translationFr": "Je cherche refuge auprès des paroles parfaites d'Allah contre le mal de ce qu'Il a créé.",
        "translationEs": "Busco refugio en las palabras perfectas de Alá contra el mal de lo que Él ha creado.",
        "translationUr": "میں اللہ کے کامل کلمات کے ذریعے ہر اس چیز کے شر سے پناہ مانگتا ہوں جو اس نے پیدا کی۔",
        "translationFa": "پناه می‌برم به کلمات کامل خدا از شر آنچه آفریده است.",
        "repetitions": 3,
        "source": "Sahih Muslim / Hisn al-Muslim",
        "sourceArabic": "صحيح مسلم / حصن المسلم",
    },
    {
        "id": 205,
        "category": "Adhkar_Masae",
        "textArabic": "بِسْمِ اللَّهِ الَّذِي لَا يَضُرُّ مَعَ اسْمِهِ شَيْءٌ فِي الْأَرْضِ وَلَا فِي السَّمَاءِ وَهُوَ السَّمِيعُ الْعَلِيمُ",
        "transliteration": "Bismillahil-ladhi la yadurru ma'as-mihi shay'un fil-ardi wa la fis-sama'i wa Huwas-Sami'ul-'Alim.",
        "translationDe": "Im Namen Allahs, mit Dessen Namen nichts Schaden nehmen kann, weder auf der Erde noch im Himmel, und Er ist der Allhörende, der Allwissende.",
        "translationEn": "In the name of Allah, with whose name nothing can cause harm in the earth nor in the heavens, and He is the All-Hearing, the All-Knowing.",
        "translationFr": "Au nom d'Allah, tel qu'en compagnie de Son nom rien ne peut nuire sur terre ni au ciel, et Il est l'Audient, l'Omniscient.",
        "translationEs": "En el nombre de Alá, con cuyo nombre nada puede causar daño en la tierra ni en los cielos, y Él es el que todo lo oye, el que todo lo sabe.",
        "translationUr": "اللہ کے نام کے ساتھ جس کے نام کے ساتھ زمین و آسمان میں کوئی چیز نقصان نہیں پہنچا سکتی، اور وہ سننے والا، جاننے والا ہے۔",
        "translationFa": "به نام خداوندی که با نام او هیچ چیز در زمین و آسمان گزندی نمی‌رساند و او شنوا و داناست.",
        "repetitions": 3,
        "source": "Jami' at-Tirmidhi & Abu Dawud / Hisn al-Muslim",
        "sourceArabic": "جامع الترمذي وأبو داود / حصن المسلم",
    },
    {
        "id": 206,
        "category": "Adhkar_Masae",
        "textArabic": "حَسْبِيَ اللَّهُ لَا إِلَهَ إِلَّا هُوَ عَلَيْهِ تَوَكَّلْتُ وَهُوَ رَبُّ الْعَرْشِ الْعَظِيمِ",
        "transliteration": "Hasbiyallahu la ilaha illa Huwa, 'alayhi tawakkaltu wa Huwa Rabbul-'Arshil-'Adhim.",
        "translationDe": "Allah genügt mir. Es gibt keinen Gott außer Ihm. Auf Ihn vertraue ich, und Er ist der Herr des gewaltigen Throns.",
        "translationEn": "Allah is sufficient for me. There is no God but Him. In Him I put my trust, and He is the Lord of the Mighty Throne.",
        "translationFr": "Allah me suffit. Il n'y a de divinité que Lui. En Lui je place ma confiance, et Il est le Seigneur du Trône immense.",
        "translationEs": "Alá me basta. No hay más dios que Él. En Él he puesto mi confianza, y Él es el Señor del Trono Majestuoso.",
        "translationUr": "مجھے اللہ کافی ہے، اس کے سوا کوئی معبود نہیں، اسی پر میں نے بھروسہ کیا اور وہ عرش عظیم کا رب ہے۔",
        "translationFa": "خداوند برای من کافی است، معبودی جز او نیست، بر او توکل کردم و او پروردگار عرش بزرگ است.",
        "repetitions": 7,
        "source": "Abu Dawud / Hisn al-Muslim",
        "sourceArabic": "أبو داود / حصن المسلم",
    },
    {
        "id": 207,
        "category": "Adhkar_Masae",
        "textArabic": "رَضِيتُ بِاللَّهِ رَبَّاً، وَبِالْإِسْلَامِ دِيناً، وَبِمُحَمَّدٍ صلى الله عليه وسلم نَبِيَّاً",
        "transliteration": "Raditu billahi Rabban, wa bil-Islami dinan, wa bi-Muhammadin (ﷺ) nabiyya.",
        "translationDe": "Ich bin zufrieden mit Allah als Herrn, mit dem Islam als Religion und mit Muhammad (ﷺ) als Propheten.",
        "translationEn": "I am pleased with Allah as my Lord, with Islam as my religion and with Muhammad (ﷺ) as my Prophet.",
        "translationFr": "Je suis satisfait d'Allah comme Seigneur, de l'Islam comme religion et de Muhammad (ﷺ) comme Prophète.",
        "translationEs": "Estoy complacido con Alá como mi Señor, con el Islam como mi religión y con Muhammad (ﷺ) como mi Profeta.",
        "translationUr": "میں اللہ کے رب ہونے، اسلام کے دین ہونے اور محمد (صلی اللہ علیہ وآلہ وسلم) کے نبی ہونے پر راضی ہوں۔",
        "translationFa": "خشنودم که الله پروردگار من است و اسلام دین من و محمد (ص) پیامبر من است.",
        "repetitions": 3,
        "source": "Jami' at-Tirmidhi & Abu Dawud / Hisn al-Muslim",
        "sourceArabic": "جامع الترمذي وأبو داود / حصن المسلم",
    },
    {
        "id": 208,
        "category": "Adhkar_Masae",
        "textArabic": "سُبْحَانَ اللهِ وَبِحَمْدِهِ",
        "transliteration": "Subhanallahi wa bi-hamdihi.",
        "translationDe": "Preis sei Allah und Lob sei Ihm.",
        "translationEn": "Glory is to Allah and praise is to Him.",
        "translationFr": "Gloire et louange à Allah.",
        "translationEs": "Gloria sea a Alá y la alabanza sea a Él.",
        "translationUr": "اللہ پاک ہے اپنی تعریفوں کے ساتھ۔",
        "translationFa": "پاک و منزه است خداوند و حمد از آن اوست.",
        "repetitions": 100,
        "source": "Sahih Muslim & Sahih Al-Bukhari",
        "sourceArabic": "صحيح مسلم وصحيح البخاري",
    },
    {
        "id": 209,
        "category": "Adhkar_Masae",
        "textArabic": "يَا حَيُّ يَا قَيُّومُ بِرَحْمَتِكَ أَسْتَغِيثُ، أَصْلِحْ لِي شَأْنِي كُلَّهُ وَلَا تَكِلْنِي إِلَى نَفْسِي طَرْفَةَ عَيْنٍ",
        "transliteration": "Ya Hayyu ya Qayyumu bi-rahmatika astaghith, aslih li sha'ni kullahu wa la takilni ila nafsi tarfata 'ayn.",
        "translationDe": "O Lebendiger, o Beständiger, durch Deine Barmherzigkeit suche ich Hilfe. Berichtige all meine Angelegenheiten und überlasse mich nicht mir selbst, auch nicht für den Augenzwinker eines Augetes.",
        "translationEn": "O Ever Living One, O Self-Sustaining One, in Your Mercy I seek relief. Set all my affairs right, and do not leave me to myself even for the blink of an eye.",
        "translationFr": "Ô Vivant, Ô Subsistant par Toi-même, j'implore Ton secours par Ta miséricorde. Améliore ma situation entière et ne m'abandonne pas à moi-même ne fût-ce qu'un clin d'œil.",
        "translationEs": "¡Oh Viviente, oh Sustentador de todo! En Tu misericordia busco alivio. Corrige todos mis asuntos y no me dejes a mi suerte ni por un abrir y cerrar de ojos.",
        "translationUr": "اے زندہ جاوید، اے سب کو تھامنے والے، میں تیری رحمت کے ذریعے فریاد کرتا ہوں، میرے تمام حالات درست کر دے اور مجھے ایک لمحے کے لیے بھی میرے نفس کے حوالے نہ کر۔",
        "translationFa": "ای زنده، ای پاینده، به رحمت تو فریادرس می‌خواهم، تمام امور مرا اصلاح کن و مرا حتی برای یک چشم بر هم زدن به خودم وامگذار.",
        "repetitions": 1,
        "source": "Sunan an-Nasa'i / Hisn al-Muslim",
        "sourceArabic": "سنن النسائي / حصن المسلم",
    },
    # ── Adhkar_Nawm (Sleep) ─────────────────────────────────────────────────
    {
        "id": 301,
        "category": "Adhkar_Nawm",
        "textArabic": "بِاسْمِكَ رَبِّي وَضَعْتُ جَنْبِي، وَبِكَ أَرْفَعُهُ، فَإِنْ أَمْسَكْتَ نَفْسِي فَارْحَمْهَا، وَإِنْ أَرْسَلْتَهَا فَاحْفَظْهَا بِمَا تَحْفَظُ بِهِ عِبَادَكَ الصَّالِحِينَ",
        "transliteration": "Bismika Rabbi wad'tu janbi wa bika arfa'uhu, fa-in amsakta nafsi farhamha, wa in arsaltaha fahfazha bima tahfazu bihi 'ibadakas-salihin.",
        "translationDe": "In Deinem Namen, mein Herr, lege ich meine Seite nieder, und durch Dich erhebe ich sie wieder. Wenn Du meine Seele zurückhältst (sterben lässt), so erbarme Dich ihrer. Und wenn Du sie zurücksendest (leben lässt), so beschütze sie, wie Du Deine rechtschaffenen Diener beschützt.",
        "translationEn": "In Your name, my Lord, I lie down on my side, and by You I rise. If You should take my soul, have mercy on it, and if You should return it, protect it as You protect Your righteous servants.",
        "translationFr": "C'est en Ton nom, mon Seigneur, que je pose mon côté, et par Toi que je le relève. Si Tu retiens mon âme, fais-lui miséricorde, et si Tu la renvoies, protège-la comme Tu protèges Tes serviteurs vertueux.",
        "translationEs": "En Tu nombre, mi Señor, me acuesto de lado, y por Ti me levanto. Si Te llevas mi alma, ten misericordia de ella, y si la devuelves, protégela como proteges a Tus siervos justos.",
        "translationUr": "تیرے نام کے ساتھ اے میرے رب! میں نے اپنا پہلو (بستر پر) رکھا اور تیری ہی مدد سے میں اسے اٹھاؤں گا، اگر تو میری جان روک لے تو اس پر رحم کرنا، اور اگر تو اسے چھوڑ دے تو اس کی حفاظت کرنا جس طرح تو اپنے نیک بندوں کی حفاظت کرتا ہے۔",
        "translationFa": "به نام تو ای پروردگارم پهلویم را بر زمین نهادم و به کمک تو آن را بلند می‌کنم، اگر جانم را گرفتی بر آن رحم کن و اگر آن را بازگرداندی، محافظت کن همانگونه که از بندگان صالحت محافظت می‌کنی.",
        "repetitions": 1,
        "source": "Sahih Al-Bukhari & Sahih Muslim",
        "sourceArabic": "صحيح البخاري وصحيح مسلم",
    },
    {
        "id": 302,
        "category": "Adhkar_Nawm",
        "textArabic": "اللَّهُمَّ بِاسْمِكَ أَمُوتُ وَأَحْيَا",
        "transliteration": "Allahumma bika amutu wa ahya.",
        "translationDe": "O Allah, in Deinem Namen sterbe ich und lebe ich.",
        "translationEn": "O Allah, in Your Name I die and I live.",
        "translationFr": "Ô Allah, en Ton nom je meurs et je vis.",
        "translationEs": "¡Oh Alá! En Tu nombre muero y vivo.",
        "translationUr": "اے اللہ! تیرے نام کے ساتھ ہی میں مرتا ہوں اور جیتا ہوں۔",
        "translationFa": "خداوندا، به نام تو می‌میرم و زنده می‌شوم.",
        "repetitions": 1,
        "source": "Sahih Al-Bukhari / Hisn al-Muslim",
        "sourceArabic": "صحيح البخاري / حصن المسلم",
    },
    {
        "id": 303,
        "category": "Adhkar_Nawm",
        "textArabic": "اللَّهُمَّ قِنِي عَذَابَكَ يَوْمَ تَبْعَثُ عِبَادَكَ",
        "transliteration": "Allahumma qini 'adhabaka yawma tab'athu 'ibadak.",
        "translationDe": "O Allah, schütze mich vor Deiner Strafe an dem Tag, an dem Du Deine Diener auferweckst.",
        "translationEn": "O Allah, protect me from Your punishment on the Day You resurrect Your servants.",
        "translationFr": "Ô Allah, protège-moi de Ton châtiment le jour où Tu ressusciteras Tes serviteurs.",
        "translationEs": "¡Oh Alá! Protégeme de Tu castigo el Día que resucites a Tus siervos.",
        "translationUr": "اے اللہ! مجھے اپنے عذاب سے بچا جس دن تو اپنے بندوں کو اٹھائے گا۔",
        "translationFa": "خداوندا، مرا از عذابت در روزی که بندگانت را برمی‌انگیزی مصون بدار.",
        "repetitions": 3,
        "source": "Jami' at-Tirmidhi & Abu Dawud / Hisn al-Muslim",
        "sourceArabic": "جامع الترمذي وأبو داود / حصن المسلم",
    },
    {
        "id": 304,
        "category": "Adhkar_Nawm",
        "textArabic": "سُبْحَانَ اللَّهِ (33) ، وَالْحَمْدُ لِلَّهِ (33)، وَاللَّهُ أَكْبَرُ (34)",
        "transliteration": "Subhanallah (33x) / Alhamdulillah (33x) / Allahu Akbar (34x)",
        "translationDe": "Preis sei Allah / Alles Lob gebührt Allah / Allah ist am größten.",
        "translationEn": "Glory is to Allah / Praise is to Allah / Allah is the Greatest.",
        "translationFr": "Gloire à Allah / Louange à Allah / Allah est le plus Grand.",
        "translationEs": "Gloria sea a Alá / Alabanza sea a Alá / Alá es el más Grande.",
        "translationUr": "اللہ پاک ہے / تمام تعریف اللہ کے لیے ہے / اللہ سب سے بڑا ہے۔",
        "translationFa": "پاک و منزه است خداوند / حمد مخصوص خداست / خداوند بزرگترین است.",
        "repetitions": 1,
        "source": "Sahih Al-Bukhari & Sahih Muslim",
        "sourceArabic": "صحيح البخاري وصحيح مسلم",
    },
    {
        "id": 305,
        "category": "Adhkar_Nawm",
        "textArabic": "اللَّهُمَّ أَسْلَمْتُ نَفْسِي إِلَيْكَ، وَفَوَّضْتُ أَمْرِي إِلَيْكَ، وَوَجَّهْتُ وَجْهِي إِلَيْكَ، وَأَلْجَأْتُ ظَهْرِي إِلَيْكَ، رَغْبَةً وَرَهْبَةً إِلَيْكَ، لَا مَلْجَأَ وَلَا مَنْجَا مِنْكَ إِلَّا إِلَيْكَ، آمَنْتُ بِكِتَابِكَ الَّذِي أَنْزَلْتَ، وَبِنَبِيِّكَ الَّذِي أَرْسَلْتَ",
        "transliteration": "Allahumma aslamtu nafsi ilayk, wa fawwadtu amri ilayk, wa wajjahtu wajhi ilayk, wa alja'tu zahri ilayk, raghbatan wa rahbatan ilayk. La malja'a wa la manja minka illa ilayk. Amantu bi-kitabikal-ladhi anzalt, wa bi-nabiyyikal-ladhi arsalt.",
        "translationDe": "O Allah, ich ergebe meine Seele Dir, und ich überlose meine Angelegenheit Dir. Ich wende mein Gesicht Dir zu und stütze meinen Rücken an Dich, aus Verlangen nach Dir und aus Furcht vor Dir. Es gibt keine Zuflucht und keine Rettung vor Dir außer bei Dir. Ich glaube an Dein Buch, das Du herabgesandt hast, und an Deinen Propheten, den Du gesandt hast.",
        "translationEn": "O Allah, I submit my soul to You, and I entrust my affair to You. I turn my face to You and I lean my back against You, in desire and fear of You. There is no refuge and no salvation from You except in You. I believe in Your Book which You have revealed and in Your Prophet whom You have sent.",
        "translationFr": "Ô Allah, je Soumets mon âme à Toi, et je Te confie mon affaire. Je tourne mon visage vers Toi et je m'appuie sur Toi, par désir et par crainte de Toi. Il n'y a de refuge ni de salut contre Toi qu'en Toi. Je crois en Ton Livre que Tu as révélé et en Ton Prophète que Tu as envoyé.",
        "translationEs": "¡Oh Alá! Someto mi alma a Ti, y Te encomiendo mi asunto. Vuelvo mi rostro hacia Ti y apoyo mi espalda en Ti, con deseo y temor de Ti. No hay refugio ni salvación de Ti excepto en Ti. Creo en Tu Libro que has revelado y en Tu Profeta que has enviado.",
        "translationUr": "اے اللہ! میں نے اپنی جان تیرے سپرد کر دی، اور اپنا معاملہ تیرے حوالے کر دیا، اور اپنا چہرہ تیری طرف پھیر لیا، اور اپنی پیٹھ تیری طرف جھکا دی، تیری رغبت اور تیرے خوف کے ساتھ، تیرے سوا نہ کوئی پناہ گاہ ہے اور نہ نجات کی جگہ مگر تیری ہی طرف، میں تیری اس کتاب پر ایمان لایا جو تو نے نازل فرمائی اور تیرے اس نبی پر جسے تو نے بھیجا۔",
        "translationFa": "خداوندا، نفسم را به تو تسلیم کردم و کارم را به تو واگذاردم و رویم را به سوی تو گرداندم و پشتم را به تو تکیه دادم، از روی رغبت و ترس به سوی تو، هیچ پناهگاه و نجاتگاهی از تو جز به سوی تو نیست، به کتابی که نازل کردی و به پیامبری که فرستادی ایمان آوردم.",
        "repetitions": 1,
        "source": "Sahih Al-Bukhari & Sahih Muslim",
        "sourceArabic": "صحيح البخاري وصحيح مسلم",
    },
    {
        "id": 306,
        "category": "Adhkar_Nawm",
        "textArabic": "سُبْحَانَكَ اللَّهُمَّ رَبِّي بِكَ وَضَعْتُ جَنْبِي وَبِكَ أَرْفَعُهُ، إِنْ أَمْسَكْتَ نَفْسِي فَاغْفِرْ لَهَا، وَإِنْ أَرْسَلْتَهَا فَاحْفَظْهَا بِمَا تَحْفَظُ بِهِ عِبَادَكَ الصَّالِحِينَ",
        "transliteration": "Subhanakal-lahumma Rabbi bika wad'tu janbi wa bika arfa'uhu, in amsakta nafsi faghfir laha, wa in arsaltaha fahfazha bima tahfazu bihi 'ibadakas-salihin.",
        "translationDe": "Gepriesen bist Du, o Allah, mein Herr. In Deinem Namen lege ich meine Seite nieder und durch Dich erhebe ich sie. Wenn Du meine Seele zurückhältst, so vergib ihr, und wenn Du sie zurücksendest, so beschütze sie, wie Du Deine rechtschaffenen Diener beschützt.",
        "translationEn": "Glory is to You, O Allah, my Lord. In Your Name I lie down on my side and by You I rise. If You should take my soul, forgive it, and if You should return it, protect it as You protect Your righteous servants.",
        "translationFr": "Gloire à Toi, Ô Allah, mon Seigneur. C'est en Ton nom que je pose mon côté et par Toi que je le relève. Si Tu retiens mon âme, pardonne-lui, et si Tu la renvoies, protège-la comme Tu protèges Tes serviteurs vertueux.",
        "translationEs": "Gloria a Ti, ¡oh Alá!, mi Señor. En Tu nombre me acuesto de lado y por Ti me levanto. Si Te llevas mi alma, perdónala, y si la devuelves, protégela como proteges a Tus siervos justos.",
        "translationUr": "پاک ہے تو اے اللہ میرے رب! تیرے نام کے ساتھ میں نے اپنا پہلو رکھا اور تیرے ہی ساتھ میں اسے اٹھاؤں گا، اگر تو نے میری جان روک لی تو اسے بخش دینا، اور اگر تو نے اسے چھوڑ دیا تو اس کی حفاظت کرنا جس طرح تو اپنے نیک بندوں کی حفاظت کرتا ہے۔",
        "translationFa": "پاک و منزهی خداوندا ای پروردگارم، به نام تو پهلویم را نهادم و به تو آن را بلند می‌کنم، اگر جانم را گرفتی آن را بیامرز و اگر بازگرداندی محافظت کن همانگونه که از بندگان صالحت محافظت می‌کنی.",
        "repetitions": 1,
        "source": "Sahih Al-Bukhari / Hisn al-Muslim",
        "sourceArabic": "صحيح البخاري / حصن المسلم",
    },
    # ── Adhkar_Khorouj (Leaving home) ──────────────────────────────────────
    {
        "id": 401,
        "category": "Adhkar_Khorouj",
        "textArabic": "بِسْمِ اللَّهِ، تَوَكَّلْتُ عَلَى اللَّهِ، وَلَا حَوْلَ وَلَا قُوَّةَ إِلَّا بِاللَّهِ",
        "transliteration": "Bismillahi, tawakkaltu 'alallahi, wa la hawla wa la quwwata illa billah.",
        "translationDe": "Im Namen Allahs, ich vertraue auf Allah, und es gibt keine Macht noch Kraft außer durch Allah.",
        "translationEn": "In the name of Allah, I place my trust in Allah, and there is no might nor power except with Allah.",
        "translationFr": "Au nom d'Allah, je place ma confiance en Allah, et il n'y a de force ni de puissance que par Allah.",
        "translationEs": "En el nombre de Alá, pongo mi confianza en Alá, y no hay fuerza ni poder excepto con Alá.",
        "translationUr": "اللہ کے نام کے ساتھ، میں نے اللہ پر بھروسہ کیا، اور گناہوں سے بچنے کی طاقت اور نیکی کرنے کی قوت اللہ ہی کی طرف سے ہے۔",
        "translationFa": "به نام خدا، بر خدا توکل کردم و هیچ دگرگونی و نیرویی جز به وسیله خدا نیست.",
        "repetitions": 1,
        "source": "Sunan Abi Dawud & At-Tirmidhi / Hisn al-Muslim",
        "sourceArabic": "سنن أبي داود والترمذي / حصن المسلم",
    },
    {
        "id": 402,
        "category": "Adhkar_Khorouj",
        "textArabic": "اللَّهُمَّ إِنِّي أَعُوذُ بِكَ أَنْ أَضِلَّ أَوْ أُضَلَّ، أَوْ أَزِلَّ أَوْ أُزَلَّ، أَوْ أَظْلِمَ أَوْ أُظْلَمَ، أَوْ أَجْهَلَ أَوْ يُجْهَلَ عَلَيَّ",
        "transliteration": "Allahumma inni a'udhu bika an adilla aw udalla, aw azilla aw uzalla, aw azlima aw uzlama, aw ajhala aw yujhala 'alayya.",
        "translationDe": "O Allah, ich suche Zuflucht bei Dir davor, dass ich in die Irre gehe oder irregeführt werde, dass ich fehle oder zum Fehlen gebracht werde, dass ich Unrecht tue oder mir Unrecht angetan wird, oder dass ich mich unwissend verhalte oder man mir gegenüber unwissend entgegentritt.",
        "translationEn": "O Allah, I seek refuge in You from leading others astray or being led astray, from causing others to slip or being made to slip, from wrongdoing or being wronged, or from behaving ignorantly or being treated ignorantly.",
        "translationFr": "Ô Allah, je cherche refuge auprès de Toi contre le fait d'égarer ou d'être égaré, de trébucher ou d'être poussé à trébucher, de commettre une injustice ou d'en subir une, ou d'agir avec ignorance ou d'être traité avec ignorance.",
        "translationEs": "¡Oh Alá! Busco refugio en Ti de extraviar a otros o ser extraviado, de hacer tropezar a otros o ser hecho tropezar, de cometer injusticia o sufrir injusticia, o de actuar con ignorancia o ser tratado con ignorancia.",
        "translationUr": "اے اللہ! میں تیری پناہ مانگتا ہوں اس سے کہ میں بہک جاؤں یا بہکا دیا جاؤں، یا میں پھسل جاؤں یا مجھے پھسلا دیا جائے، یا میں ظلم کروں یا مجھ پر ظلم کیا جائے، یا میں نادانی کروں یا میرے ساتھ نادانی کی جائے۔",
        "translationFa": "خداوندا، به تو پناه می‌برم از اینکه گمراه شوم یا گمراه شوم، یا بلغزم یا لغزانده شوم، یا ستم کنم یا بر من ستم شود، یا نادانی کنم یا بر من نادانی شود.",
        "repetitions": 1,
        "source": "Sunan Abi Dawud, At-Tirmidhi, An-Nasa'i & Ibn Majah / Hisn al-Muslim",
        "sourceArabic": "سنن أبي داود والترمذي والنسائي وابن ماجه / حصن المسلم",
    },
    # ── Adhkar_Dukhoul (Entering home) ─────────────────────────────────────
    {
        "id": 501,
        "category": "Adhkar_Dukhoul",
        "textArabic": "بِسْمِ اللَّهِ وَلَجْنَا، وَبِسْمِ اللَّهِ خَرَجْنَا، وَعَلَى اللَّهِ رَبِّنَا تَوَكَّلْنَا",
        "transliteration": "Bismillahi walajna, wa bismillahi kharajna, wa 'alallahi Rabbina tawalkalna.",
        "translationDe": "Im Namen Allahs treten wir ein, und im Namen Allahs gehen wir hinaus, und auf Allah, unseren Herrn, verlassen wir uns.",
        "translationEn": "In the name of Allah we enter, and in the name of Allah we leave, and upon Allah our Lord we rely.",
        "translationFr": "Au nom d'Allah nous entrons, et au nom d'Allah nous sortons, et en Allah notre Seigneur nous plaçons notre confiance.",
        "translationEs": "En el nombre de Alá entramos, y en el nombre de Alá salimos, y en Alá nuestro Señor confiamos.",
        "translationUr": "اللہ کے نام کے ساتھ ہم داخل ہوئے، اور اللہ کے نام کے ساتھ ہم نکلے، اور اپنے رب اللہ ہی پر ہم نے بھروسہ کیا۔",
        "translationFa": "به نام خدا وارد شدیم و به نام خدا خارج شدیم و بر پروردگارمان خدا توکل کردیم.",
        "repetitions": 1,
        "source": "Sunan Abi Dawud / Hisn al-Muslim",
        "sourceArabic": "سنن أبي داود / حصن المسلم",
    },
    {
        "id": 502,
        "category": "Adhkar_Dukhoul",
        "textArabic": "السَّلَامُ عَلَيْنَا وَعَلَى عِبَادِ اللَّهِ الصَّالِحِينَ",
        "transliteration": "As-salamu 'alayna wa 'ala 'ibadillahis-salihin.",
        "translationDe": "Friede sei mit uns und mit den rechtschaffenen Dienern Allahs.",
        "translationEn": "Peace be upon us and upon the righteous servants of Allah.",
        "translationFr": "Paix sur nous et sur les serviteurs vertueux d'Allah.",
        "translationEs": "La paz sea con nosotros y con los siervos justos de Alá.",
        "translationUr": "ہم پر سلام ہو اور اللہ کے نیک بندوں پر۔",
        "translationFa": "سلام بر ما و بر بندگان صالح خدا.",
        "repetitions": 1,
        "source": "Sahih Al-Bukhari (Al-Adab al-Mufrad) & Sure An-Nur:61",
        "sourceArabic": "صحيح البخاري (الأدب المفرد) وسورة النور: 61",
    },
]


# ---------------------------------------------------------------------------
# DB generation
# ---------------------------------------------------------------------------

def create_database(path: str) -> None:
    if os.path.exists(path):
        os.remove(path)

    conn = sqlite3.connect(path)
    cur = conn.cursor()

    # ── Main table (schema must match Room's @Entity exactly) ───────────────
    cur.execute("""
        CREATE TABLE adkar (
            id               INTEGER NOT NULL,
            category         TEXT    NOT NULL,
            textArabic       TEXT    NOT NULL,
            transliteration  TEXT    NOT NULL,
            translationDe    TEXT    NOT NULL,
            translationEn    TEXT    NOT NULL,
            translationFr    TEXT    NOT NULL,
            translationEs    TEXT    NOT NULL,
            translationUr    TEXT    NOT NULL,
            translationFa    TEXT    NOT NULL,
            repetitions      INTEGER NOT NULL,
            source           TEXT    NOT NULL,
            sourceArabic     TEXT    NOT NULL,
            isFavorite       INTEGER NOT NULL,
            lastCompletedDate TEXT,
            PRIMARY KEY(id)
        )
    """)

    # ── Room internal metadata table ────────────────────────────────────────
    cur.execute("""
        CREATE TABLE room_master_table (
            id            INTEGER PRIMARY KEY,
            identity_hash TEXT
        )
    """)
    cur.execute(
        "INSERT INTO room_master_table (id, identity_hash) VALUES (42, ?)",
        (ROOM_IDENTITY_HASH,)
    )

    # ── Insert adkar ────────────────────────────────────────────────────────
    for a in ADKAR:
        cur.execute("""
            INSERT INTO adkar (
                id, category, textArabic, transliteration,
                translationDe, translationEn, translationFr, translationEs,
                translationUr, translationFa, repetitions, source, sourceArabic,
                isFavorite, lastCompletedDate
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            a["id"], a["category"], a["textArabic"], a["transliteration"],
            a["translationDe"], a["translationEn"], a["translationFr"], a["translationEs"],
            a["translationUr"], a["translationFa"], a["repetitions"],
            a["source"], a["sourceArabic"],
            0,    # isFavorite default
            None, # lastCompletedDate default
        ))

    conn.commit()
    conn.close()

    # ── Set SQLite user_version (Room DB version) ───────────────────────────
    with open(path, "r+b") as f:
        f.seek(60)
        f.write(struct.pack(">I", ROOM_DB_VERSION))

    print(f"✓ Created {path}")
    print(f"  Rows   : {len(ADKAR)}")
    print(f"  Version: {ROOM_DB_VERSION}")
    print(f"  Hash   : {ROOM_IDENTITY_HASH}")
    print(f"\n→ Copy to: app/src/main/assets/adkar.db")


if __name__ == "__main__":
    create_database(OUTPUT_FILE)
