"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                         SkufUp - Beer Detector 🍺                            ║
║                                                                              ║
║  The app listens to the microphone and waits for beer can opening sound.    ║
║  When it hears the characteristic "pshhh" - launches a game or website.     ║
║                                                                              ║
║  How it works:                                                               ║
║  1. Microphone continuously records sound                                    ║
║  2. Each loud sound is compared with reference "pshhh" template             ║
║  3. If similarity is above 55% - it's beer! Launch the game!                ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""

# ============================================================================
# LIBRARY IMPORTS
# ============================================================================

import tkinter as tk                    # GUI (windows, buttons)
from tkinter import ttk, filedialog, messagebox
import threading                        # Multithreading (listen in background)
import os                               # File and path operations
import sys                              # System functions
import json                             # Save settings to file
import webbrowser                       # Open websites in browser
import subprocess                       # Launch programs (games)
import winreg                           # Windows registry (for autostart)
import ctypes                           # Windows API (for single instance check)

# Localization support
from localization import t, set_language, get_current_language, get_localization


# ============================================================================
# SINGLE INSTANCE PROTECTION
# ============================================================================

def check_single_instance():
    """
    Проверяет, что программа ещё не запущена.
    
    Зачем это нужно:
    - Если запустить программу дважды, будут два микрофона слушать одновременно
    - Это вызовет конфликты и двойные срабатывания
    
    Как работает:
    - Создаём "мьютекс" (mutex) - специальный флаг в Windows
    - Если флаг уже занят - значит программа уже запущена
    
    Возвращает:
        True  - можно запускать (первый экземпляр)
        False - уже запущено (второй экземпляр - нужно закрыться)
    """
    mutex_name = "SkufUp_SingleInstance_Mutex"  # Уникальное имя нашей программы
    
    kernel32 = ctypes.windll.kernel32
    mutex = kernel32.CreateMutexW(None, False, mutex_name)
    last_error = kernel32.GetLastError()
    
    # Код 183 означает "мьютекс уже существует" = программа уже запущена
    if last_error == 183:  # ERROR_ALREADY_EXISTS
        return False
    return True


# ============================================================================
# РАБОТА С НАСТРОЙКАМИ
# ============================================================================

def get_app_path():
    """
    Получить папку, где лежит программа.
    
    Почему это сложно:
    - Если запущен .py файл - это одна папка
    - Если запущен .exe файл - это другая папка
    
    PyInstaller (который делает .exe) меняет пути, поэтому нужна проверка.
    """
    if getattr(sys, 'frozen', False):
        # Запущен как .exe (скомпилированный PyInstaller)
        return os.path.dirname(sys.executable)
    # Запущен как .py файл (через Python)
    return os.path.dirname(os.path.abspath(__file__))


# Путь к файлу с настройками пользователя
SETTINGS_FILE = os.path.join(get_app_path(), "user_settings.json")

# Имя программы (используется для автозагрузки)
APP_NAME = "SkufUp"


