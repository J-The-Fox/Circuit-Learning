# Internal Mdoules
import os
import sys
import time
import datetime
import inspect
import configparser
import json
import _thread
import random
# External Modules
_IMPORT_ERROR = []
try:
    import pygame
except ImportError:
    _IMPORT_ERROR.append("pygame")
try:
    import psutil
except ImportError:
    _IMPORT_ERROR.append("psutil")
# Custom Modules
import logger
import decorators
import button
import debug
import menu
import network

# -----=====[Set Up Configuration]=====----- #
logging_config = configparser.ConfigParser()
logging_config.read(os.path.join(os.path.dirname(__file__).replace("modules", "docs"), "configuration", "Logger.conf"))
debug_config = configparser.ConfigParser()
debug_config.read(os.path.join(os.path.dirname(__file__).replace("modules", "docs"), "configuration", "Debug.conf"))
main_config = configparser.ConfigParser()
main_config.read(os.path.join(os.path.dirname(__file__).replace("modules", "docs"), "configuration", "Main.conf"))

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

logging.init(True) # Initialize The Logger
logging.write("Starting Circuit Learning...", lvl=logger.Logger.INFO)

# -----=====[Check For Missing Modules]=====----- #
if len(_IMPORT_ERROR) > 0:
    logging.write("Missing Module(s): " + ", ".join(_IMPORT_ERROR), lvl=logger.Logger.ERROR)
    logging.write("Would you like to install them? (y/N)" ,lvl=logger.Logger.INFO)
    if input("»»» ").lower() == "y":
        logging.write("Installing Missing Modules...", lvl=logger.Logger.INFO)
        os.system("python3 -m pip install " + " ".join(_IMPORT_ERROR))
        # Reimport The Modules In Case They Were Installed
        import pygame
        import psutil
    else:
        logging.write("Can Not Continue Without The Missing Modules. Exiting...", lvl=logger.Logger.CRITICAL)
        sys.exit()

del _IMPORT_ERROR # Delete The Temporary Variable To Save Memory

pygame.init()

# -----=====[Set Up Debugging]=====----- #
# Must Be Set Up After Pygame Is Initialized As It Uses Pygame For Fonts, Colors, Etc.
_debug = debug.Debug(
    font=pygame.font.Font(os.path.join(os.path.dirname(__file__), "fonts", "tokeely-brookings", "Tokeely_Brookings.ttf").replace("modules", "docs"), 10),
    textSpacing=10,
    textColor=(243, 156, 41),
    backgroundTextColor="Black",
    debugTextScreenLocation="Top left",
    debugLogScreenLocation="Top right",
    logfile=os.path.join(os.path.dirname(__file__).replace("modules", "docs"), "logs", "Circuit_Learning.log")
)


timer = time.perf_counter()

