import pygame
import json
import os
import ctypes

try:
    ctypes.windll.shcore.SetProcessDpiAwareness(2)
except Exception:
    try:
        ctypes.windll.user32.SetProcessDPIAware()
    except Exception:
        pass

pygame.init()

RESOLUTIONS = [
    (1280, 720),
    (1600, 900),
    (1920, 1080),
    (2560, 1440),
    (3840, 2160)
]
FPS_OPTIONS = [60, 120, 144, 240]
LANGUAGES = ["RU", "EN"]
SCREEN_MODES = ["WINDOWED", "FULLSCREEN"]

# Дефолтные настройки профиля
current_res_idx = 2
current_fps_idx = 0
current_lang_idx = 0
current_mode_idx = 0 # 0 - Оконный, 1 - Полноэкранный
show_fps_counter = True # Показывать ли счетчик FPS по умолчанию

WINDOW_WIDTH, WINDOW_HEIGHT = RESOLUTIONS[current_res_idx]
FPS = FPS_OPTIONS[current_fps_idx]
LANG = LANGUAGES[current_lang_idx]
SCREEN_MODE = SCREEN_MODES[current_mode_idx]

# Цвета
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
CYAN = (0, 255, 255)
ORANGE = (255, 165, 0)
GRAY = (25, 25, 25)
LIGHT_GRAY = (55, 55, 55)
GREEN = (0, 255, 100)

LOCALIZATION = {
    "RU": {
        "title": "КВАНТОВАЯ ВСЕЛЕННАЯ IDLE",
        "btn_play": "НАЧАТЬ ИГРУ",
        "btn_settings": "НАСТРОЙКИ",
        "btn_back": "НАЗАД",
        "settings_title": "НАСТРОЙКИ ВСЕЛЕННОЙ",
        "res_label": "Разрешение: ",
        "fps_label": "Лимит кадров: ",
        "lang_label": "Язык / Language: ",
        "mode_label": "Режим экрана: ",
        "fps_show_label": "Показ FPS: ",
        "singularity_tip": "КЛИКАЙ ДЛЯ СЖАТИЯ МАТЕРИИ",
        "density_label": "Плотность: ",
        "epoch_quarks": "ЭПОХА КВАРКОВ ЗАПУЩЕНА (АВТОСЕЙВ РАБОТАЕТ)",
        "quarks_current": "Кварки в наличии: ",
        "on": "ВКЛ",
        "off": "ВЫКЛ",
        "windowed": "ОКОННЫЙ",
        "fullscreen": "ПОЛНЫЙ ЭКРАН"
    },
    "EN": {
        "title": "QUANTUM SPACE IDLE",
        "btn_play": "PLAY GAME",
        "btn_settings": "SETTINGS",
        "btn_back": "BACK",
        "settings_title": "UNIVERSE SETTINGS",
        "res_label": "Resolution: ",
        "fps_label": "Frame Rate: ",
        "lang_label": "Language / Язык: ",
        "mode_label": "Display Mode: ",
        "fps_show_label": "Show FPS: ",
        "singularity_tip": "CLICK TO COMPRESS MATTER",
        "density_label": "Density: ",
        "epoch_quarks": "QUARK EPOCH STARTED (AUTOSAVE ACTIVE)",
        "quarks_current": "Available Quarks: ",
        "on": "ON",
        "off": "OFF",
        "windowed": "WINDOWED",
        "fullscreen": "FULLSCREEN"
    }
}

def get_text(key):
    return LOCALIZATION[LANG][key]

def update_system_settings():
    global WINDOW_WIDTH, WINDOW_HEIGHT, FPS, LANG, SCREEN_MODE
    WINDOW_WIDTH, WINDOW_HEIGHT = RESOLUTIONS[current_res_idx]
    FPS = FPS_OPTIONS[current_fps_idx]
    LANG = LANGUAGES[current_lang_idx]
    SCREEN_MODE = SCREEN_MODES[current_mode_idx]

SAVE_FILE = "savegame.json"

def save_game(quarks, big_bang_triggered, upgrade_count, auto_cps, upgrade_cost, state):
    data = {
        "quarks": quarks,
        "big_bang_triggered": big_bang_triggered,
        "upgrade_count": upgrade_count,
        "auto_cps": auto_cps,
        "upgrade_cost": upgrade_cost,
        "state": state,
        "res_idx": current_res_idx,
        "fps_idx": current_fps_idx,
        "lang_idx": current_lang_idx,
        "mode_idx": current_mode_idx,
        "show_fps": show_fps_counter
    }
    try:
        with open(SAVE_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)
    except Exception as e:
        print(f"Ошибка сохранения: {e}")

def load_game():
    global current_res_idx, current_fps_idx, current_lang_idx, current_mode_idx, show_fps_counter
    if os.path.exists(SAVE_FILE):
        try:
            with open(SAVE_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                current_res_idx = data.get("res_idx", current_res_idx)
                current_fps_idx = data.get("fps_idx", current_fps_idx)
                current_lang_idx = data.get("lang_idx", current_lang_idx)
                current_mode_idx = data.get("mode_idx", current_mode_idx)
                show_fps_counter = data.get("show_fps", show_fps_counter)
                update_system_settings()
                return data
        except Exception as e:
            print(f"Ошибка загрузки: {e}")
    return None
