#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# GNU GENERAL PUBLIC LICENSE. Version 3, 29 June 2007
# https://github.com/J-The-Fox/Circuit-Learning/

# -----=====[Imports]=====----- #
# Built-In Mdoules
import os
import sys
import time
import datetime
import inspect
import configparser
import json
import random
import warnings
import traceback
import _thread
# External Modules
import pygame # https://www.pygame.org/, https://github.com/pygame/pygame/, https://pypi.org/project/pygame/, 
import psutil # https://pypi.org/project/psutil/
import pygame_gui # https://github.com/MyreMylar/pygame_gui, https://pypi.org/project/pygame-gui/
import pygame_widgets # https://pypi.org/project/pygame-widgets/
# Custom Modules
import logger
import button
import debug
import pygame_debug
import menu
import network
from decorators import running_time
from utility import strtobool
from parts import *

# Main Class #
class Main(object):

    @running_time
    def __init__(self):
        # -----=====[Set Up A Timer]=====----- #
        self._timer = time.perf_counter()

        # -----=====[Set Up Configuration]=====----- #
        self._logging_config = configparser.ConfigParser()
        self._logging_config.read(os.path.join(os.path.dirname(__file__).replace("modules", "docs"), "configuration", "Logger.conf"))
        self._debug_config = configparser.ConfigParser()
        self._debug_config.read(os.path.join(os.path.dirname(__file__).replace("modules", "docs"), "configuration", "Debug.conf"))
        self._main_config = configparser.ConfigParser()
        self._main_config.read(os.path.join(os.path.dirname(__file__).replace("modules", "docs"), "configuration", "Main.conf"))

        # -----=====[Set Up Logging]=====----- #
        try:
            _log_path = self._logging_config.get("File", "path") # Check If A Log File Path Is Set In The Config File
        except configparser.NoOptionError: # If The Path Is Not Set, Use The Default Path
            _log_path = os.path.join(os.path.dirname(__file__).replace("modules", "docs"), "logs")

        self._logging = logger.Logger(
            mode=self._logging_config.getint("General", "logMode"),
            write_mode=self._logging_config.get("General", "writeMode"),
            format=str(self._logging_config.get("General", "format")).split("/"), # Turn The String Into A List Using "/" As The Delimiter
            date_format=self._logging_config.get("General", "dateFormat"),
            log_file=self._logging_config.get("File", "name"),
            log_file_path=_log_path,
            levelsShown=self._logging_config.get("General", "levelsShown").split("/"), # Turn The String Into A List Using "/" As The Delimiter
            use_color=self._logging_config.getboolean("General", "useColor")
        )

        # Make The Path If It Does Not Exist And If The Config Says It's Ok To Do So
        if os.path.exists(_log_path) is False and strtobool(self._logging_config.get("File", "createDirOnFail").capitalize().split(" ")[0]) == True: # Can't Use bool Because It Returns True For Any String That Is Not Empty So It Checks If It Is Equal To "True" Instead
            os.mkdir(_log_path)

        del _log_path # Delete The Log Path Variable To Save Memory

        self._logging.init(True) # Initialize The Logger
        self._logging.write("Starting Circuit Learning v{}.{}.{}{}, Build: {}...".format(self._main_config.getint("Version", "major"), self._main_config.getint("Version", "minor"), self._main_config.getint("Version", "bugFix"), self._main_config.get("Version", "release"), self._main_config.get("Version", "build")), lvl=logger.Logger.INFO)

        # Inform The User If They Are Using A Developmental, Beta, Or Pre-Release Build. These Builds Can Be Unstable And May Contain Bugs
        if "-dev" in self._main_config.get("Version", "release"):
            self._logging.write("This Is A Developmental Build. This Build Is Unstable!", lvl=logger.Logger.NOTICE)
        elif "-beta" in self._main_config.get("Version", "release"):
            self._logging.write("You Are Using A Beta Build. Some Things May Not Work As They Should Or Be Broken", lvl=logger.Logger.NOTICE)
        elif "-prerelase" in self._main_config.get("Version", "release"):
            self._logging.write("You Are Using A Pre-Release Build. Some Bugs May Still Be Present", lvl=logger.Logger.NOTICE)

        # -----=====[Set Up Pygame and Pygame GUI]=====----- #
        self._logging.write("Setting Up Pygame...", lvl=logger.Logger.INFO)
        pygame.init() # Initialize Pygame
        self._display_info = pygame.display.Info() # Get The Display Info

        # Set The Caption
        pygame.display.set_caption(self._main_config.get("Display", "caption"))

        # Set The Clock
        self._clock = pygame.time.Clock()
        self._fps = self._main_config.getint("Clock", "fps")

        # Set Full Screen Mode If fullscreen Is True
        if self._main_config.getboolean("Display", "fullscreen") == True:
            self._logging.write("Forcing Fullscreen Mode...", lvl=logger.Logger.INFO)
            self._logging.write(f"Screen Size Is ({self._display_info.current_w}, {self._display_info.current_h})", lvl=logger.Logger.DEBUG)
            self._screen = pygame.display.set_mode((self._display_info.current_w, self._display_info.current_h), pygame.FULLSCREEN)
        else:
            self._screen = pygame.display.set_mode((self._main_config.getint("Display", "width"), self._main_config.getint("Display", "height")), pygame.RESIZABLE) # Set The Screen Size
        
        # -----=====[Set Up Debug]=====----- #
        self._debug = pygame_debug.Debug(
            font=pygame.font.Font(os.path.join(os.path.dirname(__file__), "fonts", "tokeely-brookings", "Tokeely_Brookings.ttf").replace("modules", "docs"), 10),
            textSpacing=10,
            textColor=(243, 156, 41),
            backgroundTextColor="Black",
            debugTextScreenLocation="Top left",
            debugLogScreenLocation="Top right",
            logfile=os.path.join(os.path.dirname(__file__).replace("modules", "docs"), "logs", "Circuit_Learning.log")
        )

    @running_time
    def start_up_screen(self):
        alpha = 0
        fadeIn = True
        image = pygame.image.load(os.path.join(os.path.dirname(__file__).replace(os.path.dirname(__file__), "docs/images/icons"), "made_with_pygame.png")).convert_alpha()
        while True:
            self._screen.fill((0, 0, 0))

            # Fade In and Out
            if fadeIn is True and alpha <= 255:
                alpha += 5
            elif fadeIn is False and alpha > 0:
                alpha -= 5
            elif alpha > 255:
                fadeIn = False
            else:
                del fadeIn, alpha, image
                return
            image.set_alpha(alpha)

            # Display Image
            self._screen.blit(image, (self._screen.get_width()/ 2 - image.get_width() / 2, self._screen.get_height() / 2 - image.get_height() / 2))

            # Event Handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    self._logging.close(0)
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        pygame.quit()
                        self._logging.close(0)
                        sys.exit()

            self._debug.displayDebugText(True, [f"Current Date + Time: {datetime.datetime.now()}", f"Current Uptime: {round(time.perf_counter() - self._timer, 2)}", "", f"Ticks Per Second (TPS): {60}",  f"Frames Per Second (FPS): {round(self._clock.get_fps(), 2)}", "", f"Process PID: {os.getpid()}", f"RAM Usage: {psutil.Process(os.getpid()).memory_info()[0] / 1000000} Megabytes", f"Total RAM: {round((psutil.virtual_memory()[0] - psutil.virtual_memory()[0] / 8) / 1000000000, 2)} Gigabytes", f"Total Swap: {psutil.swap_memory()[0]} Bytes", f"Total Swap Used: {psutil.swap_memory()[0]} Bytes", f"CPU Usage: {psutil.cpu_percent()}%", "", f"Window Size: {self._screen.get_size()}", f"Mouse POS: {pygame.mouse.get_pos()}", f"Keys Pressed: {pygame_debug.parseKeysPressed(pygame.key.get_pressed())}", f"Mouse Buttons: {pygame.mouse.get_pressed()}", "", f"Current Function: {inspect.stack()[0][3]}", "", f"Playing Music: {pygame.mixer_music.get_busy()}", f"Playing Sound: {pygame.mixer.get_busy()}"])
            self._debug.displayLog(True, (800, 300))
            self._clock.tick(self._fps)
            pygame.display.update() # Update Screen

    @running_time
    def main_menu(self):
        _font = pygame.font.Font(os.path.join(os.path.dirname(__file__).replace("modules", "docs"), "fonts", "tokeely-brookings", "Tokeely_Brookings.ttf"), 100)
        while True:
            self._screen.fill((10, 10, 10))
            # Draw A Pattern On The Screen For The Background
            for x in range(0, self._screen.get_width(), 10):
                for y in range(0, self._screen.get_height(), 10):
                    pygame.draw.rect(self._screen, ((0, 0, 0)), pygame.rect.Rect(x, y, 5, 5))

            # Text
            self._screen.blit(_font.render("Circuit Learning", True, (255, 255, 255)), (self._screen.get_width() / 2 - _font.size("Circuit Learning")[0] / 2, self._screen.get_height() / 3.5 - _font.size("Circuit Learning")[1] / 2))

            # Pygame Events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self._logging.close(0)
                    pygame.quit()
                    sys.exit(0)
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        self._logging.close(0)
                        pygame.quit()
                        sys.exit(0)
            
            self._debug.displayDebugText(True, [f"Current Date + Time: {datetime.datetime.now()}", f"Current Uptime: {round(time.perf_counter() - self._timer, 2)}", "", f"Ticks Per Second (TPS): {60}",  f"Frames Per Second (FPS): {round(self._clock.get_fps(), 2)}", "", f"Process PID: {os.getpid()}", f"RAM Usage: {psutil.Process(os.getpid()).memory_info()[0] / 1000000} Megabytes", f"Total RAM: {round((psutil.virtual_memory()[0] - psutil.virtual_memory()[0] / 8) / 1000000000, 2)} Gigabytes", f"Total Swap: {psutil.swap_memory()[0]} Bytes", f"Total Swap Used: {psutil.swap_memory()[0]} Bytes", f"CPU Usage: {psutil.cpu_percent()}%", "", f"Window Size: {self._screen.get_size()}", f"Mouse POS: {pygame.mouse.get_pos()}", f"Keys Pressed: {pygame_debug.parseKeysPressed(pygame.key.get_pressed())}", f"Mouse Buttons: {pygame.mouse.get_pressed()}", "", f"Current Function: {inspect.stack()[0][3]}", "", f"Playing Music: {pygame.mixer_music.get_busy()}", f"Playing Sound: {pygame.mixer.get_busy()}"])
            self._debug.displayLog(True, (1000, 300))
            self._clock.tick(60)
            pygame.display.update()

if __name__ == "__main__":
    main = Main()
    main.start_up_screen()
    main.main_menu()
