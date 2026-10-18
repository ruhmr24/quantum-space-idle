import pygame
import sys
import math
import config

# Инициализация окна с настройками из конфига
pygame.init()
screen = pygame.display.set_mode((config.WINDOW_WIDTH, config.WINDOW_HEIGHT))
pygame.display.set_caption("Quantum Space Idle v1.0")
clock = pygame.time.Clock()

# Состояния игры (Добавили SETTINGS)
STATES = {"MENU": 0, "SETTINGS": 1, "SINGULARITY": 2, "BANG_SCENE": 3, "GAME": 4}
current_state = STATES["MENU"]

# Ресурсы
quarks = 0
singularity_size = 6
required_quarks = 15
upgrade_count = 0
auto_cps = 0
upgrade_cost = 10

# Загрузка
saved_data = config.load_game()
if saved_data:
    quarks = saved_data.get("quarks", 0)
    upgrade_count = saved_data.get("upgrade_count", 0)
    auto_cps = saved_data.get("auto_cps", 0)
    upgrade_cost = saved_data.get("upgrade_cost", 10)
    # Если старый сейв не знает про "state", игра просто начнется с Главного Меню
    current_state = saved_data.get("state", STATES["MENU"])


# Обновляем окно под загруженные настройки экрана
screen = pygame.display.set_mode((config.WINDOW_WIDTH, config.WINDOW_HEIGHT))

# Таймеры
AUTO_SAVE_EVENT = pygame.USEREVENT + 1
pygame.time.set_timer(AUTO_SAVE_EVENT, 15000)

IDLE_TICK_EVENT = pygame.USEREVENT + 2
pygame.time.set_timer(IDLE_TICK_EVENT, 1000)

