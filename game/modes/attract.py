################################################################################################
## This mode is the Lucky 7 Attract Mode.
################################################################################################

###############################
## Global Imports
###############################
import procgame.game
from procgame.game import AdvancedMode

import pygame
from pygame.locals import *
from pygame.font import *

class L7AttractMode(procgame.game.AdvancedMode):
    """
    Example Mode
    """
    def __init__(self, game):
        super(L7AttractMode, self).__init__(game=game, priority=2, mode_type=AdvancedMode.Game) # 2 is higher than BGM
        # stuff that gets done EXACTLY once.
        # happens when the "parent" Game creates this mode
        pass

    def mode_started(self):
        print("L7 Attract mode started")
        #self.game.displayText("hit the flashing target for bonus")

    def mode_stopped(self):
        print("L7 Attract mode stopped")
        # do cleanup of the mode here.

    def sw_target1_active(self, sw):
        pass
        return procgame.game.SwitchStop


