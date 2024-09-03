################################################################################################
## This mode is the Lucky 7 Base Game Mode.
################################################################################################

###############################
## Global Imports
###############################
import procgame.game
import pygame
from pygame.locals import *
from pygame.font import *
import logging

class BaseMode(procgame.game.Mode):
    def __init__(self, game, priority):
        super(BaseMode, self).__init__(game=game, priority=priority)
        self.logger = logging.getLogger('game.BaseMode')

    def mode_started(self):
        pass

    def mode_stopped(self):
        pass