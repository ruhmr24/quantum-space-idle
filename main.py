import pygame, sys, math, random, config, particles, ui

pygame.init()

# 1. ОБЪЯВЛЯЕМ ФУНКЦИЮ СОЗДАНИЯ ОКНА НА САМОМ ВЕРХУ
def create_display():
    flags = pygame.DOUBLEBUF
    if config.SCREEN_MODE == "FULLSCREEN": flags |= pygame.FULLSCREEN
    return pygame.display.set_mode((config.WINDOW_WIDTH, config.WINDOW_HEIGHT), flags)

# 2. ОПРЕДЕЛЯЕМ ГЛОБАЛЬНЫЕ СИСТЕМНЫЕ ТАЙМЕРЫ И ИВЕНТЫ
AUTO_SAVE_EVENT, IDLE_TICK_EVENT = pygame.USEREVENT + 1, pygame.USEREVENT + 2
pygame.time.set_timer(AUTO_SAVE_EVENT, 15000)
pygame.time.set_timer(IDLE_TICK_EVENT, 1000)

# 3. ИНИЦИАЛИЗИРУЕМ СТАРТОВОЕ ОКНО И ИГРОВЫЕ ПЕРЕМЕННЫЕ
screen = create_display()
pygame.display.set_caption("Quantum Space Idle")
clock = pygame.time.Clock()

STATES = {"MENU": 0, "SETTINGS": 1, "SINGULARITY": 2, "BANG_SCENE": 3, "GAME": 4, "PAUSE": 5}
current_state, prev_state = STATES["MENU"], STATES["MENU"]

quarks, singularity_size, required_quarks = 0, 6, 15
upgrade_count, auto_cps, upgrade_cost = 0, 0, 10

shake_mgr = particles.ShakeManager()
slide_panel = ui.SlidingPanel()
particles_list = []
menu_particles = [particles.CosmicDust(random.randint(0, config.WINDOW_WIDTH), random.randint(0, config.WINDOW_HEIGHT), False) for _ in range(120)]

# 4. БЕЗОПАСНАЯ ЗАГРУЗКА И ПЕРЕСОЗДАНИЕ ОКНА
saved_data = config.load_game()
if saved_data:
    quarks, upgrade_count = saved_data.get("quarks", 0), saved_data.get("upgrade_count", 0)
    auto_cps, upgrade_cost = saved_data.get("auto_cps", 0), saved_data.get("upgrade_cost", 10)
    current_state = saved_data.get("state", STATES["MENU"])
    screen = create_display()
    if current_state == STATES["GAME"]:
        slide_panel.activate(); slide_panel.current_x = config.SPACE_WIDTH

