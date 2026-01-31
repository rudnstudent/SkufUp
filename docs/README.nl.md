# 🍺 SkufUp — Bier Openingsdetector

<div align="center">

**🌐 Taal:**  
[![English](https://img.shields.io/badge/English-blue.svg)](../README.md) [![Русский](https://img.shields.io/badge/Русский-red.svg)](README.ru.md) [![Deutsch](https://img.shields.io/badge/Deutsch-yellow.svg)](README.de.md) [![Español](https://img.shields.io/badge/Español-orange.svg)](README.es.md) [![Français](https://img.shields.io/badge/Français-purple.svg)](README.fr.md) [![中文](https://img.shields.io/badge/中文-green.svg)](README.zh.md) [![Čeština](https://img.shields.io/badge/Čeština-darkblue.svg)](README.cs.md) [![Nederlands](https://img.shields.io/badge/Nederlands-darkorange.svg)](README.nl.md)

</div>

<div align="center">

> *🍻 Tijdens de ontwikkeling werden 56 blikjes bier geconsumeerd 🍻*

</div>

<div align="center">

![Beer Detection](https://gifs.obs.ru-moscow-1.hc.sbercloud.ru/9a9d843e4afa4c94fd32eac95b1e07a2483b293d5eb816cff79ad64a51b59acf.gif)

**Open een biertje → Spel start**

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![Windows](https://img.shields.io/badge/Platform-Windows-blue.svg)](https://windows.com)
[![ML](https://img.shields.io/badge/ML-RandomForest-green.svg)](https://scikit-learn.org)
[![License](https://img.shields.io/badge/License-Free-brightgreen.svg)](#)

</div>

---

## 🎯 Wat is dit?

**SkufUp** luistert naar je microfoon en wacht op het karakteristieke **"psshhh"** geluid van het openen van een bierblikje.  
Wanneer het dat hoort — start automatisch een spel of opent een website!

<div align="center">

| Voor het bier 😢 | | Na het bier 🍺 |
|:---:|:---:|:---:|
| <img src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcStzvxmAUkKO2cwGsKxnqy2RRSrQom17-wHh4LCQw7Byg&s" width="200" height="200"> | ➡️ | <img src="https://www.meme-arsenal.com/memes/0e757738df2f12eb86e17f227bc55b92.jpg" width="200" height="200"> |

</div>

---

## ✨ Functies

- 🤖 **ML Detector** — getraind op echte opnames, ~95% nauwkeurigheid
- 🎮 **Procescontrole** — opent het spel niet als het al draait
- 🌐 **Website ondersteuning** — kan elke URL openen
- 🚀 **Autostart** — start met Windows
- 🎨 **Mooie interface** — donker thema, minimalistisch design

---

## 📦 Installatie

### Optie 1: Kant-en-klare installer
Download `SkufUp_Setup.exe` van [Releases](https://github.com/rudnstudent/SkufUp/releases/tag/new_languages) en voer het uit.

### Optie 2: Vanuit broncode
```bash
# Repository klonen
git clone https://github.com/your-username/SkufUp.git
cd SkufUp

# Afhankelijkheden installeren
pip install -r requirements.txt

# Uitvoeren
python gui_app.py
```

---

## 🚀 Hoe te gebruiken

<div align="center">

![How to use](https://gifs.obs.ru-moscow-1.hc.sbercloud.ru/bbfec04fc1cb15ad8ccc0df98b2275829fe4196bd4c22bc1836a912796f418d5.gif)

</div>

1. **Start** SkufUp
2. **Kies** een spel (.exe) of geef een website op
3. **Druk** op START
4. **Open een biertje** 🍺
5. **Geniet!** 🎮

---

## 🔧 Hoe de ML Detector werkt

```
🎤 Microfoon → 📊 Audio-analyse → 🤖 ML Model → ✅ Bier!
```

| Stap | Beschrijving |
|------|--------------|
| 1️⃣ | Microfoon neemt geluid op in realtime |
| 2️⃣ | Kenmerken geëxtraheerd: spectrum, envelope, frequenties |
| 3️⃣ | RandomForest classificeert: bier of niet |
| 4️⃣ | Extra controles: H/L ratio, centroid, duur |
| 5️⃣ | Als alles klopt → start spel/website |

**Karakteristieke kenmerken van "psshhh":**
- 📈 Hoge frequenties (2-8 kHz) — gas sissen
- ⚡ Snelle attack — plotseling begin
- 📉 Korte duur — 100-500 ms

---

<div align="center">

## 🍻 Proost!

![Cheers](https://media.tenor.com/780S-3Ft-8kAAAAM/beer-time.gif)

**Gemaakt met 🍺 en ❤️**

</div>
