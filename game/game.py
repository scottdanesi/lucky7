#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pinproc
import procgame
from procgame.game import BasicGame
from procgame.game import GameController
from procgame import *
import procgame.game
import logging

from my_modes import *

logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")

class Lucky7Game(game.BasicGame):
    def __init__(self):
        super(Lucky7Game, self).__init__(pinproc.MachineTypePDB)
        # Global Game Variables
        self.versionMajor = "V.01"
        self.versionMinor = "r.04"
        self.logger = logging.getLogger('game.core')
        self.load_config('config/lucky7.yaml')

        self.sound = procgame.sound.SoundController(self)
        self.setup()
        #self.reset()
        #self.sound.play_music('music1', loops=-1)
        #self.sound.play('sound1')
        self.logger.info("Game Initialized")

    def setup(self):
        # System Mode definitions
        self.utilities_mode = UtilitiesMode(game=self,priority=0)
        self.service_mode = ServiceMode(game=self,priority=1)
        self.score_display_mode = ScoreDisplaysMode(game=self,priority=2)

        # Game Modes
        self.attract_mode = L7AttractMode(game=self,priority=5)

        # Add System Level Modes
        self.modes.add(self.utilities_mode)
        self.modes.add(self.service_mode)
        self.modes.add(self.score_display_mode)

        self.reset()


        #self.sound.register_sound('sound1', 'assets/sfx/drain.wav')
        #self.sound.register_music('music1', 'assets/music/mainplay.wav')

    def reset(self):
        # Let's disable all the LEDs and set them to an off state upon startup.
        for led in self.leds:
            self.LEDs.disable(led.name)

        # Reset all global variables, remove all modes and add back in attract mode.
        # Remove Game Specific Modes
        self.modes.remove(self.attract_mode)

        # Add Attract Mode back in
        self.modes.add(self.attract_mode)


    def tick(self):
        super(Lucky7Game, self).tick()
        # Ensure that modes tick correctly
        # self.modes.tick()

if __name__ == '__main__':
    print("////////////////////////////// Lucky 7 Starting ///////////////////////////////")
    game = Lucky7Game()
    game.run_loop()