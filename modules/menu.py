# Built-In Modules
import os
import sys
# External Modules
import pygame

class Radio():

    def __init__(self, name: str, num_options: int, location: tuple, size: tuple, color: str = "white", hoverColor: str = "black", borderRadius: int | float = 5) -> None:
        """
        Creates A New Radio Button
        """

        self.surface = pygame.display.get_surface()

        self.name = name
        self.num_options = num_options
        self.location = location
        self.size = size
        self.color = color
        self.hoverColor = hoverColor
        self.currentColor = color
        self.borderRadius = borderRadius
        self.options = []
        self.selected = None

    def display(self) -> None:
        """
        Displays The Radio Button On The Current Surface
        """
        for option in self.options:
            option.display()
    
    def addOption(self, option: str) -> None:
        """
        Adds An Option To The Radio Button
        """
        # self.options.append(RadioOption(option, self, len(self.options)))
        pass

    def getSelected(self) -> str:
        """
        Returns The Currently Selected Option
        """

        return self.selected

class DropDown():

    def __init__(self, name: str, num_options: int, location: tuple, size: tuple, color: str = "white", hoverColor: str = "grey", borderRadius: int | float = 5) -> None:
        """
        Creates A New Drop Down Menu
        """

        self.surface = pygame.display.get_surface()

        self.name = name
        self.num_options = num_options
        self.location = location
        self.size = size
        self.color = color
        self.hoverColor = hoverColor
        self.currentColor = color
        self.borderRadius = borderRadius
        self.options = []
        self.selected = None

    def display(self) -> None:
        """
        Displays The Drop Down Menu On The Current Surface
        """
        
        pass
        