# Built-In Modules
import os
import json
import platform
import datetime
import configparser
# External Modules
try:
    import pygame
except ImportError:
    pass
try:
    import pygame_gui # Not Used As pygame_gui Has No Way To Get A Version Without Checking Through Python Itself
except ImportError:
    pass
try:
    import psutil
except ImportError:
    pass
try:
    import requests
except ImportError:
    pass
try:
    import hashlib
except ImportError:
    pass
# Custom Modules
import logger

__all__ = ["Debug", "generate_debug_log"]

__version__ = "0.1.7"

# -----=====[Set Up Configuration]=====----- #
_logging_config = configparser.ConfigParser()
_logging_config.read(os.path.join(os.path.dirname(__file__).replace("modules", "docs"), "configuration", "Logger.conf"))
_debug_config = configparser.ConfigParser()
_debug_config.read(os.path.join(os.path.dirname(__file__).replace("modules", "docs"), "configuration", "Debug.conf"))
_main_config = configparser.ConfigParser()
_main_config.read(os.path.join(os.path.dirname(__file__).replace("modules", "docs"), "configuration", "Main.conf"))

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

# -----=====[Functions]=====----- #

def generate_debug_log(file_name = None, file_path = "docs/logs", extra_info = None):
    """
    Generates A Debug Log

    Arguments:
        file_name (str) - The Log File Name
        file_path (str) - The Log File Path
    """

    _logging.write("Generating Debug Log...", lvl=logger.Logger.INFO)


    if file_name is None:
        file_name = "debug_log_{}.log".format(datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S"))

    with open(os.path.join(file_path, file_name), 'a') as debug_log:
        debug_log.write("============================================================\n")

        # -----=====[Date and Time]=====----- #
        debug_log.write("This Debug Log Was Generated On: " + str(datetime.datetime.now()) + "\n")
        debug_log.write("============================================================\n")

        # -----=====[App Information]=====----- #
        debug_log.write("App Information:\n")
        debug_log.write("    Version: " + str(_main_config.getint("Version", "major")) + "." + str(_main_config.getint("Version", "minor")) + "." + str(_main_config.getint("Version", "bugFix")) + "\n")
        debug_log.write("    Build: " + str(_main_config.get("Version", "Build")) + "\n")
        debug_log.write("============================================================\n")

        # -----=====[OS Information]=====----- #
        debug_log.write("OS Information:\n")
        debug_log.write("    OS: " + str(platform.system()) + "\n")
        if platform.system() == "Windows":
            debug_log.write("    Windows Version: " + str(platform.win32_ver()) + "\n")
            debug_log.write("    Windows Edition: " + str(platform.win32_edition()) + "\n")
        elif platform.system() == "Darwin":
            debug_log.write("    Mac Version: " + str(platform.mac_ver()[0]) + "\n")
        debug_log.write("    Architecture: " + str(platform.architecture()[0]) + "\n")
        debug_log.write("============================================================\n")

        # -----=====[System Utilization Information At The Creation Of The Debug Log]=====----- #
        debug_log.write("System Utilization Information:\n")
        try:
            debug_log.write("    CPU Usage: " + str(psutil.cpu_percent()) + "%\n")
            debug_log.write("    Memory Usage: " + str(psutil.virtual_memory().percent) + "%\n")
            debug_log.write("    Disk Usage: " + str(psutil.disk_usage("/").percent) + "%\n")
        except NameError:
            debug_log.write("    CPU Usage: psutil Not Installed.\n")
            debug_log.write("    Memory Usage: psutil Not Installed.\n")
            debug_log.write("    Disk Usage: psutil Not Installed.\n")
        debug_log.write("============================================================\n")
        
        # -----=====[Python Information]=====----- #
        debug_log.write("Python Information:\n")
        debug_log.write("    Python Version: " + str(platform.python_version()) + "\n")
        debug_log.write("    Python Build: " + str(platform.python_build()[0].split(":")[1]) + ", " + str(platform.python_build()[1]) + "\n")
        debug_log.write("    Python Branch: " + str(platform.python_branch()) + "\n")
        debug_log.write("    Python Compiler: " + str(platform.python_compiler()) + "\n")
        debug_log.write("    Python Implementation: " + str(platform.python_implementation()) + "\n")
        debug_log.write("============================================================\n")

        # -----=====[Python Package Information]=====----- #
        debug_log.write("Python Package Information:\n")
        try:
            debug_log.write("    psutil Version: " + str(psutil.__version__) + "\n")
        except NameError:
            debug_log.write("    psutil Version: psutil Not Installed.\n")
        try:
            debug_log.write("    pygame Version: " + str(pygame.version.ver) + "\n")
        except NameError:
            debug_log.write("    pygame Version: pygame Not Installed.\n")
        debug_log.write("    pygame-gui Version: No Version Info. \n")
        try:
            debug_log.write("    requests Version: " + str(requests.__version__) + "\n")
        except NameError:
            debug_log.write("    requests Version: requests Not Installed.\n")
        debug_log.write("    -----------------------\n")
        debug_log.write("    logger Version: " + str(logger.__version__) + "\n")
        debug_log.write("    debug Version: " + str(__version__) + "\n")
        debug_log.write("============================================================\n")

        # Grab The Last Lines Of The Log File. Set From The Config File: Debug.conf. Default Is 100 Lines
        debug_log.write("Last " + str(_debug_config.getint("DebugLog", "logLines")) + " Lines Of The Log File:\n")
        with open(os.path.join(_log_path, _logging_config.get("File", "name")), 'r') as log_file:
            _log_file = log_file.readlines()
            _log_file = _log_file[-_debug_config.getint("DebugLog", "logLines"):]
            for _line in _log_file:
                debug_log.write(_line)
            log_file.close()
        debug_log.write("============================================================\n")

        # -----=====[Contents Of The Config Files]=====----- #
        debug_log.write("Contents Of The Config Files:\n")

        debug_log.write("    Debug.conf:\n")
        try:
            with open(os.path.join(os.path.dirname(__file__).replace("modules", "docs"), "configuration", "Debug.conf"), 'r') as config_file:
                _debug_config_file = config_file.readlines()
                for _line in _debug_config_file:
                    debug_log.write("        " + _line)
                config_file.close()
        except FileNotFoundError:
            debug_log.write("        Debug.conf Not Found.\n")

        debug_log.write("\n    Logger.conf:\n")
        try:
            with open(os.path.join(os.path.dirname(__file__).replace("modules", "docs"), "configuration", "Logger.conf"), 'r') as config_file:
                _logging_config_file = config_file.readlines()
                for _line in _logging_config_file:
                    debug_log.write("        " + _line)
                config_file.close()
        except FileNotFoundError:
            debug_log.write("        Logger.conf Not Found.\n")

        debug_log.write("\n    Main.conf:\n")
        try:
            with open(os.path.join(os.path.dirname(__file__).replace("modules", "docs"), "configuration", "Main.conf"), 'r') as config_file:
                _main_config_file = config_file.readlines()
                for _line in _main_config_file:
                    debug_log.write("        " + _line)
                config_file.close()
        except FileNotFoundError:
            debug_log.write("        Main.conf Not Found.\n")

        debug_log.write("\n    Updater.conf:\n")
        try:
            with open(os.path.join(os.path.dirname(__file__).replace("modules", "docs"), "configuration", "Updater.conf"), 'r') as config_file:
                _main_config_file = config_file.readlines()
                for _line in _main_config_file:
                    debug_log.write("        " + _line)
                config_file.close()
        except FileNotFoundError:
            debug_log.write("        Updater.conf Not Found.\n")
        debug_log.write("\n============================================================\n")

        # -----=====[File Hashes (To See If Files Have Been Modified)]=====----- #
        # For Each File In The Modules Directory, Generate A Hash And Store It In A Dictionary
        new_files = []
        new_hashes = {}
        for root, dirs, files in os.walk(os.path.dirname(__file__)):
            for file in files:
                if str(file).endswith(".pyc") is False:
                    new_files.append(file)
                    try:
                        new_hashes[file] = hashlib.md5(open(os.path.join(root, file), 'rb').read()).hexdigest()
                    except NameError:
                        new_hashes[file] = " "

        # Open The Hash File
        try:
            with open(os.path.join(os.path.dirname(__file__).replace("modules", "docs"), ".cache", "hashes.json")) as json_file:
                hashes = json.load(json_file)
                json_file.close()
        except FileNotFoundError as e:
            debug_log.write("No Hash File Found. Will Be Created On Next Game Start.\n")
            debug_log.write("" + str(e) + "\n")
        except json.decoder.JSONDecodeError as e: # If The Hash File Is Empty, Delete It
            debug_log.write("Hash File Is Empty. Will Be Created On Next Game Start.\n")
            debug_log.write("" + str(e) + "\n")
            _logging.write("Hash File Is Empty", lvl=logger.Logger.ERROR, extra_msg=e)
            os.remove(os.path.join(os.path.dirname(__file__).replace("modules", "docs"), ".cache", "hashes.json"))

        # Print An Error If hashlib Is Not Installed
        try:
            hashlib.md5(open(os.path.join(os.path.dirname(__file__), "debug.py"), 'rb').read()).hexdigest()
        except NameError as e:
            debug_log.write("hashlib Not Installed. No File Hashes Will Be Generated.\n")
            debug_log.write("" + str(e) + "\n\n")

        # Compare Each Of The Hashes To The New Hashes. 
        # If They Are Different, The File Has Been Modified. 
        # If The File Is Not In The Old Hashes, It Is A New File
        debug_log.write("File Hashes (md5):\n")
        for file in new_files:
            try:
                if hashes[file] != new_hashes[file]:
                    debug_log.write("    (Modified) " + str(file) + ": " + str(hashes[file]) + " -> " + str(new_hashes[file]) + "\n")
                else:
                    debug_log.write("    (Unchaged) " + str(file) + ": " + str(hashes[file]) + "\n")
            except KeyError: # If A KeyError Is Thrown, The File Is New As It Was Not In The Old Hashes Originally
                debug_log.write("    (New File) " + str(file) + ": " + str(new_hashes[file]) + "\n")
            except UnboundLocalError: # An UnboundLocalError Will Be Thrown As Hashes Is Not Defined If The File Was Not Found. This Is To Be Expected
                debug_log.write("    " + str(file) + ": " + str(new_hashes[file])+ "\n")
        debug_log.write("============================================================\n")

        # Extra Information That Can Be Passed In (Stuff Like Errors, Exceptions, Etc.)
        debug_log.write("Extra Information:\n")
        if extra_info is not None:
            # Add 4 Spaces To The Start Of Each Line To Make It Look Nice
            extra_info = str(extra_info[:0]).strip() + "    " + str(extra_info[0:]).strip()
            # Replace Newlines With Newlines And 4 Spaces
            extra_info = extra_info.replace("\n", "\n    ")
            debug_log.write(extra_info + "\n")
        else:
            debug_log.write("    None Provided\n")
        debug_log.write("============================================================\n")


        debug_log.write("End Of Debug Log \n")

        debug_log.close()

    _logging.write("Finished Generating Debug Log", lvl=logger.Logger.INFO)
    _logging.write("Saved Debug Log To: " + str(os.path.join(file_path, file_name)), lvl=logger.Logger.INFO)

    del root, dirs, files, _log_file # Clean Up Memory

if __name__ == "__main__":
    generate_debug_log(extra_info="This Debug Log Was Generated From debug.py Being Run Directly.")
