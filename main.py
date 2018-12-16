import pygame
import win32api
import win32con
import win32gui
from ctypes import windll
import random as rnd
import math

SetWindowPos = windll.user32.SetWindowPos

size = (win32api.GetSystemMetrics(0), win32api.GetSystemMetrics(1))

pygame.init()
pygame.mixer.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode(size, pygame.NOFRAME) # For borderless, use pygame.NOFRAME
done = False
fuchsia = (200, 200, 200)  # Transparency color
white = (255, 255, 255)

snowy_sprt = pygame.image.load("snowy.png")
sparkle_anim = pygame.image.load("sparkle.png")
sparkle_size = (sparkle_anim.get_rect().size[1], sparkle_anim.get_rect().size[1])

# Set window transparency color
hwnd = pygame.display.get_wm_info()["window"]
win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE,
                       win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE) | win32con.WS_EX_LAYERED)
win32gui.SetLayeredWindowAttributes(hwnd, win32api.RGB(*fuchsia), 0, win32con.LWA_COLORKEY)

SetWindowPos(hwnd, -1, 0, 0, 0, 0, 0x0001)


class Snowy:
    def __init__(self, pos, size, vec):
        global sparkle_anim
        self.pos = pos
        self.size = size
        self.x_vector = 1
        self.x_coef = 1
        self.coef = vec
        self.is_sparkle = False
        self.wanna_be_sparkle = False
        self.anim = pygame.image.load("sparkle.png").convert_alpha()
        self.anim.fill((rnd.randint(128,254), rnd.randint(128,254), rnd.randint(128,254)), special_flags=pygame.BLEND_RGBA_MIN)
        self.image_index = 0
        self.image_index_vector = 1

    def logic(self):
        global size, sparkle_size
        self.pos = (self.pos[0] + self.get_x_ro(), self.pos[1] + 4)
        if self.pos[1] > size[1]:
            self.pos = (self.pos[0], self.pos[1] - size[1])
            if self.wanna_be_sparkle:
                self.is_sparkle = True
                self.wanna_be_sparkle = False
            else:
                self.is_sparkle = False
        if self.pos[0] > size[0]:
            self.pos = (self.pos[0] - size[0], self.pos[1])

        #Sparkle logic
        self.image_index += 0.2 * self.image_index_vector * self.coef
        if self.image_index >= int(self.anim.get_rect()[2] / sparkle_size[0]) or self.image_index <= 0:
            self.image_index_vector *= -1


    def get_x_ro(self):
        result = math.sin(self.x_coef)
        self.x_coef += 0.05 * self.coef * self.x_vector

        return result

    def draw(self, screen):
        global sparkle_anim, snowy_sprt, sparkle_size
        if not self.is_sparkle:
            screen.blit(snowy_sprt, (self.pos[0], self.pos[1]))
        else:
            index = max(0, min(int(self.anim.get_rect()[2] / 9)-1, self.image_index))
            screen.blit(self.anim, (self.pos[0], self.pos[1]),
                        (int(index) * sparkle_size[0], 0, sparkle_size[0], sparkle_size[1]))




snowies = []
for _ in range(100):
    snowies.append(Snowy((rnd.randrange(0,2000), rnd.randrange(-1000,0)), rnd.uniform(0,3), rnd.uniform(0,2)))

pygame.mixer.music.load('4.mp3')
#pygame.mixer.music.load('Sparkle.mp3')
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.01)
sparkle_ticks = 0
sparkle_time = 120

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    screen.fill(fuchsia)  # Transparent background
    for s in snowies:
        s.logic()
        s.draw(screen)
    pygame.display.update()
    clock.tick(30)
    sparkle_ticks += 1
    if sparkle_ticks == 30 * sparkle_time:
        sparkle_ticks = 0
        sound = pygame.mixer.Sound('Sparkle.wav')
        sound.set_volume(0.03)
        sound.play()
        for i in range(len(snowies)):
            if rnd.randrange(0,2) == 0:
                snowies[i].wanna_be_sparkle = True

