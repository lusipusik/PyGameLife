import pygame
from Life import Life
from Board import Board

# class GameParameters:
#     def __init__(self):
#         self.window_width = 1000
#         self.window_height = 500
#         self.board_width=60
#         self.board_height=30
#         self.board_offset_left=80
#         self.board_offset_top=70
#         self.board_cell_size=40


def main():
    pygame.init()
    # params = GameParameters()
    screen = pygame.display.set_mode((2000, 1000))
    clock = pygame.time.Clock()
    pygame.display.set_caption('Игра «Жизнь»')
    board = Life(60, 30, 80, 70, 40)

    # Включено ли обновление поля
    time_on = False
    ticks = 0
    speed = 1
    xmove = 0
    ymove = 0
    zoom = 0
    running = True
    fps = 50

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 4:
                    zoom += 2
                elif event.button == 5:
                    zoom = max(zoom - 2, -30)
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                board.get_click(event.pos)
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                time_on = not time_on
            if event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
                speed += 1
            if event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
                speed -= 1
        
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

        if ticks >= speed:
            if time_on:
                board.next_move()
            ticks = -1
        ticks += 1

        screen.fill((0, 0, 0))
        board.render(screen)
        clock.tick(fps)
        pygame.display.flip()
        print('FLIP')
    
    pygame.quit()


if __name__ == '__main__':
    main()
