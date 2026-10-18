import pygame
import sys
import random
import math

# Инициализация
pygame.init()
WIDTH, HEIGHT = 900, 600 # Немного расширили окно для панели апгрейдов
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Universe Idle: Эволюция Материи v0.3")

# Цвета
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
CYAN = (0, 255, 255)
ORANGE = (255, 165, 0)
GRAY = (50, 50, 50)
LIGHT_GRAY = (80, 80, 80)

clock = pygame.time.Clock()
font = pygame.font.SysFont("Courier", 20, bold=True)
font_large = pygame.font.SysFont("Courier", 24, bold=True)

# Игровой баланс и ресурсы
quarks = 0
singularity_size = 4
big_bang_triggered = False
required_quarks = 15

# Параметры автоматизации (Idle)
auto_cps = 0  # Сколько кварков капает в секунду автоматически
upgrade_cost = 10
upgrade_count = 0

# Таймер для ежесекундного начисления
pygame.time.set_timer(pygame.USEREVENT, 1000)

# Класс для взрыва и фоновой космической пыли
class CosmicDust:
    def __init__(self, x, y, is_explosion=True):
        self.x = x
        self.y = y
        angle = random.uniform(0, 2 * math.pi)
        if is_explosion:
            speed = random.uniform(2, 7)
            self.life = random.randint(40, 80)
        else:
            # Спокойное ленивое движение пыли в космосе
            speed = random.uniform(0.2, 1)
            self.life = random.randint(200, 400)
            
        self.vx = math.cos(angle) * speed
        self.vy = math.sin(angle) * speed
        self.color = random.choice([WHITE, CYAN, ORANGE])

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.life -= 1
        
        # Отражение от стенок для фоновой пыли (чтобы не улетала за экран)
        if self.x < 0 or self.x > 650: self.vx *= -1
        if self.y < 0 or self.y > HEIGHT: self.vy *= -1

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, (int(self.x), int(self.y), 2, 2))

particles = []

running = True
while running:
    # 1. ОБРАБОТКА ВВОДА
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
        # Таймер: срабатывает раз в секунду
        if event.type == pygame.USEREVENT and big_bang_triggered:
            quarks += auto_cps
            # Каждую секунду от работающих сил рождается немного новой фоновой пыли
            for _ in range(upgrade_count * 2):
                particles.append(CosmicDust(random.randint(50, 600), random.randint(50, 550), is_explosion=False))

        # Клики мыши
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_x, mouse_y = event.pos
            
            # --- ЛОГИКА ДО ВЗРЫВА ---
            if not big_bang_triggered:
                center_x, center_y = 325, HEIGHT // 2 # Центр космического экрана (до 650px)
                distance = math.hypot(mouse_x - center_x, mouse_y - center_y)
                if distance < singularity_size + 20:
                    quarks += 1
                    singularity_size += 2
                    if quarks >= required_quarks:
                        big_bang_triggered = True
                        for _ in range(200):
                            particles.append(CosmicDust(center_x, center_y, is_explosion=True))
                            
            # --- ЛОГИКА ПОСЛЕ ВЗРЫВА (МАГАЗИН) ---
            else:
                # Проверяем клик по кнопке апгрейда (Кнопка находится в правой панели)
                if 670 <= mouse_x <= 880 and 150 <= mouse_y <= 210:
                    if quarks >= upgrade_cost:
                        quarks -= upgrade_cost
                        upgrade_count += 1
                        auto_cps += 1
                        upgrade_cost = int(upgrade_cost * 1.5) # Цена растет по-канонам Idle игр!

    # 2. ЛОГИКА ИГРЫ
    for p in particles[:]:
        p.update()
        if p.life <= 0:
            particles.remove(p)

    # 3. ОТРИСОВКА
    screen.fill(BLACK)
    
    # Разделительная линия между космосом и меню апгрейдов
    pygame.draw.line(screen, GRAY, (650, 0), (650, HEIGHT), 3)

    # --- ЛЕВАЯ СТОРОНА: КОСМОС ---
    if not big_bang_triggered:
        # Сингулярность
        pygame.draw.rect(screen, WHITE, (325 - singularity_size//2, HEIGHT//2 - singularity_size//2, singularity_size, singularity_size))
        tip_text = font.render("КЛИКАЙ ДЛЯ СЖАТИЯ ЭНЕРГИИ", True, CYAN)
        screen.blit(tip_text, (325 - tip_text.get_width() // 2, HEIGHT // 2 + 50))
    else:
        # Отрисовка взрыва и пыли
        for p in particles:
            p.draw(screen)
            
        # Статус эпохи
        status_text = font.render("ЭПОХА: КВАРКОВЫЙ СУП", True, CYAN)
        screen.blit(status_text, (20, HEIGHT - 40))

    # --- ПРАВАЯ СТОРОНА: ИНТЕРФЕЙС И АПГРЕЙДЫ ---
    # Ресурсы
    ui_title = font_large.render("ВСЕЛЕННАЯ", True, WHITE)
    screen.blit(ui_title, (670, 20))
    
    ui_quarks = font.render(f"Кварки: {quarks}", True, WHITE)
    screen.blit(ui_quarks, (670, 60))
    
    ui_cps = font.render(f"Авто-доход: +{auto_cps}/сек", True, CYAN)
    screen.blit(ui_cps, (670, 90))

    # Кнопка Апгрейда (появляется только после Большого взрыва)
    if big_bang_triggered:
        # Проверяем, хватает ли денег на кнопку для подсветки
        button_color = LIGHT_GRAY if quarks >= upgrade_cost else GRAY
        pygame.draw.rect(screen, button_color, (670, 150, 210, 60)) # Тело кнопки
        pygame.draw.rect(screen, WHITE, (670, 150, 210, 60), 2)     # Рамка
        
        btn_text1 = font.render("Сильное Взаимод.", True, WHITE)
        btn_text2 = font.render(f"Цена: {upgrade_cost} Кв.", True, ORANGE)
        screen.blit(btn_text1, (680, 155))
        screen.blit(btn_text2, (680, 180))
        
        # Статистика купленного
        owned_text = font.render(f"Куплено сил: {upgrade_count}", True, WHITE)
        screen.blit(owned_text, (670, 230))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()