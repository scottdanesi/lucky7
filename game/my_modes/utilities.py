################################################################################################
## This mode is the Lucky 7 Utilities Mode.
################################################################################################

###############################
## Global Imports
###############################
import procgame.game
import pygame
from pygame.locals import *
from pygame.font import *

class UtilitiesMode(procgame.game.Mode):
    def __init__(self, game, priority):
        super(UtilitiesMode, self).__init__(game=game, priority=priority)

    def mode_started(self):
        pass

    def mode_stopped(self):
        pass

    ####################################################################################################################
    ## LED UTILITIES
    ####################################################################################################################
    def disableAllLEDs(self, tagFilter=None):
        # This function will stop and disable ALL LEDs in the system and clear the entire queue.
        # use the tagFilter to only disable LEDs with a specific tag in the YAML definition file.
        for led in self.game.leds:
            if tagFilter is None or tagFilter in led.tags:
                self.game.LEDs.stop_script(led.name)
                # Disable by setting all LEDs to 000000, since these are most likely stuck on by default upon boot up.
                self.game.LEDs.enable(led.name, color="000000")
                # Remove from the internal queue list
                self.game.LEDs.disable(led.name)