def load_settings():
    """
    Загрузить настройки из файла.
    
    Настройки хранятся в JSON формате (это как текстовый файл, но структурированный).
    
    Пример содержимого user_settings.json:
    {
        "target_type": "game",
        "target_path": "C:/Games/cs2.exe",
        "minimize_on_start": true
    }
    
    Возвращает:
        dict - словарь с настройками
        {} - пустой словарь, если файла нет или он повреждён
    """
    if os.path.exists(SETTINGS_FILE):
        try:
            with open(SETTINGS_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            # Файл повреждён - вернём пустые настройки
            pass
    return {}


def save_settings(settings):
    """
    Сохранить настройки в файл.
    
    Аргументы:
        settings: словарь с настройками для сохранения
    
    Возвращает:
        True  - успешно сохранено
        False - ошибка (нет прав, диск переполнен и т.д.)
    """
    try:
        # Создаём папку, если её нет
        settings_dir = os.path.dirname(SETTINGS_FILE)
        if settings_dir and not os.path.exists(settings_dir):
            os.makedirs(settings_dir)
        
        # Записываем в файл (красиво отформатировано с отступами)
        with open(SETTINGS_FILE, 'w', encoding='utf-8') as f:
            json.dump(settings, f, ensure_ascii=False, indent=2)
        return True
    except Exception as e:
        print(f"Ошибка сохранения: {e}")
        return False


# ============================================================================
# ГЛАВНЫЙ КЛАСС ПРИЛОЖЕНИЯ
# ============================================================================

class SkufUpApp:
    """
    Главный класс программы SkufUp.
    
    Что он делает:
    1. Создаёт окно с кнопками
    2. Позволяет выбрать игру или сайт
    3. Слушает микрофон в фоне
    4. Запускает игру/сайт когда слышит пиво
    
    Атрибуты:
        root           - главное окно программы
        is_listening   - сейчас слушаем микрофон? (True/False)
        settings       - текущие настройки пользователя
        last_launch_time - когда последний раз запускали игру (для cooldown)
    """
    
    def __init__(self):
        """
        Constructor - called when the application is created.
        Here we set up the window and load settings.
        """
        
        # ===== LOAD SETTINGS AND LANGUAGE =====
        self.settings = load_settings()     # Load saved settings
        
        # Set language from settings (default: English)
        saved_lang = self.settings.get("language", "en")
        set_language(saved_lang)
        
        # ===== CREATE WINDOW =====
        self.root = tk.Tk()
        self.root.title(t("window_title"))
        self.root.geometry("520x700")           # Window size
        self.root.resizable(False, False)       # Fixed size
        self.root.configure(bg="#1a1a2e")       # Dark background
        
        # ===== WINDOW ICON =====
        try:
            icon_path = os.path.join(get_app_path(), "beer.ico")
            if os.path.exists(icon_path):
                self.root.iconbitmap(icon_path)
        except:
            pass  # It's ok if no icon
        
        # ===== STATE VARIABLES =====
        self.is_listening = False           # Currently listening? (no)
        self.stop_flag = threading.Event()  # Flag to stop the thread
        self.last_launch_time = 0           # Last launch time (for 1 hour cooldown)
        
        # ===== СОЗДАЁМ ИНТЕРФЕЙС =====
        self.create_widgets()
        
        # ===== АВТОЗАПУСК ПРОСЛУШИВАНИЯ =====
        # Если уже есть настройки - сразу начинаем слушать
        if self.settings.get("target_path"):
            self.root.after(500, self.start_listening)  # Через 0.5 сек
        
        # ===== ОБРАБОТКА ЗАКРЫТИЯ ОКНА =====
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
    
    
    # ========================================================================
    # СОЗДАНИЕ ИНТЕРФЕЙСА (ВСЕ КНОПКИ И НАДПИСИ)
    # ========================================================================
    
    def create_widgets(self):
        """
        Создание всех элементов интерфейса.
        
        Структура окна:
        ┌─────────────────────────────────┐
        │         🍺 SkufUp               │  <- Заголовок
        │    Детектор звука открытия      │
        │                                 │
        │      ● Не активен               │  <- Статус (меняет цвет)
        │                                 │
        │  ┌─────────────────────────┐    │
        │  │ Что открывать:          │    │  <- Блок выбора
        │  │ [Игра] [Сайт]           │    │
        │  │                         │    │
        │  │ Текущий выбор: CS2      │    │
        │  └─────────────────────────┘    │
        │                                 │
        │     [     ▶ СТАРТ     ]         │  <- Большая кнопка
        │                                 │
        │  ☐ Запускать при старте Windows │
        │  ☐ Сворачивать при запуске      │
        │                                 │
        │        [Свернуть]               │
        └─────────────────────────────────┘
        """
        
        # ----- HEADER -----
        title = tk.Label(
            self.root,
            text=t("title"),
            font=("Segoe UI", 28, "bold"),
            fg="#eab308",   # Yellow (beer color!)
            bg="#1a1a2e"
        )
        title.pack(pady=(20, 5))
        
        # Subtitle
        self.subtitle_label = tk.Label(
            self.root,
            text=t("subtitle"),
            font=("Segoe UI", 11),
            fg="#888888",
            bg="#1a1a2e"
        )
        self.subtitle_label.pack()
        
        # ----- LANGUAGE SELECTOR -----
        lang_frame = tk.Frame(self.root, bg="#1a1a2e")
        lang_frame.pack(pady=5)
        
        tk.Label(
            lang_frame,
            text="🌐",
            font=("Segoe UI", 12),
            fg="#888888",
            bg="#1a1a2e"
        ).pack(side=tk.LEFT, padx=5)
        
        # Language options
        self.languages = {
            "en": "English",
            "ru": "Русский", 
            "de": "Deutsch",
            "es": "Español",
            "fr": "Français",
            "zh": "中文",
            "cs": "Čeština",
            "nl": "Nederlands"
        }
        
        self.lang_var = tk.StringVar(value=self.languages.get(get_current_language(), "English"))
        
        self.lang_combo = ttk.Combobox(
            lang_frame,
            textvariable=self.lang_var,
            values=list(self.languages.values()),
            state="readonly",
            width=12,
            font=("Segoe UI", 10)
        )
        self.lang_combo.pack(side=tk.LEFT, padx=5)
        self.lang_combo.bind("<<ComboboxSelected>>", self.change_language)
        
        # ----- STATUS INDICATOR -----
        # Shows current state: listening / not listening / beer!
        status_frame = tk.Frame(self.root, bg="#1a1a2e")
        status_frame.pack(pady=15)
        
        # Colored circle (changes color based on status)
        self.status_indicator = tk.Label(
            status_frame,
            text="●",
            font=("Segoe UI", 24),
            fg="#666666",   # Gray = not active
            bg="#1a1a2e"
        )
        self.status_indicator.pack(side=tk.LEFT, padx=5)
        
        # Status text
        self.status_label = tk.Label(
            status_frame,
            text=t("status_inactive"),
            font=("Segoe UI", 14),
            fg="#888888",
            bg="#1a1a2e"
        )
        self.status_label.pack(side=tk.LEFT)
        
        # ----- TARGET SELECTION BLOCK -----
        # Here user selects game or website
        target_frame = tk.Frame(self.root, bg="#252547", padx=20, pady=15)
        target_frame.pack(pady=10, padx=20, fill=tk.X)
        
        self.target_label = tk.Label(
            target_frame,
            text=t("target_label"),
            font=("Segoe UI", 11, "bold"),
            fg="#ffffff",
            bg="#252547"
        )
        self.target_label.pack(anchor=tk.W)
        
        # "Select game" and "Enter website" buttons
        btn_type_frame = tk.Frame(target_frame, bg="#252547")
        btn_type_frame.pack(fill=tk.X, pady=10)
        
        # Game selection button (blue)
        self.btn_game = tk.Button(
            btn_type_frame,
            text=t("btn_select_game"),
            font=("Segoe UI", 11),
            fg="#ffffff",
            bg="#3b82f6",
            activebackground="#2563eb",
            activeforeground="#ffffff",
            relief=tk.FLAT,
            cursor="hand2",
            padx=15,
            pady=8,
            command=self.select_game
        )
        self.btn_game.pack(side=tk.LEFT, padx=(0, 10))
        
        # Website selection button (purple)
        self.btn_website = tk.Button(
            btn_type_frame,
            text=t("btn_select_website"),
            font=("Segoe UI", 11),
            fg="#ffffff",
            bg="#8b5cf6",
            activebackground="#7c3aed",
            activeforeground="#ffffff",
            relief=tk.FLAT,
            cursor="hand2",
            padx=15,
            pady=8,
            command=self.show_website_input
        )
        self.btn_website.pack(side=tk.LEFT)
        
        # ----- WEBSITE INPUT FIELD -----
        # Shown when user clicks "Enter website"
        self.website_frame = tk.Frame(target_frame, bg="#252547")
        
        self.url_hint_label = tk.Label(
            self.website_frame,
            text=t("url_hint"),
            font=("Segoe UI", 9),
            fg="#888888",
            bg="#252547"
        )
        self.url_hint_label.pack(anchor=tk.W)
        
        # URL input field
        self.url_entry = tk.Entry(
            self.website_frame,
            font=("Segoe UI", 12),
            bg="#1a1a2e",
            fg="#ffffff",
            insertbackground="#ffffff",
            relief=tk.FLAT,
            width=40
        )
        self.url_entry.pack(fill=tk.X, pady=5, ipady=8)
        
        # Key bindings
        self.url_entry.bind('<Return>', self.save_website)      # Enter
        self.url_entry.bind('<KP_Enter>', self.save_website)    # Numpad Enter
        self.url_entry.bind('<Control-v>', self.paste_url)      # Ctrl+V
        self.url_entry.bind('<Control-V>', self.paste_url)      # Ctrl+V (capital V)
        self.url_entry.bind('<Button-3>', self.show_context_menu)  # Right mouse button
        
        # Save website button
        self.save_url_btn = tk.Button(
            self.website_frame,
            text=t("btn_save_url"),
            font=("Segoe UI", 10),
            fg="#ffffff",
            bg="#22c55e",   # Green
            activebackground="#16a34a",
            relief=tk.FLAT,
            cursor="hand2",
            command=self.save_website
        )
        self.save_url_btn.pack(anchor=tk.W, pady=(5, 0))
        
        # ----- CONTEXT MENU -----
        # Appears on right click in input field
        self.context_menu = tk.Menu(self.root, tearoff=0, bg="#252547", fg="#ffffff")
        self.context_menu.add_command(label=t("menu_paste"), command=self.paste_url_from_menu)
        self.context_menu.add_command(label=t("menu_clear"), command=lambda: self.url_entry.delete(0, tk.END))
        
        # ----- CURRENT TARGET DISPLAY -----
        # Shows what is currently selected (game or website)
        self.current_target_frame = tk.Frame(target_frame, bg="#1a1a2e", padx=10, pady=10)
        
        # Target type (🎮 Game: or 🌐 Website:)
        self.target_type_label = tk.Label(
            self.current_target_frame,
            text="",
            font=("Segoe UI", 10),
            fg="#888888",
            bg="#1a1a2e"
        )
        self.target_type_label.pack(anchor=tk.W)
        
        # Path to game or website URL
        self.target_path_label = tk.Label(
            self.current_target_frame,
            text="",
            font=("Segoe UI", 11, "bold"),
            fg="#22c55e",
            bg="#1a1a2e",
            wraplength=420  # Wrap long strings
        )
        self.target_path_label.pack(anchor=tk.W)
        
        # "Change" button
        self.btn_change = tk.Button(
            self.current_target_frame,
            text=t("btn_change"),
            font=("Segoe UI", 9),
            fg="#888888",
            bg="#333355",
            activebackground="#444466",
            relief=tk.FLAT,
            cursor="hand2",
            command=self.clear_target
        )
        self.btn_change.pack(anchor=tk.W, pady=(5, 0))
        
        # Update display (shows current target or hides the block)
        self.update_target_display()
        
        # ----- BIG START/STOP BUTTON -----
        self.toggle_btn = tk.Button(
            self.root,
            text=t("btn_start"),
            font=("Segoe UI", 24, "bold"),
            fg="#ffffff",
            bg="#16a34a",   # Green
            activebackground="#15803d",
            activeforeground="#ffffff",
            width=20,
            height=2,
            relief=tk.FLAT,
            cursor="hand2",
            command=self.toggle_listening
        )
        self.toggle_btn.pack(pady=30, padx=30, fill=tk.X)
        
        # ----- "AUTOSTART" CHECKBOX -----
        self.autostart_var = tk.BooleanVar(value=self.is_autostart_enabled())
        self.autostart_cb = tk.Checkbutton(
            self.root,
            text=t("autostart_label"),
            variable=self.autostart_var,
            font=("Segoe UI", 10),
            fg="#888888",
            bg="#1a1a2e",
            selectcolor="#252547",
            activebackground="#1a1a2e",
            command=self.toggle_autostart
        )
        self.autostart_cb.pack(padx=30)
        
        # ----- "MINIMIZE ON START" CHECKBOX -----
        self.minimize_var = tk.BooleanVar(value=self.settings.get("minimize_on_start", False))
        self.minimize_cb = tk.Checkbutton(
            self.root,
            text=t("minimize_label"),
            variable=self.minimize_var,
            font=("Segoe UI", 10),
            fg="#888888",
            bg="#1a1a2e",
            selectcolor="#252547",
            activebackground="#1a1a2e",
            command=self.toggle_minimize_on_start
        )
        self.minimize_cb.pack(padx=30)
        
        # ----- "MINIMIZE" BUTTON -----
        self.minimize_btn = tk.Button(
            self.root,
            text=t("btn_minimize"),
            font=("Segoe UI", 9),
            fg="#666666",
            bg="#252547",
            activebackground="#333355",
            relief=tk.FLAT,
            cursor="hand2",
            command=self.root.iconify  # Minimize window
        )
        self.minimize_btn.pack(pady=10)
    
    
    # ========================================================================
    # METHODS FOR WORKING WITH TARGET (GAME OR WEBSITE)
    # ========================================================================
    
    def change_language(self, event=None):
        """
        Change application language and refresh UI.
        """
        # Get language code from display name
        selected_name = self.lang_var.get()
        new_lang = "en"
        for code, name in self.languages.items():
            if name == selected_name:
                new_lang = code
                break
        
        set_language(new_lang)
        
        # Save language to settings
        self.settings["language"] = new_lang
        save_settings(self.settings)
        
        # Update all UI texts
        self.root.title(t("window_title"))
        self.subtitle_label.config(text=t("subtitle"))
        self.status_label.config(text=t("status_inactive") if not self.is_listening else t("status_listening"))
        self.target_label.config(text=t("target_label"))
        self.btn_game.config(text=t("btn_select_game"))
        self.btn_website.config(text=t("btn_select_website"))
        self.url_hint_label.config(text=t("url_hint"))
        self.save_url_btn.config(text=t("btn_save_url"))
        self.btn_change.config(text=t("btn_change"))
        self.toggle_btn.config(text=t("btn_stop") if self.is_listening else t("btn_start"))
        self.autostart_cb.config(text=t("autostart_label"))
        self.minimize_cb.config(text=t("minimize_label"))
        self.minimize_btn.config(text=t("btn_minimize"))
        
        # Update context menu
        self.context_menu.entryconfig(0, label=t("menu_paste"))
        self.context_menu.entryconfig(1, label=t("menu_clear"))
        
        # Update target display
        self.update_target_display()
    
    def update_target_display(self):
        """
                Update current target display.
        
        If target is selected - show it.
        If not selected - hide the block.
        """
        target_type = self.settings.get("target_type", "")
        target_path = self.settings.get("target_path", "")
        
        if target_path:
            # Target exists - show it
            self.current_target_frame.pack(fill=tk.X, pady=(10, 0))
            self.website_frame.pack_forget()  # Hide website input field
            
            if target_type == "game":
                self.target_type_label.config(text=t("target_type_game"))
                # Show only filename, not full path
                self.target_path_label.config(text=os.path.basename(target_path))
            else:
                self.target_type_label.config(text=t("target_type_website"))
                self.target_path_label.config(text=target_path)
        else:
            # No target - hide both blocks
            self.current_target_frame.pack_forget()
            self.website_frame.pack_forget()
    
    def select_game(self):
        """
        Open game selection dialog (.exe file).
        """
        file_path = filedialog.askopenfilename(
            title=t("dialog_select_game"),
            filetypes=[
                (t("dialog_exe_files"), "*.exe"),
                (t("dialog_all_files"), "*.*")
            ]
        )
        
        if file_path:
            # User selected a file
            self.settings["target_type"] = "game"
            self.settings["target_path"] = file_path
            
            if save_settings(self.settings):
                messagebox.showinfo(t("dialog_saved_game"), t("dialog_game_saved_msg", os.path.basename(file_path)))
                self.update_target_display()
    
    def show_website_input(self):
        """
        Show URL input field.
        """
        self.current_target_frame.pack_forget()  # Hide current target
        self.website_frame.pack(fill=tk.X, pady=(10, 0))  # Show input field
        self.url_entry.delete(0, tk.END)  # Clear field
        self.url_entry.focus_set()  # Set focus to field
    
    def save_website(self, event=None):
        """
        Save entered website.
        
        Called when Enter is pressed or "Save" button is clicked.
        """
        url = self.url_entry.get().strip()
        
        if not url:
            return  # Empty string - do nothing
        
        # Add https:// if user didn't write it
        if not url.startswith(("http://", "https://")):
            url = "https://" + url
        
        self.settings["target_type"] = "website"
        self.settings["target_path"] = url
        
        if save_settings(self.settings):
            messagebox.showinfo(t("dialog_saved_website"), t("dialog_website_saved_msg", url))
            self.update_target_display()
        else:
            messagebox.showerror(t("dialog_error"), t("dialog_save_error"))
    
    def clear_target(self):
        """
        Clear current target (for changing).
        """
        self.settings["target_type"] = ""
        self.settings["target_path"] = ""
        save_settings(self.settings)
        self.update_target_display()
    
    def paste_url(self, event=None):
        """
        Paste URL from clipboard (Ctrl+V).
        """
        try:
            clipboard = self.root.clipboard_get()
            self.url_entry.delete(0, tk.END)
            self.url_entry.insert(0, clipboard)
        except:
            pass
        return "break"  # Don't pass event further
    
    def paste_url_from_menu(self):
        """
        Paste URL from context menu.
        """
        try:
            clipboard = self.root.clipboard_get()
            self.url_entry.delete(0, tk.END)
            self.url_entry.insert(0, clipboard)
        except:
            pass
    
    def show_context_menu(self, event):
        """
        Show context menu on right click.
        """
        try:
            self.context_menu.tk_popup(event.x_root, event.y_root)
        finally:
            self.context_menu.grab_release()
    
    
    # ========================================================================
    # MICROPHONE LISTENING METHODS
    # ========================================================================
    
    def toggle_listening(self):
        """
        Toggle listening (start/stop).
        """
        if self.is_listening:
            self.stop_listening()
        else:
            self.start_listening()
    
    def start_listening(self):
        """
        Start listening to microphone.
        
        1. Check that target is selected (game or website)
        2. Change button to "STOP"
        3. Start listening thread
        """
        # Check if target exists
        if not self.settings.get("target_path"):
            messagebox.showwarning(t("dialog_warning"), t("dialog_select_target"))
            return
        
        self.is_listening = True
        self.stop_flag.clear()
        
        # Change indicator to green
        self.status_indicator.config(fg="#22c55e")
        self.status_label.config(text=t("status_listening"), fg="#22c55e")
        
        # Change button to "STOP" (red)
        self.toggle_btn.config(text=t("btn_stop"), bg="#dc2626", activebackground="#b91c1c")
        
        # Start listening in separate thread (so window doesn't freeze)
        self.listen_thread = threading.Thread(target=self.listen_loop, daemon=True)
        self.listen_thread.start()
    
    def stop_listening(self):
        """
        Stop listening to microphone.
        """
        self.is_listening = False
        self.stop_flag.set()  # Signal thread to stop
        
        # Change indicator to gray
        self.status_indicator.config(fg="#666666")
        self.status_label.config(text=t("status_stopped"), fg="#888888")
        
        # Change button to "START" (green)
        self.toggle_btn.config(text=t("btn_start"), bg="#16a34a", activebackground="#15803d")
    
    def listen_loop(self):
        """
        Главный цикл прослушивания (работает в отдельном потоке).
        
        Этот метод:
        1. Создаёт детектор звука
        2. Запускает микрофон
        3. В цикле проверяет: это звук открытия банки?
        4. Если да - вызывает on_beer_detected()
        """
        try:
            # Импортируем ML детектор (более точный!)
            # Если ML модель не найдена, используем старый детектор
            try:
                from audio_detector_ml import BeerCanDetector
                print("   ✅ Используется ML детектор")
            except ImportError:
                from audio_detector import BeerCanDetector
                print("   ⚠️ ML детектор недоступен, используется базовый")
            
            # Создаём детектор и запускаем микрофон
            detector = BeerCanDetector()
            detector.start_stream()
            
            # Бесконечный цикл (пока не нажмут СТОП)
            while not self.stop_flag.is_set():
                try:
                    # Проверяем: это пиво?
                    if detector.detect():
                        # Да! Вызываем обработчик в главном потоке
                        self.root.after(0, self.on_beer_detected)
                except:
                    continue  # Игнорируем ошибки
            
            # Останавливаем микрофон
            detector.stop_stream()
            
        except Exception as e:
            # Показываем ошибку пользователю
            self.root.after(0, lambda: messagebox.showerror("Ошибка", str(e)))
    
    def on_beer_detected(self):
        """
        Обработка обнаружения звука открытия пива.
        
        Вызывается когда детектор распознал "пшик" банки.
        """
        # Меняем индикатор на жёлтый
        self.status_indicator.config(fg="#eab308")
        self.status_label.config(text=t("status_beer"), fg="#eab308")
        
        # Запускаем игру или открываем сайт
        self.launch_target()
        
        # Через 2 секунды возвращаем статус "Слушаю..."
        self.root.after(2000, self.restore_status)
    
    def restore_status(self):
        """
        Восстановить статус "Слушаю..." после обнаружения пива.
        """
        if self.is_listening:
            self.status_indicator.config(fg="#22c55e")
            self.status_label.config(text=t("status_listening"), fg="#22c55e")
    
    def launch_target(self):
        """
        Запустить игру или открыть сайт.
        
        Для ИГРЫ: проверяем, запущена ли уже (через psutil)
        Для САЙТА: есть cooldown 1 час
        """
        import time
        
        target_type = self.settings.get("target_type")
        target_path = self.settings.get("target_path")
        current_time = time.time()
        
        # Запускаем в зависимости от типа цели
        if target_type == "game" and target_path:
            # Проверяем, запущена ли уже эта игра
            if self._is_game_running(target_path):
                print("🎮 Игра уже запущена, пропускаем")
                return
            
            try:
                # Запускаем .exe файл
                subprocess.Popen([target_path], cwd=os.path.dirname(target_path))
                print(f"🎮 Запущена игра: {os.path.basename(target_path)}")
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось запустить: {e}")
                
        elif target_type == "website" and target_path:
            # Для сайтов: проверяем cooldown 1 час
            if current_time - self.last_launch_time < 3600:
                print("🌐 Сайт: ещё не прошёл час, пропускаем")
                return
            
            # Открываем сайт в браузере
            webbrowser.open_new_tab(target_path)
            self.last_launch_time = current_time  # Запоминаем время
            print(f"🌐 Открыт сайт: {target_path}")
    
    def _is_game_running(self, game_path: str) -> bool:
        """
        Проверить, запущена ли игра.
        
        Аргументы:
            game_path: полный путь к .exe файлу игры
        
        Возвращает:
            True - игра уже запущена
            False - игра не запущена
        """
        try:
            import psutil
            game_name = os.path.basename(game_path).lower()
            
            for proc in psutil.process_iter(['name']):
                try:
                    if proc.info['name'].lower() == game_name:
                        return True
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
            return False
        except ImportError:
            # Если psutil не установлен, пропускаем проверку
            print("⚠️ psutil не установлен, проверка процессов недоступна")
            return False
    
    
    # ========================================================================
    # МЕТОДЫ АВТОЗАПУСКА WINDOWS
    # ========================================================================
    
    def is_autostart_enabled(self):
        """
        Проверить, включен ли автозапуск.
        
        Автозапуск - это запись в реестре Windows:
        HKEY_CURRENT_USER\\Software\\Microsoft\\Windows\\CurrentVersion\\Run
        
        Возвращает:
            True  - программа в автозагрузке
            False - не в автозагрузке
        """
        try:
            key = winreg.OpenKey(
                winreg.HKEY_CURRENT_USER,
                r"Software\Microsoft\Windows\CurrentVersion\Run",
                0, winreg.KEY_READ
            )
            try:
                winreg.QueryValueEx(key, APP_NAME)
                winreg.CloseKey(key)
                return True  # Есть запись = автозапуск включён
            except FileNotFoundError:
                winreg.CloseKey(key)
                return False  # Нет записи = автозапуск выключен
        except:
            return False
    
    def toggle_autostart(self):
        """
        Переключить автозапуск (вкл/выкл).
        """
        if self.autostart_var.get():
            self.enable_autostart()
        else:
            self.disable_autostart()
    
    def toggle_minimize_on_start(self):
        """
        Переключить сворачивание при запуске.
        """
        self.settings["minimize_on_start"] = self.minimize_var.get()
        save_settings(self.settings)
    
    def enable_autostart(self):
        """
        Добавить программу в автозагрузку Windows.
        """
        try:
            key = winreg.OpenKey(
                winreg.HKEY_CURRENT_USER,
                r"Software\Microsoft\Windows\CurrentVersion\Run",
                0, winreg.KEY_SET_VALUE
            )
            
            # Получаем путь к программе
            if getattr(sys, 'frozen', False):
                # Это .exe файл
                exe_path = sys.executable
            else:
                # Это .py файл (для разработки)
                exe_path = f'"{sys.executable}" "{os.path.abspath(__file__)}"'
            
            # Записываем в реестр
            winreg.SetValueEx(key, APP_NAME, 0, winreg.REG_SZ, f'"{exe_path}"')
            winreg.CloseKey(key)
            
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось добавить в автозагрузку: {e}")
            self.autostart_var.set(False)
    
    def disable_autostart(self):
        """
        Удалить программу из автозагрузки Windows.
        """
        try:
            key = winreg.OpenKey(
                winreg.HKEY_CURRENT_USER,
                r"Software\Microsoft\Windows\CurrentVersion\Run",
                0, winreg.KEY_SET_VALUE
            )
            try:
                winreg.DeleteValue(key, APP_NAME)
            except FileNotFoundError:
                pass  # Записи и так нет
            winreg.CloseKey(key)
        except:
            pass
    
    
    # ========================================================================
    # МЕТОДЫ ЗАКРЫТИЯ ПРОГРАММЫ
    # ========================================================================
    
    def on_close(self):
        """
        Обработка закрытия окна (кнопка X).
        
        Останавливаем прослушивание и закрываем окно.
        """
        self.stop_flag.set()      # Сигнал потоку остановиться
        self.is_listening = False
        self.root.destroy()       # Закрываем окно
    
    def run(self, silent=False):
        """
        Запуск программы.
        
        Аргументы:
            silent: если True - программа свернётся сразу после запуска
        """
        # Сворачиваем если нужно
        if silent or self.settings.get("minimize_on_start", False):
            self.root.after(100, self.start_listening)  # Запускаем прослушивание
            self.root.after(200, self.root.iconify)     # Сворачиваем окно
        
        # Главный цикл Tkinter (окно работает пока его не закроют)
        self.root.mainloop()


# ============================================================================
# ТОЧКА ВХОДА (ЗАПУСК ПРОГРАММЫ)
# ============================================================================

def main():
    """
    Главная функция - точка входа в программу.
    
    1. Проверяем, что программа ещё не запущена
    2. Создаём приложение
    3. Запускаем его
    """
    
    # Проверяем единственный экземпляр
    if not check_single_instance():
        # Программа уже запущена - тихо выходим
        sys.exit(0)
    
    # Проверяем аргументы командной строки
    silent_mode = "--silent" in sys.argv
    
    # Создаём и запускаем приложение
    app = SkufUpApp()
    app.run(silent=silent_mode)


# Это стандартная проверка Python:
# Код ниже выполнится только если файл запущен напрямую,
# а не импортирован как модуль
if __name__ == "__main__":
    main()
