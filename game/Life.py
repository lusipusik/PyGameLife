import pygame
import copy
from Board import Board


class Life(Board):
    def __init__(self, width, height, left=10, top=10, cell_size=30):
        self.height = height
        self.width = width
        self.xmove = 0
        self.ymove = 0
        self.zoom = 0
        super().__init__(width, height, left, top, cell_size)

    def on_click(self, cell):
        self.board[cell[1]][cell[0]] = (self.board[cell[1]][cell[0]] + 1) % 2

    def render(self, screen):
        cell_size = self.cell_size + self.zoom
        for y in range(self.height):
            for x in range(self.width):
                if self.board[y][x]:
                    # живые клетки рисуем зелеными
                    pygame.draw.rect(screen, pygame.Color("green"),
                                     (x * cell_size + (self.left - self.zoom * self.width / 2) + self.xmove,
                                      y * cell_size + (self.top - self.zoom * self.height / 2) + self.ymove,
                                      cell_size,
                                      cell_size))
                pygame.draw.rect(screen, pygame.Color(255, 255, 255),
                                (x * cell_size + (self.left - self.zoom * self.width / 2) + self.xmove,
                                 y * cell_size + (self.top - self.zoom * self.height / 2) + self.ymove,
                                cell_size,
                                cell_size), 1)

    def next_move(self):
        tmp_board = copy.deepcopy(self.board)
        for y in range(self.height):
            for x in range(self.width):
                s = 0
                for dy in range(-1, 2):
                    for dx in range(-1, 2):
                        if x + dx < 0 or x + dx >= self.width or y + dy < 0 or y + dy >= self.height:
                            continue
                        s += self.board[y + dy][x + dx]
                s -= self.board[y][x]
                if s == 3:
                    tmp_board[y][x] = 1
                elif s < 2 or s > 3:
                    tmp_board[y][x] = 0
        self.board = copy.deepcopy(tmp_board)

    def xyz(self, xmove, ymove, zoom):
        self.xmove = xmove
        self.ymove = ymove
        self.zoom = zoom