import os
import sys

import pygame

class Part():

    def __init__(self) -> None:
        self.screen = pygame.display.set_mode((800, 600), pygame.RESIZABLE)
        self.clock = pygame.time.Clock()
    
    def main(self):
        while True:
            self.screen.fill((25, 25, 25))
            # Draw A Pattern On The Screen For The Background
            for x in range(0, self.screen.get_width(), 10):
                for y in range(0, self.screen.get_height(), 10):
                    pygame.draw.rect(self.screen, (20, 20, 20), pygame.rect.Rect(x, y, 5, 5))

            # Pygame Events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            
            self.clock.tick(60)
            pygame.display.update()

if __name__ == "__main__":
    main = Part()
    main.main()