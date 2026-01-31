# 🍺 SkufUp — 啤酒开启检测器

<div align="center">

**🌐 语言:**  
[![English](https://img.shields.io/badge/English-blue.svg)](../README.md) [![Русский](https://img.shields.io/badge/Русский-red.svg)](README.ru.md) [![Deutsch](https://img.shields.io/badge/Deutsch-yellow.svg)](README.de.md) [![Español](https://img.shields.io/badge/Español-orange.svg)](README.es.md) [![Français](https://img.shields.io/badge/Français-purple.svg)](README.fr.md) [![中文](https://img.shields.io/badge/中文-green.svg)](README.zh.md) [![Čeština](https://img.shields.io/badge/Čeština-darkblue.svg)](README.cs.md) [![Nederlands](https://img.shields.io/badge/Nederlands-darkorange.svg)](README.nl.md)

</div>

<div align="center">

> *🍻 开发过程中消耗了56罐啤酒 🍻*

</div>

<div align="center">

![Beer Detection](https://gifs.obs.ru-moscow-1.hc.sbercloud.ru/9a9d843e4afa4c94fd32eac95b1e07a2483b293d5eb816cff79ad64a51b59acf.gif)

**打开啤酒 → 游戏启动**

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![Windows](https://img.shields.io/badge/Platform-Windows-blue.svg)](https://windows.com)
[![ML](https://img.shields.io/badge/ML-RandomForest-green.svg)](https://scikit-learn.org)
[![License](https://img.shields.io/badge/License-Free-brightgreen.svg)](#)

</div>

---

## 🎯 这是什么？

**SkufUp** 监听你的麦克风，等待啤酒罐打开时特有的 **"噗嗤"** 声音。  
当它听到时 — 自动启动游戏或打开网站！

<div align="center">

| 喝啤酒之前 😢 | | 喝啤酒之后 🍺 |
|:---:|:---:|:---:|
| <img src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcStzvxmAUkKO2cwGsKxnqy2RRSrQom17-wHh4LCQw7Byg&s" width="200" height="200"> | ➡️ | <img src="https://www.meme-arsenal.com/memes/0e757738df2f12eb86e17f227bc55b92.jpg" width="200" height="200"> |

</div>

---

## ✨ 特点

- 🤖 **机器学习检测器** — 使用真实录音训练，准确率约95%
- 🎮 **进程检查** — 如果游戏已经在运行，不会重复打开
- 🌐 **网站支持** — 可以打开任何URL
- 🚀 **开机自启** — 随Windows启动
- 🎨 **精美界面** — 深色主题，简约设计

---

## 📦 安装

### 方式1：现成安装程序
从 [Releases](https://github.com/rudnstudent/SkufUp/releases/tag/new_languages) 下载 `SkufUp_Setup.exe` 并运行。

### 方式2：从源代码
```bash
# 克隆仓库
git clone https://github.com/your-username/SkufUp.git
cd SkufUp

# 安装依赖
pip install -r requirements.txt

# 运行
python gui_app.py
```

---

## 🚀 使用方法

<div align="center">

![How to use](https://gifs.obs.ru-moscow-1.hc.sbercloud.ru/bbfec04fc1cb15ad8ccc0df98b2275829fe4196bd4c22bc1836a912796f418d5.gif)

</div>

1. **启动** SkufUp
2. **选择** 游戏（.exe）或指定网站
3. **点击** 开始
4. **打开啤酒** 🍺
5. **享受！** 🎮

---

## 🔧 机器学习检测器工作原理

```
🎤 麦克风 → 📊 音频分析 → 🤖 机器学习模型 → ✅ 啤酒！
```

| 步骤 | 描述 |
|------|------|
| 1️⃣ | 麦克风实时录制声音 |
| 2️⃣ | 提取特征：频谱、包络、频率 |
| 3️⃣ | RandomForest分类：是否是啤酒 |
| 4️⃣ | 额外检查：高低频比、质心、持续时间 |
| 5️⃣ | 如果全部匹配 → 启动游戏/网站 |

**"噗嗤"声的特征：**
- 📈 高频（2-8 kHz）— 气体嘶嘶声
- ⚡ 快速起音 — 突然开始
- 📉 持续时间短 — 100-500毫秒

---

<div align="center">

## 🍻 干杯！

![Cheers](https://media.tenor.com/780S-3Ft-8kAAAAM/beer-time.gif)

**用 🍺 和 ❤️ 制作**

</div>
