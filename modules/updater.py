"""
This Is The Screen That Will Be Shown When The Actual Program Is Updating
"""

# Built-In Modules
import os
import sys
import json
import _thread
import locale
import configparser
# External Modules
import pygame
import requests
import psutil
# Custom Modules
import logger
from debug import generate_debug_log

for lang in locale.locale_alias.values():
    print(lang)

# -----=====[Set Up Configuration]=====----- #
_logging_config = configparser.ConfigParser()
_logging_config.read(os.path.join(os.path.dirname(__file__).replace("modules", "docs"), "configuration", "Logger.conf"))
_updater_config = configparser.ConfigParser()
_updater_config.read(os.path.join(os.path.dirname(__file__).replace("modules", "docs"), "configuration", "Updater.conf"))

# -----=====[Set Up Logging]=====----- #
try:
    _log_path = _logging_config.get("File", "path") # Check If A Log File Path Is Set In The Config File
except configparser.NoOptionError: # If The Path Is Not Set, Use The Default Path
    _log_path = os.path.join(os.path.dirname(__file__).replace("modules", "docs"), "logs")

_logging = logger.Logger(
    mode=_logging_config.getint("General", "logMode"),
    write_mode=_logging_config.get("General", "writeMode"),
    format=str(_logging_config.get("General", "format")).split("/"), # Turn The String Into A List Using "/" As The Delimiter
    date_format=_logging_config.get("General", "dateFormat"),
    log_file=_logging_config.get("File", "name"),
    log_file_path=_log_path,
    levelsShown=_logging_config.get("General", "levelsShown").split("/"), # Turn The String Into A List Using "/" As The Delimiter
    use_color=_logging_config.getboolean("General", "useColor")
)

del _log_path, _logging_config

# -----=====[Set Up Pygame]=====----- #
pygame.init()
_screen = pygame.display.set_mode((_updater_config.getint("General", "width"), _updater_config.getint("General", "height")))
_clock = pygame.time.Clock()
_fps = _updater_config.getint("General", "fps")
pygame.display.set_caption(_updater_config.get("General", "caption"))


# Creates A Window With An Animation That Shows The Program Is Updating
# The Animation Is Bar That Moves From Left To Right
updating = True
def main():

    test_bar = pygame.rect.Rect(_updater_config.getint("General", "width") / 2 - 250, 100, 500, 20)
    test_bar2 =  pygame.rect.Rect(_updater_config.getint("General", "width") / 2 - 250, 100, 200, 20)

    # Get The Current Theme
    try:
        with open(os.path.join(os.path.dirname(__file__).replace("modules", "docs"), "configuration", "Settings.json"), "r") as json_theme_file:
            theme = json.load(json_theme_file)['theme']
            json_theme_file.close()
        _logging.write("Loading Theme From Settings File", logger.Logger.INFO)
        _logging.write(f"Theme In Settings File: {theme}", logger.Logger.DEBUG)
    except FileNotFoundError as e:
        _logging.write("The Settings File Was Not Found.", logger.Logger.ERROR, extra_msg=e)
        generate_debug_log(extra_info="The Settings File Was Not Found.\nExit Code 2")



    # Load The Theme From The Themes Folder. If The Theme Is Not Found, Use The Default Theme
    # Looking For The Theme In The Themes Folder Is A Safety Measure To Make Sure The Theme Is Valid. Also It Makes It Easier To Add New Themes!
    _logging.write("Loading Theme From Themes Folder...", logger.Logger.INFO)
    try:
        with open(os.path.join(os.path.dirname(__file__).replace("modules", "docs"), "themes", theme + ".json"), "r") as json_theme_file:
            _logging.write(f"Found Theme File: {theme}.json", logger.Logger.DEBUG)
            theme = json.load(json_theme_file)
            json_theme_file.close()
        _logging.write("Theme Loaded Successfully", logger.Logger.INFO)
    except FileNotFoundError as e:
        _logging.write("Could Not Find Theme", logger.Logger.INFO)
        with open(os.path.join(os.path.dirname(__file__).replace("modules", "docs"), "themes", "dark.json"), "r") as json_theme_file:
            theme = json.load(json_theme_file)
            json_theme_file.close()


    while updating:
        # Draw The Background
        _screen.fill(theme['background']['main_color'])
        # Draw A Pattern On The Screen For The Background
        for x in range(0, _screen.get_width(), 10):
            for y in range(0, _screen.get_height(), 10):
                pygame.draw.rect(_screen, (theme['background']['secondary_color']), pygame.rect.Rect(x, y, 5, 5))

        # Event Handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pygame.draw.rect(_screen, ((255, 255, 255)), test_bar, 0, 10)
        pygame.draw.rect(_screen, ((128, 255, 0)), test_bar2, 0, 10)
        # Make A Second Bar Bounce Off The Sides Of The First Bar
        if test_bar2.x + test_bar2.width >= test_bar.x + test_bar.width:
            direction = "left"
        elif test_bar2.x <= test_bar.x:
            direction = "right"

        if direction == "left":
            test_bar2.x -= 5
        elif direction == "right":
            test_bar2.x += 5

        # Create The Bar Animation

        _clock.tick(_fps)
        pygame.display.update()

if __name__ == "__main__":
    main()