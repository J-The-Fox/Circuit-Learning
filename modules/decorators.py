"""
Provides Some Helpful Decorators For Use In Other Files
"""

# Internal Modules
import os
import time
import configparser
from typing import Any, Callable
# Custom Modules
import logger

__all__ = ["running_time", "memorize"]

# -----=====[Set Up Configuration]=====----- #
_logging_config = configparser.ConfigParser()
_logging_config.read(os.path.join(os.path.dirname(__file__).replace("modules", "docs"), "configuration", "Logger.conf"))

# -----=====[Set Up Logging]=====----- #
try:
    _log_path = _logging_config.get("File", "path") # Check If A Log File Path Is Set In The Config File
except configparser.NoOptionError:
    _log_path = None

logging = logger.Logger(
    mode=_logging_config.getint("General", "logMode"),
    write_mode=_logging_config.get("General", "writeMode"),
    format=str(_logging_config.get("General", "format")).split("/"), # Turn The String Into A List Using "/" As The Delimiter
    log_file=_logging_config.get("File", "name"),
    log_file_path=_log_path if _log_path != None else os.path.join(os.path.dirname(__file__).replace("modules", "docs/logs")), # If The Path Is Not Set, Use The Default Path
    levelsShown=_logging_config.get("General", "levelsShown").split("/"), # Turn The String Into A List Using "/" As The Delimiter
    use_color=_logging_config.getboolean("General", "useColor")
)

def running_time(func: Callable[..., Any]) -> Callable[..., Any]:
    """
    Times How Long A Function or Method Takes To Complete
    """

    def wrapper(*args: Any, **kwargs: Any) -> Any:
        start_time = time.perf_counter() # Create A Start Time
        value = func(*args, **kwargs) # Run The Function And Store The Return Value
        end_time = time.perf_counter() # Create An End Time
        logging.write(f"{func.__name__} Completed In {end_time - start_time} Seconds.", lvl=logger.Logger.DEBUG) # Log The Total Time

        return value # Return The Return Value

    return wrapper # Return The Wrapper

def memorize(func: Callable[..., Any]) -> Callable[..., Any]:
    """
    Take A Function And Store The Argumemnts And The Keyword Arguments In A Cache To Speed Up Repetitive Tasks Such As Calculating Digits
    """

    # Create A Cache
    cache = {}

    def wrapper(*args: Any, **kwargs: Any) -> Any:
        key = str(args) + str(kwargs)
        # The Key Is The Arguments And Keyword Arguments Added Together In A String
        # If The Key Is Not Stored In The Cache, Store It In The Cache
        if key not in cache:
            cache[key] = func(*args, **kwargs)

        return cache[key]
    
    return wrapper # Return The Wrapper