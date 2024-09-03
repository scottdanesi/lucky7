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
import random

class BaseMode(procgame.game.Mode):
    def __init__(self, game, priority):
        super(BaseMode, self).__init__(game=game, priority=priority)
        self.logger = logging.getLogger('game.BaseMode')

        # LED Scripts
        self.playerBlinkScript = []
        self.playerBlinkScript.append({'color': 'FFFFFF', 'time': 195, 'fade': True})
        self.playerBlinkScript.append({'color': 'FFFFFF', 'time': 195, 'fade': True})
        self.playerBlinkScript.append({'color': '000000', 'time': 195, 'fade': True})
        self.playerBlinkScript.append({'color': '000000', 'time': 195, 'fade': True})

        self.rollBlinkScript = []
        self.rollBlinkScript.append({'color': '000000', 'time': 201, 'fade': True})
        self.rollBlinkScript.append({'color': '000000', 'time': 201, 'fade': True})
        self.rollBlinkScript.append({'color': 'FFFFFF', 'time': 201, 'fade': True})
        self.rollBlinkScript.append({'color': 'FFFFFF', 'time': 201, 'fade': True})

        self.frameBlinkScript = []
        self.frameBlinkScript.append({'color': 'FFFFFF', 'time': 210, 'fade': True})
        self.frameBlinkScript.append({'color': 'FFFFFF', 'time': 210, 'fade': True})
        self.frameBlinkScript.append({'color': '000000', 'time': 210, 'fade': True})
        self.frameBlinkScript.append({'color': '000000', 'time': 210, 'fade': True})

        self.shootForScript = []
        self.shootForScript.append({'color': 'FFFFFF', 'time': 190, 'fade': True})
        self.shootForScript.append({'color': 'FFFFFF', 'time': 190, 'fade': True})
        self.shootForScript.append({'color': '000000', 'time': 190, 'fade': True})
        self.shootForScript.append({'color': '000000', 'time': 190, 'fade': True})

        self.bonusBlinkScript = []
        self.bonusBlinkScript.append({'color': 'FFFFFF', 'time': 175, 'fade': True})
        self.bonusBlinkScript.append({'color': 'FFFFFF', 'time': 175, 'fade': True})
        self.bonusBlinkScript.append({'color': '000000', 'time': 175, 'fade': True})
        self.bonusBlinkScript.append({'color': '000000', 'time': 175, 'fade': True})

        self.bonusBlinkScript7 = []
        self.bonusBlinkScript7.append({'color': 'FFFFFF', 'time': 160, 'fade': True})
        self.bonusBlinkScript7.append({'color': 'FFFFFF', 'time': 160, 'fade': True})
        self.bonusBlinkScript7.append({'color': '000000', 'time': 160, 'fade': True})
        self.bonusBlinkScript7.append({'color': '000000', 'time': 160, 'fade': True})

    def mode_started(self):
        self.game.modes.add(self.game.attract_mode)

    def mode_stopped(self):
        pass

    def update_lamps(self,disableAllPrior=False):

        if self.game.ball == 0:
            # no game in play
            return 0

        if disableAllPrior:
            self.game.utilities_mode.disableAllLEDs("Backglass")

        # Set constant On Lamps
        self.game.LEDs.enable('Big7A',color='FFFFFF')
        self.game.LEDs.enable('Big7B',color='FFFFFF')
        self.game.LEDs.enable('Big7C',color='FFFFFF')
        self.game.LEDs.enable('Big7D',color='FFFFFF')
        self.game.LEDs.enable('Big7E',color='FFFFFF')
        self.game.LEDs.enable('Big7F',color='FFFFFF')
        self.game.LEDs.enable('Big7G',color='FFFFFF')
        self.game.LEDs.enable('Big7H',color='FFFFFF')
        self.game.LEDs.enable('LUCKY_LA',color='FFFFFF')
        self.game.LEDs.enable('LUCKY_LB',color='FFFFFF')
        self.game.LEDs.enable('LUCKY_UA',color='FFFFFF')
        self.game.LEDs.enable('LUCKY_UB',color='FFFFFF')
        self.game.LEDs.enable('LUCKY_CA',color='FFFFFF')
        self.game.LEDs.enable('LUCKY_CB',color='FFFFFF')
        self.game.LEDs.enable('LUCKY_KA',color='FFFFFF')
        self.game.LEDs.enable('LUCKY_KB',color='FFFFFF')
        self.game.LEDs.enable('LUCKY_YA',color='FFFFFF')
        self.game.LEDs.enable('LUCKY_YB',color='FFFFFF')
        self.game.LEDs.enable('BallScoreA',color='FFFFFF')
        self.game.LEDs.enable('BallScoreB',color='FFFFFF')
        self.game.LEDs.enable('BallScoreC',color='FFFFFF')
        self.game.LEDs.enable('ScoreInstA',color='FFFFFF')
        self.game.LEDs.enable('ScoreInstB',color='FFFFFF')
        self.game.LEDs.enable('ScoreInstC',color='FFFFFF')
        self.game.LEDs.enable('ScoreInstD',color='FFFFFF')
        self.game.LEDs.enable('FramesA',color='FFFFFF')
        self.game.LEDs.enable('FramesB',color='FFFFFF')
        self.game.LEDs.enable('FramesC',color='FFFFFF')
        self.game.LEDs.enable('FramesD',color='FFFFFF')

        self.p = self.game.current_player()

        if(self.p.name.upper() == 'PLAYER 1'):
            self.game.LEDs.run_script("Player1A", self.playerBlinkScript)
            self.game.LEDs.run_script("Player1B", self.playerBlinkScript)
            self.game.LEDs.stop_script("Player2A")
            self.game.LEDs.stop_script("Player2B")
        elif(self.p.name.upper() == 'PLAYER 2'):
            self.game.LEDs.run_script("Player2A", self.playerBlinkScript)
            self.game.LEDs.run_script("Player2B", self.playerBlinkScript)
            self.game.LEDs.stop_script("Player1A")
            self.game.LEDs.stop_script("Player1B")

        if(self.game.roll_number == 1):
            self.game.LEDs.run_script("1stRoll", self.rollBlinkScript)
            self.game.LEDs.stop_script("2ndRoll")
        elif(self.game.roll_number == 2):
            self.game.LEDs.run_script("2ndRoll", self.rollBlinkScript)
            self.game.LEDs.stop_script("1stRoll")

        match self.game.ball:
            # Frames
            case 1:
                self.game.LEDs.run_script('ShootUnder7A', self.generateRandomBlinkSpeedScript())
                self.game.LEDs.run_script('ShootUnder7B', self.generateRandomBlinkSpeedScript())
                self.game.LEDs.run_script('ShootUnder7C', self.generateRandomBlinkSpeedScript())
                self.game.LEDs.run_script('ShootUnder7D', self.generateRandomBlinkSpeedScript())
                self.game.LEDs.disable('ShootOver7A')
                self.game.LEDs.disable('ShootOver7B')
                self.game.LEDs.disable('ShootOver7C')

                self.game.LEDs.run_script('RedBonus10', self.bonusBlinkScript)
                self.game.LEDs.disable('RedBonus20')
                self.game.LEDs.disable('RedBonus50')
                self.game.LEDs.disable('YellowBonus10')
                self.game.LEDs.disable('YellowBonus20')
                self.game.LEDs.disable('YellowBonus50')

                self.game.LEDs.run_script('BlueBonus20', self.bonusBlinkScript7)
                self.game.LEDs.disable('BlueBonus50')
                self.game.LEDs.disable('BlueBonus100')

                self.game.LEDs.run_script('Frame1A', self.frameBlinkScript)
                self.game.LEDs.run_script('Frame1B', self.frameBlinkScript)
                self.game.LEDs.disable('Frame2A')
                self.game.LEDs.disable('Frame2B')
                self.game.LEDs.disable('Frame3A')
                self.game.LEDs.disable('Frame3B')
                self.game.LEDs.disable('Frame4A')
                self.game.LEDs.disable('Frame4B')
                self.game.LEDs.disable('Frame5A')
                self.game.LEDs.disable('Frame5B')
                self.game.LEDs.disable('Frame6A')
                self.game.LEDs.disable('Frame6B')
            case 2:
                self.game.LEDs.run_script('ShootUnder7A', self.generateRandomBlinkSpeedScript())
                self.game.LEDs.run_script('ShootUnder7B', self.generateRandomBlinkSpeedScript())
                self.game.LEDs.run_script('ShootUnder7C', self.generateRandomBlinkSpeedScript())
                self.game.LEDs.run_script('ShootUnder7D', self.generateRandomBlinkSpeedScript())
                self.game.LEDs.disable('ShootOver7A')
                self.game.LEDs.disable('ShootOver7B')
                self.game.LEDs.disable('ShootOver7C')

                self.game.LEDs.disable('RedBonus10')
                self.game.LEDs.run_script('RedBonus20', self.bonusBlinkScript)
                self.game.LEDs.disable('RedBonus50')
                self.game.LEDs.disable('YellowBonus10')
                self.game.LEDs.disable('YellowBonus20')
                self.game.LEDs.disable('YellowBonus50')

                self.game.LEDs.run_script('BlueBonus20', self.bonusBlinkScript7)
                self.game.LEDs.disable('BlueBonus50')
                self.game.LEDs.disable('BlueBonus100')

                self.game.LEDs.enable('Frame1A',color='FFFFFF')
                self.game.LEDs.enable('Frame1B',color='FFFFFF')
                self.game.LEDs.run_script('Frame2A', self.frameBlinkScript)
                self.game.LEDs.run_script('Frame2B', self.frameBlinkScript)
                self.game.LEDs.disable('Frame3A')
                self.game.LEDs.disable('Frame3B')
                self.game.LEDs.disable('Frame4A')
                self.game.LEDs.disable('Frame4B')
                self.game.LEDs.disable('Frame5A')
                self.game.LEDs.disable('Frame5B')
                self.game.LEDs.disable('Frame6A')
                self.game.LEDs.disable('Frame6B')
            case 3:
                self.game.LEDs.run_script('ShootUnder7A', self.generateRandomBlinkSpeedScript())
                self.game.LEDs.run_script('ShootUnder7B', self.generateRandomBlinkSpeedScript())
                self.game.LEDs.run_script('ShootUnder7C', self.generateRandomBlinkSpeedScript())
                self.game.LEDs.run_script('ShootUnder7D', self.generateRandomBlinkSpeedScript())
                self.game.LEDs.disable('ShootOver7A')
                self.game.LEDs.disable('ShootOver7B')
                self.game.LEDs.disable('ShootOver7C')

                self.game.LEDs.disable('RedBonus10')
                self.game.LEDs.disable('RedBonus20')
                self.game.LEDs.run_script('RedBonus50', self.bonusBlinkScript)
                self.game.LEDs.disable('YellowBonus10')
                self.game.LEDs.disable('YellowBonus20')
                self.game.LEDs.disable('YellowBonus50')

                self.game.LEDs.disable('BlueBonus20')
                self.game.LEDs.run_script('BlueBonus50', self.bonusBlinkScript7)
                self.game.LEDs.disable('BlueBonus100')

                self.game.LEDs.enable('Frame1A',color='FFFFFF')
                self.game.LEDs.enable('Frame1B',color='FFFFFF')
                self.game.LEDs.enable('Frame2A',color='FFFFFF')
                self.game.LEDs.enable('Frame2B',color='FFFFFF')
                self.game.LEDs.run_script('Frame3A', self.frameBlinkScript)
                self.game.LEDs.run_script('Frame3B', self.frameBlinkScript)
                self.game.LEDs.disable('Frame4A')
                self.game.LEDs.disable('Frame4B')
                self.game.LEDs.disable('Frame5A')
                self.game.LEDs.disable('Frame5B')
                self.game.LEDs.disable('Frame6A')
                self.game.LEDs.disable('Frame6B')
            case 4:
                self.game.LEDs.run_script('ShootOver7A', self.generateRandomBlinkSpeedScript())
                self.game.LEDs.run_script('ShootOver7B', self.generateRandomBlinkSpeedScript())
                self.game.LEDs.run_script('ShootOver7C', self.generateRandomBlinkSpeedScript())
                self.game.LEDs.disable('ShootUnder7A')
                self.game.LEDs.disable('ShootUnder7B')
                self.game.LEDs.disable('ShootUnder7C')
                self.game.LEDs.disable('ShootUnder7D')

                self.game.LEDs.disable('RedBonus10')
                self.game.LEDs.disable('RedBonus20')
                self.game.LEDs.disable('RedBonus50')
                self.game.LEDs.run_script('YellowBonus10', self.bonusBlinkScript)
                self.game.LEDs.disable('YellowBonus20')
                self.game.LEDs.disable('YellowBonus50')

                self.game.LEDs.disable('BlueBonus20')
                self.game.LEDs.run_script('BlueBonus50', self.bonusBlinkScript7)
                self.game.LEDs.disable('BlueBonus100')

                self.game.LEDs.enable('Frame1A',color='FFFFFF')
                self.game.LEDs.enable('Frame1B',color='FFFFFF')
                self.game.LEDs.enable('Frame2A',color='FFFFFF')
                self.game.LEDs.enable('Frame2B',color='FFFFFF')
                self.game.LEDs.enable('Frame3A',color='FFFFFF')
                self.game.LEDs.enable('Frame3B',color='FFFFFF')
                self.game.LEDs.run_script('Frame4A', self.frameBlinkScript)
                self.game.LEDs.run_script('Frame4B', self.frameBlinkScript)
                self.game.LEDs.disable('Frame5A')
                self.game.LEDs.disable('Frame5B')
                self.game.LEDs.disable('Frame6A')
                self.game.LEDs.disable('Frame6B')
            case 5:
                self.game.LEDs.run_script('ShootOver7A', self.generateRandomBlinkSpeedScript())
                self.game.LEDs.run_script('ShootOver7B', self.generateRandomBlinkSpeedScript())
                self.game.LEDs.run_script('ShootOver7C', self.generateRandomBlinkSpeedScript())
                self.game.LEDs.disable('ShootUnder7A')
                self.game.LEDs.disable('ShootUnder7B')
                self.game.LEDs.disable('ShootUnder7C')
                self.game.LEDs.disable('ShootUnder7D')

                self.game.LEDs.disable('RedBonus10')
                self.game.LEDs.disable('RedBonus20')
                self.game.LEDs.disable('RedBonus50')
                self.game.LEDs.disable('YellowBonus10')
                self.game.LEDs.run_script('YellowBonus20', self.bonusBlinkScript)
                self.game.LEDs.disable('YellowBonus50')

                self.game.LEDs.disable('BlueBonus20')
                self.game.LEDs.disable('BlueBonus50')
                self.game.LEDs.run_script('BlueBonus100', self.bonusBlinkScript7)

                self.game.LEDs.enable('Frame1A',color='FFFFFF')
                self.game.LEDs.enable('Frame1B',color='FFFFFF')
                self.game.LEDs.enable('Frame2A',color='FFFFFF')
                self.game.LEDs.enable('Frame2B',color='FFFFFF')
                self.game.LEDs.enable('Frame3A',color='FFFFFF')
                self.game.LEDs.enable('Frame3B',color='FFFFFF')
                self.game.LEDs.enable('Frame4A',color='FFFFFF')
                self.game.LEDs.enable('Frame4B',color='FFFFFF')
                self.game.LEDs.run_script('Frame5A', self.frameBlinkScript)
                self.game.LEDs.run_script('Frame5B', self.frameBlinkScript)
                self.game.LEDs.disable('Frame6A')
                self.game.LEDs.disable('Frame6B')
            case 6:
                self.game.LEDs.run_script('ShootOver7A', self.generateRandomBlinkSpeedScript())
                self.game.LEDs.run_script('ShootOver7B', self.generateRandomBlinkSpeedScript())
                self.game.LEDs.run_script('ShootOver7C', self.generateRandomBlinkSpeedScript())
                self.game.LEDs.disable('ShootUnder7A')
                self.game.LEDs.disable('ShootUnder7B')
                self.game.LEDs.disable('ShootUnder7C')
                self.game.LEDs.disable('ShootUnder7D')

                self.game.LEDs.disable('RedBonus10')
                self.game.LEDs.disable('RedBonus20')
                self.game.LEDs.disable('RedBonus50')
                self.game.LEDs.disable('YellowBonus10')
                self.game.LEDs.disable('YellowBonus20')
                self.game.LEDs.run_script('YellowBonus50', self.bonusBlinkScript)

                self.game.LEDs.disable('BlueBonus20')
                self.game.LEDs.disable('BlueBonus50')
                self.game.LEDs.run_script('BlueBonus100', self.bonusBlinkScript7)

                self.game.LEDs.enable('Frame1A',color='FFFFFF')
                self.game.LEDs.enable('Frame1B',color='FFFFFF')
                self.game.LEDs.enable('Frame2A',color='FFFFFF')
                self.game.LEDs.enable('Frame2B',color='FFFFFF')
                self.game.LEDs.enable('Frame3A',color='FFFFFF')
                self.game.LEDs.enable('Frame3B',color='FFFFFF')
                self.game.LEDs.enable('Frame4A',color='FFFFFF')
                self.game.LEDs.enable('Frame4B',color='FFFFFF')
                self.game.LEDs.enable('Frame5A',color='FFFFFF')
                self.game.LEDs.enable('Frame5B',color='FFFFFF')
                self.game.LEDs.run_script('Frame6A', self.frameBlinkScript)
                self.game.LEDs.run_script('Frame6B', self.frameBlinkScript)

    def generateRandomBlinkSpeedScript(self, minspeed=140, maxspeed=300, length=50):
        # Initialize an empty script list
        script = []

        # Alternate between 'FFFFFF' (on) and '000000' (off)
        colors = ['FFFFFF', '000000']

        for i in range(length):
            # Randomly choose a fade time between minspeed and maxspeed
            random_time = random.randint(minspeed, maxspeed)

            # Alternate the color by using the modulo of the index
            color = colors[i % 2]

            # Append the step to the script list
            script.append({'color': color, 'time': random_time, 'fade': True})

        return script


    def start_game(self):
        self.logger.info("Game Started")

        #Reset Prior Game Scores
        self.game.game_data['LastGameScores']['LastPlayer1Score'] = ' '
        self.game.game_data['LastGameScores']['LastPlayer2Score'] = ' '

        self.game.modes.remove(self.game.attract_mode)

        self.game.add_player() #will be first player at this point
        self.game.ball = 1
        self.game.roll_number = 1

        self.game.score_display_mode.updateScoreDisplays()
        self.game.update_lamps()

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

