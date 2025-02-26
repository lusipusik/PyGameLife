import pygame
import tkinter as tk


class Board:

    def __init__(self, width, height, left=10, top=10, cell_size=30):
        root = tk.Tk()
        monitors_width = root.winfo_screenwidth()
        monitors_height = root.winfo_screenheight()
        root.destroy()
        self.width = width
        self.height = height
        self.board = [[0] * width for _ in range(height)]
        self.left = 0
        self.top = 0
        self.cell_size = 0
        self.xmove = 0
        self.ymove = 0
        self.zoom = 0
        self.set_view(left, top, cell_size)

    def render(self, screen):
        cell_size = self.cell_size + self.zoom
        for y in range(self.height):
            for x in range(self.width):
                pygame.draw.rect(screen, pygame.Color(255, 255, 255),
                                 (x * cell_size + (self.left - self.zoom * self.width / 2) + self.xmove,
                                  y * cell_size + (self.top - self.zoom * self.height / 2) + self.ymove,
                                  cell_size,
                                  cell_size), 1)

    # настройка внешнего вида
    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    # cell - кортеж (x, y)
    def on_click(self, cell):
        # заглушка для реальных игровых полей
        pass
    def xyz(self, xmove, ymove, zoom):
        self.xmove = xmove
        self.ymove = ymove
        self.zoom = zoom

    def get_cell(self, mouse_pos):
        cell_size = self.cell_size + self.zoom  # текущий размер клетки с зумом
        # Корректируем смещение центра поля при зуме
        offset_x = (self.left - self.zoom * self.width / 2) + self.xmove
        offset_y = (self.top - self.zoom * self.height / 2) + self.ymove
        # Вычисляем координаты клетки
        cell_x = (mouse_pos[0] - offset_x) // cell_size
        cell_y = (mouse_pos[1] - offset_y) // cell_size
        # Проверка границ
        if cell_x < 0 or cell_x >= self.width or cell_y < 0 or cell_y >= self.height:
            return None
        return int(cell_x), int(cell_y)

    def get_click(self, mouse_pos):
        cell = self.get_cell(mouse_pos)
        if cell:
            self.on_click(cell)


