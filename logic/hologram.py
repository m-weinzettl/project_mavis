import math
import pygame
import random


def hologram_window(get_state, is_running, set_running):
    pygame.init()

    info = pygame.display.Info()
    screen_width = info.current_w
    screen_height = info.current_h

    flags = pygame.NOFRAME
    screen = pygame.display.set_mode((screen_width, screen_height), flags)
    pygame.display.set_caption("Mavis AI Cyberface")
    clock = pygame.time.Clock()

    try:
        import ctypes
        hwnd = pygame.display.get_wm_info()['window']
        ctypes.windll.user32.SetWindowPos(hwnd, -1, 0, 0, 0, 0, 0x0001 | 0x0002)
    except Exception:
        pass

    try:
        face_img = pygame.image.load("images/mavis_face_lisa.jpg")
        face_img = pygame.transform.smoothscale(face_img, (screen_width, screen_height))
    except Exception:
        face_img = None

    angle = 0
    scan_y = 0
    scan_dir = 1

    while is_running():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                set_running(False)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    set_running(False)

        screen.fill((5, 5, 10))
        current_state = get_state()

        if face_img:
            screen.blit(face_img, (0, 0))

        if current_state == "LISTENING":
            scan_y += scan_dir * 6
            if scan_y > screen_height or scan_y < 0:
                scan_dir *= -1
            pygame.draw.line(screen, (0, 240, 255), (0, scan_y), (screen_width, scan_y), 3)

            for _ in range(2):
                line_y = random.randint(0, screen_height)
                pygame.draw.line(screen, (0, 150, 200), (0, line_y), (screen_width, line_y), 1)

        elif current_state == "SPEAKING":
            points = []
            for x in range(0, screen_width, 15):
                wave = math.sin(x * 0.02 + angle * 5) * random.randint(20, 50)
                y = int(screen_height * 0.85) + int(wave)
                points.append((x, y))
            if len(points) > 1:
                pygame.draw.lines(screen, (0, 255, 150), False, points, 4)

            for _ in range(15):
                px = random.randint(0, screen_width)
                py = random.randint(0, screen_height)
                pygame.draw.circle(screen, (0, 255, 150), (px, py), random.randint(1, 3))

        else:
            overlay = pygame.Surface((screen_width, screen_height), pygame.SRCALPHA)
            pulse_alpha = int(12 + math.sin(angle) * 8)
            overlay.fill((0, 200, 255, pulse_alpha))
            screen.blit(overlay, (0, 0))

            for y in range(0, screen_height, 6):
                pygame.draw.line(screen, (0, 0, 0), (0, y), (screen_width, y), 1)

        angle += 0.05
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()