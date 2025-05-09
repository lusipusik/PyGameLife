import pygame
import random


class Board:
    def __init__(self, width, height, left=10, top=10, cell_size=30):
        self.width = width
        self.height = height
        self.cell_size = cell_size
        self.zoom = 0
        self.offset_x = left
        self.offset_y = top

        # Инициализация доски с клетками, содержащими параметры
        self.board = [[{
            'type': 0,  # 0 - пусто, 1 - семечко, 2 - бутон, 3 - корень
            'energy': 0,
            'sun': random.randint(1, 3),
            'fertility': random.randint(1, 3),
            'age': 0,
            'next_sun_change': random.randint(10, 20)
        } for _ in range(width)] for _ in range(height)]

        self.set_view(left, top, cell_size)

    def render(self, screen, display_mode=1, zoom=0, camera_x=0, camera_y=0):
        # Текущий размер клетки с учетом масштаба
        current_cell_size = max(1, self.cell_size + zoom)  # Не меньше 1 пикселя

        # Рассчитываем общие размеры поля
        total_width = self.width * current_cell_size
        total_height = self.height * current_cell_size

        # Рассчитываем толщину линий в зависимости от масштаба
        border_width = max(1, int(1 - zoom * -0.05))  # Уменьшаем толщину при отдалении

        # Центрируем камеру
        screen_width, screen_height = screen.get_size()
        render_offset_x = (screen_width - total_width) // 2 + camera_x
        render_offset_y = (screen_height - total_height) // 2 + camera_y

        for y in range(self.height):
            for x in range(self.width):
                cell = self.board[y][x]

                # Координаты клетки на экране
                cell_x = x * current_cell_size + render_offset_x
                cell_y = y * current_cell_size + render_offset_y

                # Определяем цвет в зависимости от режима
                if display_mode == 1:  # Обычный режим
                    color = (0, 0, 0)  # По умолчанию черный
                    if cell['type'] == 1:
                        color = (0, 0, 200)  # Семечко - синий
                    elif cell['type'] == 2:
                        color = (0, 180, 0)  # Бутон - зеленый
                    elif cell['type'] == 3:
                        color = (139, 69, 19)  # Корень - коричневый

                elif display_mode == 2:  # Энергия (яркие синие оттенки)
                    intensity = min(255, max(0, cell['energy'] * 40))  # Увеличили множитель для большей яркости
                    color = (
                        intensity // 3,  # Добавляем немного красного
                        intensity // 3,  # Добавляем немного зеленого
                        intensity  # Основной синий канал
                    )

                elif display_mode == 3:  # Почва (коричневые оттенки)
                    intensity = min(255, max(0, cell['fertility'] * 25))
                    color = (intensity, intensity // 2, 0)

                elif display_mode == 4:  # Солнце (желтый)
                    intensity = min(255, max(0, cell['sun'] * 85))
                    color = (intensity, intensity, 0)

                # Рисуем клетку
                pygame.draw.rect(screen, color, (cell_x, cell_y, current_cell_size, current_cell_size))

                # Граница клетки
                border_color = (200, 200, 200) if cell['fertility'] > 3 else (100, 100, 100)
                pygame.draw.rect(screen, border_color,
                                 (cell_x, cell_y, current_cell_size, current_cell_size),
                                 border_width)  # Используем динамическую толщину

                # Эффект для очень плодородных клеток
                if display_mode == 1 and cell['fertility'] > 5:
                    glow_size = 2
                    glow_color = (
                        min(255, color[0] + 100),
                        min(255, color[1] + 100),
                        min(255, color[2] + 100)
                    )
                    pygame.draw.rect(screen, glow_color,
                                     (cell_x - glow_size, cell_y - glow_size,
                                      current_cell_size + glow_size * 2, current_cell_size + glow_size * 2),
                                     glow_size)

    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def on_click(self, cell):
        x, y = cell
        if self.board[y][x]['type'] == 0:  # только на пустые клетки
            self.board[y][x]['type'] = 1  # семечко
            self.board[y][x]['energy'] = 3  # начальная энергия

    def xyz(self, xmove, ymove, zoom):
        # Применяем перемещение
        self.offset_x += xmove
        self.offset_y += ymove

        # Сохраняем новый zoom
        old_zoom = self.zoom
        self.zoom = zoom

        # Корректируем смещение при изменении масштаба
        zoom_factor = (self.cell_size + self.zoom) / (self.cell_size + old_zoom)
        self.offset_x = self.offset_x * zoom_factor
        self.offset_y = self.offset_y * zoom_factor

        # Корректируем смещение при изменении масштаба
        if old_zoom != self.zoom:
            zoom_factor = (self.zoom - old_zoom) / (self.cell_size + old_zoom)
            self.xmove -= self.zoom_center_x * zoom_factor
            self.ymove -= self.zoom_center_y * zoom_factor

    def get_cell(self, mouse_pos):
        cell_size = self.cell_size + self.zoom
        offset_x = (self.left - self.zoom * self.width / 2) + self.xmove
        offset_y = (self.top - self.zoom * self.height / 2) + self.ymove
        cell_x = (mouse_pos[0] - offset_x) // cell_size
        cell_y = (mouse_pos[1] - offset_y) // cell_size
        if cell_x < 0 or cell_x >= self.width or cell_y < 0 or cell_y >= self.height:
            return None
        return int(cell_x), int(cell_y)

    def get_click(self, mouse_pos, zoom, camera_x, camera_y):
        current_cell_size = max(1, self.cell_size + zoom)
        total_width = self.width * current_cell_size
        total_height = self.height * current_cell_size

        screen_width, screen_height = pygame.display.get_surface().get_size()
        offset_x = (screen_width - total_width) // 2 + camera_x
        offset_y = (screen_height - total_height) // 2 + camera_y

        cell_x = int((mouse_pos[0] - offset_x) // current_cell_size)
        cell_y = int((mouse_pos[1] - offset_y) // current_cell_size)

        if 0 <= cell_x < self.width and 0 <= cell_y < self.height:
            self.on_click((cell_x, cell_y))