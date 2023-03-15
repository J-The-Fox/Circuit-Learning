import os
import sys
import time
import json

import pygame



class Sprite():
    def __init__(self, image, x, y, width, height) -> None:
        self.image = image
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))