def draw_pixel_button(surf, text, x, y, w, h, mx, my):
    """Универсальная отрисовка интерактивной кнопки"""
    is_hover = x <= mx <= x + w and y <= my <= y + h
    color = config.LIGHT_GRAY if is_hover else config.GRAY
    pygame.draw.rect(surf, color, (x, y, w, h))
    pygame.draw.rect(surf, config.WHITE, (x, y, w, h), 2)
    
    font = pygame.font.SysFont("Courier", int(config.WINDOW_HEIGHT * 0.03), bold=True)
    rendered_text = font.render(text, True, config.WHITE)
    surf.blit(rendered_text, (x + w//2 - rendered_text.get_width()//2, y + h//2 - rendered_text.get_height()//2))
    return is_hover

running = True
while running:
    mouse_x, mouse_y = pygame.mouse.get_pos()
    
    # Динамические шрифты, подстраивающиеся под текущую высоту окна
    font_large = pygame.font.SysFont("Courier", int(config.WINDOW_HEIGHT * 0.05), bold=True)
    font_medium = pygame.font.SysFont("Courier", int(config.WINDOW_HEIGHT * 0.035), bold=True)

    # 1. ОБРАБОТКА ИВЕНТОВ
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            config.save_game(quarks, current_state == STATES["GAME"], upgrade_count, auto_cps, upgrade_cost, current_state)
            running = False

        if event.type == AUTO_SAVE_EVENT and current_state != STATES["MENU"] and current_state != STATES["SETTINGS"]:
            config.save_game(quarks, current_state == STATES["GAME"], upgrade_count, auto_cps, upgrade_cost, current_state)

        if event.type == IDLE_TICK_EVENT and current_state == STATES["GAME"]:
            quarks += auto_cps

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            
            # Клики в МЕНЮ
            if current_state == STATES["MENU"]:
                # Кнопка ИГРАТЬ
                if config.WINDOW_WIDTH//2 - 150 <= mouse_x <= config.WINDOW_WIDTH//2 + 150 and config.WINDOW_HEIGHT*0.5 <= mouse_y <= config.WINDOW_HEIGHT*0.5 + 50:
                    if current_state == STATES["GAME"] or quarks > 0:
                        pass # Если уже в игре, кнопка не сбросит состояние
                    else:
                        current_state = STATES["SINGULARITY"]
                # Кнопка НАСТРОЙКИ
                elif config.WINDOW_WIDTH//2 - 150 <= mouse_x <= config.WINDOW_WIDTH//2 + 150 and config.WINDOW_HEIGHT*0.6 <= mouse_y <= config.WINDOW_HEIGHT*0.6 + 50:
                    current_state = STATES["SETTINGS"]

            # Клики в НАСТРОЙКАХ
            elif current_state == STATES["SETTINGS"]:
                # Переключатель РАЗРЕШЕНИЯ
                if config.WINDOW_WIDTH//2 - 200 <= mouse_x <= config.WINDOW_WIDTH//2 + 200 and config.WINDOW_HEIGHT*0.3 <= mouse_y <= config.WINDOW_HEIGHT*0.3 + 45:
                    config.current_res_idx = (config.current_res_idx + 1) % len(config.RESOLUTIONS)
                    config.update_system_settings()
                    screen = pygame.display.set_mode((config.WINDOW_WIDTH, config.WINDOW_HEIGHT)) # Мгновенно меняем окно
                
                # Переключатель FPS
                elif config.WINDOW_WIDTH//2 - 200 <= mouse_x <= config.WINDOW_WIDTH//2 + 200 and config.WINDOW_HEIGHT*0.42 <= mouse_y <= config.WINDOW_HEIGHT*0.42 + 45:
                    config.current_fps_idx = (config.current_fps_idx + 1) % len(config.FPS_OPTIONS)
                    config.update_system_settings()

                # Переключатель ЯЗЫКА
                elif config.WINDOW_WIDTH//2 - 200 <= mouse_x <= config.WINDOW_WIDTH//2 + 200 and config.WINDOW_HEIGHT*0.54 <= mouse_y <= config.WINDOW_HEIGHT*0.54 + 45:
                    config.current_lang_idx = (config.current_lang_idx + 1) % len(config.LANGUAGES)
                    config.update_system_settings()

                # Кнопка НАЗАД
                elif config.WINDOW_WIDTH//2 - 100 <= mouse_x <= config.WINDOW_WIDTH//2 + 100 and config.WINDOW_HEIGHT*0.75 <= mouse_y <= config.WINDOW_HEIGHT*0.75 + 50:
                    config.save_game(quarks, current_state == STATES["GAME"], upgrade_count, auto_cps, upgrade_cost, STATES["MENU"])
                    current_state = STATES["MENU"]

            # Клики в СИНГУЛЯРНОСТИ
            elif current_state == STATES["SINGULARITY"]:
                cx, cy = config.WINDOW_WIDTH // 2, config.WINDOW_HEIGHT // 2
                if math.hypot(mouse_x - cx, mouse_y - cy) < singularity_size + 30:
                    quarks += 1
                    singularity_size += 2
                    if quarks >= required_quarks:
                        current_state = STATES["GAME"] # Тут будет BANG_SCENE

    # 2. ОТРИСОВКА ЭКРАНОВ
    screen.fill(config.BLACK)

    # --- ЭКРАН: ГЛАВНОЕ МЕНЮ ---
    if current_state == STATES["MENU"]:
        title = font_large.render(config.get_text("title"), True, config.CYAN)
        screen.blit(title, (config.WINDOW_WIDTH//2 - title.get_width()//2, config.WINDOW_HEIGHT * 0.3))
        
        draw_pixel_button(screen, config.get_text("btn_play"), config.WINDOW_WIDTH//2 - 150, int(config.WINDOW_HEIGHT*0.5), 300, 50, mouse_x, mouse_y)
        draw_pixel_button(screen, config.get_text("btn_settings"), config.WINDOW_WIDTH//2 - 150, int(config.WINDOW_HEIGHT*0.6), 300, 50, mouse_x, mouse_y)

    # --- ЭКРАН: НАСТРОЙКИ ---
    elif current_state == STATES["SETTINGS"]:
        st_title = font_large.render(config.get_text("settings_title"), True, config.ORANGE)
        screen.blit(st_title, (config.WINDOW_WIDTH//2 - st_title.get_width()//2, config.WINDOW_HEIGHT * 0.15))
        
        # Кнопки-переключатели настроек
        res_str = f"{config.RESOLUTIONS[config.current_res_idx][0]}x{config.RESOLUTIONS[config.current_res_idx][1]}"
        draw_pixel_button(screen, config.get_text("res_label") + res_str, config.WINDOW_WIDTH//2 - 200, int(config.WINDOW_HEIGHT*0.3), 400, 45, mouse_x, mouse_y)
        
        fps_str = f"{config.FPS_OPTIONS[config.current_fps_idx]} HZ"
        draw_pixel_button(screen, config.get_text("fps_label") + fps_str, config.WINDOW_WIDTH//2 - 200, int(config.WINDOW_HEIGHT*0.42), 400, 45, mouse_x, mouse_y)
        
        lang_str = f"{config.LANGUAGES[config.current_lang_idx]}"
        draw_pixel_button(screen, config.get_text("lang_label") + lang_str, config.WINDOW_WIDTH//2 - 200, int(config.WINDOW_HEIGHT*0.54), 400, 45, mouse_x, mouse_y)
        
        # Кнопка выхода в меню
        draw_pixel_button(screen, config.get_text("btn_back"), config.WINDOW_WIDTH//2 - 100, int(config.WINDOW_HEIGHT*0.75), 200, 50, mouse_x, mouse_y)

    # --- ЭКРАН: СИНГУЛЯРНОСТЬ ---
    elif current_state == STATES["SINGULARITY"]:
        cx, cy = config.WINDOW_WIDTH // 2, config.WINDOW_HEIGHT // 2
        pygame.draw.rect(screen, config.WHITE, (cx - singularity_size//2, cy - singularity_size//2, singularity_size, singularity_size))
        
        txt = font_medium.render(config.get_text("singularity_tip"), True, config.CYAN)
        screen.blit(txt, (config.WINDOW_WIDTH//2 - txt.get_width()//2, cy + 60))
        
        score = font_medium.render(config.get_text("density_label") + f"{quarks}/{required_quarks}", True, config.WHITE)
        screen.blit(score, (20, 20))

    # --- ЭКРАН: ГЕЙМПЛЕЙ ---
    elif current_state == STATES["GAME"]:
        txt_game = font_medium.render(config.get_text("epoch_quarks"), True, config.ORANGE)
        screen.blit(txt_game, (config.WINDOW_WIDTH//2 - txt_game.get_width()//2, config.WINDOW_HEIGHT//2))
        
        score = font_medium.render(config.get_text("quarks_current") + f"{quarks}", True, config.WHITE)
        screen.blit(score, (20, 20))

    pygame.display.flip()
    clock.tick(config.FPS) # Частота кадров теперь привязана к настройкам геймера!

pygame.quit()
sys.exit()
