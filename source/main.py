import pygame
from Life import Life
from Board import Board

class GameParameters:
    window_width = pygame.display.Info().current_w - 20
    window_height = pygame.display.Info().current_h - 100
    board_width=60
    board_height=30
    board_offset_left=80
    board_offset_top=70
    board_cell_size=40


def main():
    pygame.init()
    screen = pygame.display.set_mode((GameParameters.monitors_width, GameParameters.monitors_height))
    clock = pygame.time.Clock()
    pygame.display.set_caption('Игра «Жизнь»')
    params = GameParameters()
    brd = Board(params.window_width, params.window_height,
                params.board_offset_left, params.board_offset_top,
                params.board_cell_size)
    board = Life(params.window_width, params.window_height,
                params.board_offset_left, params.board_offset_top,
                params.board_cell_size)

    # Включено ли обновление поля
    time_on = False
    ticks = 0
    speed = 10
    xmove = 0
    ymove = 0
    zoom = 0
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 4:
                    zoom += 2
                elif event.button == 5:
                    zoom -= 2
                    if zoom < -30:
                        zoom = -30
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                board.get_click(event.pos)
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                time_on = not time_on
            if event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
                speed += 1
            if event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
                speed -= 1
        brd.xyz(xmove, ymove, zoom)
        board.xyz(xmove, ymove, zoom)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            xmove = xmove + 3
        if keys[pygame.K_d]:
            xmove = xmove - 3
        if keys[pygame.K_w]:
            ymove = ymove + 3
        if keys[pygame.K_s]:
            ymove = ymove - 3
        screen.fill((0, 0, 0))
        board.render(screen)
        brd.render(screen)
        if ticks >= speed:
            if time_on:
                board.next_move()
            ticks = 0
        pygame.display.flip()
        clock.tick(150)
        ticks += 1
    pygame.quit()


if __name__ == '__main__':
    main()