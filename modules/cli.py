import os
import sys
import configparser
# External Modules
_IMPORTERROR = []
try:
    import pygame
except ImportError:
    _IMPORTERROR.append("pygame")
try:
    import requests
except ImportError:
    _IMPORTERROR.append("requests")
try:
    import psutil
except ImportError:
    _IMPORTERROR.append("psutil")
try:
    import pygame_gui
except ImportError:
    _IMPORTERROR.append("pygame_gui")
# Custom Modules
import logger
import decorators
from debug import generate_debug_log

# -----=====[Set Up Configuration]=====----- #
_logging_config = configparser.ConfigParser()
_logging_config.read(os.path.join(os.path.dirname(__file__).replace("modules", "docs"), "configuration", "Logger.conf"))

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

# Check For Missing Modules
if len(_IMPORTERROR) > 0:
    _logging.write("The Following Modules Could Not Be Imported: {}".format(", ".join(_IMPORTERROR)), logger.Logger.CRITICAL)
    _logging.write("Please Install The Missing Modules And Try Again", logger.Logger.CRITICAL)
    generate_debug_log(extra_info="    The Following Modules Could Not Be Imported: {}. \n    Exit Code 1.".format(", ".join(_IMPORTERROR)))
    _logging.close(1)
    sys.exit(1)

_logging.write("All Modules Are Installed!", lvl=logger.Logger.INFO)
del _logging

import Circuit_Learning

main = Circuit_Learning.Main()
main.start_up_screen()
main.main_menu()
