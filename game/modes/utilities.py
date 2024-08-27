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
    def __init__(self, game):
        super(L7AttractMode, self).__init__(game=game, priority=2) # 2 is higher than BGM
        self.led = None
        self.previousLEDName = None
        self.test_sequence = []
        self.test_sequence.append({'color': 'FFFFFF', 'time': 500, 'fade': False})
        self.test_sequence.append({'color': '000000', 'time': 500, 'fade': False})
        self.delayS = 1
        self.items = []
        self.item = None
        self.set_items(self.game.leds)

    def mode_started(self):
        print("L7 Attract mode started")
        self.set_items(self.game.leds)
        self.disableAllLEDs()
        self.change_led()

    def mode_stopped(self):
        print("L7 Attract mode stopped")
        self.cancel_delayed('next_led')
        self.disableAllLEDs()
        # do cleanup of the mode here.

    def startTestLEDShow(self):
        pass

    def change_item(self):
        self.change_led()

    def disableAllLEDs(self):
        # Will move this to utilities mode later on
        for led in self.game.leds:
            self.game.LEDs.stop_script(led.name)
            self.game.LEDs.disable(led.name)

    def set_items(self, item_list):
        if(len(item_list)>0):
            for self.item in sorted(item_list,key=lambda s: s.label):
                self.items.append(self.item)

    def change_led(self):
        print ("ATTRACT LED TRIGGERED: " + str(self.item.name))
        if self.previousLEDName is not None:
            self.game.LEDs.stop_script(self.previousLEDName)
        self.game.LEDs.run_script(self.item.name, self.test_sequence)
        self.previousLEDName = self.item.name
        self.led = self.item
        self.delay(name='next_led', event_type=None, delay=self.delayS, handler=self.change_led)

