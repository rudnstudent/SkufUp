# 🍺 SkufUp — Beer Can Opening Detector

<div align="center">

**🌐 Language:**  
[![English](https://img.shields.io/badge/English-blue.svg)](README.md) [![Русский](https://img.shields.io/badge/Русский-red.svg)](docs/README.ru.md) [![Deutsch](https://img.shields.io/badge/Deutsch-yellow.svg)](docs/README.de.md) [![Español](https://img.shields.io/badge/Español-orange.svg)](docs/README.es.md) [![Français](https://img.shields.io/badge/Français-purple.svg)](docs/README.fr.md) [![中文](https://img.shields.io/badge/中文-green.svg)](docs/README.zh.md) [![Čeština](https://img.shields.io/badge/Čeština-darkblue.svg)](docs/README.cs.md) [![Nederlands](https://img.shields.io/badge/Nederlands-darkorange.svg)](docs/README.nl.md)

</div>

<div align="center">

> *🍻 56 cans of beer were consumed during development 🍻*

</div>

<div align="center">

![Beer Detection](https://gifs.obs.ru-moscow-1.hc.sbercloud.ru/9a9d843e4afa4c94fd32eac95b1e07a2483b293d5eb816cff79ad64a51b59acf.gif)

**Open a beer → Game launches**

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![Windows](https://img.shields.io/badge/Platform-Windows-blue.svg)](https://windows.com)
[![ML](https://img.shields.io/badge/ML-RandomForest-green.svg)](https://scikit-learn.org)
[![License](https://img.shields.io/badge/License-Free-brightgreen.svg)](#)

</div>

---

## 🎯 What is this?

**SkufUp** listens to your microphone and waits for the characteristic **"pshhh"** sound of opening a beer can.  
When it hears it — automatically launches a game or opens a website!

<div align="center">

| Before beer 😢 | | After beer 🍺 |
|:---:|:---:|:---:|
| <img src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcStzvxmAUkKO2cwGsKxnqy2RRSrQom17-wHh4LCQw7Byg&s" width="200" height="200"> | ➡️ | <img src="https://www.meme-arsenal.com/memes/0e757738df2f12eb86e17f227bc55b92.jpg" width="200" height="200"> |

</div>

---

## ✨ Features

- 🤖 **ML Detector** — trained on real recordings, ~95% accuracy
- 🎮 **Process Check** — won't open the game if it's already running
- 🌐 **Website Support** — can open any URL
- 🚀 **Autostart** — launches with Windows
- 🎨 **Beautiful Interface** — dark theme, minimalist design

---

## 📦 Installation

### Option 1: Ready-made Installer
Download `SkufUp_Setup.exe` from [Releases](https://github.com/rudnstudent/SkufUp/releases/tag/new_languages) and run it.

### Option 2: From Source
```bash
# Clone the repository
git clone https://github.com/your-username/SkufUp.git
cd SkufUp

# Install dependencies
pip install -r requirements.txt

# Run
python gui_app.py
```

---

## 🚀 How to Use

<div align="center">

![How to use](https://gifs.obs.ru-moscow-1.hc.sbercloud.ru/bbfec04fc1cb15ad8ccc0df98b2275829fe4196bd4c22bc1836a912796f418d5.gif)

</div>

1. **Launch** SkufUp
2. **Choose** a game (.exe) or specify a website
3. **Press** START
4. **Open a beer** 🍺
5. **Enjoy!** 🎮

---

## 🔧 How the ML Detector Works

```
🎤 Microphone → 📊 Audio Analysis → 🤖 ML Model → ✅ Beer!
```

| Step | Description |
|------|-------------|
| 1️⃣ | Microphone records sound in real-time |
| 2️⃣ | Features extracted: spectrum, envelope, frequencies |
| 3️⃣ | RandomForest classifies: beer or not |
| 4️⃣ | Additional checks: H/L ratio, centroid, duration |
| 5️⃣ | If everything matches → launch game/website |

**Characteristic features of "pshhh":**
- 📈 High frequencies (2-8 kHz) — gas hissing
- ⚡ Fast attack — sudden onset
- 📉 Short duration — 100-500 ms

---

## 📁 Project Structure

```
Source Code/
├── gui_app.py              # 🖥️ Main application with GUI
├── audio_detector_ml.py    # 🤖 ML sound detector
├── audio_detector.py       # 📊 Basic detector (fallback)
├── train_model.py          # 🎓 ML model training
├── analyze_audio.py        # 📈 Audio file analysis
├── config.py               # ⚙️ Settings
├── beer_sound_template.py  # 🍺 Reference sounds
├── build_installer.py      # 📦 Installer builder
└── requirements.txt        # 📋 Dependencies
```

---

## ⚙️ Configuration

Open `config.py`:

```python
DETECTOR_SETTINGS = {
    "similarity_threshold": 0.45,  # Similarity threshold
    "peak_threshold": 0.1,         # Volume threshold
    "cooldown": 3.0,               # Pause between triggers
    "debug_mode": True,            # Show logs
}
```

| Problem | Solution |
|---------|----------|
| False positives | Increase `similarity_threshold` to 0.55-0.60 |
| Doesn't catch can | Decrease `similarity_threshold` to 0.40 |
| Too frequent triggers | Increase `cooldown` to 5-10 sec |

---

## 🛠️ Building .exe

```bash
# Build application
pyinstaller SkufUp.spec --noconfirm

# Create installer
python build_installer.py
pyinstaller --onefile --windowed --name=SkufUp_Setup --icon=setup.ico SkufUp_Installer.py
```

---

## 🎓 Training Your Own Model

If you want to improve accuracy:

```bash
# 1. Put your recordings in sound/ folder
# 2. Analyze
python analyze_audio.py

# 3. Train model
python train_model.py

# 4. Rebuild exe
pyinstaller SkufUp.spec --noconfirm
```

---

## 🐛 Debugging

Enable `debug_mode: True` and watch the console:

```
🔈 [████████░░░░░░░░░░░░] RMS:0.023 Peak:0.089
🔊 [████████████████████] RMS:0.156 Peak:0.423
   🤖 ML probability: 89% | H/L: 15.2 | Centroid: 8500Hz
🍺 CAN OPENED! (ML: 89%, H/L: 15.2)
```

---

<div align="center">

## 🍻 Enjoy your beer!

![Cheers](https://media.tenor.com/780S-3Ft-8kAAAAM/beer-time.gif)

**Made with 🍺 and ❤️**

</div>


