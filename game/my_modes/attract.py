################################################################################################
## This mode is the Lucky 7 Attract Mode.
################################################################################################

###############################
## Global Imports
###############################
import procgame.game
import pygame
from pygame.locals import *
from pygame.font import *

class L7AttractMode(procgame.game.Mode):
    def __init__(self, game, priority):
        super(L7AttractMode, self).__init__(game=game, priority=priority)
        self.led = None
        self.previousLEDName = None
        self.test_sequence = []
        self.test_sequence.append({'color': 'FFFFFF', 'time': 500, 'fade': False})
        self.test_sequence.append({'color': '000000', 'time': 500, 'fade': False})
        self.delayS = 1
        self.items = []
        self.item = None
        self.current_index = 0  # Index to track current LED
        self.set_items(self.game.leds)

        ###############################################################################################################
        ## BIG 7 Lightshow Script
        ###############################################################################################################
        self.Big7LEDScriptFade = 200

        # Define the patterns for each script
        self.Big7Lightshows = {
            'A': ['FFFFFF', 'FFFFFF', 'FFFFFF', '000000', '000000', '000000', '000000', '000000'],
            'B': ['000000', 'FFFFFF', 'FFFFFF', 'FFFFFF', '000000', '000000', '000000', '000000'],
            'C': ['000000', '000000', 'FFFFFF', 'FFFFFF', 'FFFFFF', '000000', '000000', '000000'],
            'D': ['000000', '000000', '000000', 'FFFFFF', 'FFFFFF', 'FFFFFF', '000000', '000000'],
            'E': ['000000', '000000', '000000', '000000', 'FFFFFF', 'FFFFFF', 'FFFFFF', '000000'],
            'F': ['000000', '000000', '000000', '000000', '000000', 'FFFFFF', 'FFFFFF', 'FFFFFF'],
            'G': ['FFFFFF', '000000', '000000', '000000', '000000', '000000', 'FFFFFF', 'FFFFFF'],
            'H': ['FFFFFF', 'FFFFFF', '000000', '000000', '000000', '000000', '000000', 'FFFFFF'],
        }

        ###############################################################################################################
        ## LUCKY Lightshow Script
        ###############################################################################################################
        self.LUCKYScriptFade = 175

        self.LUCKYLightshows = {
            'A': ['FFFFFF', '000000', '000000', '000000', '000000', '000000', '000000', '000000'],
            'B': ['000000', 'FFFFFF', '000000', '000000', '000000', '000000', '000000', 'FFFFFF'],
            'C': ['000000', '000000', 'FFFFFF', '000000', '000000', '000000', 'FFFFFF', '000000'],
            'D': ['000000', '000000', '000000', 'FFFFFF', '000000', 'FFFFFF', '000000', '000000'],
            'E': ['000000', '000000', '000000', '000000', 'FFFFFF', '000000', '000000', '000000'],
        }

        ###############################################################################################################
        ## Score Numbers Lightshow Scripts
        ###############################################################################################################
        self.ScoreNumberScriptFade = 220

        self.ScoreNumbersLightshows = {
            'A': ['FFFFFF', '000000', '000000', '000000', '000000', '000000', '000000', '000000', '000000', '000000', '000000', '000000', '000000', '000000', '000000', '000000'],
            'B': ['000000', 'FFFFFF', '000000', '000000', '000000', '000000', '000000', '000000', '000000', '000000', '000000', '000000', '000000', '000000', '000000', '000000'],
            'C': ['000000', '000000', 'FFFFFF', '000000', '000000', '000000', '000000', '000000', '000000', '000000', '000000', '000000', '000000', '000000', '000000', '000000'],
            'D': ['000000', '000000', '000000', 'FFFFFF', '000000', '000000', '000000', '000000', '000000', '000000', '000000', '000000', '000000', '000000', '000000', '000000'],
            'E': ['000000', '000000', '000000', '000000', 'FFFFFF', '000000', '000000', '000000', '000000', '000000', '000000', '000000', '000000', '000000', '000000', '000000'],
            'F': ['000000', '000000', '000000', '000000', '000000', 'FFFFFF', '000000', '000000', '000000', '000000', '000000', '000000', '000000', '000000', '000000', '000000'],
            'G': ['000000', '000000', '000000', '000000', '000000', '000000', 'FFFFFF', '000000', 'FFFFFF', '000000', 'FFFFFF', '000000', '000000', '000000', '000000', '000000'],
            'H': ['000000', '000000', '000000', '000000', '000000', '000000', '000000', '000000', '000000', '000000', '000000', 'FFFFFF', '000000', '000000', '000000', '000000'],
            'I': ['000000', '000000', '000000', '000000', '000000', '000000', '000000', '000000', '000000', '000000', '000000', '000000', 'FFFFFF', '000000', '000000', '000000'],
            'J': ['000000', '000000', '000000', '000000', '000000', '000000', '000000', '000000', '000000', '000000', '000000', '000000', '000000', 'FFFFFF', '000000', '000000'],
            'K': ['000000', '000000', '000000', '000000', '000000', '000000', '000000', '000000', '000000', '000000', '000000', '000000', '000000', '000000', 'FFFFFF', '000000'],
            'L': ['000000', '000000', '000000', '000000', '000000', '000000', '000000', '000000', '000000', '000000', '000000', '000000', '000000', '000000', '000000', 'FFFFFF'],
        }

        ###############################################################################################################
        ## Player 1 and 2 Lightshow Scripts
        ###############################################################################################################
        self.Player1Player2ScriptFade = 905

        self.Player1Player2Lightshows = {
            'A': ['FFFFFF', '000000'],
            'B': ['000000', 'FFFFFF'],
        }

        ###############################################################################################################
        ## Frame Numbers Lightshow Scripts
        ###############################################################################################################
        self.FrameNumberScriptFade = 90

        self.FrameNumbersLightshows = {
            'A': ['FFFFFF', '000000', '000000', '000000', '000000', '000000', '000000', '000000', '000000', '000000', '000000', '000000', '000000', '000000', '000000', '000000'],
            'B': ['000000', 'FFFFFF', '000000', '000000', '000000', '000000', '000000', '000000', '000000', '000000', '000000', '000000', '000000', '000000', '000000', '000000'],
            'C': ['000000', '000000', 'FFFFFF', '000000', '000000', '000000', '000000', '000000', '000000', '000000', '000000', '000000', '000000', '000000', '000000', '000000'],
            'D': ['000000', '000000', '000000', 'FFFFFF', '000000', '000000', '000000', '000000', '000000', '000000', '000000', '000000', '000000', '000000', '000000', '000000'],
            'E': ['000000', '000000', '000000', '000000', 'FFFFFF', '000000', '000000', '000000', '000000', '000000', '000000', '000000', '000000', '000000', '000000', '000000'],
            'F': ['000000', '000000', '000000', '000000', '000000', 'FFFFFF', '000000', '000000', '000000', '000000', '000000', '000000', '000000', '000000', '000000', '000000'],
            'G': ['000000', '000000', '000000', '000000', '000000', '000000', 'FFFFFF', 'FFFFFF', '000000', '000000', 'FFFFFF', 'FFFFFF', '000000', '000000', 'FFFFFF', 'FFFFFF'],
        }

        ###############################################################################################################
        ## Score Numbers Lightshow Scripts
        ###############################################################################################################
        self.BonusNumberScriptFade = 160

        self.BonusNumbersLightshows = {
            'A': ['FFFFFF', '000000', '000000', '000000', '000000', '000000', '000000', '000000', '000000', '000000', '000000', '000000', '000000'],
            'B': ['000000', 'FFFFFF', '000000', '000000', '000000', '000000', '000000', '000000', '000000', '000000', '000000', '000000', '000000'],
            'C': ['000000', '000000', 'FFFFFF', '000000', '000000', '000000', '000000', '000000', '000000', '000000', '000000', '000000', '000000'],
            'D': ['000000', '000000', '000000', 'FFFFFF', '000000', '000000', '000000', '000000', '000000', '000000', '000000', '000000', '000000'],
            'E': ['000000', '000000', '000000', '000000', 'FFFFFF', '000000', '000000', '000000', '000000', '000000', '000000', '000000', '000000'],
            'F': ['000000', '000000', '000000', '000000', '000000', 'FFFFFF', '000000', '000000', '000000', '000000', '000000', '000000', '000000'],
            'G': ['000000', '000000', '000000', '000000', '000000', '000000', 'FFFFFF', '000000', '000000', '000000', '000000', '000000', '000000'],
            'H': ['000000', '000000', '000000', '000000', '000000', '000000', '000000', 'FFFFFF', '000000', '000000', '000000', '000000', '000000'],
            'I': ['000000', '000000', '000000', '000000', '000000', '000000', '000000', '000000', 'FFFFFF', '000000', '000000', '000000', '000000'],
        }

    def mode_started(self):
        self.game.logger.debug("L7 Attract mode started")
        self.set_items(self.game.leds)
        self.game.utilities_mode.disableAllLEDs("Backglass")
        self.defineLightshows()
        self.startLightshow1()

    def mode_stopped(self):
        self.game.logger.debug("L7 Attract mode stopped")
        self.game.utilities_mode.disableAllLEDs("Backglass")
        #self.cancel_delayed('next_led')
        # do cleanup of the mode here.

    def defineLightshows(self):
        pass

    def create_led_script(self, fade_time, pattern):
        script = []
        for color in pattern:
            script.append({'color': color, 'time': fade_time, 'fade': True})
        return script

    def startTestLEDShow(self):
        pass

    def change_item(self):
        self.change_led()

    def disableAllLEDs(self):
        # Will move this to utilities mode later on
        for led in self.items:
            # print(f"DISABLING LED: {str(led.name)}")
            self.game.LEDs.stop_script(led.name)
            # Disable by setting all LEDs to 000000, since these are most likely stuck on by default upon boot up.
            self.game.LEDs.enable(led.name,color="000000")

    def set_items(self, item_list):
        if(len(item_list)>0):
            for self.item in sorted(item_list,key=lambda s: s.label):
                self.items.append(self.item)

    def startLightshow1(self):
        self.game.LEDs.run_script("Big7A", self.create_led_script(self.Big7LEDScriptFade, self.Big7Lightshows['A']))
        self.game.LEDs.run_script("Big7B", self.create_led_script(self.Big7LEDScriptFade, self.Big7Lightshows['B']))
        self.game.LEDs.run_script("Big7C", self.create_led_script(self.Big7LEDScriptFade, self.Big7Lightshows['C']))
        self.game.LEDs.run_script("Big7D", self.create_led_script(self.Big7LEDScriptFade, self.Big7Lightshows['D']))
        self.game.LEDs.run_script("Big7E", self.create_led_script(self.Big7LEDScriptFade, self.Big7Lightshows['E']))
        self.game.LEDs.run_script("Big7F", self.create_led_script(self.Big7LEDScriptFade, self.Big7Lightshows['F']))
        self.game.LEDs.run_script("Big7G", self.create_led_script(self.Big7LEDScriptFade, self.Big7Lightshows['G']))
        self.game.LEDs.run_script("Big7H", self.create_led_script(self.Big7LEDScriptFade, self.Big7Lightshows['H']))

        self.game.LEDs.run_script("LUCKY_LA", self.create_led_script(self.LUCKYScriptFade, self.LUCKYLightshows['A']))
        self.game.LEDs.run_script("LUCKY_LB", self.create_led_script(self.LUCKYScriptFade, self.LUCKYLightshows['A']))
        self.game.LEDs.run_script("LUCKY_UA", self.create_led_script(self.LUCKYScriptFade, self.LUCKYLightshows['B']))
        self.game.LEDs.run_script("LUCKY_UB", self.create_led_script(self.LUCKYScriptFade, self.LUCKYLightshows['B']))
        self.game.LEDs.run_script("LUCKY_CA", self.create_led_script(self.LUCKYScriptFade, self.LUCKYLightshows['C']))
        self.game.LEDs.run_script("LUCKY_CB", self.create_led_script(self.LUCKYScriptFade, self.LUCKYLightshows['C']))
        self.game.LEDs.run_script("LUCKY_KA", self.create_led_script(self.LUCKYScriptFade, self.LUCKYLightshows['D']))
        self.game.LEDs.run_script("LUCKY_KB", self.create_led_script(self.LUCKYScriptFade, self.LUCKYLightshows['D']))
        self.game.LEDs.run_script("LUCKY_YA", self.create_led_script(self.LUCKYScriptFade, self.LUCKYLightshows['E']))
        self.game.LEDs.run_script("LUCKY_YB", self.create_led_script(self.LUCKYScriptFade, self.LUCKYLightshows['E']))

        self.game.LEDs.run_script("Score1", self.create_led_script(self.ScoreNumberScriptFade, self.ScoreNumbersLightshows['A']))
        self.game.LEDs.run_script("Score2", self.create_led_script(self.ScoreNumberScriptFade, self.ScoreNumbersLightshows['B']))
        self.game.LEDs.run_script("Score3", self.create_led_script(self.ScoreNumberScriptFade, self.ScoreNumbersLightshows['C']))
        self.game.LEDs.run_script("Score4", self.create_led_script(self.ScoreNumberScriptFade, self.ScoreNumbersLightshows['D']))
        self.game.LEDs.run_script("Score5", self.create_led_script(self.ScoreNumberScriptFade, self.ScoreNumbersLightshows['E']))
        self.game.LEDs.run_script("Score6", self.create_led_script(self.ScoreNumberScriptFade, self.ScoreNumbersLightshows['F']))
        self.game.LEDs.run_script("Score7A", self.create_led_script(self.ScoreNumberScriptFade, self.ScoreNumbersLightshows['G']))
        self.game.LEDs.run_script("Score7B", self.create_led_script(self.ScoreNumberScriptFade, self.ScoreNumbersLightshows['G']))
        self.game.LEDs.run_script("Score8", self.create_led_script(self.ScoreNumberScriptFade, self.ScoreNumbersLightshows['H']))
        self.game.LEDs.run_script("Score9", self.create_led_script(self.ScoreNumberScriptFade, self.ScoreNumbersLightshows['I']))
        self.game.LEDs.run_script("Score10", self.create_led_script(self.ScoreNumberScriptFade, self.ScoreNumbersLightshows['J']))
        self.game.LEDs.run_script("Score11", self.create_led_script(self.ScoreNumberScriptFade, self.ScoreNumbersLightshows['K']))
        self.game.LEDs.run_script("Score12", self.create_led_script(self.ScoreNumberScriptFade, self.ScoreNumbersLightshows['L']))

        self.game.LEDs.run_script("Player1A", self.create_led_script(self.Player1Player2ScriptFade, self.Player1Player2Lightshows['A']))
        self.game.LEDs.run_script("Player1B", self.create_led_script(self.Player1Player2ScriptFade, self.Player1Player2Lightshows['A']))
        self.game.LEDs.run_script("Player2A", self.create_led_script(self.Player1Player2ScriptFade, self.Player1Player2Lightshows['B']))
        self.game.LEDs.run_script("Player2B", self.create_led_script(self.Player1Player2ScriptFade, self.Player1Player2Lightshows['B']))

        self.game.LEDs.run_script("Frame1A", self.create_led_script(self.FrameNumberScriptFade, self.FrameNumbersLightshows['A']))
        self.game.LEDs.run_script("Frame1B", self.create_led_script(self.FrameNumberScriptFade, self.FrameNumbersLightshows['A']))
        self.game.LEDs.run_script("Frame2A", self.create_led_script(self.FrameNumberScriptFade, self.FrameNumbersLightshows['B']))
        self.game.LEDs.run_script("Frame2B", self.create_led_script(self.FrameNumberScriptFade, self.FrameNumbersLightshows['B']))
        self.game.LEDs.run_script("Frame3A", self.create_led_script(self.FrameNumberScriptFade, self.FrameNumbersLightshows['C']))
        self.game.LEDs.run_script("Frame3B", self.create_led_script(self.FrameNumberScriptFade, self.FrameNumbersLightshows['C']))
        self.game.LEDs.run_script("Frame4A", self.create_led_script(self.FrameNumberScriptFade, self.FrameNumbersLightshows['D']))
        self.game.LEDs.run_script("Frame4B", self.create_led_script(self.FrameNumberScriptFade, self.FrameNumbersLightshows['D']))
        self.game.LEDs.run_script("Frame5A", self.create_led_script(self.FrameNumberScriptFade, self.FrameNumbersLightshows['E']))
        self.game.LEDs.run_script("Frame5B", self.create_led_script(self.FrameNumberScriptFade, self.FrameNumbersLightshows['E']))
        self.game.LEDs.run_script("Frame6A", self.create_led_script(self.FrameNumberScriptFade, self.FrameNumbersLightshows['F']))
        self.game.LEDs.run_script("Frame6B", self.create_led_script(self.FrameNumberScriptFade, self.FrameNumbersLightshows['F']))
        self.game.LEDs.run_script("GameOverA", self.create_led_script(self.FrameNumberScriptFade, self.FrameNumbersLightshows['G']))
        self.game.LEDs.run_script("GameOverB", self.create_led_script(self.FrameNumberScriptFade, self.FrameNumbersLightshows['G']))

        self.game.LEDs.run_script("RedBonus50", self.create_led_script(self.BonusNumberScriptFade, self.BonusNumbersLightshows['A']))
        self.game.LEDs.run_script("RedBonus20", self.create_led_script(self.BonusNumberScriptFade, self.BonusNumbersLightshows['B']))
        self.game.LEDs.run_script("RedBonus10", self.create_led_script(self.BonusNumberScriptFade, self.BonusNumbersLightshows['C']))
        self.game.LEDs.run_script("BlueBonus20", self.create_led_script(self.BonusNumberScriptFade, self.BonusNumbersLightshows['D']))
        self.game.LEDs.run_script("BlueBonus50", self.create_led_script(self.BonusNumberScriptFade, self.BonusNumbersLightshows['E']))
        self.game.LEDs.run_script("BlueBonus100", self.create_led_script(self.BonusNumberScriptFade, self.BonusNumbersLightshows['F']))
        self.game.LEDs.run_script("YellowBonus10", self.create_led_script(self.BonusNumberScriptFade, self.BonusNumbersLightshows['G']))
        self.game.LEDs.run_script("YellowBonus20", self.create_led_script(self.BonusNumberScriptFade, self.BonusNumbersLightshows['H']))
        self.game.LEDs.run_script("YellowBonus50", self.create_led_script(self.BonusNumberScriptFade, self.BonusNumbersLightshows['I']))

    def change_led(self):
        if not self.items:
            return  # If the list is empty, do nothing

        self.item = self.items[self.current_index]
        self.game.logger.debug("ATTRACT LED TRIGGERED: " + str(self.item.name))

        if self.previousLEDName is not None:
            #self.game.LEDs.stop_script(self.previousLEDName)
            self.game.LEDs.disable(self.previousLEDName)
            #self.game.LEDs.enable(self.item.name,color="FFFFFF",dest_color="000000",fade=150, blend=True)

        #self.game.LEDs.run_script(self.item.name, self.test_sequence)
        self.game.LEDs.enable(self.item.name,color="FFFFFF",fade=0, blend=True)
        self.previousLEDName = self.item.name
        self.led = self.item.name

        # Increment the index and loop back if necessary
        self.current_index = (self.current_index + 1) % len(self.items)

        # Set up the next delay
        self.delay(name='next_led', delay=.05, handler=self.change_led)

    def tick(self):
        super(L7AttractMode, self).tick()
        # Ensure that modes tick correctly
        # self.modes.tick()

