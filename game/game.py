#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pinproc
import procgame
from procgame import *
import logging

from modes import *

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")

class Lucky7Game(procgame.game.BasicGame):
    def __init__(self):
        super(Lucky7Game, self).__init__(pinproc.MachineTypePDB)

        self.logger = logging.getLogger('game.core')
        self.load_config('config/lucky7.yaml')
        self.sound = procgame.sound.SoundController(self)
        self.setup()
        self.reset()
        self.sound.play_music('music1', loops=-1)
        self.sound.play('sound1')

        self.logger.info("Game Initialized")

    def setup(self):

        # Mode definitions
        self.attract_mode = L7AttractMode(game=self)  # Priority 2 - System Level
        self.score_display_mode = ScoreDisplaysMode(game=self)  # Priority 2 - System Level

        self.sound.register_sound('sound1', 'assets/sfx/drain.wav')
        self.sound.register_music('music1', 'assets/music/mainplay.wav')


if __name__ == '__main__':
    print("////////////////////////////// Lucky 7 Starting ///////////////////////////////")
    game = Lucky7Game()
    game.run_loop()