import pygame
import tkinter as tk
from Life1 import Life
from Board1 import Board


def main():
    pygame.init()
    root = tk.Tk()
    monitors_width = root.winfo_screenwidth()
    monitors_height = root.winfo_screenheight()
    root.destroy()
    screen = pygame.display.set_mode((monitors_width, monitors_height - 90))
    clock = pygame.time.Clock()
    pygame.display.set_caption('Игра «Жизнь»')
    brd = Board(60, 30, 80, 70, 40)
    board = Life(60, 30, 80, 70, 40)

    # Включено ли обновление поля
    time_on = False
    ticks = 0
    speed = 10
    xmove = 0
    ymove = 0
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_d:
                xmove = xmove + 1
            if event.type == pygame.KEYDOWN and event.key == pygame.K_a:
                xmove = xmove - 1
            if event.type == pygame.KEYDOWN and event.key == pygame.K_s:
                ymove = ymove + 1
            if event.type == pygame.KEYDOWN and event.key == pygame.K_w:
                ymove = ymove - 1
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                board.get_click(event.pos)
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                time_on = not time_on
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 4:
                speed += 1
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 5:
                speed -= 1

        screen.fill((0, 0, 0))
        board.render(screen, xmove, ymove)
        print(ymove, xmove)
        brd.render(screen, xmove, ymove)
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