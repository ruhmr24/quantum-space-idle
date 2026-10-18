import pygame
import random
import math
import config

class CosmicDust:
    def __init__(self, x, y, is_explosion=True):
        self.x, self.y = x, y
        angle = random.uniform(0, 2 * math.pi)
        speed = random.uniform(3, 9) if is_explosion else random.uniform(0.3, 1.2)
        self.life = random.randint(40, 70) if is_explosion else random.randint(200, 350)
        self.vx, self.vy = math.cos(angle) * speed, math.sin(angle) * speed
        self.color = random.choice([config.WHITE, config.CYAN, config.ORANGE])
        self.size = random.choice([2, 3])

    def update(self, space_width, mx=None, my=None):
        if mx is not None and my is not None:
            dist = math.hypot(self.x - mx, self.y - my)
            if dist < 100:
                angle = math.atan2(self.y - my, self.x - mx)
                force = (100 - dist) * 0.02
                self.vx += math.cos(angle) * force
                self.vy += math.sin(angle) * force
        
        if mx is not None:  # Если это частица в меню, добавляем трение
            self.vx *= 0.98
            self.vy *= 0.98

        self.x += self.vx
        self.y += self.vy
        self.life -= 1
        
        if self.x < 0 or self.x > space_width: self.vx *= -1
        if self.y < 0 or self.y > config.WINDOW_HEIGHT: self.vy *= -1

    def draw(self, surface, offset_x=0, offset_y=0):
        pygame.draw.rect(surface, self.color, (int(self.x + offset_x), int(self.y + offset_y), self.size, self.size))

class ShakeManager:
    def __init__(self): self.intensity, self.duration = 0, 0
    def trigger(self, intensity, duration): self.intensity, self.duration = intensity, duration
    def get_offset(self):
        if self.duration > 0:
            self.duration -= 1
            curr_int = self.intensity * (self.duration / 60.0)
            if curr_int < 1: curr_int = 1
            return random.uniform(-curr_int, curr_int), random.uniform(-curr_int, curr_int)
        return 0, 0
