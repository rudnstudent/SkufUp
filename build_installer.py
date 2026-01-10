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

# Встроенные данные приложения (сжатый exe)
APP_DATA = """''' + encoded + '''"""

# Иконка приложения
ICO_DATA = """''' + ico_encoded + '''"""

APP_NAME = "SkufUp"
APP_EXE = "SkufUp.exe"

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
    try:
        import tkinter as tk
        from tkinter import messagebox
    except ImportError:
        return False
    
    def install():
        btn_install.config(state='disabled', text='Установка...')
        root.update()
        
        try:
            install_dir = get_install_dir()
            exe_path = extract_exe(install_dir)
            
            # Ярлык на рабочий стол
            if var_desktop.get():
                desktop = get_desktop_path()
                shortcut_path = os.path.join(desktop, f"{APP_NAME}.lnk")
                create_shortcut(exe_path, shortcut_path, "SkufUp - Детектор звука пива")
            
            # Автозагрузка
            if var_autostart.get():
                add_to_autostart(exe_path)
            
            messagebox.showinfo("Успех!", 
                f"✅ {APP_NAME} успешно установлен!\\n\\n"
                f"Папка: {install_dir}\\n\\n"
                "Программа будет запущена.")
            
            # Запускаем
            if var_run.get():
                os.startfile(exe_path)
            
            root.destroy()
            
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось установить: {e}")
            btn_install.config(state='normal', text='Установить')
    
    # Создаём окно
    root = tk.Tk()
    root.title(f"{APP_NAME} - Установщик")
    root.geometry("450x380")
    root.resizable(False, False)
    root.configure(bg="#1a1a2e")
    
    # Центрируем окно
    root.update_idletasks()
    x = (root.winfo_screenwidth() - 450) // 2
    y = (root.winfo_screenheight() - 380) // 2
    root.geometry(f"+{x}+{y}")
    
    # Заголовок
    tk.Label(
        root,
        text="🍺 SkufUp",
        font=("Segoe UI", 24, "bold"),
        fg="#eab308",
        bg="#1a1a2e"
    ).pack(pady=20)
    
    tk.Label(
        root,
        text="Детектор звука открытия пива",
        font=("Segoe UI", 10),
        fg="#888888",
        bg="#1a1a2e"
    ).pack()
    
    # Опции
    options_frame = tk.Frame(root, bg="#1a1a2e")
    options_frame.pack(pady=20)
    
    var_desktop = tk.BooleanVar(value=True)
    var_autostart = tk.BooleanVar(value=True)
    var_run = tk.BooleanVar(value=True)
    
    tk.Checkbutton(
        options_frame,
        text="Создать ярлык на рабочем столе",
        variable=var_desktop,
        font=("Segoe UI", 10),
        fg="#ffffff",
        bg="#1a1a2e",
        selectcolor="#252547",
        activebackground="#1a1a2e"
    ).pack(anchor='w', pady=3)
    
    tk.Checkbutton(
        options_frame,
        text="Запускать при старте Windows",
        variable=var_autostart,
        font=("Segoe UI", 10),
        fg="#ffffff",
        bg="#1a1a2e",
        selectcolor="#252547",
        activebackground="#1a1a2e"
    ).pack(anchor='w', pady=3)
    
    tk.Checkbutton(
        options_frame,
        text="Запустить после установки",
        variable=var_run,
        font=("Segoe UI", 10),
        fg="#ffffff",
        bg="#1a1a2e",
        selectcolor="#252547",
        activebackground="#1a1a2e"
    ).pack(anchor='w', pady=3)
    
    # Путь установки
    tk.Label(
        root,
        text=f"Папка: {get_install_dir()}",
        font=("Segoe UI", 8),
        fg="#666666",
        bg="#1a1a2e"
    ).pack(pady=10)
    
    # Кнопка установки
    btn_install = tk.Button(
        root,
        text="  🚀  УСТАНОВИТЬ  ",
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
    print()
    print("╔══════════════════════════════════════╗")
    print("║     🍺 SkufUp - Установщик 🍺        ║")
    print("╚══════════════════════════════════════╝")
    print()
    
    install_dir = get_install_dir()
    print(f"Папка установки: {install_dir}")
    print()
    
    input("Нажмите Enter для установки...")
    print()
    
    # Установка
    exe_path = extract_exe(install_dir)
    
    # Ярлык
    print("🖥️ Создание ярлыка на рабочем столе...")
    desktop = get_desktop_path()
    shortcut_path = os.path.join(desktop, f"{APP_NAME}.lnk")
    create_shortcut(exe_path, shortcut_path, "SkufUp - Детектор звука пива")
    print("   ✅ Ярлык создан")
    
    # Автозагрузка
    print("🚀 Добавление в автозагрузку...")
    add_to_autostart(exe_path)
    print("   ✅ Добавлено в автозагрузку")
    
    print()
    print("╔══════════════════════════════════════╗")
    print("║     ✅ Установка завершена!          ║")
    print("╚══════════════════════════════════════╝")
    print()
    
    run = input("Запустить SkufUp сейчас? (Y/N): ")
    if run.lower() == 'y':
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