running = True
while running:
    # Честные физические координаты мыши без скейлинга
    mouse_x, mouse_y = pygame.mouse.get_pos()

    f_large = pygame.font.SysFont("Courier", int(config.WINDOW_HEIGHT * 0.05), bold=True)
    f_med = pygame.font.SysFont("Courier", int(config.WINDOW_HEIGHT * 0.035), bold=True)
    f_fps = pygame.font.SysFont("Courier", int(config.WINDOW_HEIGHT * 0.025), bold=True)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            config.save_game(quarks, current_state, upgrade_count, auto_cps, upgrade_cost); running = False
        
        if event.type == AUTO_SAVE_EVENT and current_state in [STATES["SINGULARITY"], STATES["GAME"]]:
            config.save_game(quarks, current_state, upgrade_count, auto_cps, upgrade_cost)
            
        if event.type == IDLE_TICK_EVENT and current_state == STATES["GAME"]:
            quarks += auto_cps
            if auto_cps > 0:
                for _ in range(upgrade_count * 2): 
                    particles_list.append(particles.CosmicDust(random.randint(50, config.SPACE_WIDTH - 50), random.randint(50, config.WINDOW_HEIGHT - 50), False))

        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            if current_state == STATES["GAME"] or current_state == STATES["SINGULARITY"]: current_state = STATES["PAUSE"]
            elif current_state == STATES["PAUSE"]: current_state = STATES["GAME"]

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            cx = config.WINDOW_WIDTH // 2
            bw = int(config.WINDOW_WIDTH * 0.25)
            if bw < 350: bw = 350
            bh = int(config.WINDOW_HEIGHT * 0.05)
            if bh < 45: bh = 45

            if current_state == STATES["MENU"]:
                if cx - bw//2 <= mouse_x <= cx + bw//2 and int(config.WINDOW_HEIGHT*0.48) <= mouse_y <= int(config.WINDOW_HEIGHT*0.48) + bh:
                    current_state = STATES["GAME"] if auto_cps > 0 or quarks > required_quarks else STATES["SINGULARITY"]
                elif cx - bw//2 <= mouse_x <= cx + bw//2 and int(config.WINDOW_HEIGHT*0.58) <= mouse_y <= int(config.WINDOW_HEIGHT*0.58) + bh:
                    prev_state, current_state = STATES["MENU"], STATES["SETTINGS"]

            elif current_state == STATES["SETTINGS"]:
                # Проверка кликов по 5 кнопкам настроек с динамическим шагом 9%
                for i in range(5):
                    y_p = int(config.WINDOW_HEIGHT * (0.23 + i * 0.09))
                    if cx - bw//2 <= mouse_x <= cx + bw//2 and y_p <= mouse_y <= y_p + bh:
                        if i == 0:
                            config.current_res_idx = (config.current_res_idx + 1) % len(config.RESOLUTIONS); config.update_system_settings()
                            pygame.display.quit(); pygame.display.init(); screen = create_display(); pygame.event.clear()
                        elif i == 1:
                            config.current_fps_idx = (config.current_fps_idx + 1) % len(config.FPS_OPTIONS); config.update_system_settings()
                        elif i == 2:
                            config.current_mode_idx = (config.current_mode_idx + 1) % len(config.SCREEN_MODES); config.update_system_settings()
                            pygame.display.quit(); pygame.display.init(); screen = create_display(); pygame.event.clear()

                        elif i == 3:
                            config.show_fps_counter = not config.show_fps_counter
                        elif i == 4:
                            config.current_lang_idx = (config.current_lang_idx + 1) % len(config.LANGUAGES); config.update_system_settings()

                # Кнопка НАЗАД в настройках
                if cx - 100 <= mouse_x <= cx + 100 and int(config.WINDOW_HEIGHT*0.78) <= mouse_y <= int(config.WINDOW_HEIGHT*0.78) + bh:
                    config.save_game(quarks, current_state, upgrade_count, auto_cps, upgrade_cost); current_state = prev_state

            elif current_state == STATES["SINGULARITY"]:
                line_x, line_y = config.WINDOW_WIDTH // 2, config.WINDOW_HEIGHT // 2
                if math.hypot(mouse_x - line_x, mouse_y - line_y) < singularity_size + 30:
                    quarks += 1; singularity_size += 2
                    if quarks >= required_quarks: current_state = STATES["BANG_SCENE"]

            elif current_state == STATES["GAME"] and slide_panel.current_x <= config.SPACE_WIDTH + 10:
                btn_y, btn_h = 170, 75
                btn_w = config.WINDOW_WIDTH - config.SPACE_WIDTH - 40
                x_pos = int(slide_panel.current_x)
                if (x_pos + 20) <= mouse_x <= (x_pos + 20) + btn_w and btn_y <= mouse_y <= btn_y + btn_h:
                    if quarks >= upgrade_cost:
                        quarks -= upgrade_cost; upgrade_count += 1; auto_cps += 1; upgrade_cost = int(upgrade_cost * 1.5)
                        for _ in range(15): particles_list.append(particles.CosmicDust(mouse_x, mouse_y, False))

            elif current_state == STATES["PAUSE"]:
                if cx - 150 <= mouse_x <= cx + 150 and int(config.WINDOW_HEIGHT*0.35) <= mouse_y <= int(config.WINDOW_HEIGHT*0.35) + 50: current_state = STATES["GAME"]
                elif cx - 150 <= mouse_x <= cx + 150 and int(config.WINDOW_HEIGHT*0.47) <= mouse_y <= int(config.WINDOW_HEIGHT*0.47) + 50: prev_state, current_state = STATES["PAUSE"], STATES["SETTINGS"]
                elif cx - 150 <= mouse_x <= cx + 150 and int(config.WINDOW_HEIGHT*0.59) <= mouse_y <= int(config.WINDOW_HEIGHT*0.59) + 50: config.save_game(quarks, current_state, upgrade_count, auto_cps, upgrade_cost); current_state = STATES["MENU"]

    if current_state == STATES["BANG_SCENE"]:
        shake_mgr.trigger(25, 60); cx, cy = config.SPACE_WIDTH // 2, config.WINDOW_HEIGHT // 2
        for _ in range(300): particles_list.append(particles.CosmicDust(cx, cy, True))
        slide_panel.activate(); current_state = STATES["GAME"]

    screen.fill(config.BLACK)
    
    if current_state in [STATES["MENU"], STATES["SETTINGS"]]:
        for p in menu_particles: p.update(config.WINDOW_WIDTH, mouse_x, mouse_y); p.draw(screen)
        ui.draw_menu_system(screen, current_state, f_large, mouse_x, mouse_y)
    elif current_state == STATES["SINGULARITY"]:
        cx, cy = config.WINDOW_WIDTH // 2, config.WINDOW_HEIGHT // 2
        pygame.draw.rect(screen, config.WHITE, (cx - singularity_size//2, cy - singularity_size//2, singularity_size, singularity_size))
        txt = f_med.render(config.get_text("singularity_tip"), True, config.CYAN)
        screen.blit(txt, (config.WINDOW_WIDTH//2 - txt.get_width()//2, cy + 60))
        score = f_med.render(config.get_text("density_label") + f"{quarks}/{required_quarks}", True, config.WHITE)
        screen.blit(score, (20, 20))
    elif current_state in [STATES["GAME"], STATES["PAUSE"]]:
        ox, oy = shake_mgr.get_offset()
        for p in particles_list[:]:
            p.update(config.SPACE_WIDTH); p.draw(screen, ox, oy)
            if p.life <= 0 and p.vx > 1: particles_list.remove(p)
        slide_panel.update(); slide_panel.draw(screen, quarks, auto_cps, upgrade_cost, upgrade_count, mouse_x, mouse_y)
        if current_state == STATES["PAUSE"]:
            ov = pygame.Surface((config.WINDOW_WIDTH, config.WINDOW_HEIGHT), pygame.SRCALPHA); ov.fill((0, 0, 0, 180)); screen.blit(ov, (0, 0))
            ui.draw_btn(screen, config.get_text("btn_resume"), "resume", config.WINDOW_WIDTH//2 - 150, int(config.WINDOW_HEIGHT*0.35), 300, 50, mouse_x, mouse_y)
            ui.draw_btn(screen, config.get_text("btn_settings"), "settings_p", config.WINDOW_WIDTH//2 - 150, int(config.WINDOW_HEIGHT*0.47), 300, 50, mouse_x, mouse_y)
            ui.draw_btn(screen, config.get_text("btn_to_menu"), "to_menu", config.WINDOW_WIDTH//2 - 150, int(config.WINDOW_HEIGHT*0.59), 300, 50, mouse_x, mouse_y)

    if config.show_fps_counter:
        fps_text = f_fps.render(f"FPS: {int(clock.get_fps())}", True, config.GREEN)
        screen.blit(fps_text, (config.WINDOW_WIDTH - fps_text.get_width() - 20, 20))

    pygame.display.flip(); clock.tick(config.FPS)



pygame.quit()
sys.exit()