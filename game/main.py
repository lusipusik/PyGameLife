import pygame

def main():
    pygame.init()
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    clock = pygame.time.Clock()
    pygame.display.set_caption('Игра «Жизнь»')