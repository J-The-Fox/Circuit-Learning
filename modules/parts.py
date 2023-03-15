import os
import sys

import pygame

class Part():

    def __init__(self) -> None:
        self.surface = pygame.display.get_surface()
        pass

    def create(self):
        """
        Creates A New Part
        """
