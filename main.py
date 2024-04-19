from PIL import Image
from queue import Queue
import random
import pygame
import pygame.image
import threading
import os

import track


def generate(bg_path, inner_path):
    background = Image.open(bg_path)
    inner = Image.open(inner_path)

    bg_w, bg_h = background.size
    img_w, img_h = inner.size

    new_x = random.randint(0, bg_w - img_w)
    new_y = random.randint(0, bg_h - img_h)

    background.paste(inner, (new_x, new_y))
    background.save("output.png")

    return new_x, new_y


def main():
    pygame.init()

    padding = 128
    cursor = (0, 0)
    hidden_x, hidden_y = generate("background.jpg", "faces/yaron.jpg")
    running = True

    background = pygame.image.load("output.png")
    width = background.get_width()
    height = background.get_height()
    screen = pygame.display.set_mode((width, height))
    screen.blit(background, (0, 0))
    pygame.display.flip()

    tracker_share = Queue()
    tracker_thread = threading.Thread(target=track.capture_thread, args=(tracker_share, width, height), daemon=True)
    tracker_thread.start()

    while running:
        event = pygame.event.poll()

        if event.type == pygame.QUIT:
            running = False
            continue

        try:
            cursor = tracker_share.get_nowait()

            screen.blit(background, (0, 0))
            screen.fill("red", (cursor, (8, 8)))
            pygame.display.flip()
        except Exception:
            continue

        if cursor[0] >= hidden_x - padding \
            and cursor[1] >= hidden_y - padding \
            and cursor[0] <= hidden_x + 64 + padding \
            and cursor[1] <= hidden_y + 64 + padding:

            hidden_x, hidden_y = generate("background.jpg", "faces/yaron.jpg")

            background = pygame.image.load("output.png")
            screen.blit(background, (0, 0))
            pygame.display.flip()

    os.remove("output.png")
    pygame.quit()


if __name__ == "__main__":
    main()
