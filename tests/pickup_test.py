# Built-In Modules
import sys
# External Modules
import pygame

pygame.init()    

class Pickup():

    def __init__(self) -> None:
        self.screen = pygame.display.set_mode((800, 600), pygame.RESIZABLE)
        self.clock = pygame.time.Clock()
    def main(self):
        diode = pygame.rect.Rect(0, 0, 100, 100)
        pygame.display.set_caption("Pickup Test")
        while True:
            self.screen.fill((25, 25, 25))
            # Draw A Pattern On The Screen For The Background
            for x in range(0, self.screen.get_width(), 10):
                for y in range(0, self.screen.get_height(), 10):
                    pygame.draw.rect(self.screen, (20, 20, 20), pygame.rect.Rect(x, y, 5, 5))

            pygame.draw.rect(self.screen, (243, 156, 41), diode)

            if diode.collidepoint(pygame.mouse.get_pos()):
                pygame.draw.rect(self.screen, (255, 255, 255), diode, 3)

            # Move The Diode When The Mouse Is Clicked
            if pygame.mouse.get_pressed()[0] and diode.collidepoint(pygame.mouse.get_pos()):
                diode.center = pygame.mouse.get_pos()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.clock.tick(60)
            pygame.display.update()

if __name__ == "__main__":
    main = Pickup()
    main.main()