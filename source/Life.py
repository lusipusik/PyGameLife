import pygame
import random
from Board import Board


class Life(Board):
    def __init__(self, width, height, left=10, top=10, cell_size=30):
        super().__init__(width, height, left, top, cell_size)
        # Инициализируем плодородность от 1 до 3
        for y in range(self.height):
            for x in range(self.width):
                self.board[y][x]['fertility'] = random.randint(1, 3)

    def distribute_fertility(self, x, y, excess):
        """Распределяет избыточную плодородность на соседние клетки"""
        neighbors = []
        for dy in [-1, 0, 1]:
            for dx in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue
                nx, ny = x + dx, y + dy
                if 0 <= nx < self.width and 0 <= ny < self.height:
                    neighbors.append((nx, ny))

        if not neighbors:
            return

        per_neighbor = excess // len(neighbors)
        remainder = excess % len(neighbors)

        for nx, ny in neighbors:
            self.board[ny][nx]['fertility'] += per_neighbor

        for i in range(remainder):
            nx, ny = neighbors[i]
            self.board[ny][nx]['fertility'] += 1

    def next_move(self):
        # Обновляем солнце
        for y in range(self.height):
            for x in range(self.width):
                cell = self.board[y][x]
                cell['next_sun_change'] -= 1
                if cell['next_sun_change'] <= 0:
                    cell['sun'] = random.randint(2, 3)  # Солнце 2 или 3
                    cell['next_sun_change'] = random.randint(8, 12)

        new_board = [[cell.copy() for cell in row] for row in self.board]
        total_energy = 0  # Для контроля сохранения энергии

        for y in range(self.height):
            for x in range(self.width):
                cell = self.board[y][x]
                new_cell = new_board[y][x]

                # Обработка переполнения плодородности
                if cell['fertility'] > 3:
                    excess = cell['fertility'] - 3
                    new_cell['fertility'] = 3
                    self.distribute_fertility(x, y, excess)

                # Обработка семечка
                if cell['type'] == 1:
                    new_cell['type'] = 2  # бутон
                    new_cell['energy'] = 3  # Энергия сохраняется
                    new_cell['age'] = 0

                # Обработка бутона
                elif cell['type'] == 2:
                    new_cell['age'] += 1
                    total_energy += cell['energy']

                    # Смерть при отрицательной энергии
                    if cell['energy'] < 0:
                        new_cell['type'] = 0
                        new_cell['fertility'] += 1  # Возвращаем часть энергии в почву
                        continue

                    # Трата энергии (1 единица каждые 4 хода после 5 ходов)
                    if cell['age'] >= 5 and cell['age'] % 4 == 0:
                        new_cell['energy'] -= 1

                    # Создание корня требует 1 энергии и даёт +1 к плодородности
                    if cell['energy'] >= 1:
                        max_fertility = -1
                        best_pos = None
                        for dy, dx in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                            ny, nx = y + dy, x + dx
                            if 0 <= ny < self.height and 0 <= nx < self.width:
                                neighbor = self.board[ny][nx]
                                if neighbor['type'] == 0 and neighbor['fertility'] > max_fertility:
                                    max_fertility = neighbor['fertility']
                                    best_pos = (ny, nx)

                        if best_pos is not None:
                            ny, nx = best_pos
                            new_board[ny][nx]['type'] = 3
                            new_board[ny][nx]['energy'] = 0
                            new_cell['energy'] -= 1
                            new_board[ny][nx]['fertility'] += 1

                    # Размножение требует 2 энергии
                    if cell['energy'] >= 2:
                        attempts = 5
                        while attempts > 0:
                            attempts -= 1
                            dy = random.randint(-3, 3)
                            dx = random.randint(-3, 3)
                            ny, nx = y + dy, x + dx
                            if 0 <= ny < self.height and 0 <= nx < self.width:
                                target = new_board[ny][nx]
                                if target['type'] == 0:
                                    target['type'] = 1
                                    target['energy'] = 3
                                    new_cell['energy'] -= 2  # Четко 2 энергии на размножение
                                    break
                                else:
                                    target['fertility'] += 1
                                    new_cell['energy'] -= 2
                                    break

                # Обработка корня
                elif cell['type'] == 3:
                    has_bud = False

                    for dy, dx in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                        ny, nx = y + dy, x + dx
                        if 0 <= ny < self.height and 0 <= nx < self.width:
                            if self.board[ny][nx]['type'] == 2:
                                has_bud = True
                                if cell['fertility'] > 0:
                                    energy_gain = min(cell['sun'], cell['fertility'])
                                    new_cell['fertility'] -= energy_gain
                                    new_board[ny][nx]['energy'] += energy_gain
                                break

                    if not has_bud:
                        new_cell['type'] = 0
                        new_cell['fertility'] += 1

        self.board = new_board