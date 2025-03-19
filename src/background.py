import pygame
import os
import time

class Background:
    def __init__(self, image_folder):
        self.frames = self.load_frames(image_folder)
        self.frame_index = 0
        self.frame_delay = 0.1  # Delay between frames in seconds
        self.last_time = time.time()

    def load_frames(self, folder):
        frames = []
        for filename in sorted(os.listdir(folder)):
            if filename.endswith('.png'):
                frame_path = os.path.join(folder, filename)
                frame_image = pygame.image.load(frame_path)
                frames.append(frame_image)
                print(f"Loaded frame: {frame_path}")
        return frames

    def update(self):
        current_time = time.time()
        if current_time - self.last_time >= self.frame_delay:
            self.frame_index = (self.frame_index + 1) % len(self.frames)
            self.last_time = current_time

    def draw(self, screen):
        screen.blit(self.frames[self.frame_index], (0, 0))

# Initialize Pygame and the screen
pygame.init()
screen = pygame.display.set_mode((1600, 1000))
clock = pygame.time.Clock()

# Create a Background object with the path to the folder containing the frames
background = Background(r'C:\Users\CHRISTIAN\OneDrive\Documents\Projects\Pokemon Guessing Game\src\images\GIF frames')

# Game loop
running = True
while running:
    screen.fill((0, 0, 0))  # Optional: Clear screen with black color

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    background.update()  # Update to the next frame
    background.draw(screen)  # Draw the current frame

    pygame.display.flip()  # Update the display
    clock.tick(60)  # Limit frame rate to 60 FPS

pygame.quit()
