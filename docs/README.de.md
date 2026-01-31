# 🍺 SkufUp — Bierdosen-Öffnungsdetektor

<div align="center">

**🌐 Sprache:**  
[![English](https://img.shields.io/badge/English-blue.svg)](../README.md) [![Русский](https://img.shields.io/badge/Русский-red.svg)](README.ru.md) [![Deutsch](https://img.shields.io/badge/Deutsch-yellow.svg)](README.de.md) [![Español](https://img.shields.io/badge/Español-orange.svg)](README.es.md) [![Français](https://img.shields.io/badge/Français-purple.svg)](README.fr.md) [![中文](https://img.shields.io/badge/中文-green.svg)](README.zh.md) [![Čeština](https://img.shields.io/badge/Čeština-darkblue.svg)](README.cs.md) [![Nederlands](https://img.shields.io/badge/Nederlands-darkorange.svg)](README.nl.md)

</div>

<div align="center">

> *🍻 Während der Entwicklung wurden 56 Dosen Bier konsumiert 🍻*

</div>

<div align="center">

![Beer Detection](https://gifs.obs.ru-moscow-1.hc.sbercloud.ru/9a9d843e4afa4c94fd32eac95b1e07a2483b293d5eb816cff79ad64a51b59acf.gif)

**Öffne ein Bier → Spiel startet**

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![Windows](https://img.shields.io/badge/Platform-Windows-blue.svg)](https://windows.com)
[![ML](https://img.shields.io/badge/ML-RandomForest-green.svg)](https://scikit-learn.org)
[![License](https://img.shields.io/badge/License-Free-brightgreen.svg)](#)

</div>

---

## 🎯 Was ist das?

**SkufUp** hört auf dein Mikrofon und wartet auf das charakteristische **"Psshhh"**-Geräusch einer sich öffnenden Bierdose.  
Wenn es das hört — startet automatisch ein Spiel oder öffnet eine Website!

<div align="center">

| Vor dem Bier 😢 | | Nach dem Bier 🍺 |
|:---:|:---:|:---:|
| <img src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcStzvxmAUkKO2cwGsKxnqy2RRSrQom17-wHh4LCQw7Byg&s" width="200" height="200"> | ➡️ | <img src="https://www.meme-arsenal.com/memes/0e757738df2f12eb86e17f227bc55b92.jpg" width="200" height="200"> |

</div>

---

## ✨ Features

- 🤖 **ML-Detektor** — trainiert mit echten Aufnahmen, ~95% Genauigkeit
- 🎮 **Prozessprüfung** — startet das Spiel nicht, wenn es bereits läuft
- 🌐 **Website-Unterstützung** — kann jede URL öffnen
- 🚀 **Autostart** — startet mit Windows
- 🎨 **Schöne Oberfläche** — dunkles Theme, minimalistisches Design

---

## 📦 Installation

### Option 1: Fertiger Installer
Lade `SkufUp_Setup.exe` von [Releases](https://github.com/rudnstudent/SkufUp/releases/tag/new_languages) herunter und führe es aus.

### Option 2: Aus Quellcode
```bash
# Repository klonen
git clone https://github.com/your-username/SkufUp.git
cd SkufUp

# Abhängigkeiten installieren
pip install -r requirements.txt

# Ausführen
python gui_app.py
```

---

## 🚀 Verwendung

<div align="center">

![How to use](https://gifs.obs.ru-moscow-1.hc.sbercloud.ru/bbfec04fc1cb15ad8ccc0df98b2275829fe4196bd4c22bc1836a912796f418d5.gif)

</div>

1. **Starte** SkufUp
2. **Wähle** ein Spiel (.exe) oder gib eine Website an
3. **Drücke** START
4. **Öffne ein Bier** 🍺
5. **Genieße!** 🎮

---

## 🔧 Wie der ML-Detektor funktioniert

```
🎤 Mikrofon → 📊 Audio-Analyse → 🤖 ML-Modell → ✅ Bier!
```

| Schritt | Beschreibung |
|---------|--------------|
| 1️⃣ | Mikrofon nimmt Sound in Echtzeit auf |
| 2️⃣ | Features extrahiert: Spektrum, Hüllkurve, Frequenzen |
| 3️⃣ | RandomForest klassifiziert: Bier oder nicht |
| 4️⃣ | Zusätzliche Prüfungen: H/L-Verhältnis, Centroid, Dauer |
| 5️⃣ | Wenn alles passt → Spiel/Website starten |

**Charakteristische Merkmale von "Psshhh":**
- 📈 Hohe Frequenzen (2-8 kHz) — Gaszischen
- ⚡ Schneller Anstieg — plötzlicher Beginn
- 📉 Kurze Dauer — 100-500 ms

---

<div align="center">

## 🍻 Prost!

![Cheers](https://media.tenor.com/780S-3Ft-8kAAAAM/beer-time.gif)

**Gemacht mit 🍺 und ❤️**

</div>
