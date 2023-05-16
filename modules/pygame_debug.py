"""
This File Is Used To Show Debug Info Using Pygame.

It Would Be In debug.py But If The pygame Module Is Missing Or Damaged. A Debug Log Could Not Be Generated
"""

import os
import configparser
# External Modules
import pygame
# Custom Modules
import logger

pygame.init()

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

        if pygame is None:
            return

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

        if pygame is None:
            return

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
        except FileNotFoundError as error:
            _logging.write("Log File Not Found", lvl=logger.Logger.ERROR, extra_msg=error)
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

def parseKeysPressed(keysPressed: pygame.key.ScancodeWrapper):
    """
    Parse The ScancodeWrapper And Output A List That Contains All The Current Keys Being Pressed
    
    Arguments:
        keysPressed (pygame.key.ScancodeWrapper) - The ScancodeWrapper To Be Parsed
    """

    allKeysPressed = []

    # Shift Keys
    if keysPressed[pygame.K_LSHIFT]:
        allKeysPressed.append("LShift")
    if keysPressed[pygame.K_RSHIFT]:
        allKeysPressed.append("RShift")

    # Numbers + Shift Varaients
    if keysPressed[pygame.K_0] and keysPressed[pygame.K_LSHIFT] or keysPressed[pygame.K_0] and keysPressed[pygame.K_RSHIFT]:
        allKeysPressed.append(")")
    elif keysPressed[pygame.K_0]:
        allKeysPressed.append("0")
    if keysPressed[pygame.K_1] and keysPressed[pygame.K_LSHIFT] or keysPressed[pygame.K_1] and keysPressed[pygame.K_RSHIFT]:
        allKeysPressed.append("!")
    elif keysPressed[pygame.K_1]:
        allKeysPressed.append("1")
    if keysPressed[pygame.K_2] and keysPressed[pygame.K_LSHIFT] or keysPressed[pygame.K_2] and keysPressed[pygame.K_RSHIFT]:
        allKeysPressed.append("@")
    elif keysPressed[pygame.K_2]:
        allKeysPressed.append("2")
    if keysPressed[pygame.K_3] and keysPressed[pygame.K_LSHIFT] or keysPressed[pygame.K_3] and keysPressed[pygame.K_RSHIFT]:
        allKeysPressed.append("#")
    elif keysPressed[pygame.K_3]:
        allKeysPressed.append("3")
    if keysPressed[pygame.K_4] and keysPressed[pygame.K_LSHIFT] or keysPressed[pygame.K_4] and keysPressed[pygame.K_RSHIFT]:
        allKeysPressed.append("$")
    elif keysPressed[pygame.K_4]:
        allKeysPressed.append("4")
    if keysPressed[pygame.K_5] and keysPressed[pygame.K_LSHIFT] or keysPressed[pygame.K_5] and keysPressed[pygame.K_RSHIFT]:
        allKeysPressed.append("%")
    elif keysPressed[pygame.K_5]:
        allKeysPressed.append("5")
    if keysPressed[pygame.K_6] and keysPressed[pygame.K_LSHIFT] or keysPressed[pygame.K_6] and keysPressed[pygame.K_RSHIFT]:
        allKeysPressed.append("^")
    elif keysPressed[pygame.K_6]:
        allKeysPressed.append("6")
    if keysPressed[pygame.K_7] and keysPressed[pygame.K_LSHIFT] or keysPressed[pygame.K_7] and keysPressed[pygame.K_RSHIFT]:
        allKeysPressed.append("&")
    elif keysPressed[pygame.K_7]:
        allKeysPressed.append("7")
    if keysPressed[pygame.K_8] and keysPressed[pygame.K_LSHIFT] or keysPressed[pygame.K_8] and keysPressed[pygame.K_RSHIFT]:
        allKeysPressed.append("*")
    elif keysPressed[pygame.K_8]:
        allKeysPressed.append("8")
    if keysPressed[pygame.K_9] and keysPressed[pygame.K_LSHIFT] or keysPressed[pygame.K_9] and keysPressed[pygame.K_RSHIFT]:
        allKeysPressed.append("(")
    elif keysPressed[pygame.K_9]:
        allKeysPressed.append("9")
    
    # Letters <- Not Adding Capital Letters. Too Much Work For That ATM - J-The-Fox
    if keysPressed[pygame.K_a]:
        allKeysPressed.append("a")
    if keysPressed[pygame.K_b]:
        allKeysPressed.append("b")
    if keysPressed[pygame.K_c]:
        allKeysPressed.append("c")
    if keysPressed[pygame.K_d]:
        allKeysPressed.append("d")
    if keysPressed[pygame.K_e]:
        allKeysPressed.append("e")
    if keysPressed[pygame.K_f]:
        allKeysPressed.append("f")
    if keysPressed[pygame.K_g]:
        allKeysPressed.append("g")
    if keysPressed[pygame.K_h]:
        allKeysPressed.append("h")
    if keysPressed[pygame.K_i]:
        allKeysPressed.append("i")
    if keysPressed[pygame.K_j]:
        allKeysPressed.append("j")
    if keysPressed[pygame.K_k]:
        allKeysPressed.append("k")
    if keysPressed[pygame.K_l]:
        allKeysPressed.append("l")
    if keysPressed[pygame.K_m]:
        allKeysPressed.append("m")
    if keysPressed[pygame.K_n]:
        allKeysPressed.append("n")
    if keysPressed[pygame.K_o]:
        allKeysPressed.append("o")
    if keysPressed[pygame.K_p]:
        allKeysPressed.append("p")
    if keysPressed[pygame.K_q]:
        allKeysPressed.append("q")
    if keysPressed[pygame.K_r]:
        allKeysPressed.append("r")
    if keysPressed[pygame.K_s]:
        allKeysPressed.append("s")
    if keysPressed[pygame.K_t]:
        allKeysPressed.append("t")
    if keysPressed[pygame.K_u]:
        allKeysPressed.append("u")
    if keysPressed[pygame.K_v]:
        allKeysPressed.append("v")
    if keysPressed[pygame.K_w]:
        allKeysPressed.append("w")
    if keysPressed[pygame.K_x]:
        allKeysPressed.append("x")
    if keysPressed[pygame.K_y]:
        allKeysPressed.append("y")
    if keysPressed[pygame.K_z]:
        allKeysPressed.append("z")

    # Action Keys
    if keysPressed[pygame.K_SPACE]:
        allKeysPressed.append("Space")
    if keysPressed[pygame.K_LEFT]:
        allKeysPressed.append("Left")
    if keysPressed[pygame.K_UP]:
        allKeysPressed.append("Up")
    if keysPressed[pygame.K_DOWN]:
        allKeysPressed.append("Down")
    if keysPressed[pygame.K_RIGHT]:
        allKeysPressed.append("Right")
    if keysPressed[pygame.K_BACKSPACE]:
        allKeysPressed.append("Backspace")
    if keysPressed[pygame.K_RETURN]:
        allKeysPressed.append("Return")
    if keysPressed[pygame.K_TAB]:
        allKeysPressed.append("Tab")
    if keysPressed[pygame.K_ESCAPE]:
        allKeysPressed.append("Escape")
    if keysPressed[pygame.K_LCTRL]:
        allKeysPressed.append("LCtrl")
    if keysPressed[pygame.K_RCTRL]:
        allKeysPressed.append("RCtrl")

    # Function Keys
    if keysPressed[pygame.K_F1]:
        allKeysPressed.append("Func1")
    if keysPressed[pygame.K_F2]:
        allKeysPressed.append("Func2")
    if keysPressed[pygame.K_F3]:
        allKeysPressed.append("Func3")
    if keysPressed[pygame.K_F4]:
        allKeysPressed.append("Func4")
    if keysPressed[pygame.K_F5]:
        allKeysPressed.append("Func5")
    if keysPressed[pygame.K_F6]:
        allKeysPressed.append("Func6")
    if keysPressed[pygame.K_F7]:
        allKeysPressed.append("Func7")
    if keysPressed[pygame.K_F8]:
        allKeysPressed.append("Func8")
    if keysPressed[pygame.K_F9]:
        allKeysPressed.append("Func9")
    if keysPressed[pygame.K_F10]:
        allKeysPressed.append("Func10")
    if keysPressed[pygame.K_F11]:
        allKeysPressed.append("Func11")
    if keysPressed[pygame.K_F12]:
        allKeysPressed.append("Func12")
        
    # Symbols + Shift Varaients
    if keysPressed[pygame.K_BACKSLASH] and keysPressed[pygame.K_LSHIFT] or keysPressed[pygame.K_BACKSLASH] and keysPressed[pygame.K_RSHIFT]:
        allKeysPressed.append("|")
    elif keysPressed[pygame.K_BACKSLASH]:
        allKeysPressed.append("\\")
    if keysPressed[pygame.K_SLASH] and keysPressed[pygame.K_LSHIFT] or keysPressed[pygame.K_SLASH] and keysPressed[pygame.K_RSHIFT]:
        allKeysPressed.append("?")
    elif keysPressed[pygame.K_SLASH]:
        allKeysPressed.append("/")
    if keysPressed[pygame.K_MINUS] and keysPressed[pygame.K_LSHIFT] or keysPressed[pygame.K_MINUS] and keysPressed[pygame.K_RSHIFT]:
        allKeysPressed.append("_")
    elif keysPressed[pygame.K_MINUS]:
        allKeysPressed.append("-")
    if keysPressed[pygame.K_EQUALS] and keysPressed[pygame.K_LSHIFT] or keysPressed[pygame.K_EQUALS] and keysPressed[pygame.K_RSHIFT]:
        allKeysPressed.append("+")
    elif keysPressed[pygame.K_EQUALS]:
        allKeysPressed.append("=")
    if keysPressed[pygame.K_SEMICOLON] and keysPressed[pygame.K_LSHIFT] or keysPressed[pygame.K_SEMICOLON] and keysPressed[pygame.K_RSHIFT]:
        allKeysPressed.append(":")
    elif keysPressed[pygame.K_SEMICOLON]:
        allKeysPressed.append(":")
    if keysPressed[pygame.K_COMMA] and keysPressed[pygame.K_LSHIFT] or keysPressed[pygame.K_COMMA] and keysPressed[pygame.K_RSHIFT]:
        allKeysPressed.append("<")
    elif keysPressed[pygame.K_COMMA]:
        allKeysPressed.append(",")
    if keysPressed[pygame.K_PERIOD] and keysPressed[pygame.K_LSHIFT] or keysPressed[pygame.K_PERIOD] and keysPressed[pygame.K_RSHIFT]:
        allKeysPressed.append(">")
    elif keysPressed[pygame.K_PERIOD]:
        allKeysPressed.append(".")
    if keysPressed[pygame.K_BACKQUOTE] and keysPressed[pygame.K_LSHIFT] or keysPressed[pygame.K_BACKQUOTE] and keysPressed[pygame.K_RSHIFT]:
        allKeysPressed.append("~")
    elif keysPressed[pygame.K_BACKQUOTE]:
        allKeysPressed.append(" ` ")
    if keysPressed[pygame.K_QUOTE] and keysPressed[pygame.K_LSHIFT] or keysPressed[pygame.K_QUOTE] and keysPressed[pygame.K_RSHIFT]:
        allKeysPressed.append(' " ')
    elif keysPressed[pygame.K_QUOTE]:
        allKeysPressed.append(" ' ")
    if keysPressed[pygame.K_RIGHTBRACKET] and keysPressed[pygame.K_LSHIFT] or keysPressed[pygame.K_RIGHTBRACKET] and keysPressed[pygame.K_RSHIFT]:
        allKeysPressed.append("}")
    elif keysPressed[pygame.K_RIGHTBRACKET]:
        allKeysPressed.append("]")
    if keysPressed[pygame.K_LEFTBRACKET] and keysPressed[pygame.K_LSHIFT] or keysPressed[pygame.K_LEFTBRACKET] and keysPressed[pygame.K_RSHIFT]:
        allKeysPressed.append("{")
    elif keysPressed[pygame.K_LEFTBRACKET]:
        allKeysPressed.append("[")
    
    return allKeysPressed # Return The List Of Keys Pressed, Theres A Lot Of Them