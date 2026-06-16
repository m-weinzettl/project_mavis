import math
import pygame
import sys

pygame.init()

screen_width = 800
screen_height = 800
screen = pygame.display.set_mode((screen_width, screen_height), pygame.HIDDEN)

color_cyan = (0, 240, 255)
color_blue = (0, 100, 255)
color_dark = (0, 30, 50)
color_bg = (8, 8, 12)

screen.fill(color_bg)

cx, cy = screen_width // 2, screen_height // 2

for r in range(80, 380, 50):
    pygame.draw.circle(screen, (5, 20, 35), (cx, cy), r, 1)

pygame.draw.circle(screen, color_dark, (cx, cy), 160, 0)
pygame.draw.circle(screen, color_blue, (cx, cy), 160, 3)
pygame.draw.circle(screen, color_cyan, (cx, cy), 150, 2)

pygame.draw.circle(screen, color_cyan, (cx, cy), 50, 0)
pygame.draw.circle(screen, (255, 255, 255), (cx, cy), 25, 0)

pygame.draw.circle(screen, color_cyan, (cx, cy), 200, 1)

for i in range(0, 360, 15):
    rad = math.radians(i)
    x1 = cx + math.cos(rad) * 165
    y1 = cy + math.sin(rad) * 165
    x2 = cx + math.cos(rad) * 185
    y2 = cy + math.sin(rad) * 185
    pygame.draw.line(screen, color_cyan, (x1, y1), (x2, y2), 3)

for i in range(0, 360, 30):
    rad = math.radians(i + 15)
    x1 = cx + math.cos(rad) * 220
    y1 = cy + math.sin(rad) * 220
    x2 = cx + math.cos(rad) * 250
    y2 = cy + math.sin(rad) * 250
    pygame.draw.line(screen, color_blue, (x1, y1), (x2, y2), 4)

for i in range(0, 360, 2):
    if i % 20 < 10:
        rad = math.radians(i)
        pygame.draw.arc(screen, color_cyan, (cx - 290, cy - 290, 580, 580), rad, rad + 0.1, 3)

pygame.image.save(screen, "mavis_avatar.png")
pygame.quit()
sys.exit()