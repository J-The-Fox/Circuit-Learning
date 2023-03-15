# Built-In Modules
import os
import configparser
# External Modules
_IMPORTERROR = []
try:
    import requests
except ModuleNotFoundError:
    _IMPORTERROR.append("requests")
# Custom Modules
import logger

__all__ = ["check_connection"]

# -----=====[Set Up Configuration]=====----- #
logging_config = configparser.ConfigParser()
logging_config.read(os.path.join(os.path.dirname(__file__).replace("modules", "docs"), "configuration", "Logger.conf"))

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


# Adding A Running Time Decarator Breakes This Function, Returns None Always
def check_connection():
    """
    Check If The Computer Is Connected To The Internet
    """

    # Check If The "requests" Module Is Installed
    if "requests" in _IMPORTERROR:
        logging.write(f"Module Error.", lvl=logger.Logger.ERROR, extra_msg="Module 'requests' Is Not Installed")
        return None

    # Try To Connect To The Internet, If It Fails, Return False, Else, Return True
    try:
        requests.get("https://stackoverflow.com") # Why Not Use stackoverflow.com?
        logging.write(f"[network]: Succesfully Reached Out To URL 'https://stackoverflow.com'", lvl=logger.Logger.INFO)
        return True # Return True If There Is No Error
    except requests.exceptions.ConnectionError:
        logging.write(f"[network]: Netork Error.", lvl=logger.Logger.ERROR, extra_msg="Could Not Reach URL: https://stackoverflow.com") # Log The Error If There Is One
        return False # Return False If There Is An Error
