import os
import sys
import json
import configparser
# External Modules
_MISSINGREQUIRED = []
_MISSINGOPTIONAL = []
try:
    import pygame
except ImportError:
    _MISSINGREQUIRED.append("pygame")
try:
    import requests
except ImportError:
    _MISSINGOPTIONAL.append("requests")
try:
    import psutil
except ImportError:
    _MISSINGOPTIONAL.append("psutil")
try:
    import pygame_gui
except ImportError:
    _MISSINGREQUIRED.append("pygame_gui")
try:
    import hashlib
except ImportError:
    _MISSINGOPTIONAL.append("hashlib")
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

# Check For Missing Modules. If Any Required Modules Are Missing, Exit The Program
# Required Modules: pygame - Used For The GUI 
#                   pygame_gui - Extends Pygame GUI
# Optional Modules: requests - Used For Checking For Updates 
#                   hashlib - Used For Generating Hashes, 
#                   psutil - Used For Getting System Information And Monitoring
if len(_MISSINGREQUIRED) > 0:
    _logging.write("Missing Required Modules: {}".format(", ".join(_MISSINGREQUIRED)), lvl=logger.Logger.CRITICAL)
    _logging.write("Please Install Them And Try Again", lvl=logger.Logger.ERROR)
    generate_debug_log(extra_info="Missing Required Modules: {}".format(", ".join(_MISSINGREQUIRED)))
    _logging.close(1)
    sys.exit(1)
_logging.write("All Required Modules Are Installed!", lvl=logger.Logger.INFO)
if len(_MISSINGOPTIONAL) > 0:
    _logging.write("Missing Optional Modules: {}".format(", ".join(_MISSINGOPTIONAL)), lvl=logger.Logger.WARNING)
    _logging.write("Some Features May Not Work Correctly Or Not At All", lvl=logger.Logger.NOTICE)

del _MISSINGREQUIRED, _MISSINGOPTIONAL # Clean Up Memory


# Generate A Hash File If One Does Not Exist
try:
    if os.path.exists(os.path.join(os.path.dirname(__file__).replace("modules", "docs"), ".cache", "hashes.json")) is False:
        _logging.write("Generating Hash File...", lvl=logger.Logger.INFO)
        new_files = []
        new_hashes = {}
        for root, dirs, files in os.walk(os.path.dirname(__file__)):
            for file in files:
                if str(file).endswith(".pyc") is False:
                    new_files.append(file)
                    new_hashes[file] = hashlib.md5(open(os.path.join(root, file), 'rb').read()).hexdigest()
    
        # Write The Hashes To The Hash File
        with open(os.path.join(os.path.dirname(__file__).replace("modules", "docs"), ".cache", "hashes.json"), "w") as hash_file:
            json.dump(new_hashes, hash_file, indent=4)
            hash_file.close()
        _logging.write("Stored In {}".format(os.path.join(os.path.dirname(__file__).replace("modules", "docs"), ".cache", "hashes.json")), lvl=logger.Logger.INFO)
        del hash_file
except NameError as e:
    _logging.write("An Error Occurred While Generating The Hash File.", logger.Logger.ERROR, extra_msg=e)

del _logging

import Circuit_Learning

main = Circuit_Learning.Main()
main.start_up_screen()
main.main_menu()
