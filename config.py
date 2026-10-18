import pygame, json, os, ctypes
try: ctypes.windll.shcore.SetProcessDpiAwareness(2)
except Exception: pass
pygame.init()

RESOLUTIONS = [(1280, 720), (1600, 900), (1920, 1080), (2560, 1440), (3840, 2160)]
FPS_OPTIONS = [60, 120, 144, 240]
LANGUAGES = ["RU", "EN"]
SCREEN_MODES = ["WINDOWED", "FULLSCREEN"]

current_res_idx, current_fps_idx, current_lang_idx, current_mode_idx = 2, 0, 0, 0
show_fps_counter = True

# Фиксированные размеры холста, под которые пишется вся игра
V_WIDTH, V_HEIGHT = 1920, 1080
V_SPACE_WIDTH = int(V_WIDTH * 0.75)

WINDOW_WIDTH, WINDOW_HEIGHT = RESOLUTIONS[current_res_idx]
SPACE_WIDTH = int(WINDOW_WIDTH * 0.75)
FPS = FPS_OPTIONS[current_fps_idx]
LANG = LANGUAGES[current_lang_idx]
SCREEN_MODE = SCREEN_MODES[current_mode_idx]

BLACK, WHITE = (0, 0, 0), (255, 255, 255)
CYAN, ORANGE = (0, 255, 255), (255, 165, 0)
GRAY, LIGHT_GRAY = (25, 25, 25), (55, 55, 55)
GREEN = (0, 255, 100)

LOCALIZATION = {
    "RU": {
        "title": "КВАНТОВАЯ ВСЕЛЕННАЯ IDLE", "btn_play": "НАЧАТЬ ИГРУ", "btn_settings": "НАСТРОЙКИ",
        "btn_back": "НАЗАД", "settings_title": "НАСТРОЙКИ ВСЕЛЕННОЙ", "res_label": "Разрешение: ",
        "fps_label": "Лимит кадров: ", "lang_label": "Язык: ", "mode_label": "Режим экрана: ",
        "fps_show_label": "Показ FPS: ", "singularity_tip": "КЛИКАЙ ДЛЯ СЖАТИЯ МАТЕРИИ",
        "density_label": "Плотность: ", "epoch_quarks": "ЭПОХА КВАРКОВ (АВТОСЕЙВ РАБОТАЕТ)",
        "quarks_current": "Кварки: ", "on": "ВКЛ", "off": "ВЫКЛ", "windowed": "ОКОННЫЙ", "fullscreen": "ПОЛНЫЙ",
        "shop_title": "МАГАЗИН", "btn_strong_force": "Сильное Взаимод.", "owned_label": "Куплено: ",
        "btn_resume": "ПРОДОЛЖИТЬ", "btn_to_menu": "ГЛАВНОЕ МЕНЮ"
    },
    "EN": {
        "title": "QUANTUM SPACE IDLE", "btn_play": "PLAY GAME", "btn_settings": "SETTINGS",
        "btn_back": "BACK", "settings_title": "UNIVERSE SETTINGS", "res_label": "Resolution: ",
        "fps_label": "Frame Rate: ", "lang_label": "Language: ", "mode_label": "Display Mode: ",
        "fps_show_label": "Show FPS: ", "singularity_tip": "CLICK TO COMPRESS MATTER",
        "density_label": "Density: ", "epoch_quarks": "QUARK EPOCH (AUTOSAVE ACTIVE)",
        "quarks_current": "Quarks: ", "on": "ON", "off": "OFF", "windowed": "WINDOWED", "fullscreen": "FULLSCREEN",
        "shop_title": "SHOP", "btn_strong_force": "Strong Force", "owned_label": "Owned: ",
        "btn_resume": "RESUME", "btn_to_menu": "MAIN MENU"
    }
}

def get_text(key): return LOCALIZATION[LANG][key]

def update_system_settings():
    global WINDOW_WIDTH, WINDOW_HEIGHT, FPS, LANG, SCREEN_MODE, SPACE_WIDTH
    WINDOW_WIDTH, WINDOW_HEIGHT = RESOLUTIONS[current_res_idx]
    SPACE_WIDTH = int(WINDOW_WIDTH * 0.75)
    FPS = FPS_OPTIONS[current_fps_idx]
    LANG = LANGUAGES[current_lang_idx]
    SCREEN_MODE = SCREEN_MODES[current_mode_idx]

SAVE_FILE = "savegame.json"
def save_game(quarks, state, upgrade_count, auto_cps, upgrade_cost):
    data = {
        "quarks": quarks, "upgrade_count": upgrade_count, "auto_cps": auto_cps,
        "upgrade_cost": upgrade_cost, "state": state, "res_idx": current_res_idx,
        "fps_idx": current_fps_idx, "lang_idx": current_lang_idx, "mode_idx": current_mode_idx, "show_fps": show_fps_counter
    }
    try:
        with open(SAVE_FILE, "w", encoding="utf-8") as f: json.dump(data, f, indent=4)
    except Exception: pass

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
        except Exception: pass
    return None
