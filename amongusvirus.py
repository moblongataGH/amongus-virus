import pygame
import random
import os
import sys
import time
import ctypes

WINDOW_SIZE = (200, 200)
MOVE_DELAY = 0.1
DUPLICATE_INTERVAL = 10  # seconds
IMAGE_PATH = os.path.join(os.path.dirname(__file__), "images.png")  # Should be a PNG with transparency

def set_dpi_awareness():
    try:
        ctypes.windll.user32.SetProcessDPIAware()
    except Exception:
        pass

def get_screen_size():
    user32 = ctypes.windll.user32
    return user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)

def get_random_position():
    screen_w, screen_h = get_screen_size()
    x = random.randint(0, screen_w - WINDOW_SIZE[0])
    y = random.randint(0, screen_h - WINDOW_SIZE[1])
    return x, y

def move_window(hwnd, x, y):
    ctypes.windll.user32.MoveWindow(hwnd, x, y, WINDOW_SIZE[0], WINDOW_SIZE[1], True)

def get_hwnd():
    return pygame.display.get_wm_info()['window']

def set_window_always_on_top(hwnd):
    HWND_TOPMOST = -1
    SWP_NOMOVE = 0x0002
    SWP_NOSIZE = 0x0001
    SWP_SHOWWINDOW = 0x0040
    ctypes.windll.user32.SetWindowPos(hwnd, HWND_TOPMOST, 0, 0, 0, 0,
                                      SWP_NOMOVE | SWP_NOSIZE | SWP_SHOWWINDOW)

def duplicate():
    python = sys.executable
    os.spawnl(os.P_NOWAIT, python, python, __file__)

def load_amongus_image():
    try:
        img = pygame.image.load(IMAGE_PATH).convert_alpha()
        img = pygame.transform.smoothscale(img, WINDOW_SIZE)
        # Remove transparency by blitting onto a solid background
        visor_color = (192, 217, 223)
        solid_bg = pygame.Surface(WINDOW_SIZE)
        solid_bg.fill(visor_color)
        solid_bg.blit(img, (0, 0))
        # Convert to remove alpha channel
        solid_bg = solid_bg.convert()
        return solid_bg
    except Exception as e:
        print(f"Error loading image: {e}")
        return None

def main():
    set_dpi_awareness()
    pos = get_random_position()
    os.environ['SDL_VIDEO_WINDOW_POS'] = f"{pos[0]},{pos[1]}"

    pygame.init()
    screen = pygame.display.set_mode(WINDOW_SIZE)  # Use standard window frame
    pygame.display.set_caption("AMONG US WINDOW")
    hwnd = get_hwnd()
    move_window(hwnd, pos[0], pos[1])
    set_window_always_on_top(hwnd)

    amongus_img = load_amongus_image()
    if amongus_img is None:
        pygame.quit()
        sys.exit("Image not found.")

    clock = pygame.time.Clock()
    last_move = time.time()
    start_time = time.time()
    running = True

    visor_color = (192, 217, 223)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_BACKSPACE):
                duplicate()
                running = False

        screen.fill(visor_color)
        screen.blit(amongus_img, (0, 0))
        pygame.display.update()

        if time.time() - last_move > MOVE_DELAY:
            new_x, new_y = get_random_position()
            move_window(hwnd, new_x, new_y)
            last_move = time.time()

        if time.time() - start_time > DUPLICATE_INTERVAL:
            duplicate()
            start_time = time.time()

        clock.tick(30)

    pygame.quit()

if __name__ == "__main__":
    main()
