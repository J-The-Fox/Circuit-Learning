# Built-In Modules
import os
import datetime
import configparser
# External Modules
import colorama
import pygame
# Custom Modules
import logger

__all__ = ["Debug"]

# -----=====[Set Up Configuration]=====----- #
_logging_config = configparser.ConfigParser()
_logging_config.read(os.path.join(os.path.dirname(__file__).replace("modules", "docs"), "configuration", "Logger.conf"))

# -----=====[Set Up Logging]=====----- #
try:
    _log_path = _logging_config.get("File", "path") # Check If A Log File Path Is Set In The Config File
except configparser.NoOptionError:
    _log_path = None

_logging = logger.Logger(
    mode=_logging_config.getint("General", "logMode"),
    write_mode=_logging_config.get("General", "writeMode"),
    format=str(_logging_config.get("General", "format")).split("/"), # Turn The String Into A List Using "/" As The Delimiter
    log_file=_logging_config.get("File", "name"),
    log_file_path=_log_path if _log_path != None else os.path.join(os.path.dirname(__file__).replace("modules", "docs/logs")), # If The Path Is Not Set, Use The Default Path
    levelsShown=_logging_config.get("General", "levelsShown").split("/"), # Turn The String Into A List Using "/" As The Delimiter
    use_color=_logging_config.getboolean("General", "useColor")
)

class Debug():
    """
    Debug Class
    """

    def __init__(self, font: pygame.font.Font, textSpacing: int, textColor: str, backgroundTextColor: str, debugTextScreenLocation: str | int, debugLogScreenLocation: str | int, logfile: str):

        # Parse The Screen Location of The Debug Text and Debug Log #
        # Debug Text
        if str(debugTextScreenLocation).capitalize() == "1" or str(debugTextScreenLocation).capitalize() == "Topleft" or str(debugTextScreenLocation).capitalize() == "Top left":
            self.debugTextLocation = '1'
        elif str(debugTextScreenLocation).capitalize() == "2" or str(debugTextScreenLocation).capitalize() == "Topright" or str(debugTextScreenLocation).capitalize() == "Top right":
            self.debugTextLocation = '2'
        else:
            self.debugTextLocation = None
            _logging.write("[class-debug]: Invalid or No Location Given", lvl=logger.Logger.ERROR)
            return
        # Debug Log
        if str(debugLogScreenLocation).capitalize() == "1" or str(debugLogScreenLocation).capitalize() == "Topleft" or str(debugLogScreenLocation).capitalize() == "Top left":
            self.debugLogLocation = '1'
        elif str(debugLogScreenLocation).capitalize() == "2" or str(debugLogScreenLocation).capitalize() == "Topright" or str(debugLogScreenLocation).capitalize() == "Top right":
            self.debugLogLocation = '2'
        else:
            self.debugLogLocation = None
            _logging.write("[class-debug]: Invalid or No Location Given", lvl=logger.Logger.ERROR)
            return

        self.font = font
        self.textSpacing = textSpacing
        self.textColor = textColor
        self.backgroundColor = backgroundTextColor
        self.logfile = logfile

    def displayDebugText(self, enabled: bool, msg: str | list):
        """
        Displays Debug Messages To The Screen

        Arguments:
            enabled (bool) - If True, The Debug Text Will Be Displayed
            msg (str | list) - The Message To Be Displayed
        """

        if enabled != True: # If Debug Text Is Disabled, Return
            return

        if isinstance(msg, str): # If msg Is Of Type 'str'
            displaySurface = pygame.display.get_surface() # Get The Display Surface
            debugSurf = self.font.render(str(msg), True, self.textColor) # Render The Debug Text
            debugRect = debugSurf.get_rect(topleft = (10, 10)) # Get The Debug Text Rect
            pygame.draw.rect(displaySurface, self.backgroundColor, debugRect) # Draw A Background Rect
            displaySurface.blit(debugSurf, debugRect) # Blit The Debug Text To The Display Surface

        elif isinstance(msg, list): # If msg Is Of Type 'list'
            count = 0 # Count Variable
            displaySurfuce = pygame.display.get_surface() # Get The Display Surface
            for text in msg: # For Each Item In The List
                debugSurf = self.font.render(str(text), True, self.textColor) # Render The Debug Text
                debugRect = debugSurf.get_rect(topleft = (10, 10 + count)) # Get The Debug Text Rect
                pygame.draw.rect(displaySurfuce, self.backgroundColor, debugRect) # Draw A Background Rect
                displaySurfuce.blit(debugSurf, debugRect) # Blit The Debug Text To The Display Surface

                count += self.textSpacing

    def displayLog(self, enabled: bool, textBoxSize: tuple):
        """
        Displays A Log File Or A Text Document To The Screen

        Arguments:
            enabled (bool) - If True, The Log Will Be Displayed
            textBoxSize (tuple) - The Size Of The Text Box
        """

        if enabled != True: # If Debug Log Is Disabled, Return
            return

        _textLogList = [] # List To Store The Log File

        surface = pygame.display.get_surface() # Get The Display Surface
        
        # Try To Open The Log File, If It Fails, Return
        try:
            with open(self.logfile, 'r') as logFileHandler:
                for _line in logFileHandler:
                    _textLogList.append(_line)
                logFileHandler.close()
        except FileNotFoundError:
            print(f"x {str(datetime.datetime.now())} - [{colorama.Fore.RED}ERROR{colorama.Fore.RESET}] - The Log File Doesn't Exist") 
            print(f"╰─> The File {self.logfile} Does Not Exist.")
            return

        _logSurface = pygame.Surface((textBoxSize[0], textBoxSize[1])).convert_alpha() # Create A Surface For The Log
        _logSurface.fill((10, 10, 10, 100)) # Fill The Surface With A Transparent Color

        
        lineNum = 0
        if self.debugLogLocation == "1":
            surface.blit(_logSurface, (0, 0))
        elif self.debugLogLocation == "2":
            surface.blit(_logSurface, (pygame.display.get_window_size()[0] - textBoxSize[0], 0))
            for _text in reversed(_textLogList[:]):
                if lineNum < _logSurface.get_height():
                    surface.blit(self.font.render(str(_text).replace("\n", ""), True, "Orange"), (pygame.display.get_window_size()[0] - _logSurface.get_width() + 10, _logSurface.get_height() - 20 - lineNum))
                    lineNum += self.font.get_height()