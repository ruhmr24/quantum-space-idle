import pygame
import config

button_animations = {}

def draw_btn(surf, text, tag, tx, ty, tw, th, mx, my):
    global button_animations
    if tag not in button_animations: button_animations[tag] = {"w": tw, "h": th}
    is_hover = tx <= mx <= tx + tw and ty <= my <= ty + th
    dw = tw * 1.05 if is_hover else tw
    dh = th * 1.05 if is_hover else th
    button_animations[tag]["w"] += (dw - button_animations[tag]["w"]) * 0.2
    button_animations[tag]["h"] += (dh - button_animations[tag]["h"]) * 0.2
    w, h = int(button_animations[tag]["w"]), int(button_animations[tag]["h"])
    x, y = tx - (w - tw) // 2, ty - (h - th) // 2
    pygame.draw.rect(surf, config.LIGHT_GRAY if is_hover else config.GRAY, (x, y, w, h))
    pygame.draw.rect(surf, config.GREEN if is_hover else config.WHITE, (x, y, w, h), 2)
    
    font = pygame.font.SysFont("Courier", int(config.WINDOW_HEIGHT * 0.025), bold=True)
    r_txt = font.render(text, True, config.WHITE)
    surf.blit(r_txt, (x + w//2 - r_txt.get_width()//2, y + h//2 - r_txt.get_height()//2))
    return is_hover

class SlidingPanel:
    def __init__(self):
        self.current_x = float(config.WINDOW_WIDTH)
        self.is_active = False

    def activate(self): self.is_active = True
    def update(self):
        if self.is_active: self.current_x += (config.SPACE_WIDTH - self.current_x) * 0.08

    def draw(self, surface, quarks, auto_cps, upgrade_cost, upgrade_count, mouse_x, mouse_y):
        if self.current_x >= config.WINDOW_WIDTH: return False
        x_pos = int(self.current_x)
        panel_w = config.WINDOW_WIDTH - x_pos
        
        pygame.draw.rect(surface, config.GRAY, (x_pos, 0, panel_w, config.WINDOW_HEIGHT))
        pygame.draw.line(surface, config.LIGHT_GRAY, (x_pos, 0), (x_pos, config.WINDOW_HEIGHT), 3)

        font_l = pygame.font.SysFont("Courier", int(config.WINDOW_HEIGHT * 0.04), bold=True)
        font_m = pygame.font.SysFont("Courier", int(config.WINDOW_HEIGHT * 0.025), bold=True)

        surface.blit(font_l.render(config.get_text("shop_title"), True, config.WHITE), (x_pos + 20, 20))
        surface.blit(font_m.render(f"{config.get_text('quarks_current')}{quarks}", True, config.WHITE), (x_pos + 20, 70))
        surface.blit(font_m.render(f"CPS: +{auto_cps}", True, config.CYAN), (x_pos + 20, 105))

        if x_pos <= config.SPACE_WIDTH + 10:
            btn_y, btn_w, btn_h = 170, (config.WINDOW_WIDTH - config.SPACE_WIDTH) - 40, 75
            is_hover = (x_pos + 20) <= mouse_x <= (x_pos + 20) + btn_w and btn_y <= mouse_y <= btn_y + btn_h
            pygame.draw.rect(surface, config.LIGHT_GRAY if is_hover else config.GRAY, (x_pos + 20, btn_y, btn_w, btn_h))
            pygame.draw.rect(surface, config.GREEN if is_hover else config.WHITE, (x_pos + 20, btn_y, btn_w, btn_h), 2)
            
            t1 = font_m.render(config.get_text("btn_strong_force"), True, config.WHITE)
            t2 = font_m.render(f"Cost: {upgrade_cost} Q.", True, config.ORANGE)
            
            surface.blit(t1, (x_pos + 20 + btn_w//2 - t1.get_width()//2, btn_y + int(btn_h * 0.15)))
            surface.blit(t2, (x_pos + 20 + btn_w//2 - t2.get_width()//2, btn_y + int(btn_h * 0.55)))

            owned_str = f"{config.get_text('owned_label')}{upgrade_count}"
            surface.blit(font_m.render(owned_str, True, config.WHITE), (x_pos + 20, btn_y + btn_h + 15))
            return is_hover
        return False

def draw_menu_system(surf, state, font_l, mx, my):
    # ДИНАМИЧЕСКИЕ ПРОПОРЦИИ ПОД ЛЮБОЙ МОНИТОР
    cx = config.WINDOW_WIDTH // 2
    btn_w, btn_h = int(config.WINDOW_WIDTH * 0.25), int(config.WINDOW_HEIGHT * 0.05)
    if btn_w < 350: btn_w = 350
    if btn_h < 45: btn_h = 45

    if state == 0: # MENU
        title = font_l.render(config.get_text("title"), True, config.CYAN)
        surf.blit(title, (cx - title.get_width()//2, int(config.WINDOW_HEIGHT * 0.25)))
        draw_btn(surf, config.get_text("btn_play"), "play", cx - btn_w//2, int(config.WINDOW_HEIGHT * 0.48), btn_w, btn_h, mx, my)
        draw_btn(surf, config.get_text("btn_settings"), "settings", cx - btn_w//2, int(config.WINDOW_HEIGHT * 0.58), btn_w, btn_h, mx, my)
    
    elif state == 1: # SETTINGS
        st_title = font_l.render(config.get_text("settings_title"), True, config.ORANGE)
        surf.blit(st_title, (cx - st_title.get_width()//2, int(config.WINDOW_HEIGHT * 0.1)))
        
        # Расставляем кнопки по вертикали с шагом 9% от высоты экрана (теперь ничего не налезет)
        labels = [
            f"{config.get_text('res_label')}{config.WINDOW_WIDTH}x{config.WINDOW_HEIGHT}",
            f"{config.get_text('fps_label')}{config.FPS} HZ",
            f"{config.get_text('mode_label')}{config.get_text('fullscreen') if config.SCREEN_MODE == 'FULLSCREEN' else config.get_text('windowed')}",
            f"{config.get_text('fps_show_label')}{config.get_text('on') if config.show_fps_counter else config.get_text('off')}",
            f"{config.get_text('lang_label')}{config.LANG}"
        ]
        tags = ["res", "fps", "mode", "fps_show", "lang"]
        
        for i, text in enumerate(labels):
            y_pos = int(config.WINDOW_HEIGHT * (0.23 + i * 0.09))
            draw_btn(surf, text, tags[i], cx - btn_w//2, y_pos, btn_w, btn_h, mx, my)
            
        draw_btn(surf, config.get_text("btn_back"), "back", cx - 100, int(config.WINDOW_HEIGHT * 0.78), 200, btn_h, mx, my)
