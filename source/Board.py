import pygame
import random


class Board:
    def __init__(self, width, height, left=10, top=10, cell_size=30):
        self.width = width
        self.height = height
        self.left = left
        self.top = top
        self.cell_size = cell_size
        self.xmove = 0
        self.ymove = 0
        self.zoom = 0

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

    def render(self, screen):
        cell_size = self.cell_size + self.zoom
        for y in range(self.height):
            for x in range(self.width):
                cell = self.board[y][x]
                color = (0, 0, 0)  # черный для пустых клеток

                if cell['type'] == 1:  # семечко - синий
                    color = (0, 0, 255)
                elif cell['type'] == 2:  # бутон - зеленый
                    color = (0, 255, 0)
                elif cell['type'] == 3:  # корень - коричневый
                    color = (139, 69, 19)

                pygame.draw.rect(screen, color,
                                 (x * cell_size + (self.left - self.zoom * self.width / 2) + self.xmove,
                                  y * cell_size + (self.top - self.zoom * self.height / 2) + self.ymove,
                                  cell_size,
                                  cell_size))
                pygame.draw.rect(screen, pygame.Color(255, 255, 255),
                                 (x * cell_size + (self.left - self.zoom * self.width / 2) + self.xmove,
                                  y * cell_size + (self.top - self.zoom * self.height / 2) + self.ymove,
                                  cell_size,
                                  cell_size), 1)

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
        self.xmove = xmove
        self.ymove = ymove
        self.zoom = zoom

    def get_cell(self, mouse_pos):
        cell_size = self.cell_size + self.zoom
        offset_x = (self.left - self.zoom * self.width / 2) + self.xmove
        offset_y = (self.top - self.zoom * self.height / 2) + self.ymove
        cell_x = (mouse_pos[0] - offset_x) // cell_size
        cell_y = (mouse_pos[1] - offset_y) // cell_size
        if cell_x < 0 or cell_x >= self.width or cell_y < 0 or cell_y >= self.height:
            return None
        return int(cell_x), int(cell_y)

    def get_click(self, mouse_pos):
        cell = self.get_cell(mouse_pos)
        if cell:
            self.on_click(cell)