class Circuit_Learning():

    def __init__(self) -> None:
        self.logger = logger.Logger(mode=logger.Logger.LOGTOTERM, format=['dt', 'lvl', 'msg'], log_file="Narro.log", log_file_path=os.path.join(os.path.dirname(__file__).replace("modules", "docs/logs")), write_mode='w', levelsShown=[logger.Logger.BUG, logger.Logger.DEBUG, logger.Logger.INFO, logger.Logger.WARN, logger.Logger.ERROR, logger.Logger.CRITICAL])

        self.screenInfo = pygame.display.Info()
        self.screen = pygame.display.set_mode((self.screenInfo.current_w, self.screenInfo.current_h), pygame.FULLSCREEN)
        self.clock = pygame.time.Clock()
        self.parts = []

        # Settings (Pulled From Settings.json)
        # NOTE: This Is Means That In Order For The Settings To Be Changed, The Game Must Be Restarted
        with open(os.path.join(os.path.dirname(__file__), "configuration", "settings.json").replace("modules", "docs"), "r") as f:
            _game_settings = json.load(f)
            f.close()
        
        # Set Themes Here
        _theme = _game_settings["theme"]
        if _theme == "dark":
            logging.write("Theme: Dark", lvl=logger.Logger.INFO)
            self.backgroundColor = (20, 20, 20)
            self.backgroundColor2 = (25, 25, 25)
            self.buttonColor = (40, 40, 40)
            self.buttonHoverColor = (50, 50, 50)
            self.textColor = (255, 255, 255)
        elif _theme == "light":
            logging.write("Theme: Light", lvl=logger.Logger.INFO)
            self.backgroundColor = (235, 235, 235)
            self.backgroundColor2 = (230, 230, 230)
            self.buttonColor = (215, 215, 215)
            self.buttonHoverColor = (205, 205, 205)
            self.textColor = (0, 0, 0)

        _accentColor = str(_game_settings["accentColor"]).split(",")
        self.accentColor = (int(_accentColor[0]), int(_accentColor[1]), int(_accentColor[2]))
        logging.write("Accent Color: " + str(self.accentColor), lvl=logger.Logger.INFO)

        self.sound = bool(_game_settings["sound"])
        logging.write("Sound Enabled: " + str(self.sound), lvl=logger.Logger.INFO)
        self.music = bool(_game_settings["music"])
        logging.write("Music Enabled: " + str(self.music), lvl=logger.Logger.INFO)

        del _accentColor, _game_settings, _theme # Delete The Temporary Variables To Save Memory

    # def get_parts(self):
    #     parts = []
    #     with open(os.path.join(os.path.dirname(__file__), "parts.txt"), 'r') as f:
    #         for part in f.readlines():
    #             parts.append(part.strip())
    #         f.close()

    #     for part in parts:
    #         if str(part).capitalize() == "And":
    #             self.parts.append(pygame.rect.Rect(0, 0, 50, 25))
    #         elif str(part).capitalize() == "Or":
    #             self.parts.append(pygame.rect.Rect(0, 0, 50, 25))
    #         else:
    #             pass

    @decorators.running_time
    def start_screen(self):
        _font = pygame.font.Font(os.path.join(os.path.dirname(__file__), "Tokeely_Brookings.ttf").replace("modules", "docs/fonts/tokeely-brookings"), 100)
        _buttons = button.ButtonGroup("Start Screen Buttons")
        _buttons.append(button.Button(None, (self.screen.get_width() / 2 - 150 / 2, 400), (200, 100), "Start", 30, os.path.join(os.path.dirname(__file__), "Tokeely_Brookings.ttf").replace("modules", "docs/fonts/tokeely-brookings"), textColor=self.accentColor, color=self.buttonColor, hoverColor=self.buttonHoverColor, borderRadius=15))
        _buttons.append(button.Button(None, (self.screen.get_width() / 2 - 150 / 2, 600), (200, 100), "Settings", 30, os.path.join(os.path.dirname(__file__), "Tokeely_Brookings.ttf").replace("modules", "docs/fonts/tokeely-brookings"), textColor=self.accentColor, color=self.buttonColor, hoverColor=self.buttonHoverColor, borderRadius=15))
        _buttons.append(button.Button(None, (self.screen.get_width() / 2 - 150 / 2, 500), (200, 100), "Quit", 30, os.path.join(os.path.dirname(__file__), "Tokeely_Brookings.ttf").replace("modules", "docs/fonts/tokeely-brookings"), textColor=self.accentColor, color=self.buttonColor, hoverColor=self.buttonHoverColor, borderRadius=15))
        while True:
            self.screen.fill(self.backgroundColor)
            # Draw A Pattern On The Screen For The Background
            for x in range(0, self.screen.get_width(), 10):
                for y in range(0, self.screen.get_height(), 10):
                    pygame.draw.rect(self.screen, (self.backgroundColor2), pygame.rect.Rect(x, y, 5, 5))

            # Buttons
            _buttons.displayButtons()
            _buttons.setPos("Start", (self.screen.get_width() / 2 - 150 / 2, self.screen.get_height() - 450))
            _buttons.setPos("Settings", (self.screen.get_width() / 2 - 150 / 2, self.screen.get_height() - 300))
            _buttons.setPos("Quit", (self.screen.get_width() / 2 - 150 / 2, self.screen.get_height() - 150))
            if _buttons.getPressMode("Start"):
                # logging.write("Starting Game", logger.Logger.INFO)
                logging.write("Entering main()", logging.DEBUG)
                self.main()
            elif _buttons.getPressMode("Quit"):
                logging.close(0)
                pygame.quit()
                sys.exit()
            elif _buttons.getPressMode("Settings"):
                logging.write("Entering settings()", logging.DEBUG)
                self.settings()

            # Text
            self.screen.blit(_font.render("Circuit Learning", True, self.textColor), (self.screen.get_width() / 2 - _font.size("Circuit Learning")[0] / 2, self.screen.get_height() / 3.5 - _font.size("Circuit Learning")[1] / 2))

            # Pygame Events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    logging.close(0)
                    pygame.quit()
                    sys.exit()
            
            _debug.displayDebugText(True, [f"Current Date + Time: {datetime.datetime.now()}", f"Current Uptime: {round(time.perf_counter() - timer, 2)}", "", f"Ticks Per Second (TPS): {60}",  f"Frames Per Second (FPS): {round(self.clock.get_fps(), 2)}", "", f"Process PID: {os.getpid()}", f"RAM Usage: {psutil.Process(os.getpid()).memory_info()[0] / 1000000} Megabytes", f"Total RAM: {round((psutil.virtual_memory()[0] - psutil.virtual_memory()[0] / 8) / 1000000000, 2)} Gigabytes", f"Total Swap: {psutil.swap_memory()[0]} Bytes", f"Total Swap Used: {psutil.swap_memory()[0]} Bytes", f"CPU Usage: {psutil.cpu_percent()}%", "", f"Window Size: {self.screen.get_size()}", f"Mouse POS: {pygame.mouse.get_pos()}", f"Keys Pressed: N/A", f"Mouse Buttons: {pygame.mouse.get_pressed()}", "", f"Current Function: {inspect.stack()[0][3]}", "", f"Playing Music: {pygame.mixer_music.get_busy()}", f"Playing Sound: {pygame.mixer.get_busy()}"])
            _debug.displayLog(True, (1000, 300))
            self.clock.tick(60)
            pygame.display.update()

    @decorators.running_time
    def main(self):

        part_storage = pygame.rect.Rect(self.screen.get_width() - 150, 0, self.screen.get_width(), self.screen.get_height())

        # Paused Screen
        paused = False
        pausedText = pygame.font.Font(os.path.join(os.path.dirname(__file__), "Tokeely_Brookings.ttf").replace("modules", "docs/fonts/tokeely-brookings"), 55)
        transparancy = pygame.Surface((self.screenInfo.current_w, self.screenInfo.current_h)).convert_alpha() # Create Surface
        transparancy.fill((10, 10, 10, 100)) # Fill The Surface With A Transparent Color
        pauseMenu = pygame.rect.Rect(self.screen.get_width() / 2 - 400 / 2, self.screen.get_height() / 2 - 600 / 2, 150, 250)
        pauseMenu.center = (self.screen.get_width() / 2, self.screen.get_height() / 2)
        pauseButtons = button.ButtonGroup("pauseButtons")
        # pauseButtons.append(button.Button(None, (self.screen.get_width() / 2 - 50, 350), (100, 50), "Return", 20, os.path.join(os.path.dirname(__file__), "Tokeely_Brookings.ttf").replace("modules", "docs/fonts/tokeely-brookings"), textColor=(243, 156, 41), color=(40, 40, 40), hoverColor=(50, 50, 50), borderRadius=15))
        pauseButtons.append(button.Button(None, (self.screen.get_width() / 2 - 50, 425), (100, 50), "Save", 20, os.path.join(os.path.dirname(__file__), "Tokeely_Brookings.ttf").replace("modules", "docs/fonts/tokeely-brookings"), textColor=self.accentColor, color=self.buttonColor, hoverColor=self.buttonHoverColor, borderRadius=15))
        pauseButtons.append(button.Button(None, (self.screen.get_width() / 2 - 50, 500), (100, 50), "Quit", 20, os.path.join(os.path.dirname(__file__), "Tokeely_Brookings.ttf").replace("modules", "docs/fonts/tokeely-brookings"), textColor=self.accentColor, color=self.buttonColor, hoverColor=self.buttonHoverColor, borderRadius=15))

        while True:

            self.screen.fill(self.backgroundColor)
            # Draw A Pattern On The Screen For The Background
            for x in range(0, self.screen.get_width(), 10):
                for y in range(0, self.screen.get_height(), 10):
                    pygame.draw.rect(self.screen, self.backgroundColor2, pygame.rect.Rect(x, y, 5, 5))

            # Draw A Rectangle For The Different Components
            # Make The Part Storage Rectangle Expandable And Collapsible When The Mouse Is Hovering Over It
            part_storage.height = self.screen.get_height()
            if part_storage.collidepoint(pygame.mouse.get_pos()):
                part_storage.width = 150
                part_storage.x = self.screen.get_width() - 150
                pygame.draw.rect(self.screen, (50, 50, 50), part_storage)
                # Draw The Different Components That Can Be Used When The Part Storage Rectangle Is Expanded
                # for part in self.parts:
                #     part.center = (self.screen.get_width() - 75, random.randint(0, self.screen.get_height()))
                #     pygame.draw.rect(self.screen, (50, 50, 50), part)
            else:
                part_storage.width = 50
                part_storage.x = self.screen.get_width() - 50
                pygame.draw.rect(self.screen, (50, 50, 50), part_storage)

            

            # Draw The Different Components

            
            # Pygame Events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    logging.close(0)
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE and paused:
                        paused = False
                    elif event.key == pygame.K_ESCAPE:
                        paused = True

            # Pause Menu
            if paused:
                # pauseMenu = pygame.rect.Rect(self.screen.get_width() / 2 - 150 / 2, self.screen.get_height() / 2 - 150 / 2, 400, 600)
                pauseMenu.center = (self.screen.get_width() / 2, self.screen.get_height() / 2)
                # Draw The Transparent Surface And Render The Paused Text
                self.screen.blit(transparancy, (0, 0))
                self.screen.blit(pausedText.render("Paused", True, (243, 156, 41)), (self.screen.get_width() / 2 - pausedText.size("Paused")[0] / 2, self.screen.get_height() / 2 - 600 / 2 + 50))
                # Draw The Pause Menu
                pygame.draw.rect(self.screen, (30, 30, 30), pauseMenu, 0, 15)
                pauseButtons.displayButtons()
                # Make Sure The Buttons Are In The Correct Position If The Screen Is Resized
                # pauseButtons.setPos("Return", (self.screen.get_width() / 2 - 50, 350))
                pauseButtons.setPos("Save", (self.screen.get_width() / 2 - 50, 425))
                pauseButtons.setPos("Quit", (self.screen.get_width() / 2 - 50, 500))

                # if pauseButtons.getPressMode("Return"):
                #     paused = False
                if pauseButtons.getPressMode("Save"):
                    pass # Will Be Implemented Later. Self Explanatory
                if pauseButtons.getPressMode("Quit"):
                    logging.write("Entering start_screen()", logging.DEBUG)
                    self.start_screen() # Plan On Having A Quit Confirmation Screen (I.E. Are You Sure You Want To Quit?)

            _debug.displayDebugText(True, [f"Current Date + Time: {datetime.datetime.now()}", f"Current Uptime: {round(time.perf_counter() - timer, 2)}", "", f"Ticks Per Second (TPS): {60}",  f"Frames Per Second (FPS): {round(self.clock.get_fps(), 2)}", "", f"Process PID: {os.getpid()}", f"RAM Usage: {psutil.Process(os.getpid()).memory_info()[0] / 1000000} Megabytes", f"Total RAM: {round((psutil.virtual_memory()[0] - psutil.virtual_memory()[0] / 8) / 1000000000, 2)} Gigabytes", f"Total Swap: {psutil.swap_memory()[0]} Bytes", f"Total Swap Used: {psutil.swap_memory()[0]} Bytes", f"CPU Usage: {psutil.cpu_percent()}%", "", f"Window Size: {self.screen.get_size()}", f"Mouse POS: {pygame.mouse.get_pos()}", f"Keys Pressed: N/A", f"Mouse Buttons: {pygame.mouse.get_pressed()}", "", f"Current Function: {inspect.stack()[0][3]}", "", f"Playing Music: {pygame.mixer_music.get_busy()}", f"Playing Sound: {pygame.mixer.get_busy()}", f"Is Paused: {paused}"])
            _debug.displayLog(True, (1000, 300))
            self.clock.tick(60)
            pygame.display.update()

    def settings(self):
        # Buttons
        menuButtons = button.ButtonGroup("menuButtons")
        menuButtons.append(button.Button(None, (25, self.screen.get_height() - 75), (100, 50), "Back", 20, os.path.join(os.path.dirname(__file__), "Tokeely_Brookings.ttf").replace("modules", "docs/fonts/tokeely-brookings"), textColor=self.accentColor, color=self.buttonColor, hoverColor=self.buttonHoverColor, borderRadius=15))
        menuButtons.append(button.Button(None, (self.screen.get_width() - 500, self.screen.get_height() - 75), (250, 50), "Check For Updates", 20, os.path.join(os.path.dirname(__file__), "Tokeely_Brookings.ttf").replace("modules", "docs/fonts/tokeely-brookings"), textColor=self.accentColor, color=self.buttonColor, hoverColor=self.buttonHoverColor, borderRadius=15))
        menuButtons.append(button.Button(None, (self.screen.get_width() - 225, self.screen.get_height() - 75), (200, 50), "Apply Settings", 20, os.path.join(os.path.dirname(__file__), "Tokeely_Brookings.ttf").replace("modules", "docs/fonts/tokeely-brookings"), textColor=self.accentColor, color=self.buttonColor, hoverColor=self.buttonHoverColor, borderRadius=15))
        settingButtons = button.ButtonGroup("settingButtons")
        settingButtons.append(button.ToggleButton(None, (self.screen.get_width() / 2 - 150 / 2, 800), (150, 75), "Test Button", "Test Button", 30, os.path.join(os.path.dirname(__file__), "Tokeely_Brookings.ttf").replace("modules", "docs/fonts/tokeely-brookings"), borderRadius=15))
        back_button = button.Button(None, (50, self.screen.get_height() - 100), (100, 50), "Back", 20, os.path.join(os.path.dirname(__file__), "Tokeely_Brookings.ttf").replace("modules", "docs/fonts/tokeely-brookings"), textColor=(243, 156, 41), color=(40, 40, 40), hoverColor=(50, 50, 50), borderRadius=15)

        # Text
        titleText = pygame.font.Font(os.path.join(os.path.dirname(__file__), "Tokeely_Brookings.ttf").replace("modules", "docs/fonts/tokeely-brookings"), 50)

        # Backgrounds
        backgroundRect = pygame.rect.Rect(0, 0, self.screen.get_width() - 200, self.screen.get_height() - 200)
        backgroundRect.center = (self.screen.get_width() / 2, self.screen.get_height() / 2)

        # Variables
        updating = False
        while True:
            self.screen.fill(self.backgroundColor)
            # Draw A Pattern On The Screen For The Background
            for x in range(0, self.screen.get_width(), 10):
                for y in range(0, self.screen.get_height(), 10):
                    pygame.draw.rect(self.screen, self.backgroundColor2, pygame.rect.Rect(x, y, 5, 5))

            # Draw A Background For The Settings
            pygame.draw.rect(self.screen, (30, 30, 30), backgroundRect, 0, 15)

            # Draw The Title Text
            self.screen.blit(titleText.render("Settings", True, (243, 156, 41)), (self.screen.get_width() / 2 - titleText.size("Settings")[0] / 2, 50))

            # Make A Button To Go Back To The Main Menu
            menuButtons.displayButtons()
            for each in menuButtons.getButtonNames():
                if menuButtons.getPressMode(each):
                    if each == "Back":
                        logging.write("Entering start_screen()", logging.DEBUG)
                        self.start_screen()
                    elif each == "Check For Updates" and not updating:
                        # Check For Updates
                        _thread.start_new_thread(self.check_for_updates, ()) # Start A New Thread To Check For Updates So The Game Doesn't Freeze
                        time.sleep(0.1) # Sleep For 0.1 Seconds So The Thread Can Start And The _thread._count() Function Can Update
                        updating = True # Set Updating To True So The Button Can't Be Pressed Again While It's Updating
                    elif each == "Apply Settings":
                        self.apply_settings()

            settingButtons.displayButtons()

            # Check If The Update Thread Is Done
            if _thread._count() < 1:
                updating = False

            if back_button.getPressMode():
                self.start_screen()
            
            # Pygame Events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    logging.close(0)
                    pygame.quit()
                    sys.exit()

            _debug.displayDebugText(True, [f"Current Date + Time: {datetime.datetime.now()}", f"Current Uptime: {round(time.perf_counter() - timer, 2)}", "", f"Ticks Per Second (TPS): {60}",  f"Frames Per Second (FPS): {round(self.clock.get_fps(), 2)}", "", f"Process PID: {os.getpid()}", f"RAM Usage: {psutil.Process(os.getpid()).memory_info()[0] / 1000000} Megabytes", f"Total RAM: {round((psutil.virtual_memory()[0] - psutil.virtual_memory()[0] / 8) / 1000000000, 2)} Gigabytes", f"Total Swap: {psutil.swap_memory()[0]} Bytes", f"Total Swap Used: {psutil.swap_memory()[0]} Bytes", f"CPU Usage: {psutil.cpu_percent()}%", "", f"Window Size: {self.screen.get_size()}", f"Mouse POS: {pygame.mouse.get_pos()}", f"Keys Pressed: N/A", f"Mouse Buttons: {pygame.mouse.get_pressed()}", "", f"Current Function: {inspect.stack()[0][3]}", "", f"Playing Music: {pygame.mixer_music.get_busy()}", f"Playing Sound: {pygame.mixer.get_busy()}"])
            _debug.displayLog(True, (1000, 300))
            self.clock.tick(60)
            pygame.display.update()

    def check_for_updates(self):
        """
        Checks For Updates
        """

        # See If Were Connected To The Internet
        logging.write("Checking For An Active Internet Connection...", logging.INFO)
        if network.check_connection():
            logging.write("Connected To The Internet", logging.INFO)
        else:
            logging.write("No Active Internet Connection Found", logging.WARN)
            logging.write("Using Offline Check", logging.INFO)
            logging.write("Checking For Cached Updates...", logging.INFO)
            if os.path.exists(os.path.join(os.path.dirname(__file__), "outdated_modules.txt")):
                return

        # TODO: Use The Git API To Check For Updates

        # Give Notice For Cached Updates
        logging.write("Updates Downloaded Will Be Cached For Offline Use", logging.NOTICE)

        # Check For Python Updates
        logging.write("Checking For Python Module Updates...", logging.INFO)
        logging.write("Generating Outdated Modules List...", logging.INFO) # No Need To Clear This File In Cache Because It Will Be Overwritten Once An Online Check Is Done
        os.system("python3 -m pip list --outdated | tee {}".format(os.path.join(os.path.dirname(__file__).replace("modules", "docs"), ".cache", "updates", "outdated_modules.txt")))
        logging.write("Stored In {}".format(os.path.join(os.path.dirname(__file__).replace("modules", "docs"), ".cache", "updates", "outdated_modules.txt")), logging.INFO)
        # Check For Required Modules In The Outdated List As Well As Useful Modules (wheel, setuptools and pip)
        with open(os.path.join(os.path.dirname(__file__).replace("modules", "docs"), ".cache", "updates", "outdated_modules.txt"), "r") as f:
            for i, line in enumerate(f):
                if "pygame" in line.split(" ")[0] or "requests" in line.split(" ")[0] or "psutil" in line.split(" ")[0]:
                    logging.write("Found Required Module: {}".format(line.split(" ")[0]), logging.INFO)
                    logging.write("Updating Required Module: {}".format(line.split(" ")[0]), logging.INFO)
                    os.system("python3 -m pip install --upgrade {} | tee -a {}".format(line.split(" ")[0],  os.path.join(os.path.dirname(__file__).replace("modules", "docs"), "logs", "Circuit_Learning.log")))
                elif "wheel" in line.split(" ")[0] or "setuptools" in line.split(" ")[0] or "pip" in line.split(" ")[0]:
                    logging.write("Found Useful Module: {}".format(line.split(" ")[0]), logging.INFO)
                    logging.write("Updating Useful Module: {}".format(line.split(" ")[0]), logging.INFO)
                    os.system("python3 -m pip install --upgrade {} | tee -a {}".format(line.split(" ")[0], os.path.join(os.path.dirname(__file__).replace("modules", "docs"), "logs", "Circuit_Learning.log")))
                elif i >= 2:
                    logging.write("Found Module: {} But Skipping Upgrade".format(line.split(" ")[0]), logging.INFO)
        logging.write("Finished ", logging.INFO)
        

    def apply_settings(self):
        """
        Takes The Current State Of The Settings Menu And Applies Them To The Settings.json File  
        Note: When Settings Are Applied, The Game Needs To Be Restarted For Them To Take Effect

        Takes No Arguments
        """

        logging.write("Applying Settings...", logging.INFO)
        #TODO: Open The Settings.json File And Apply The Settings
        logging.write("Finished", logging.INFO)
        logging.write("A Game Restart Is Required For The Settings To Take Effect", logging.NOTICE)
        

if __name__ == "__main__":
    main = Circuit_Learning()
    main.start_screen()