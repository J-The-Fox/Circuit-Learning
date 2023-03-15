"""
This Is The Screen That Will Be Shown When The Actual Program Is Updating
"""

# Built-In Modules
import os
import sys
import _thread
import configparser
# External Modules
import pygame
import requests
import psutil
# Custom Modules
import logger

# -----=====[Set Up Configuration]=====----- #
logging_config = configparser.ConfigParser()
logging_config.read(os.path.join(os.path.dirname(__file__).replace("modules", "docs"), "configuration", "Logger.conf"))
updater_config = configparser.ConfigParser()
updater_config.read(os.path.join(os.path.dirname(__file__).replace("modules", "docs"), "configuration", "Updater.conf"))

# -----=====[Set Up Logging]=====----- #
try:
    _log_path = logging_config.get("File", "path") # Check If A Log File Path Is Set In The Config File
except configparser.NoOptionError:
    _log_path = None

logging = logger.Logger(
    mode=logging_config.getint("General", "logMode"),
    write_mode=logging_config.get("General", "writeMode"),
    format=str(logging_config.get("General", "format")).split("/"), # Turn The String Into A List Using "/" As The Delimiter
    log_file=logging_config.get("File", "name"),
    log_file_path=_log_path if _log_path != None else os.path.join(os.path.dirname(__file__).replace("modules", "docs/logs")), # If The Path Is Not Set, Use The Default Path
    levelsShown=logging_config.get("General", "levelsShown").split("/"), # Turn The String Into A List Using "/" As The Delimiter
    use_color=logging_config.getboolean("General", "useColor")
)

# -----=====[Set Up Pygame]=====----- #
pygame.init()
screen = pygame.display.set_mode((updater_config.getint("General", "width"), updater_config.getint("General", "height")))
pygame.display.set_caption(updater_config.get("General", "title"))