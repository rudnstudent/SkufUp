# 🍺 SkufUp — Détecteur d'Ouverture de Bière

<div align="center">

**🌐 Langue:**  
[![English](https://img.shields.io/badge/English-blue.svg)](../README.md) [![Русский](https://img.shields.io/badge/Русский-red.svg)](README.ru.md) [![Deutsch](https://img.shields.io/badge/Deutsch-yellow.svg)](README.de.md) [![Español](https://img.shields.io/badge/Español-orange.svg)](README.es.md) [![Français](https://img.shields.io/badge/Français-purple.svg)](README.fr.md) [![中文](https://img.shields.io/badge/中文-green.svg)](README.zh.md) [![Čeština](https://img.shields.io/badge/Čeština-darkblue.svg)](README.cs.md) [![Nederlands](https://img.shields.io/badge/Nederlands-darkorange.svg)](README.nl.md)

</div>

<div align="center">

> *🍻 56 canettes de bière ont été consommées pendant le développement 🍻*

</div>

<div align="center">

![Beer Detection](https://gifs.obs.ru-moscow-1.hc.sbercloud.ru/9a9d843e4afa4c94fd32eac95b1e07a2483b293d5eb816cff79ad64a51b59acf.gif)

**Ouvre une bière → Le jeu se lance**

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![Windows](https://img.shields.io/badge/Platform-Windows-blue.svg)](https://windows.com)
[![ML](https://img.shields.io/badge/ML-RandomForest-green.svg)](https://scikit-learn.org)
[![License](https://img.shields.io/badge/License-Free-brightgreen.svg)](#)

</div>

---

## 🎯 Qu'est-ce que c'est?

**SkufUp** écoute ton microphone et attend le son caractéristique **"pshhh"** de l'ouverture d'une canette de bière.  
Quand il l'entend — il lance automatiquement un jeu ou ouvre un site web!

<div align="center">

| Avant la bière 😢 | | Après la bière 🍺 |
|:---:|:---:|:---:|
| <img src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcStzvxmAUkKO2cwGsKxnqy2RRSrQom17-wHh4LCQw7Byg&s" width="200" height="200"> | ➡️ | <img src="https://www.meme-arsenal.com/memes/0e757738df2f12eb86e17f227bc55b92.jpg" width="200" height="200"> |

</div>

---

## ✨ Fonctionnalités

- 🤖 **Détecteur ML** — entraîné sur de vrais enregistrements, ~95% de précision
- 🎮 **Vérification des processus** — n'ouvrira pas le jeu s'il est déjà en cours
- 🌐 **Support des sites web** — peut ouvrir n'importe quelle URL
- 🚀 **Démarrage automatique** — se lance avec Windows
- 🎨 **Belle interface** — thème sombre, design minimaliste

---

## 📦 Installation

### Option 1: Installateur prêt à l'emploi
Télécharge `SkufUp_Setup.exe` depuis [Releases](https://github.com/rudnstudent/SkufUp/releases/tag/new_languages) et exécute-le.

### Option 2: Depuis le code source
```bash
# Cloner le dépôt
git clone https://github.com/your-username/SkufUp.git
cd SkufUp

# Installer les dépendances
pip install -r requirements.txt

# Exécuter
python gui_app.py
```

---

## 🚀 Comment utiliser

<div align="center">

![How to use](https://gifs.obs.ru-moscow-1.hc.sbercloud.ru/bbfec04fc1cb15ad8ccc0df98b2275829fe4196bd4c22bc1836a912796f418d5.gif)

</div>

1. **Lance** SkufUp
2. **Choisis** un jeu (.exe) ou indique un site web
3. **Appuie** sur DÉMARRER
4. **Ouvre une bière** 🍺
5. **Profite!** 🎮

---

## 🔧 Comment fonctionne le détecteur ML

```
🎤 Microphone → 📊 Analyse audio → 🤖 Modèle ML → ✅ Bière!
```

| Étape | Description |
|-------|-------------|
| 1️⃣ | Le microphone enregistre le son en temps réel |
| 2️⃣ | Caractéristiques extraites: spectre, enveloppe, fréquences |
| 3️⃣ | RandomForest classifie: bière ou non |
| 4️⃣ | Vérifications supplémentaires: ratio H/L, centroïde, durée |
| 5️⃣ | Si tout correspond → lancer le jeu/site web |

**Caractéristiques du "pshhh":**
- 📈 Hautes fréquences (2-8 kHz) — sifflement du gaz
- ⚡ Attaque rapide — début soudain
- 📉 Courte durée — 100-500 ms

---

<div align="center">

## 🍻 Santé!

![Cheers](https://media.tenor.com/780S-3Ft-8kAAAAM/beer-time.gif)

**Fait avec 🍺 et ❤️**

</div>
