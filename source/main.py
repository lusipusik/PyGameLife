import pygame
from Life import Life


class GameParameters:
    def __init__(self):
        self.window_width = 1000
        self.window_height = 500
        self.board_width = 100
        self.board_height = 100
        self.board_cell_size = 30


def main():
    pygame.init()
    params = GameParameters()
    screen = pygame.display.set_mode((params.window_width, params.window_height))
    clock = pygame.time.Clock()
    pygame.display.set_caption('Игра «Жизнь» - Расширенная версия')

    # Инициализация доски без смещения (центрирование будет в render)
    board = Life(params.board_width, params.board_height,
                 cell_size=params.board_cell_size)

    # Параметры управления
    time_on = False
    ticks = 0
    speed = 2
    running = True
    fps = 50
    display_mode = 1

    # Параметры камеры
    camera_x = 0
    camera_y = 0
    zoom = 0
    move_speed = 5

    while running:
        # Обработка событий
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 4:  # колесо вверх - увеличение
                    zoom = min(zoom + 2, 20)  # Ограничиваем максимальный zoom
                elif event.button == 5:  # колесо вниз - уменьшение
                    zoom = max(zoom - 2, -26)  # Ограничиваем минимальный zoom
                elif event.button == 1:  # левая кнопка - добавление семечка
                    board.get_click(event.pos, zoom, camera_x, camera_y)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    time_on = not time_on
                elif event.key == pygame.K_UP:
                    speed = max(1, speed - 1)
                elif event.key == pygame.K_DOWN:
                    speed += 1
                elif event.key == pygame.K_1:
                    display_mode = 1
                elif event.key == pygame.K_2:
                    display_mode = 2
                elif event.key == pygame.K_3:
                    display_mode = 3
                elif event.key == pygame.K_4:
                    display_mode = 4
                elif event.key == pygame.K_c:  # Центрировать камеру
                    camera_x, camera_y = 0, 0
                    zoom = 0

        # Управление камерой
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            camera_x += move_speed
        if keys[pygame.K_d]:
            camera_x -= move_speed
        if keys[pygame.K_w]:
            camera_y += move_speed
        if keys[pygame.K_s]:
            camera_y -= move_speed

        # Обновление игры
        if ticks >= speed:
            if time_on:
                board.next_move()
            ticks = 0
        ticks += 1

        # Отрисовка
        screen.fill((0, 0, 0))
        board.render(screen, display_mode, zoom, camera_x, camera_y)

        # Отрисовка кнопок режимов (как в предыдущей версии)
        button_width = 100
        button_height = 30
        button_margin = 10
        buttons = [
            {"text": "Обычный (1)", "mode": 1},
            {"text": "Энергия (2)", "mode": 2},
            {"text": "Почва (3)", "mode": 3},
            {"text": "Солнце (4)", "mode": 4}
        ]

        font = pygame.font.SysFont('Arial', 16)
        for i, button in enumerate(buttons):
            rect = pygame.Rect(
                button_margin + (button_width + button_margin) * i,
                params.window_height - button_height - button_margin,
                button_width,
                button_height
            )
            color = (100, 100, 255) if button["mode"] == display_mode else (70, 70, 70)
            pygame.draw.rect(screen, color, rect)
            pygame.draw.rect(screen, (200, 200, 200), rect, 1)
            text = font.render(button["text"], True, (255, 255, 255))
            screen.blit(text, (rect.x + 5, rect.y + 5))

        # Информация об управлении
        info = [
            "Пробел: пауза",
            "ЛКМ: добавить семечко",
            "Колесо мыши: масштаб",
            "WASD: перемещение",
            "C: центрировать камеру",
            f"Скорость: {11 - speed}",
            "1-4: режимы отображения"
        ]
        for i, text in enumerate(info):
            screen.blit(font.render(text, True, (255, 255, 255)), (10, 10 + i * 20))

        pygame.display.flip()
        clock.tick(fps)

    pygame.quit()


if __name__ == '__main__':
    main()