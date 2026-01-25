"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                           SkufUp - Детектор Пива 🍺                          ║
║                                                                              ║
║  Программа слушает микрофон и ждёт звук открытия банки пива.                ║
║  Когда слышит характерный "пшик" - запускает игру или открывает сайт.       ║
║                                                                              ║
║  Как это работает:                                                           ║
║  1. Микрофон постоянно записывает звук                                       ║
║  2. Каждый громкий звук сравнивается с эталонным "пшиком" банки             ║
║  3. Если похожесть больше 55% - это пиво! Запускаем игру!                   ║
║                                                                              ║
║  Автор: Создано с помощью GitHub Copilot                                     ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""

# ============================================================================
# ИМПОРТ БИБЛИОТЕК
# ============================================================================

import tkinter as tk                    # Графический интерфейс (окна, кнопки)
from tkinter import ttk, filedialog, messagebox
import threading                        # Многопоточность (слушаем звук в фоне)
import os                               # Работа с файлами и путями
import sys                              # Системные функции
import json                             # Сохранение настроек в файл
import webbrowser                       # Открытие сайтов в браузере
import subprocess                       # Запуск программ (игр)
import winreg                           # Реестр Windows (для автозагрузки)
import ctypes                           # Windows API (для проверки одного экземпляра)


# ============================================================================
# ЗАЩИТА ОТ ПОВТОРНОГО ЗАПУСКА
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
        Конструктор - вызывается при создании программы.
        Здесь мы настраиваем окно и загружаем настройки.
        """
        
        # ===== СОЗДАНИЕ ОКНА =====
        self.root = tk.Tk()
        self.root.title("SkufUp - Детектор Пива 🍺")
        self.root.geometry("520x650")           # Размер окна
        self.root.resizable(False, False)       # Нельзя менять размер
        self.root.configure(bg="#1a1a2e")       # Тёмный фон
        
        # ===== ИКОНКА ОКНА =====
        try:
            icon_path = os.path.join(get_app_path(), "beer.ico")
            if os.path.exists(icon_path):
                self.root.iconbitmap(icon_path)
        except:
            pass  # Не страшно, если иконки нет
        
        # ===== ПЕРЕМЕННЫЕ СОСТОЯНИЯ =====
        self.is_listening = False           # Сейчас слушаем? (нет)
        self.settings = load_settings()     # Загружаем сохранённые настройки
        self.stop_flag = threading.Event()  # Флаг для остановки потока
        self.last_launch_time = 0           # Время последнего запуска (для cooldown 1 час)
        
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
        
        # ----- ЗАГОЛОВОК -----
        title = tk.Label(
            self.root,
            text="🍺 SkufUp",
            font=("Segoe UI", 28, "bold"),
            fg="#eab308",   # Жёлтый (цвет пива!)
            bg="#1a1a2e"
        )
        title.pack(pady=(20, 5))
        
        # Подзаголовок
        subtitle = tk.Label(
            self.root,
            text="Детектор звука открытия пива",
            font=("Segoe UI", 11),
            fg="#888888",
            bg="#1a1a2e"
        )
        subtitle.pack()
        
        # ----- ИНДИКАТОР СТАТУСА -----
        # Показывает текущее состояние: слушаем / не слушаем / пиво!
        status_frame = tk.Frame(self.root, bg="#1a1a2e")
        status_frame.pack(pady=15)
        
        # Цветной кружок (меняет цвет в зависимости от статуса)
        self.status_indicator = tk.Label(
            status_frame,
            text="●",
            font=("Segoe UI", 24),
            fg="#666666",   # Серый = не активен
            bg="#1a1a2e"
        )
        self.status_indicator.pack(side=tk.LEFT, padx=5)
        
        # Текст статуса
        self.status_label = tk.Label(
            status_frame,
            text="Не активен",
            font=("Segoe UI", 14),
            fg="#888888",
            bg="#1a1a2e"
        )
        self.status_label.pack(side=tk.LEFT)
        
        # ----- БЛОК ВЫБОРА ЦЕЛИ -----
        # Здесь пользователь выбирает игру или сайт
        target_frame = tk.Frame(self.root, bg="#252547", padx=20, pady=15)
        target_frame.pack(pady=10, padx=20, fill=tk.X)
        
        tk.Label(
            target_frame,
            text="Что открывать при звуке пива:",
            font=("Segoe UI", 11, "bold"),
            fg="#ffffff",
            bg="#252547"
        ).pack(anchor=tk.W)
        
        # Кнопки "Выбрать игру" и "Указать сайт"
        btn_type_frame = tk.Frame(target_frame, bg="#252547")
        btn_type_frame.pack(fill=tk.X, pady=10)
        
        # Кнопка выбора игры (синяя)
        self.btn_game = tk.Button(
            btn_type_frame,
            text="🎮 Выбрать игру",
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
        
        # Кнопка выбора сайта (фиолетовая)
        self.btn_website = tk.Button(
            btn_type_frame,
            text="🌐 Указать сайт",
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
        
        # ----- ПОЛЕ ВВОДА САЙТА -----
        # Показывается когда пользователь нажмёт "Указать сайт"
        self.website_frame = tk.Frame(target_frame, bg="#252547")
        
        tk.Label(
            self.website_frame,
            text="Введите URL и нажмите Enter:",
            font=("Segoe UI", 9),
            fg="#888888",
            bg="#252547"
        ).pack(anchor=tk.W)
        
        # Поле для ввода URL
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
        
        # Привязываем клавиши
        self.url_entry.bind('<Return>', self.save_website)      # Enter
        self.url_entry.bind('<KP_Enter>', self.save_website)    # Enter на нумпаде
        self.url_entry.bind('<Control-v>', self.paste_url)      # Ctrl+V
        self.url_entry.bind('<Control-V>', self.paste_url)      # Ctrl+V (большая V)
        self.url_entry.bind('<Button-3>', self.show_context_menu)  # Правая кнопка мыши
        
        # Кнопка сохранения сайта
        self.save_url_btn = tk.Button(
            self.website_frame,
            text="💾 Сохранить (или Enter)",
            font=("Segoe UI", 10),
            fg="#ffffff",
            bg="#22c55e",   # Зелёная
            activebackground="#16a34a",
            relief=tk.FLAT,
            cursor="hand2",
            command=self.save_website
        )
        self.save_url_btn.pack(anchor=tk.W, pady=(5, 0))
        
        # ----- КОНТЕКСТНОЕ МЕНЮ -----
        # Появляется при правом клике на поле ввода
        self.context_menu = tk.Menu(self.root, tearoff=0, bg="#252547", fg="#ffffff")
        self.context_menu.add_command(label="Вставить", command=self.paste_url_from_menu)
        self.context_menu.add_command(label="Очистить", command=lambda: self.url_entry.delete(0, tk.END))
        
        # ----- ОТОБРАЖЕНИЕ ТЕКУЩЕЙ ЦЕЛИ -----
        # Показывает что сейчас выбрано (игра или сайт)
        self.current_target_frame = tk.Frame(target_frame, bg="#1a1a2e", padx=10, pady=10)
        
        # Тип цели (🎮 Игра: или 🌐 Сайт:)
        self.target_type_label = tk.Label(
            self.current_target_frame,
            text="",
            font=("Segoe UI", 10),
            fg="#888888",
            bg="#1a1a2e"
        )
        self.target_type_label.pack(anchor=tk.W)
        
        # Путь к игре или URL сайта
        self.target_path_label = tk.Label(
            self.current_target_frame,
            text="",
            font=("Segoe UI", 11, "bold"),
            fg="#22c55e",
            bg="#1a1a2e",
            wraplength=420  # Перенос длинных строк
        )
        self.target_path_label.pack(anchor=tk.W)
        
        # Кнопка "Изменить"
        self.btn_change = tk.Button(
            self.current_target_frame,
            text="✏️ Изменить",
            font=("Segoe UI", 9),
            fg="#888888",
            bg="#333355",
            activebackground="#444466",
            relief=tk.FLAT,
            cursor="hand2",
            command=self.clear_target
        )
        self.btn_change.pack(anchor=tk.W, pady=(5, 0))
        
        # Обновляем отображение (покажет текущую цель или скроет блок)
        self.update_target_display()
        
        # ----- БОЛЬШАЯ КНОПКА СТАРТ/СТОП -----
        self.toggle_btn = tk.Button(
            self.root,
            text="▶  СТАРТ",
            font=("Segoe UI", 24, "bold"),
            fg="#ffffff",
            bg="#16a34a",   # Зелёная
            activebackground="#15803d",
            activeforeground="#ffffff",
            width=20,
            height=2,
            relief=tk.FLAT,
            cursor="hand2",
            command=self.toggle_listening
        )
        self.toggle_btn.pack(pady=30, padx=30, fill=tk.X)
        
        # ----- ГАЛОЧКА "АВТОЗАПУСК" -----
        self.autostart_var = tk.BooleanVar(value=self.is_autostart_enabled())
        autostart_cb = tk.Checkbutton(
            self.root,
            text="Запускать при старте Windows",
            variable=self.autostart_var,
            font=("Segoe UI", 10),
            fg="#888888",
            bg="#1a1a2e",
            selectcolor="#252547",
            activebackground="#1a1a2e",
            command=self.toggle_autostart
        )
        autostart_cb.pack()
        
        # ----- ГАЛОЧКА "СВОРАЧИВАТЬ ПРИ ЗАПУСКЕ" -----
        self.minimize_var = tk.BooleanVar(value=self.settings.get("minimize_on_start", False))
        minimize_cb = tk.Checkbutton(
            self.root,
            text="Сворачивать при запуске",
            variable=self.minimize_var,
            font=("Segoe UI", 10),
            fg="#888888",
            bg="#1a1a2e",
            selectcolor="#252547",
            activebackground="#1a1a2e",
            command=self.toggle_minimize_on_start
        )
        minimize_cb.pack()
        
        # ----- КНОПКА "СВЕРНУТЬ" -----
        minimize_btn = tk.Button(
            self.root,
            text="Свернуть",
            font=("Segoe UI", 9),
            fg="#666666",
            bg="#252547",
            activebackground="#333355",
            relief=tk.FLAT,
            cursor="hand2",
            command=self.root.iconify  # Свернуть окно
        )
        minimize_btn.pack(pady=10)
    
    
    # ========================================================================
    # МЕТОДЫ ДЛЯ РАБОТЫ С ЦЕЛЬЮ (ИГРА ИЛИ САЙТ)
    # ========================================================================
    
    def update_target_display(self):
        """
        Обновить отображение текущей цели.
        
        Если цель выбрана - показываем её.
        Если не выбрана - скрываем блок.
        """
        target_type = self.settings.get("target_type", "")
        target_path = self.settings.get("target_path", "")
        
        if target_path:
            # Есть цель - показываем
            self.current_target_frame.pack(fill=tk.X, pady=(10, 0))
            self.website_frame.pack_forget()  # Скрываем поле ввода сайта
            
            if target_type == "game":
                self.target_type_label.config(text="🎮 Игра:")
                # Показываем только имя файла, не весь путь
                self.target_path_label.config(text=os.path.basename(target_path))
            else:
                self.target_type_label.config(text="🌐 Сайт:")
                self.target_path_label.config(text=target_path)
        else:
            # Нет цели - скрываем оба блока
            self.current_target_frame.pack_forget()
            self.website_frame.pack_forget()
    
    def select_game(self):
        """
        Открыть диалог выбора игры (.exe файла).
        """
        file_path = filedialog.askopenfilename(
            title="Выберите игру",
            filetypes=[
                ("Исполняемые файлы", "*.exe"),
                ("Все файлы", "*.*")
            ]
        )
        
        if file_path:
            # Пользователь выбрал файл
            self.settings["target_type"] = "game"
            self.settings["target_path"] = file_path
            
            if save_settings(self.settings):
                messagebox.showinfo("Готово!", f"Игра сохранена:\n{os.path.basename(file_path)}")
                self.update_target_display()
    
    def show_website_input(self):
        """
        Показать поле для ввода URL сайта.
        """
        self.current_target_frame.pack_forget()  # Скрываем текущую цель
        self.website_frame.pack(fill=tk.X, pady=(10, 0))  # Показываем поле ввода
        self.url_entry.delete(0, tk.END)  # Очищаем поле
        self.url_entry.focus_set()  # Ставим курсор в поле
    
    def save_website(self, event=None):
        """
        Сохранить введённый сайт.
        
        Вызывается при нажатии Enter или кнопки "Сохранить".
        """
        url = self.url_entry.get().strip()
        
        if not url:
            return  # Пустая строка - ничего не делаем
        
        # Добавляем https:// если пользователь не написал
        if not url.startswith(("http://", "https://")):
            url = "https://" + url
        
        self.settings["target_type"] = "website"
        self.settings["target_path"] = url
        
        if save_settings(self.settings):
            messagebox.showinfo("Готово!", f"Сайт сохранён:\n{url}")
            self.update_target_display()
        else:
            messagebox.showerror("Ошибка", "Не удалось сохранить настройки")
    
    def clear_target(self):
        """
        Очистить текущую цель (для изменения).
        """
        self.settings["target_type"] = ""
        self.settings["target_path"] = ""
        save_settings(self.settings)
        self.update_target_display()
    
    def paste_url(self, event=None):
        """
        Вставить URL из буфера обмена (Ctrl+V).
        """
        try:
            clipboard = self.root.clipboard_get()
            self.url_entry.delete(0, tk.END)
            self.url_entry.insert(0, clipboard)
        except:
            pass
        return "break"  # Не передаём событие дальше
    
    def paste_url_from_menu(self):
        """
        Вставить URL из контекстного меню.
        """
        try:
            clipboard = self.root.clipboard_get()
            self.url_entry.delete(0, tk.END)
            self.url_entry.insert(0, clipboard)
        except:
            pass
    
    def show_context_menu(self, event):
        """
        Показать контекстное меню при правом клике.
        """
        try:
            self.context_menu.tk_popup(event.x_root, event.y_root)
        finally:
            self.context_menu.grab_release()
    
    
    # ========================================================================
    # МЕТОДЫ ПРОСЛУШИВАНИЯ МИКРОФОНА
    # ========================================================================
    
    def toggle_listening(self):
        """
        Переключить прослушивание (старт/стоп).
        """
        if self.is_listening:
            self.stop_listening()
        else:
            self.start_listening()
    
    def start_listening(self):
        """
        Начать прослушивание микрофона.
        
        1. Проверяем, что выбрана цель (игра или сайт)
        2. Меняем кнопку на "СТОП"
        3. Запускаем поток прослушивания
        """
        # Проверяем, есть ли цель
        if not self.settings.get("target_path"):
            messagebox.showwarning("Внимание", "Сначала выберите игру или укажите сайт!")
            return
        
        self.is_listening = True
        self.stop_flag.clear()
        
        # Меняем индикатор на зелёный
        self.status_indicator.config(fg="#22c55e")
        self.status_label.config(text="Слушаю...", fg="#22c55e")
        
        # Меняем кнопку на "СТОП" (красная)
        self.toggle_btn.config(text="■  СТОП", bg="#dc2626", activebackground="#b91c1c")
        
        # Запускаем прослушивание в отдельном потоке (чтобы окно не зависало)
        self.listen_thread = threading.Thread(target=self.listen_loop, daemon=True)
        self.listen_thread.start()
    
    def stop_listening(self):
        """
        Остановить прослушивание микрофона.
        """
        self.is_listening = False
        self.stop_flag.set()  # Сигнал потоку остановиться
        
        # Меняем индикатор на серый
        self.status_indicator.config(fg="#666666")
        self.status_label.config(text="Остановлен", fg="#888888")
        
        # Меняем кнопку на "СТАРТ" (зелёная)
        self.toggle_btn.config(text="▶  СТАРТ", bg="#16a34a", activebackground="#15803d")
    
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
        self.status_label.config(text="🍺 ПИВО!", fg="#eab308")
        
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
            self.status_label.config(text="Слушаю...", fg="#22c55e")
    
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
