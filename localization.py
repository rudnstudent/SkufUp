"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                      SkufUp - Localization / Локализация                     ║
║                                                                              ║
║  This file contains all translations for the application.                    ║
║  Supported languages: English (en), Russian (ru)                             ║
║                                                                              ║
║  Этот файл содержит все переводы для приложения.                            ║
║  Поддерживаемые языки: Английский (en), Русский (ru)                        ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""

# ============================================================================
# TRANSLATIONS DICTIONARY
# ============================================================================

TRANSLATIONS = {
    "en": {
        # Window
        "window_title": "SkufUp - Beer Detector 🍺",
        
        # Header
        "title": "🍺 SkufUp",
        "subtitle": "Beer can opening sound detector",
        
        # Status
        "status_inactive": "Not active",
        "status_listening": "Listening...",
        "status_stopped": "Stopped",
        "status_beer": "🍺 BEER!",
        
        # Target selection
        "target_label": "What to open when beer is detected:",
        "btn_select_game": "🎮 Select game",
        "btn_select_website": "🌐 Enter website",
        "url_hint": "Enter URL and press Enter:",
        "btn_save_url": "💾 Save (or Enter)",
        "target_type_game": "🎮 Game:",
        "target_type_website": "🌐 Website:",
        "btn_change": "✏️ Change",
        
        # Context menu
        "menu_paste": "Paste",
        "menu_clear": "Clear",
        
        # Main button
        "btn_start": "▶  START",
        "btn_stop": "■  STOP",
        
        # Checkboxes
        "autostart_label": "Launch at Windows startup",
        "minimize_label": "Minimize on launch",
        
        # Other buttons
        "btn_minimize": "Minimize",
        
        # Dialogs
        "dialog_select_game": "Select game",
        "dialog_exe_files": "Executable files",
        "dialog_all_files": "All files",
        "dialog_saved_game": "Done!",
        "dialog_game_saved_msg": "Game saved:\n{0}",
        "dialog_saved_website": "Done!",
        "dialog_website_saved_msg": "Website saved:\n{0}",
        "dialog_error": "Error",
        "dialog_save_error": "Failed to save settings",
        "dialog_warning": "Warning",
        "dialog_select_target": "First select a game or enter a website!",
        "dialog_launch_error": "Failed to launch: {0}",
        "dialog_autostart_error": "Failed to add to startup: {0}",
        
        # Console messages
        "console_ml_detector": "   ✅ Using ML detector",
        "console_basic_detector": "   ⚠️ ML detector unavailable, using basic",
        "console_game_running": "🎮 Game already running, skipping",
        "console_game_launched": "🎮 Game launched: {0}",
        "console_cooldown": "🌐 Website: hour not passed yet, skipping",
        "console_website_opened": "🌐 Website opened: {0}",
        "console_psutil_missing": "⚠️ psutil not installed, process check unavailable",
        "console_save_error": "Save error: {0}",
        
        # Language
        "language_label": "🌐 Language:",
        "language_en": "English",
        "language_ru": "Русский",
    },
    
    "de": {
        # Window
        "window_title": "SkufUp - Bier-Detektor 🍺",
        
        # Header
        "title": "🍺 SkufUp",
        "subtitle": "Bierdosen-Öffnungsgeräusch-Detektor",
        
        # Status
        "status_inactive": "Nicht aktiv",
        "status_listening": "Höre zu...",
        "status_stopped": "Gestoppt",
        "status_beer": "🍺 BIER!",
        
        # Target selection
        "target_label": "Was öffnen, wenn Bier erkannt wird:",
        "btn_select_game": "🎮 Spiel wählen",
        "btn_select_website": "🌐 Website eingeben",
        "url_hint": "URL eingeben und Enter drücken:",
        "btn_save_url": "💾 Speichern (oder Enter)",
        "target_type_game": "🎮 Spiel:",
        "target_type_website": "🌐 Website:",
        "btn_change": "✏️ Ändern",
        
        # Context menu
        "menu_paste": "Einfügen",
        "menu_clear": "Löschen",
        
        # Main button
        "btn_start": "▶  START",
        "btn_stop": "■  STOPP",
        
        # Checkboxes
        "autostart_label": "Bei Windows-Start starten",
        "minimize_label": "Beim Start minimieren",
        
        # Other buttons
        "btn_minimize": "Minimieren",
        
        # Dialogs
        "dialog_select_game": "Spiel auswählen",
        "dialog_exe_files": "Ausführbare Dateien",
        "dialog_all_files": "Alle Dateien",
        "dialog_saved_game": "Fertig!",
        "dialog_game_saved_msg": "Spiel gespeichert:\n{0}",
        "dialog_saved_website": "Fertig!",
        "dialog_website_saved_msg": "Website gespeichert:\n{0}",
        "dialog_error": "Fehler",
        "dialog_save_error": "Einstellungen konnten nicht gespeichert werden",
        "dialog_warning": "Warnung",
        "dialog_select_target": "Zuerst ein Spiel oder eine Website auswählen!",
        "dialog_launch_error": "Start fehlgeschlagen: {0}",
        "dialog_autostart_error": "Konnte nicht zum Autostart hinzugefügt werden: {0}",
        
        # Language
        "language_label": "🌐 Sprache:",
    },
    
    "es": {
        # Window
        "window_title": "SkufUp - Detector de Cerveza 🍺",
        
        # Header
        "title": "🍺 SkufUp",
        "subtitle": "Detector de sonido de apertura de lata",
        
        # Status
        "status_inactive": "No activo",
        "status_listening": "Escuchando...",
        "status_stopped": "Detenido",
        "status_beer": "🍺 ¡CERVEZA!",
        
        # Target selection
        "target_label": "Qué abrir cuando se detecte cerveza:",
        "btn_select_game": "🎮 Elegir juego",
        "btn_select_website": "🌐 Ingresar sitio web",
        "url_hint": "Ingrese URL y presione Enter:",
        "btn_save_url": "💾 Guardar (o Enter)",
        "target_type_game": "🎮 Juego:",
        "target_type_website": "🌐 Sitio web:",
        "btn_change": "✏️ Cambiar",
        
        # Context menu
        "menu_paste": "Pegar",
        "menu_clear": "Limpiar",
        
        # Main button
        "btn_start": "▶  INICIAR",
        "btn_stop": "■  DETENER",
        
        # Checkboxes
        "autostart_label": "Iniciar con Windows",
        "minimize_label": "Minimizar al iniciar",
        
        # Other buttons
        "btn_minimize": "Minimizar",
        
        # Dialogs
        "dialog_select_game": "Seleccionar juego",
        "dialog_exe_files": "Archivos ejecutables",
        "dialog_all_files": "Todos los archivos",
        "dialog_saved_game": "¡Listo!",
        "dialog_game_saved_msg": "Juego guardado:\n{0}",
        "dialog_saved_website": "¡Listo!",
        "dialog_website_saved_msg": "Sitio web guardado:\n{0}",
        "dialog_error": "Error",
        "dialog_save_error": "No se pudo guardar la configuración",
        "dialog_warning": "Advertencia",
        "dialog_select_target": "¡Primero seleccione un juego o ingrese un sitio web!",
        "dialog_launch_error": "Error al iniciar: {0}",
        "dialog_autostart_error": "No se pudo agregar al inicio: {0}",
        
        # Language
        "language_label": "🌐 Idioma:",
    },
    
    "fr": {
        # Window
        "window_title": "SkufUp - Détecteur de Bière 🍺",
        
        # Header
        "title": "🍺 SkufUp",
        "subtitle": "Détecteur de son d'ouverture de canette",
        
        # Status
        "status_inactive": "Non actif",
        "status_listening": "Écoute...",
        "status_stopped": "Arrêté",
        "status_beer": "🍺 BIÈRE!",
        
        # Target selection
        "target_label": "Que ouvrir quand la bière est détectée:",
        "btn_select_game": "🎮 Choisir un jeu",
        "btn_select_website": "🌐 Entrer un site web",
        "url_hint": "Entrez l'URL et appuyez sur Entrée:",
        "btn_save_url": "💾 Enregistrer (ou Entrée)",
        "target_type_game": "🎮 Jeu:",
        "target_type_website": "🌐 Site web:",
        "btn_change": "✏️ Modifier",
        
        # Context menu
        "menu_paste": "Coller",
        "menu_clear": "Effacer",
        
        # Main button
        "btn_start": "▶  DÉMARRER",
        "btn_stop": "■  ARRÊTER",
        
        # Checkboxes
        "autostart_label": "Lancer au démarrage de Windows",
        "minimize_label": "Réduire au lancement",
        
        # Other buttons
        "btn_minimize": "Réduire",
        
        # Dialogs
        "dialog_select_game": "Sélectionner un jeu",
        "dialog_exe_files": "Fichiers exécutables",
        "dialog_all_files": "Tous les fichiers",
        "dialog_saved_game": "Terminé!",
        "dialog_game_saved_msg": "Jeu enregistré:\n{0}",
        "dialog_saved_website": "Terminé!",
        "dialog_website_saved_msg": "Site web enregistré:\n{0}",
        "dialog_error": "Erreur",
        "dialog_save_error": "Impossible d'enregistrer les paramètres",
        "dialog_warning": "Attention",
        "dialog_select_target": "D'abord sélectionnez un jeu ou entrez un site web!",
        "dialog_launch_error": "Échec du lancement: {0}",
        "dialog_autostart_error": "Impossible d'ajouter au démarrage: {0}",
        
        # Language
        "language_label": "🌐 Langue:",
    },
    
    "zh": {
        # Window
        "window_title": "SkufUp - 啤酒检测器 🍺",
        
        # Header
        "title": "🍺 SkufUp",
        "subtitle": "啤酒罐开启声音检测器",
        
        # Status
        "status_inactive": "未激活",
        "status_listening": "监听中...",
        "status_stopped": "已停止",
        "status_beer": "🍺 啤酒！",
        
        # Target selection
        "target_label": "检测到啤酒时打开什么：",
        "btn_select_game": "🎮 选择游戏",
        "btn_select_website": "🌐 输入网站",
        "url_hint": "输入网址并按回车：",
        "btn_save_url": "💾 保存（或回车）",
        "target_type_game": "🎮 游戏：",
        "target_type_website": "🌐 网站：",
        "btn_change": "✏️ 更改",
        
        # Context menu
        "menu_paste": "粘贴",
        "menu_clear": "清除",
        
        # Main button
        "btn_start": "▶  开始",
        "btn_stop": "■  停止",
        
        # Checkboxes
        "autostart_label": "Windows启动时运行",
        "minimize_label": "启动时最小化",
        
        # Other buttons
        "btn_minimize": "最小化",
        
        # Dialogs
        "dialog_select_game": "选择游戏",
        "dialog_exe_files": "可执行文件",
        "dialog_all_files": "所有文件",
        "dialog_saved_game": "完成！",
        "dialog_game_saved_msg": "游戏已保存：\n{0}",
        "dialog_saved_website": "完成！",
        "dialog_website_saved_msg": "网站已保存：\n{0}",
        "dialog_error": "错误",
        "dialog_save_error": "无法保存设置",
        "dialog_warning": "警告",
        "dialog_select_target": "请先选择游戏或输入网站！",
        "dialog_launch_error": "启动失败：{0}",
        "dialog_autostart_error": "无法添加到启动项：{0}",
        
        # Language
        "language_label": "🌐 语言：",
    },
    
    "cs": {
        # Window
        "window_title": "SkufUp - Detektor Piva 🍺",
        
        # Header
        "title": "🍺 SkufUp",
        "subtitle": "Detektor zvuku otevření plechovky",
        
        # Status
        "status_inactive": "Neaktivní",
        "status_listening": "Poslouchám...",
        "status_stopped": "Zastaveno",
        "status_beer": "🍺 PIVO!",
        
        # Target selection
        "target_label": "Co otevřít při detekci piva:",
        "btn_select_game": "🎮 Vybrat hru",
        "btn_select_website": "🌐 Zadat web",
        "url_hint": "Zadejte URL a stiskněte Enter:",
        "btn_save_url": "💾 Uložit (nebo Enter)",
        "target_type_game": "🎮 Hra:",
        "target_type_website": "🌐 Web:",
        "btn_change": "✏️ Změnit",
        
        # Context menu
        "menu_paste": "Vložit",
        "menu_clear": "Vymazat",
        
        # Main button
        "btn_start": "▶  START",
        "btn_stop": "■  STOP",
        
        # Checkboxes
        "autostart_label": "Spustit při startu Windows",
        "minimize_label": "Minimalizovat při spuštění",
        
        # Other buttons
        "btn_minimize": "Minimalizovat",
        
        # Dialogs
        "dialog_select_game": "Vybrat hru",
        "dialog_exe_files": "Spustitelné soubory",
        "dialog_all_files": "Všechny soubory",
        "dialog_saved_game": "Hotovo!",
        "dialog_game_saved_msg": "Hra uložena:\n{0}",
        "dialog_saved_website": "Hotovo!",
        "dialog_website_saved_msg": "Web uložen:\n{0}",
        "dialog_error": "Chyba",
        "dialog_save_error": "Nepodařilo se uložit nastavení",
        "dialog_warning": "Upozornění",
        "dialog_select_target": "Nejprve vyberte hru nebo zadejte web!",
        "dialog_launch_error": "Nepodařilo se spustit: {0}",
        "dialog_autostart_error": "Nepodařilo se přidat do autostartu: {0}",
        
        # Language
        "language_label": "🌐 Jazyk:",
    },
    
    "nl": {
        # Window
        "window_title": "SkufUp - Bierdetector 🍺",
        
        # Header
        "title": "🍺 SkufUp",
        "subtitle": "Blikje-open-geluid detector",
        
        # Status
        "status_inactive": "Niet actief",
        "status_listening": "Luisteren...",
        "status_stopped": "Gestopt",
        "status_beer": "🍺 BIER!",
        
        # Target selection
        "target_label": "Wat openen bij bierdetectie:",
        "btn_select_game": "🎮 Spel kiezen",
        "btn_select_website": "🌐 Website invoeren",
        "url_hint": "Voer URL in en druk op Enter:",
        "btn_save_url": "💾 Opslaan (of Enter)",
        "target_type_game": "🎮 Spel:",
        "target_type_website": "🌐 Website:",
        "btn_change": "✏️ Wijzigen",
        
        # Context menu
        "menu_paste": "Plakken",
        "menu_clear": "Wissen",
        
        # Main button
        "btn_start": "▶  START",
        "btn_stop": "■  STOP",
        
        # Checkboxes
        "autostart_label": "Starten bij Windows opstarten",
        "minimize_label": "Minimaliseren bij opstarten",
        
        # Other buttons
        "btn_minimize": "Minimaliseren",
        
        # Dialogs
        "dialog_select_game": "Spel selecteren",
        "dialog_exe_files": "Uitvoerbare bestanden",
        "dialog_all_files": "Alle bestanden",
        "dialog_saved_game": "Klaar!",
        "dialog_game_saved_msg": "Spel opgeslagen:\n{0}",
        "dialog_saved_website": "Klaar!",
        "dialog_website_saved_msg": "Website opgeslagen:\n{0}",
        "dialog_error": "Fout",
        "dialog_save_error": "Kon instellingen niet opslaan",
        "dialog_warning": "Waarschuwing",
        "dialog_select_target": "Selecteer eerst een spel of voer een website in!",
        "dialog_launch_error": "Kon niet starten: {0}",
        "dialog_autostart_error": "Kon niet toevoegen aan opstarten: {0}",
        
        # Language
        "language_label": "🌐 Taal:",
    },
    
    "ru": {
        # Window
        "window_title": "SkufUp - Детектор Пива 🍺",
        
        # Header
        "title": "🍺 SkufUp",
        "subtitle": "Детектор звука открытия пива",
        
        # Status
        "status_inactive": "Не активен",
        "status_listening": "Слушаю...",
        "status_stopped": "Остановлен",
        "status_beer": "🍺 ПИВО!",
        
        # Target selection
        "target_label": "Что открывать при звуке пива:",
        "btn_select_game": "🎮 Выбрать игру",
        "btn_select_website": "🌐 Указать сайт",
        "url_hint": "Введите URL и нажмите Enter:",
        "btn_save_url": "💾 Сохранить (или Enter)",
        "target_type_game": "🎮 Игра:",
        "target_type_website": "🌐 Сайт:",
        "btn_change": "✏️ Изменить",
        
        # Context menu
        "menu_paste": "Вставить",
        "menu_clear": "Очистить",
        
        # Main button
        "btn_start": "▶  СТАРТ",
        "btn_stop": "■  СТОП",
        
        # Checkboxes
        "autostart_label": "Запускать при старте Windows",
        "minimize_label": "Сворачивать при запуске",
        
        # Other buttons
        "btn_minimize": "Свернуть",
        
        # Dialogs
        "dialog_select_game": "Выберите игру",
        "dialog_exe_files": "Исполняемые файлы",
        "dialog_all_files": "Все файлы",
        "dialog_saved_game": "Готово!",
        "dialog_game_saved_msg": "Игра сохранена:\n{0}",
        "dialog_saved_website": "Готово!",
        "dialog_website_saved_msg": "Сайт сохранён:\n{0}",
        "dialog_error": "Ошибка",
        "dialog_save_error": "Не удалось сохранить настройки",
        "dialog_warning": "Внимание",
        "dialog_select_target": "Сначала выберите игру или укажите сайт!",
        "dialog_launch_error": "Не удалось запустить: {0}",
        "dialog_autostart_error": "Не удалось добавить в автозагрузку: {0}",
        
        # Console messages
        "console_ml_detector": "   ✅ Используется ML детектор",
        "console_basic_detector": "   ⚠️ ML детектор недоступен, используется базовый",
        "console_game_running": "🎮 Игра уже запущена, пропускаем",
        "console_game_launched": "🎮 Запущена игра: {0}",
        "console_cooldown": "🌐 Сайт: ещё не прошёл час, пропускаем",
        "console_website_opened": "🌐 Открыт сайт: {0}",
        "console_psutil_missing": "⚠️ psutil не установлен, проверка процессов недоступна",
        "console_save_error": "Ошибка сохранения: {0}",
        
        # Language
        "language_label": "🌐 Язык:",
        "language_en": "English",
        "language_ru": "Русский",
    }
}


