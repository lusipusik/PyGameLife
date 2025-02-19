import pygame
import tkinter as tk
from Life1 import Life


def main():
    pygame.init()
    root = tk.Tk()
    monitors_width = root.winfo_screenwidth()
    monitors_height = root.winfo_screenheight()
    root.destroy()
    screen = pygame.display.set_mode((monitors_width, monitors_height - 25))
    clock = pygame.time.Clock()
    pygame.display.set_caption('Игра «Жизнь»')

    board = Life(30, 30, 10, 10, 15)

    # Включено ли обновление поля
    time_on = False
    ticks = 0
    speed = 10

    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                board.get_click(event.pos)
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE or event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
                time_on = not time_on
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 4:
                speed += 1
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 5:
                speed -= 1

        screen.fill((0, 0, 0))
        board.render(screen)
        if ticks >= speed:
            if time_on:
                board.next_move()
            ticks = 0
        pygame.display.flip()
        clock.tick(100)
        ticks += 1
    pygame.quit()


if __name__ == '__main__':
    main()