import math
import pygame


def hologram_window(get_state, is_running, set_running):
    pygame.init()
    screen_width = 400
    screen_height = 400
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Mavis Hologram Interface")
    clock = pygame.time.Clock()

    try:
        import ctypes
        hwnd = pygame.display.get_wm_info()['window']
        ctypes.windll.user32.SetWindowPos(hwnd, -1, 0, 0, 0, 0, 0x0001 | 0x0002)
    except Exception:
        pass

    angle = 0

    while is_running():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                set_running(False)

        screen.fill((10, 10, 15))
        center_x = screen_width // 2
        center_y = screen_height // 2

        current_state = get_state()

        if current_state == "LISTENING":
            color = (255, 0, 50)
            dark_color = (60, 0, 10)
            speed = 0.06
            amp = 8
        elif current_state == "SPEAKING":
            color = (0, 255, 100)
            dark_color = (0, 60, 20)
            speed = 0.08
            amp = 12
        else:
            color = (0, 243, 255)
            dark_color = (0, 50, 60)
            speed = 0.02
            amp = 5

        pulse = int(math.sin(angle) * amp)
        base_radius = 80 + pulse

        pygame.draw.circle(screen, dark_color, (center_x, center_y), base_radius + 20, 2)
        pygame.draw.circle(screen, color, (center_x, center_y), base_radius, 4)
        pygame.draw.circle(screen, color, (center_x, center_y), base_radius - 30, 1)

        for i in range(0, 360, 45):
            rad = math.radians(i + (angle * 5))
            start_x = center_x + math.cos(rad) * (base_radius - 15)
            start_y = center_y + math.sin(rad) * (base_radius - 15)
            end_x = center_x + math.cos(rad) * (base_radius + 5)
            end_y = center_y + math.sin(rad) * (base_radius + 5)
            pygame.draw.line(screen, color, (start_x, start_y), (end_x, end_y), 2)

        angle += speed
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()