# ============================================================================
# LOCALIZATION CLASS
# ============================================================================

class Localization:
    """
    Localization manager for SkufUp application.
    
    Usage:
        loc = Localization()
        loc.set_language("en")
        print(loc.get("window_title"))  # "SkufUp - Beer Detector 🍺"
    """
    
    def __init__(self, default_language: str = "en"):
        """
        Initialize localization with default language.
        
        Args:
            default_language: Language code ("en" or "ru")
        """
        self.current_language = default_language
        self.translations = TRANSLATIONS
    
    def get_available_languages(self) -> list:
        """
        Get list of available language codes.
        
        Returns:
            List of language codes (e.g., ["en", "ru"])
        """
        return list(self.translations.keys())
    
    def set_language(self, language: str) -> bool:
        """
        Set current language.
        
        Args:
            language: Language code ("en" or "ru")
            
        Returns:
            True if language was set, False if not available
        """
        if language in self.translations:
            self.current_language = language
            return True
        return False
    
    def get(self, key: str, *args) -> str:
        """
        Get translated string by key.
        
        Args:
            key: Translation key
            *args: Format arguments for the string
            
        Returns:
            Translated string, or key if not found
        """
        lang_dict = self.translations.get(self.current_language, {})
        text = lang_dict.get(key, key)
        
        # Apply format arguments if provided
        if args:
            try:
                text = text.format(*args)
            except (IndexError, KeyError):
                pass
        
        return text
    
    def __call__(self, key: str, *args) -> str:
        """
        Shorthand for get() method.
        
        Usage:
            loc = Localization()
            text = loc("window_title")
        """
        return self.get(key, *args)


# Global localization instance
_loc = Localization()


def get_localization() -> Localization:
    """Get global localization instance."""
    return _loc


def t(key: str, *args) -> str:
    """
    Translate a key using global localization.
    
    This is a convenience function for quick translations.
    
    Usage:
        from localization import t
        print(t("window_title"))
    """
    return _loc.get(key, *args)


def set_language(language: str) -> bool:
    """
    Set language for global localization.
    
    Args:
        language: Language code ("en" or "ru")
        
    Returns:
        True if language was set successfully
    """
    return _loc.set_language(language)


def get_current_language() -> str:
    """Get current language code."""
    return _loc.current_language
