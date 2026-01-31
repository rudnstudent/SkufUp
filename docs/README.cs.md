# 🍺 SkufUp — Detektor Otevření Piva

<div align="center">

**🌐 Jazyk:**  
[![English](https://img.shields.io/badge/English-blue.svg)](../README.md) [![Русский](https://img.shields.io/badge/Русский-red.svg)](README.ru.md) [![Deutsch](https://img.shields.io/badge/Deutsch-yellow.svg)](README.de.md) [![Español](https://img.shields.io/badge/Español-orange.svg)](README.es.md) [![Français](https://img.shields.io/badge/Français-purple.svg)](README.fr.md) [![中文](https://img.shields.io/badge/中文-green.svg)](README.zh.md) [![Čeština](https://img.shields.io/badge/Čeština-darkblue.svg)](README.cs.md) [![Nederlands](https://img.shields.io/badge/Nederlands-darkorange.svg)](README.nl.md)

</div>

<div align="center">

> *🍻 Během vývoje bylo spotřebováno 56 plechovek piva 🍻*

</div>

<div align="center">

![Beer Detection](https://gifs.obs.ru-moscow-1.hc.sbercloud.ru/9a9d843e4afa4c94fd32eac95b1e07a2483b293d5eb816cff79ad64a51b59acf.gif)

**Otevři pivo → Spustí se hra**

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![Windows](https://img.shields.io/badge/Platform-Windows-blue.svg)](https://windows.com)
[![ML](https://img.shields.io/badge/ML-RandomForest-green.svg)](https://scikit-learn.org)
[![License](https://img.shields.io/badge/License-Free-brightgreen.svg)](#)

</div>

---

## 🎯 Co to je?

**SkufUp** poslouchá tvůj mikrofon a čeká na charakteristický zvuk **"pšššt"** otevírání plechovky piva.  
Když ho uslyší — automaticky spustí hru nebo otevře webovou stránku!

<div align="center">

| Před pivem 😢 | | Po pivu 🍺 |
|:---:|:---:|:---:|
| <img src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcStzvxmAUkKO2cwGsKxnqy2RRSrQom17-wHh4LCQw7Byg&s" width="200" height="200"> | ➡️ | <img src="https://www.meme-arsenal.com/memes/0e757738df2f12eb86e17f227bc55b92.jpg" width="200" height="200"> |

</div>

---

## ✨ Funkce

- 🤖 **ML detektor** — natrénovaný na skutečných nahrávkách, ~95% přesnost
- 🎮 **Kontrola procesů** — nespustí hru, pokud už běží
- 🌐 **Podpora webů** — může otevřít libovolnou URL
- 🚀 **Autostart** — spouští se s Windows
- 🎨 **Krásné rozhraní** — tmavý motiv, minimalistický design

---

## 📦 Instalace

### Možnost 1: Hotový instalátor
Stáhni `SkufUp_Setup.exe` z [Releases](https://github.com/rudnstudent/SkufUp/releases/tag/new_languages) a spusť ho.

### Možnost 2: Ze zdrojového kódu
```bash
# Klonovat repozitář
git clone https://github.com/your-username/SkufUp.git
cd SkufUp

# Nainstalovat závislosti
pip install -r requirements.txt

# Spustit
python gui_app.py
```

---

## 🚀 Jak používat

<div align="center">

![How to use](https://gifs.obs.ru-moscow-1.hc.sbercloud.ru/bbfec04fc1cb15ad8ccc0df98b2275829fe4196bd4c22bc1836a912796f418d5.gif)

</div>

1. **Spusť** SkufUp
2. **Vyber** hru (.exe) nebo zadej webovou stránku
3. **Stiskni** START
4. **Otevři pivo** 🍺
5. **Užívej si!** 🎮

---

## 🔧 Jak funguje ML detektor

```
🎤 Mikrofon → 📊 Analýza zvuku → 🤖 ML model → ✅ Pivo!
```

| Krok | Popis |
|------|-------|
| 1️⃣ | Mikrofon nahrává zvuk v reálném čase |
| 2️⃣ | Extrahují se vlastnosti: spektrum, obálka, frekvence |
| 3️⃣ | RandomForest klasifikuje: pivo nebo ne |
| 4️⃣ | Dodatečné kontroly: poměr H/L, centroid, délka |
| 5️⃣ | Pokud vše sedí → spustit hru/web |

**Charakteristické znaky "pšššt":**
- 📈 Vysoké frekvence (2-8 kHz) — syčení plynu
- ⚡ Rychlý nástup — náhlý začátek
- 📉 Krátké trvání — 100-500 ms

---

<div align="center">

## 🍻 Na zdraví!

![Cheers](https://media.tenor.com/780S-3Ft-8kAAAAM/beer-time.gif)

**Vytvořeno s 🍺 a ❤️**

</div>
