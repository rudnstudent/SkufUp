"""
SkufUp Installer Builder
Создаёт единый установщик, который содержит exe внутри себя
"""

import os
import sys
import base64
import zlib

def create_installer():
    """Создаёт установщик с встроенным exe"""
    
    exe_path = os.path.join(os.path.dirname(__file__), "dist", "SkufUp.exe")
    ico_path = os.path.join(os.path.dirname(__file__), "beer.ico")
    
    if not os.path.exists(exe_path):
        print("❌ Файл dist/SkufUp.exe не найден!")
        print("   Сначала соберите приложение с помощью PyInstaller")
        return False
    
    print("📦 Читаю SkufUp.exe...")
    with open(exe_path, "rb") as f:
        exe_data = f.read()
    
    print(f"   Размер: {len(exe_data) / 1024 / 1024:.2f} МБ")
    
    # Читаем иконку
    ico_encoded = ""
    if os.path.exists(ico_path):
        print("🎨 Читаю beer.ico...")
        with open(ico_path, "rb") as f:
            ico_data = f.read()
        ico_encoded = base64.b64encode(ico_data).decode('ascii')
    
    print("🗜️ Сжимаю данные...")
    compressed = zlib.compress(exe_data, level=9)
    encoded = base64.b64encode(compressed).decode('ascii')
    
    print(f"   Сжатый размер: {len(compressed) / 1024 / 1024:.2f} МБ")
    
    installer_code = '''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════╗
║     🍺 SkufUp Installer 🍺           ║
║     Установщик приложения            ║
╚══════════════════════════════════════╝

Просто запустите этот файл для установки SkufUp.
"""

import os
import sys
import base64
import zlib
import ctypes
import winreg
import json

# Встроенные данные приложения (сжатый exe)
APP_DATA = """''' + encoded + '''"""

# Иконка приложения
ICO_DATA = """''' + ico_encoded + '''"""

APP_NAME = "SkufUp"
APP_EXE = "SkufUp.exe"

# Языки интерфейса
LANGUAGES = {
    "en": "English",
    "ru": "Русский",
    "de": "Deutsch",
    "es": "Español",
    "fr": "Français",
    "zh": "中文",
    "cs": "Čeština",
    "nl": "Nederlands"
}

# Переводы установщика
INSTALLER_TRANSLATIONS = {
    "en": {
        "title": "🍺 SkufUp",
        "subtitle": "Beer can opening sound detector",
        "language": "Language:",
        "desktop_shortcut": "Create desktop shortcut",
        "autostart": "Launch at Windows startup",
        "run_after": "Run after installation",
        "folder": "Folder:",
        "install": "  🚀  INSTALL  ",
        "installing": "Installing...",
        "success_title": "Success!",
        "success_msg": "✅ {0} successfully installed!\\n\\nFolder: {1}\\n\\nThe program will be launched.",
        "error_title": "Error",
        "error_msg": "Installation failed: {0}",
        "console_title": "🍺 SkufUp - Installer 🍺",
        "console_folder": "Installation folder:",
        "console_press": "Press Enter to install...",
        "console_shortcut": "🖥️ Creating desktop shortcut...",
        "console_shortcut_done": "   ✅ Shortcut created",
        "console_autostart": "🚀 Adding to startup...",
        "console_autostart_done": "   ✅ Added to startup",
        "console_done": "✅ Installation complete!",
        "console_run": "Run SkufUp now? (Y/N): "
    },
    "ru": {
        "title": "🍺 SkufUp",
        "subtitle": "Детектор звука открытия пива",
        "language": "Язык:",
        "desktop_shortcut": "Создать ярлык на рабочем столе",
        "autostart": "Запускать при старте Windows",
        "run_after": "Запустить после установки",
        "folder": "Папка:",
        "install": "  🚀  УСТАНОВИТЬ  ",
        "installing": "Установка...",
        "success_title": "Успех!",
        "success_msg": "✅ {0} успешно установлен!\\n\\nПапка: {1}\\n\\nПрограмма будет запущена.",
        "error_title": "Ошибка",
        "error_msg": "Не удалось установить: {0}",
        "console_title": "🍺 SkufUp - Установщик 🍺",
        "console_folder": "Папка установки:",
        "console_press": "Нажмите Enter для установки...",
        "console_shortcut": "🖥️ Создание ярлыка на рабочем столе...",
        "console_shortcut_done": "   ✅ Ярлык создан",
        "console_autostart": "🚀 Добавление в автозагрузку...",
        "console_autostart_done": "   ✅ Добавлено в автозагрузку",
        "console_done": "✅ Установка завершена!",
        "console_run": "Запустить SkufUp сейчас? (Y/N): "
    },
    "de": {
        "title": "🍺 SkufUp",
        "subtitle": "Bierdosen-Öffnungsgeräusch-Detektor",
        "language": "Sprache:",
        "desktop_shortcut": "Desktop-Verknüpfung erstellen",
        "autostart": "Bei Windows-Start ausführen",
        "run_after": "Nach Installation starten",
        "folder": "Ordner:",
        "install": "  🚀  INSTALLIEREN  ",
        "installing": "Installiere...",
        "success_title": "Erfolg!",
        "success_msg": "✅ {0} erfolgreich installiert!\\n\\nOrdner: {1}\\n\\nDas Programm wird gestartet.",
        "error_title": "Fehler",
        "error_msg": "Installation fehlgeschlagen: {0}",
        "console_title": "🍺 SkufUp - Installer 🍺",
        "console_folder": "Installationsordner:",
        "console_press": "Drücken Sie Enter zum Installieren...",
        "console_shortcut": "🖥️ Desktop-Verknüpfung erstellen...",
        "console_shortcut_done": "   ✅ Verknüpfung erstellt",
        "console_autostart": "🚀 Zum Autostart hinzufügen...",
        "console_autostart_done": "   ✅ Zum Autostart hinzugefügt",
        "console_done": "✅ Installation abgeschlossen!",
        "console_run": "SkufUp jetzt starten? (Y/N): "
    },
    "es": {
        "title": "🍺 SkufUp",
        "subtitle": "Detector de sonido de apertura de cerveza",
        "language": "Idioma:",
        "desktop_shortcut": "Crear acceso directo en escritorio",
        "autostart": "Iniciar con Windows",
        "run_after": "Ejecutar después de instalar",
        "folder": "Carpeta:",
        "install": "  🚀  INSTALAR  ",
        "installing": "Instalando...",
        "success_title": "¡Éxito!",
        "success_msg": "✅ {0} instalado correctamente!\\n\\nCarpeta: {1}\\n\\nEl programa se iniciará.",
        "error_title": "Error",
        "error_msg": "Error de instalación: {0}",
        "console_title": "🍺 SkufUp - Instalador 🍺",
        "console_folder": "Carpeta de instalación:",
        "console_press": "Presione Enter para instalar...",
        "console_shortcut": "🖥️ Creando acceso directo...",
        "console_shortcut_done": "   ✅ Acceso directo creado",
        "console_autostart": "🚀 Añadiendo al inicio...",
        "console_autostart_done": "   ✅ Añadido al inicio",
        "console_done": "✅ ¡Instalación completada!",
        "console_run": "¿Ejecutar SkufUp ahora? (Y/N): "
    },
    "fr": {
        "title": "🍺 SkufUp",
        "subtitle": "Détecteur de son d'ouverture de bière",
        "language": "Langue:",
        "desktop_shortcut": "Créer un raccourci sur le bureau",
        "autostart": "Lancer au démarrage de Windows",
        "run_after": "Lancer après l'installation",
        "folder": "Dossier:",
        "install": "  🚀  INSTALLER  ",
        "installing": "Installation...",
        "success_title": "Succès!",
        "success_msg": "✅ {0} installé avec succès!\\n\\nDossier: {1}\\n\\nLe programme sera lancé.",
        "error_title": "Erreur",
        "error_msg": "Échec de l'installation: {0}",
        "console_title": "🍺 SkufUp - Installateur 🍺",
        "console_folder": "Dossier d'installation:",
        "console_press": "Appuyez sur Entrée pour installer...",
        "console_shortcut": "🖥️ Création du raccourci...",
        "console_shortcut_done": "   ✅ Raccourci créé",
        "console_autostart": "🚀 Ajout au démarrage...",
        "console_autostart_done": "   ✅ Ajouté au démarrage",
        "console_done": "✅ Installation terminée!",
        "console_run": "Lancer SkufUp maintenant? (Y/N): "
    },
    "zh": {
        "title": "🍺 SkufUp",
        "subtitle": "啤酒开罐声音检测器",
        "language": "语言:",
        "desktop_shortcut": "创建桌面快捷方式",
        "autostart": "开机自动启动",
        "run_after": "安装后运行",
        "folder": "文件夹:",
        "install": "  🚀  安装  ",
        "installing": "安装中...",
        "success_title": "成功!",
        "success_msg": "✅ {0} 安装成功!\\n\\n文件夹: {1}\\n\\n程序将启动。",
        "error_title": "错误",
        "error_msg": "安装失败: {0}",
        "console_title": "🍺 SkufUp - 安装程序 🍺",
        "console_folder": "安装文件夹:",
        "console_press": "按Enter键安装...",
        "console_shortcut": "🖥️ 创建桌面快捷方式...",
        "console_shortcut_done": "   ✅ 快捷方式已创建",
        "console_autostart": "🚀 添加到启动...",
        "console_autostart_done": "   ✅ 已添加到启动",
        "console_done": "✅ 安装完成!",
        "console_run": "现在运行SkufUp? (Y/N): "
    },
    "cs": {
        "title": "🍺 SkufUp",
        "subtitle": "Detektor zvuku otevírání piva",
        "language": "Jazyk:",
        "desktop_shortcut": "Vytvořit zástupce na ploše",
        "autostart": "Spustit při startu Windows",
        "run_after": "Spustit po instalaci",
        "folder": "Složka:",
        "install": "  🚀  INSTALOVAT  ",
        "installing": "Instalace...",
        "success_title": "Úspěch!",
        "success_msg": "✅ {0} úspěšně nainstalován!\\n\\nSložka: {1}\\n\\nProgram bude spuštěn.",
        "error_title": "Chyba",
        "error_msg": "Instalace selhala: {0}",
        "console_title": "🍺 SkufUp - Instalátor 🍺",
        "console_folder": "Instalační složka:",
        "console_press": "Stiskněte Enter pro instalaci...",
        "console_shortcut": "🖥️ Vytváření zástupce na ploše...",
        "console_shortcut_done": "   ✅ Zástupce vytvořen",
        "console_autostart": "🚀 Přidávání do autostartu...",
        "console_autostart_done": "   ✅ Přidáno do autostartu",
        "console_done": "✅ Instalace dokončena!",
        "console_run": "Spustit SkufUp nyní? (Y/N): "
    },
    "nl": {
        "title": "🍺 SkufUp",
        "subtitle": "Bier openen geluid detector",
        "language": "Taal:",
        "desktop_shortcut": "Snelkoppeling op bureaublad maken",
        "autostart": "Starten bij Windows opstarten",
        "run_after": "Uitvoeren na installatie",
        "folder": "Map:",
        "install": "  🚀  INSTALLEREN  ",
        "installing": "Installeren...",
        "success_title": "Succes!",
        "success_msg": "✅ {0} succesvol geïnstalleerd!\\n\\nMap: {1}\\n\\nHet programma wordt gestart.",
        "error_title": "Fout",
        "error_msg": "Installatie mislukt: {0}",
        "console_title": "🍺 SkufUp - Installatie 🍺",
        "console_folder": "Installatiemap:",
        "console_press": "Druk op Enter om te installeren...",
        "console_shortcut": "🖥️ Snelkoppeling maken...",
        "console_shortcut_done": "   ✅ Snelkoppeling gemaakt",
        "console_autostart": "🚀 Toevoegen aan opstarten...",
        "console_autostart_done": "   ✅ Toegevoegd aan opstarten",
        "console_done": "✅ Installatie voltooid!",
        "console_run": "SkufUp nu starten? (Y/N): "
    }
}

# Текущий язык
current_lang = "en"

def t(key):
    """Получить перевод"""
    return INSTALLER_TRANSLATIONS.get(current_lang, INSTALLER_TRANSLATIONS["en"]).get(key, key)

def save_language_setting(install_dir, lang):
    """Сохраняет выбранный язык в user_settings.json"""
    settings_path = os.path.join(install_dir, "user_settings.json")
    settings = {}
    
    # Читаем существующие настройки
    if os.path.exists(settings_path):
        try:
            with open(settings_path, 'r', encoding='utf-8') as f:
                settings = json.load(f)
        except:
            pass
    
    # Обновляем язык
    settings['language'] = lang
    
    # Сохраняем
    try:
        with open(settings_path, 'w', encoding='utf-8') as f:
            json.dump(settings, f, ensure_ascii=False, indent=4)
        return True
    except:
        return False

def is_admin():
    """Проверка прав администратора"""
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def get_install_dir():
    """Папка установки"""
    return os.path.join(os.environ.get('LOCALAPPDATA', ''), APP_NAME)

def get_desktop_path():
    """Путь к рабочему столу (с поддержкой OneDrive)"""
    import subprocess
    try:
        # Получаем реальный путь к рабочему столу через PowerShell
        result = subprocess.run(
            ['powershell', '-Command', "[Environment]::GetFolderPath('Desktop')"],
            capture_output=True, text=True
        )
        if result.returncode == 0 and result.stdout.strip():
            return result.stdout.strip()
    except:
        pass
    # Fallback
    return os.path.join(os.environ.get('USERPROFILE', ''), 'Desktop')

def extract_exe(install_dir):
    """Распаковка exe файла"""
    print("📦 Распаковка файлов...")
    
    if not os.path.exists(install_dir):
        os.makedirs(install_dir)
    
    # Декодируем и распаковываем
    compressed = base64.b64decode(APP_DATA)
    exe_data = zlib.decompress(compressed)
    
    exe_path = os.path.join(install_dir, APP_EXE)
    with open(exe_path, 'wb') as f:
        f.write(exe_data)
    
    # Сохраняем иконку
    if ICO_DATA:
        try:
            ico_path = os.path.join(install_dir, "beer.ico")
            ico_data = base64.b64decode(ICO_DATA)
            with open(ico_path, 'wb') as f:
                f.write(ico_data)
        except:
            pass
    
    print(f"   ✅ Установлено в: {install_dir}")
    return exe_path

def create_shortcut(exe_path, shortcut_path, description=""):
    """Создание ярлыка"""
    try:
        import subprocess
        # Экранируем пути для PowerShell
        exe_escaped = exe_path.replace("'", "''")
        shortcut_escaped = shortcut_path.replace("'", "''")
        workdir_escaped = os.path.dirname(exe_path).replace("'", "''")
        
        ps_script = f"$WshShell = New-Object -comObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('{shortcut_escaped}'); $Shortcut.TargetPath = '{exe_escaped}'; $Shortcut.WorkingDirectory = '{workdir_escaped}'; $Shortcut.Save()"
        
        result = subprocess.run(['powershell', '-ExecutionPolicy', 'Bypass', '-Command', ps_script], 
                      capture_output=True, text=True)
        if result.returncode == 0:
            return True
        else:
            print(f"   ⚠️ PowerShell ошибка: {result.stderr}")
            return False
    except Exception as e:
        print(f"   ⚠️ Не удалось создать ярлык: {e}")
        return False

def add_to_autostart(exe_path):
    """Добавление в автозагрузку"""
    try:
        key = winreg.OpenKey(
            winreg.HKEY_CURRENT_USER,
            r"Software\\Microsoft\\Windows\\CurrentVersion\\Run",
            0, winreg.KEY_SET_VALUE
        )
        winreg.SetValueEx(key, APP_NAME, 0, winreg.REG_SZ, f'"{exe_path}" --silent')
        winreg.CloseKey(key)
        return True
    except Exception as e:
        print(f"   ⚠️ Не удалось добавить в автозагрузку: {e}")
        return False

def show_gui_installer():
    """GUI установщик"""
    global current_lang
    try:
        import tkinter as tk
        from tkinter import ttk, messagebox
    except ImportError:
        return False
    
    def update_ui_texts():
        """Обновить все тексты интерфейса"""
        root.title(f"{APP_NAME} - {t('install').strip()}")
        lbl_subtitle.config(text=t('subtitle'))
        lbl_lang.config(text=t('language'))
        chk_desktop.config(text=t('desktop_shortcut'))
        chk_autostart.config(text=t('autostart'))
        chk_run.config(text=t('run_after'))
        lbl_folder.config(text=f"{t('folder')} {get_install_dir()}")
        btn_install.config(text=t('install'))
    
    def on_language_change(event=None):
        """При смене языка"""
        global current_lang
        selected = lang_combo.get()
        for code, name in LANGUAGES.items():
            if name == selected:
                current_lang = code
                break
        update_ui_texts()
    
    def install():
        btn_install.config(state='disabled', text=t('installing'))
        root.update()
        
        try:
            install_dir = get_install_dir()
            exe_path = extract_exe(install_dir)
            
            # Сохраняем выбранный язык
            save_language_setting(install_dir, current_lang)
            
            # Ярлык на рабочий стол
            if var_desktop.get():
                desktop = get_desktop_path()
                shortcut_path = os.path.join(desktop, f"{APP_NAME}.lnk")
                create_shortcut(exe_path, shortcut_path, t('subtitle'))
            
            # Автозагрузка
            if var_autostart.get():
                add_to_autostart(exe_path)
            
            messagebox.showinfo(t('success_title'), 
                t('success_msg').format(APP_NAME, install_dir))
            
            # Запускаем
            if var_run.get():
                os.startfile(exe_path)
            
            root.destroy()
            
        except Exception as e:
            messagebox.showerror(t('error_title'), t('error_msg').format(e))
            btn_install.config(state='normal', text=t('install'))
    
    # Создаём окно
    root = tk.Tk()
    root.title(f"{APP_NAME} - Installer")
    root.geometry("450x430")
    root.resizable(False, False)
    root.configure(bg="#1a1a2e")
    
    # Центрируем окно
    root.update_idletasks()
    x = (root.winfo_screenwidth() - 450) // 2
    y = (root.winfo_screenheight() - 430) // 2
    root.geometry(f"+{x}+{y}")
    
    # Заголовок
    tk.Label(
        root,
        text="🍺 SkufUp",
        font=("Segoe UI", 24, "bold"),
        fg="#eab308",
        bg="#1a1a2e"
    ).pack(pady=20)
    
    lbl_subtitle = tk.Label(
        root,
        text=t('subtitle'),
        font=("Segoe UI", 10),
        fg="#888888",
        bg="#1a1a2e"
    )
    lbl_subtitle.pack()
    
    # Выбор языка
    lang_frame = tk.Frame(root, bg="#1a1a2e")
    lang_frame.pack(pady=15)
    
    lbl_lang = tk.Label(
        lang_frame,
        text=t('language'),
        font=("Segoe UI", 10),
        fg="#ffffff",
        bg="#1a1a2e"
    )
    lbl_lang.pack(side=tk.LEFT, padx=5)
    
    lang_combo = ttk.Combobox(
        lang_frame,
        values=list(LANGUAGES.values()),
        state="readonly",
        width=15,
        font=("Segoe UI", 10)
    )
    lang_combo.set(LANGUAGES.get(current_lang, "English"))
    lang_combo.pack(side=tk.LEFT, padx=5)
    lang_combo.bind("<<ComboboxSelected>>", on_language_change)
    
    # Опции
    options_frame = tk.Frame(root, bg="#1a1a2e")
    options_frame.pack(pady=15)
    
    var_desktop = tk.BooleanVar(value=True)
    var_autostart = tk.BooleanVar(value=True)
    var_run = tk.BooleanVar(value=True)
    
    chk_desktop = tk.Checkbutton(
        options_frame,
        text=t('desktop_shortcut'),
        variable=var_desktop,
        font=("Segoe UI", 10),
        fg="#ffffff",
        bg="#1a1a2e",
        selectcolor="#252547",
        activebackground="#1a1a2e"
    )
    chk_desktop.pack(anchor='w', pady=3)
    
    chk_autostart = tk.Checkbutton(
        options_frame,
        text=t('autostart'),
        variable=var_autostart,
        font=("Segoe UI", 10),
        fg="#ffffff",
        bg="#1a1a2e",
        selectcolor="#252547",
        activebackground="#1a1a2e"
    )
    chk_autostart.pack(anchor='w', pady=3)
    
    chk_run = tk.Checkbutton(
        options_frame,
        text=t('run_after'),
        variable=var_run,
        font=("Segoe UI", 10),
        fg="#ffffff",
        bg="#1a1a2e",
        selectcolor="#252547",
        activebackground="#1a1a2e"
    )
    chk_run.pack(anchor='w', pady=3)
    
    # Путь установки
    lbl_folder = tk.Label(
        root,
        text=f"{t('folder')} {get_install_dir()}",
        font=("Segoe UI", 8),
        fg="#666666",
        bg="#1a1a2e"
    )
    lbl_folder.pack(pady=10)
    
    # Кнопка установки
    btn_install = tk.Button(
        root,
        text=t('install'),
        font=("Segoe UI", 14, "bold"),
        fg="#ffffff",
        bg="#16a34a",
        activebackground="#15803d",
        padx=40,
        pady=15,
        relief=tk.FLAT,
        cursor="hand2",
        command=install
    )
    btn_install.pack(pady=20)
    
    root.mainloop()
    return True

def console_installer():
    """Консольный установщик"""
    global current_lang
    print()
    print("╔══════════════════════════════════════╗")
    print("║     🍺 SkufUp - Installer 🍺         ║")
    print("╚══════════════════════════════════════╝")
    print()
    
    # Выбор языка
    print("Select language / Выберите язык:")
    print()
    lang_list = list(LANGUAGES.items())
    for i, (code, name) in enumerate(lang_list, 1):
        print(f"  {i}. {name}")
    print()
    
    while True:
        try:
            choice = input("Enter number (1-8) [1]: ").strip()
            if choice == "":
                choice = "1"
            idx = int(choice) - 1
            if 0 <= idx < len(lang_list):
                current_lang = lang_list[idx][0]
                break
        except ValueError:
            pass
        print("Invalid choice, try again.")
    
    print()
    print("╔══════════════════════════════════════╗")
    print(f"║     {t('console_title')}        ║")
    print("╚══════════════════════════════════════╝")
    print()
    
    install_dir = get_install_dir()
    print(f"{t('console_folder')} {install_dir}")
    print()
    
    input(t('console_press'))
    print()
    
    # Установка
    exe_path = extract_exe(install_dir)
    
    # Сохраняем выбранный язык
    save_language_setting(install_dir, current_lang)
    
    # Ярлык
    print(t('console_shortcut'))
    desktop = get_desktop_path()
    shortcut_path = os.path.join(desktop, f"{APP_NAME}.lnk")
    create_shortcut(exe_path, shortcut_path, t('subtitle'))
    print(t('console_shortcut_done'))
    
    # Автозагрузка
    print(t('console_autostart'))
    add_to_autostart(exe_path)
    print(t('console_autostart_done'))
    
    print()
    print("╔══════════════════════════════════════╗")
    print(f"║     {t('console_done')}          ║")
    print("╚══════════════════════════════════════╝")
    print()
    
    run = input(t('console_run'))
    if run.lower() in ['y', 'д', 'yes', 'да']:
        os.startfile(exe_path)

def main():
    print("🍺 SkufUp Installer")
    print()
    
    # Пробуем GUI
    if not show_gui_installer():
        # Если GUI не удался - консольный режим
        console_installer()

if __name__ == "__main__":
    main()
'''
    
    output_path = os.path.join(os.path.dirname(__file__), "SkufUp_Installer.py")
    
    print("💾 Сохраняю установщик...")
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(installer_code)
    
    print(f"   Размер: {os.path.getsize(output_path) / 1024 / 1024:.2f} МБ")
    print()
    print(f"✅ Готово! Создан файл: {output_path}")
    print()
    print("Теперь можно:")
    print("1. Запустить SkufUp_Installer.py напрямую (если есть Python)")
    print("2. Скомпилировать в exe:")
    print("   pyinstaller --onefile --windowed --name=SkufUp_Setup SkufUp_Installer.py")
    
    return True

if __name__ == "__main__":
    create_installer()
