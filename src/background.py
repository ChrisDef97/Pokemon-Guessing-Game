import pygame

class Background:
    def __init__(self, image_path):
        self.image = pygame.image.load(image_path)

    def draw(self, screen):
        screen.blit(self.image, (0, 0))
