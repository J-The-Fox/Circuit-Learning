import sys
import os

import pygame

pygame.init()

# Draws A Sudoku Grid
class Grid_Test():
    def __init__(self):
        self.screen = pygame.display.set_mode((800, 600), pygame.RESIZABLE)
        self.clock = pygame.time.Clock()

    # def main(self):
    #     pygame.display.set_caption("Grid Test")
    #     while True:

    #         self.clock.tick(60)
    #         pygame.display.update()

    # def sudoku_grid(self):
        
        

if __name__ == "__main__":
    main = Grid_Test()
    main.main()
