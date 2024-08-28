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

    def mode_started(self):
        self.game.logger.debug("L7 Attract mode started")
        self.set_items(self.game.leds)
        self.disableAllLEDs()
        self.change_led()

    def mode_stopped(self):
        self.game.logger.debug("L7 Attract mode stopped")
        #self.cancel_delayed('next_led')
        # do cleanup of the mode here.

    def startTestLEDShow(self):
        pass

    def change_item(self):
        self.change_led()

    def disableAllLEDs(self):
        # Will move this to utilities mode later on
        for led in self.items:
            # print(f"DISABLING LED: {str(led.name)}")
            # self.game.LEDs.stop_script(led.name)
            self.game.LEDs.disable(led.name)

    def set_items(self, item_list):
        if(len(item_list)>0):
            for self.item in sorted(item_list,key=lambda s: s.label):
                self.items.append(self.item)

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
        self.delay(name='next_led', delay=.3, handler=self.change_led)

    def tick(self):
        super(L7AttractMode, self).tick()
        # Ensure that modes tick correctly
        # self.modes.tick()

