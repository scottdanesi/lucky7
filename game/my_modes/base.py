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
        self.game.modes.add(self.game.attract_mode)

    def mode_stopped(self):
        pass

    def start_game(self):
        self.logger.info("Game Started")

        #Reset Prior Game Scores
        self.game.game_data['LastGameScores']['LastPlayer1Score'] = ' '
        self.game.game_data['LastGameScores']['LastPlayer2Score'] = ' '

        self.game.modes.remove(self.game.attract_mode)

        self.game.add_player() #will be first player at this point
        self.game.ball = 1

        self.game.score_display_mode.updateScoreDisplays()

        #self.start_ball()

    def sw_startButton_active_for_2000ms(self, sw):
        #Force Stop Game
        self.logger.warning("FORCE STOPPING GAME")
        #### Reset Game ####
        self.game.reset()

    def sw_startButton_active(self, sw):
        if self.game.ball == 0:
            #Start New Game
            self.start_game()
        elif self.game.ball == 1 and len(self.game.players) < 2:
            #Add Player
            self.game.add_player()
            self.game.score_display_mode.updateScoreDisplays()

