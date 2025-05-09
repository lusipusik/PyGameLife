import pygame
from Life import Life


class GameParameters:
    def __init__(self):
        self.window_width = 1000
        self.window_height = 500
        self.board_width = 100
        self.board_height = 30
        self.board_offset_left = -400
        self.board_offset_top = -200
        self.board_cell_size = 30


def main():
    pygame.init()
    params = GameParameters()
    screen = pygame.display.set_mode((params.window_width, params.window_height))
    clock = pygame.time.Clock()
    pygame.display.set_caption('Игра «Жизнь» - Расширенная версия')
    board = Life(params.board_width, params.board_height, params.board_offset_left, params.board_offset_top,
                 params.board_cell_size)

    time_on = False
    ticks = 0
    speed = 2
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
                if event.button == 4:  # колесо вверх - увеличение
                    zoom += 2
                elif event.button == 5:  # колесо вниз - уменьшение
                    zoom = max(zoom - 2, -26)
                elif event.button == 1:  # левая кнопка - добавление семечка
                    board.get_click(event.pos)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    time_on = not time_on
                elif event.key == pygame.K_UP:
                    speed = max(1, speed - 1)
                elif event.key == pygame.K_DOWN:
                    speed += 1

        board.xyz(xmove, ymove, zoom)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            xmove += 3
        if keys[pygame.K_d]:
            xmove -= 3
        if keys[pygame.K_w]:
            ymove += 3
        if keys[pygame.K_s]:
            ymove -= 3

        if ticks >= speed:
            if time_on:
                board.next_move()
            ticks = 0
        ticks += 1

        screen.fill((0, 0, 0))
        board.render(screen)

        # Отображение информации о управлении
        font = pygame.font.SysFont('Arial', 16)
        info_text = [
            "Пробел: пауза/продолжить",
            "ЛКМ: добавить семечко",
            "Колесо мыши: масштаб",
            "WASD: перемещение по полю",
            "Стрелки вверх/вниз: скорость",
            f"Скорость: {11 - speed}"
        ]
        for i, text in enumerate(info_text):
            text_surface = font.render(text, True, (255, 255, 255))
            screen.blit(text_surface, (10, 10 + i * 20))

        pygame.display.flip()
        clock.tick(fps)

    pygame.quit()


if __name__ == '__main__':
    main()