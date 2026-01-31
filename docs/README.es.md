# 🍺 SkufUp — Detector de Apertura de Cerveza

<div align="center">

**🌐 Idioma:**  
[![English](https://img.shields.io/badge/English-blue.svg)](../README.md) [![Русский](https://img.shields.io/badge/Русский-red.svg)](README.ru.md) [![Deutsch](https://img.shields.io/badge/Deutsch-yellow.svg)](README.de.md) [![Español](https://img.shields.io/badge/Español-orange.svg)](README.es.md) [![Français](https://img.shields.io/badge/Français-purple.svg)](README.fr.md) [![中文](https://img.shields.io/badge/中文-green.svg)](README.zh.md) [![Čeština](https://img.shields.io/badge/Čeština-darkblue.svg)](README.cs.md) [![Nederlands](https://img.shields.io/badge/Nederlands-darkorange.svg)](README.nl.md)

</div>

<div align="center">

> *🍻 Se consumieron 56 latas de cerveza durante el desarrollo 🍻*

</div>

<div align="center">

![Beer Detection](https://gifs.obs.ru-moscow-1.hc.sbercloud.ru/9a9d843e4afa4c94fd32eac95b1e07a2483b293d5eb816cff79ad64a51b59acf.gif)

**Abre una cerveza → Se inicia el juego**

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![Windows](https://img.shields.io/badge/Platform-Windows-blue.svg)](https://windows.com)
[![ML](https://img.shields.io/badge/ML-RandomForest-green.svg)](https://scikit-learn.org)
[![License](https://img.shields.io/badge/License-Free-brightgreen.svg)](#)

</div>

---

## 🎯 ¿Qué es esto?

**SkufUp** escucha tu micrófono y espera el característico sonido **"pshhh"** de abrir una lata de cerveza.  
Cuando lo escucha — ¡automáticamente inicia un juego o abre un sitio web!

<div align="center">

| Antes de la cerveza 😢 | | Después de la cerveza 🍺 |
|:---:|:---:|:---:|
| <img src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcStzvxmAUkKO2cwGsKxnqy2RRSrQom17-wHh4LCQw7Byg&s" width="200" height="200"> | ➡️ | <img src="https://www.meme-arsenal.com/memes/0e757738df2f12eb86e17f227bc55b92.jpg" width="200" height="200"> |

</div>

---

## ✨ Características

- 🤖 **Detector ML** — entrenado con grabaciones reales, ~95% de precisión
- 🎮 **Verificación de procesos** — no abrirá el juego si ya está ejecutándose
- 🌐 **Soporte de sitios web** — puede abrir cualquier URL
- 🚀 **Inicio automático** — se inicia con Windows
- 🎨 **Interfaz bonita** — tema oscuro, diseño minimalista

---

## 📦 Instalación

### Opción 1: Instalador listo
Descarga `SkufUp_Setup.exe` de [Releases](https://github.com/rudnstudent/SkufUp/releases/tag/new_languages) y ejecútalo.

### Opción 2: Desde el código fuente
```bash
# Clonar el repositorio
git clone https://github.com/your-username/SkufUp.git
cd SkufUp

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar
python gui_app.py
```

---

## 🚀 Cómo usar

<div align="center">

![How to use](https://gifs.obs.ru-moscow-1.hc.sbercloud.ru/bbfec04fc1cb15ad8ccc0df98b2275829fe4196bd4c22bc1836a912796f418d5.gif)

</div>

1. **Inicia** SkufUp
2. **Elige** un juego (.exe) o especifica un sitio web
3. **Presiona** INICIAR
4. **Abre una cerveza** 🍺
5. **¡Disfruta!** 🎮

---

## 🔧 Cómo funciona el detector ML

```
🎤 Micrófono → 📊 Análisis de audio → 🤖 Modelo ML → ✅ ¡Cerveza!
```

| Paso | Descripción |
|------|-------------|
| 1️⃣ | El micrófono graba sonido en tiempo real |
| 2️⃣ | Se extraen características: espectro, envolvente, frecuencias |
| 3️⃣ | RandomForest clasifica: cerveza o no |
| 4️⃣ | Verificaciones adicionales: ratio H/L, centroide, duración |
| 5️⃣ | Si todo coincide → iniciar juego/sitio web |

**Características del "pshhh":**
- 📈 Frecuencias altas (2-8 kHz) — silbido del gas
- ⚡ Ataque rápido — inicio repentino
- 📉 Duración corta — 100-500 ms

---

<div align="center">

## 🍻 ¡Salud!

![Cheers](https://media.tenor.com/780S-3Ft-8kAAAAM/beer-time.gif)

**Hecho con 🍺 y ❤️**

</div>
