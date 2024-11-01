################################################################################################
## This mode is the Lucky 7 Base Game Mode.
################################################################################################
from cgitb import handler

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

        # Global Variables
        self.logger = logging.getLogger('game.BaseMode')
        self.p = self.game.current_player()
        self.lastRollExtraBall = False


        # Global Settings
        self.scoreGapSpeedS = 0.3
        self.scoreCalculating = False

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

        self.madeBonusFlashScript = []
        self.madeBonusFlashScript.append({'color': 'FFFFFF', 'time': 100, 'fade': False})
        self.madeBonusFlashScript.append({'color': '000000', 'time': 100, 'fade': False})

    def mode_started(self):
        self.game.enable_flippers(enable=False)
        self.game.modes.add(self.game.attract_mode)

    def mode_stopped(self):
        pass

    def update_lamps(self,disableAllPrior=True):

        if self.game.ball == 0:
            # no game in play
            return 0

        if disableAllPrior:
            self.game.utilities_mode.disableAllLEDs("Backglass")

        self.game.utilities_mode.setBallReturnLED(r=0,g=255,b=0,pulsetime=0)

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

        if(self.game.current_player_index == 0):
            self.game.LEDs.stop_script("Player1A")
            self.game.LEDs.stop_script("Player1B")
            self.game.LEDs.disable('Player1A')
            self.game.LEDs.disable('Player1B')
            self.game.LEDs.stop_script("Player2A")
            self.game.LEDs.stop_script("Player2B")
            self.game.LEDs.disable('Player2A')
            self.game.LEDs.disable('Player2B')
            self.game.LEDs.run_script("Player1A", self.playerBlinkScript)
            self.game.LEDs.run_script("Player1B", self.playerBlinkScript)
        elif(self.game.current_player_index == 1):
            self.game.LEDs.stop_script("Player1A")
            self.game.LEDs.stop_script("Player1B")
            self.game.LEDs.disable('Player1A')
            self.game.LEDs.disable('Player1B')
            self.game.LEDs.stop_script("Player2A")
            self.game.LEDs.stop_script("Player2B")
            self.game.LEDs.disable('Player2A')
            self.game.LEDs.disable('Player2B')
            self.game.LEDs.run_script("Player2A", self.playerBlinkScript)
            self.game.LEDs.run_script("Player2B", self.playerBlinkScript)

        if(self.game.roll_number == 1):
            self.game.LEDs.stop_script("2ndRoll")
            self.game.LEDs.run_script("1stRoll", self.rollBlinkScript)

        elif(self.game.roll_number == 2):
            self.game.LEDs.run_script("2ndRoll", self.rollBlinkScript)
            self.game.LEDs.stop_script("1stRoll")

        # Grab the current Ball Roll Score
        self.currentBallScore = self.getPlayerData(self.game.current_player_index + 1, self.game.ball, 1) + self.getPlayerData(self.game.current_player_index + 1, self.game.ball, 2)

        self.game.LEDs.disable('Score1')
        self.game.LEDs.disable('Score2')
        self.game.LEDs.disable('Score3')
        self.game.LEDs.disable('Score4')
        self.game.LEDs.disable('Score5')
        self.game.LEDs.disable('Score6')
        self.game.LEDs.disable('Score7A')
        self.game.LEDs.disable('Score7B')
        self.game.LEDs.disable('Score8')
        self.game.LEDs.disable('Score9')
        self.game.LEDs.disable('Score10')
        self.game.LEDs.disable('Score11')
        self.game.LEDs.disable('Score12')

        match self.currentBallScore:
            case 1:
                self.game.LEDs.enable('Score1',color='FFFFFF')
            case 2:
                self.game.LEDs.enable('Score2',color='FFFFFF')
            case 3:
                self.game.LEDs.enable('Score3',color='FFFFFF')
            case 4:
                self.game.LEDs.enable('Score4',color='FFFFFF')
            case 5:
                self.game.LEDs.enable('Score5',color='FFFFFF')
            case 6:
                self.game.LEDs.enable('Score6',color='FFFFFF')
            case 7:
                self.game.LEDs.run_script("Score7A", self.madeBonusFlashScript)
                self.game.LEDs.run_script("Score7B", self.madeBonusFlashScript)
                self.game.LEDs.run_script("BlueBonusMadeA", self.madeBonusFlashScript)
                self.game.LEDs.run_script("BlueBonusMadeB", self.madeBonusFlashScript)
                self.game.LEDs.run_script("BlueBonusMadeC", self.madeBonusFlashScript)
            case 8:
                self.game.LEDs.enable('Score8',color='FFFFFF')
            case 9:
                self.game.LEDs.enable('Score9',color='FFFFFF')
            case 10:
                self.game.LEDs.enable('Score10',color='FFFFFF')
            case 11:
                self.game.LEDs.enable('Score11',color='FFFFFF')
            case 12:
                self.game.LEDs.enable('Score12',color='FFFFFF')

        if self.lastRollExtraBall:
            self.game.LEDs.enable('ExtraBallA',color='FFFFFF')
            self.game.LEDs.enable('ExtraBallB',color='FFFFFF')
            self.game.LEDs.enable('ExtraBallC',color='FFFFFF')
            self.game.LEDs.enable('ExtraBallD',color='FFFFFF')

        match self.game.ball:
            # Frames
            case 1:
                if self.currentBallScore < 7 and self.game.roll_number == 2 and self.scoreCalculating == True:
                    self.game.LEDs.run_script("RedBonusMadeA", self.madeBonusFlashScript)
                    self.game.LEDs.run_script("RedBonusMadeB", self.madeBonusFlashScript)
                    self.game.LEDs.run_script("RedBonusMadeC", self.madeBonusFlashScript)

                self.game.LEDs.run_script('ShootUnder7A', self.game.utilities_mode.generateRandomBlinkSpeedScript())
                self.game.LEDs.run_script('ShootUnder7B', self.game.utilities_mode.generateRandomBlinkSpeedScript())
                self.game.LEDs.run_script('ShootUnder7C', self.game.utilities_mode.generateRandomBlinkSpeedScript())
                self.game.LEDs.run_script('ShootUnder7D', self.game.utilities_mode.generateRandomBlinkSpeedScript())
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
                if self.currentBallScore < 7 and self.game.roll_number == 2 and self.scoreCalculating == True:
                    self.game.LEDs.run_script("RedBonusMadeA", self.madeBonusFlashScript)
                    self.game.LEDs.run_script("RedBonusMadeB", self.madeBonusFlashScript)
                    self.game.LEDs.run_script("RedBonusMadeC", self.madeBonusFlashScript)

                self.game.LEDs.run_script('ShootUnder7A', self.game.utilities_mode.generateRandomBlinkSpeedScript())
                self.game.LEDs.run_script('ShootUnder7B', self.game.utilities_mode.generateRandomBlinkSpeedScript())
                self.game.LEDs.run_script('ShootUnder7C', self.game.utilities_mode.generateRandomBlinkSpeedScript())
                self.game.LEDs.run_script('ShootUnder7D', self.game.utilities_mode.generateRandomBlinkSpeedScript())
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
                if self.currentBallScore < 7 and self.game.roll_number == 2 and self.scoreCalculating == True:
                    self.game.LEDs.run_script("RedBonusMadeA", self.madeBonusFlashScript)
                    self.game.LEDs.run_script("RedBonusMadeB", self.madeBonusFlashScript)
                    self.game.LEDs.run_script("RedBonusMadeC", self.madeBonusFlashScript)

                self.game.LEDs.run_script('ShootUnder7A', self.game.utilities_mode.generateRandomBlinkSpeedScript())
                self.game.LEDs.run_script('ShootUnder7B', self.game.utilities_mode.generateRandomBlinkSpeedScript())
                self.game.LEDs.run_script('ShootUnder7C', self.game.utilities_mode.generateRandomBlinkSpeedScript())
                self.game.LEDs.run_script('ShootUnder7D', self.game.utilities_mode.generateRandomBlinkSpeedScript())
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
                if self.currentBallScore > 7 and self.game.roll_number == 2 and self.scoreCalculating == True:
                    self.game.LEDs.run_script("YellowBonusMadeA", self.madeBonusFlashScript)
                    self.game.LEDs.run_script("YellowBonusMadeB", self.madeBonusFlashScript)

                self.game.LEDs.run_script('ShootOver7A', self.game.utilities_mode.generateRandomBlinkSpeedScript())
                self.game.LEDs.run_script('ShootOver7B', self.game.utilities_mode.generateRandomBlinkSpeedScript())
                self.game.LEDs.run_script('ShootOver7C', self.game.utilities_mode.generateRandomBlinkSpeedScript())
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
                if self.currentBallScore > 7 and self.game.roll_number == 2 and self.scoreCalculating == True:
                    self.game.LEDs.run_script("YellowBonusMadeA", self.madeBonusFlashScript)
                    self.game.LEDs.run_script("YellowBonusMadeB", self.madeBonusFlashScript)

                self.game.LEDs.run_script('ShootOver7A', self.game.utilities_mode.generateRandomBlinkSpeedScript())
                self.game.LEDs.run_script('ShootOver7B', self.game.utilities_mode.generateRandomBlinkSpeedScript())
                self.game.LEDs.run_script('ShootOver7C', self.game.utilities_mode.generateRandomBlinkSpeedScript())
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
                if self.currentBallScore > 7 and self.game.roll_number == 2 and self.scoreCalculating == True:
                    self.game.LEDs.run_script("YellowBonusMadeA", self.madeBonusFlashScript)
                    self.game.LEDs.run_script("YellowBonusMadeB", self.madeBonusFlashScript)

                self.game.LEDs.run_script('ShootOver7A', self.game.utilities_mode.generateRandomBlinkSpeedScript())
                self.game.LEDs.run_script('ShootOver7B', self.game.utilities_mode.generateRandomBlinkSpeedScript())
                self.game.LEDs.run_script('ShootOver7C', self.game.utilities_mode.generateRandomBlinkSpeedScript())
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

    def start_game(self):
        self.logger.info("Game Started")

        #Reset Prior Game Scores
        self.game.game_data['LastGameScores']['LastPlayer1Score'] = ' '
        self.game.game_data['LastGameScores']['LastPlayer2Score'] = ' '

        self.game.modes.remove(self.game.attract_mode)

        self.game.add_player() # will be first player at this point
        self.game.ball = 1 # AKA Frame
        self.game.roll_number = 1

        self.game.players[0].score = 0

        # Initialize Player Data Arrays with 6 frames and 2 rolls each
        self.player1DataArray = [[0, 0] for _ in range(6)]
        self.player2DataArray = [[0, 0] for _ in range(6)]

        # Initialize Player Data Array
        for f in range(1, 7):  # Loop from 1 to 6 for 1-based indexing
            for r in range(1, 3):  # Loop from 1 to 2 for 1-based indexing
                self.setPlayerData(1, f, r, 0)
                self.setPlayerData(2, f, r, 0)

        self.game.enable_flippers(enable=True)

        self.game.score_display_mode.updateScoreDisplays()
        self.update_lamps()

    def setPlayerData(self, playerNumber, frame, roll, value):
        # Adjust for 1-based indexing by subtracting 1
        if playerNumber == 2:
            self.player2DataArray[frame - 1][roll - 1] = value
        else:
            self.player1DataArray[frame - 1][roll - 1] = value

    def getPlayerData(self, playerNumber, frame, roll):
        # Adjust for 1-based indexing by subtracting 1
        if playerNumber == 2:
            return self.player2DataArray[frame - 1][roll - 1]
        else:
            return self.player1DataArray[frame - 1][roll - 1]

    def score100Points(self):
        # self.p = self.game.current_player()
        # self.p.score += 100
        self.game.players[self.game.current_player_index].score += 100
        # Fire Chime 3

    def score10Points(self):
        # self.p = self.game.current_player()
        # self.p.score += 10
        self.game.players[self.game.current_player_index].score += 10
        # Fire Chime 2

    def score1Point(self):
        # self.p = self.game.current_player()
        # self.p.score += 1
        self.game.players[self.game.current_player_index].score += 1
        # Fire Chime 1

    def scoreAccumulator(self,pointsLeft, isExtraBall=False):
        if (pointsLeft > 0):
            self.scoreCalculating = True
        else:
            self.scoreCalculating = False
            return 0

        if pointsLeft >= 100:
            self.score100Points()
            pointsLeft -= 100
        elif (pointsLeft >= 10):
            self.score10Points()
            pointsLeft -= 10
        elif (pointsLeft >= 1):
            self.score1Point()
            pointsLeft -= 1

        if (pointsLeft > 0):
            self.game.score_display_mode.updateScoreDisplays()
            #self.update_lamps()
            self.delay(name='pointsAccumulatorDelay',delay=.3,handler=self.scoreAccumulator,param=pointsLeft)
        else:
            self.scoreCalculating = False
            if not isExtraBall:
                self.endRoll()
            self.game.score_display_mode.updateScoreDisplays()
            self.update_lamps()

    def scoreBall(self,score, isExtraBall=False):
        if not self.scoreCalculating:
            self.scoreCalculating = True

            self.currentPlayerNumber = self.game.current_player_index + 1

            self.logger.info("---------Score Ball----------")
            self.logger.info(f"Player Index: {self.currentPlayerNumber}")
            self.logger.info(f"Ball Number: {self.game.ball}")
            self.logger.info(f"Roll Number: {self.game.roll_number}")
            self.logger.info(f"Score: {score}")
            self.logger.info(f"Extra Ball: {isExtraBall}")

            ######## RULES SECTION ##########
            # EXTRA BALL #
            if isExtraBall:
                self.lastRollExtraBall = True
                self.scoreAccumulator(score,True)
                return
            else:
                self.lastRollExtraBall = False

            match self.game.ball:
                # Frames
                case 1:
                    if self.game.roll_number == 1:
                        # FIRST ROLL
                        self.setPlayerData(self.currentPlayerNumber,self.game.ball,self.game.roll_number,score) # Set the player data in the array
                        self.update_lamps()
                        self.scoreAccumulator(score)
                    else:
                        # SECOND ROLL
                        self.setPlayerData(self.currentPlayerNumber,self.game.ball,self.game.roll_number,score) # Set the player data in the array
                        self.update_lamps()
                        self.currentFrameTotal = self.getPlayerData(self.currentPlayerNumber,self.game.ball,1) + score

                        self.currentRollTotal = score
                        # See if any bonuses
                        if self.currentFrameTotal == 7:
                            self.currentRollTotal += 20
                        elif self.currentFrameTotal < 7:
                            self.currentRollTotal += 10

                        self.scoreAccumulator(self.currentRollTotal)

                case 2:
                    if self.game.roll_number == 1:
                        # FIRST ROLL
                        self.setPlayerData(self.currentPlayerNumber,self.game.ball,self.game.roll_number,score) # Set the player data in the array
                        self.update_lamps()
                        self.scoreAccumulator(score)
                    else:
                        # SECOND ROLL
                        self.setPlayerData(self.currentPlayerNumber,self.game.ball,self.game.roll_number,score) # Set the player data in the array
                        self.update_lamps()
                        self.currentFrameTotal = self.getPlayerData(self.currentPlayerNumber,self.game.ball,1) + score

                        self.currentRollTotal = score
                        # See if any bonuses
                        if self.currentFrameTotal == 7:
                            self.currentRollTotal += 20
                        elif self.currentFrameTotal < 7:
                            self.currentRollTotal += 20

                        self.scoreAccumulator(self.currentRollTotal)

                case 3:
                    if self.game.roll_number == 1:
                        # FIRST ROLL
                        self.setPlayerData(self.currentPlayerNumber,self.game.ball,self.game.roll_number,score) # Set the player data in the array
                        self.update_lamps()
                        self.scoreAccumulator(score)
                    else:
                        # SECOND ROLL
                        self.setPlayerData(self.currentPlayerNumber,self.game.ball,self.game.roll_number,score) # Set the player data in the array
                        self.update_lamps()
                        self.currentFrameTotal = self.getPlayerData(self.currentPlayerNumber,self.game.ball,1) + score

                        self.currentRollTotal = score
                        # See if any bonuses
                        if self.currentFrameTotal == 7:
                            self.currentRollTotal += 50
                        elif self.currentFrameTotal < 7:
                            self.currentRollTotal += 50

                        self.scoreAccumulator(self.currentRollTotal)

                case 4:
                    if self.game.roll_number == 1:
                        # FIRST ROLL
                        self.setPlayerData(self.currentPlayerNumber,self.game.ball,self.game.roll_number,score) # Set the player data in the array
                        self.update_lamps()
                        self.scoreAccumulator(score)
                    else:
                        # SECOND ROLL
                        self.setPlayerData(self.currentPlayerNumber,self.game.ball,self.game.roll_number,score) # Set the player data in the array
                        self.update_lamps()
                        self.currentFrameTotal = self.getPlayerData(self.currentPlayerNumber,self.game.ball,1) + score

                        self.currentRollTotal = score
                        # See if any bonuses
                        if self.currentFrameTotal == 7:
                            self.currentRollTotal += 50
                        elif self.currentFrameTotal > 7:
                            self.currentRollTotal += 10

                        self.scoreAccumulator(self.currentRollTotal)

                case 5:
                    if self.game.roll_number == 1:
                        # FIRST ROLL
                        self.setPlayerData(self.currentPlayerNumber,self.game.ball,self.game.roll_number,score) # Set the player data in the array
                        self.update_lamps()
                        self.scoreAccumulator(score)
                    else:
                        # SECOND ROLL
                        self.setPlayerData(self.currentPlayerNumber,self.game.ball,self.game.roll_number,score) # Set the player data in the array
                        self.update_lamps()
                        self.currentFrameTotal = self.getPlayerData(self.currentPlayerNumber,self.game.ball,1) + score

                        self.currentRollTotal = score
                        # See if any bonuses
                        if self.currentFrameTotal == 7:
                            self.currentRollTotal += 100
                        elif self.currentFrameTotal > 7:
                            self.currentRollTotal += 20

                        self.scoreAccumulator(self.currentRollTotal)

                case 6:
                    if self.game.roll_number == 1:
                        # FIRST ROLL
                        self.setPlayerData(self.currentPlayerNumber,self.game.ball,self.game.roll_number,score) # Set the player data in the array
                        self.update_lamps()
                        self.scoreAccumulator(score)
                    else:
                        # SECOND ROLL
                        self.setPlayerData(self.currentPlayerNumber,self.game.ball,self.game.roll_number,score) # Set the player data in the array
                        self.update_lamps()
                        self.currentFrameTotal = self.getPlayerData(self.currentPlayerNumber,self.game.ball,1) + score

                        self.currentRollTotal = score
                        # See if any bonuses
                        if self.currentFrameTotal == 7:
                            self.currentRollTotal += 100
                        elif self.currentFrameTotal > 7:
                            self.currentRollTotal += 50

                        self.scoreAccumulator(self.currentRollTotal)


    def endRoll(self):
        self.logger.info("---------END ROLL----------")
        self.logger.info(f"Current Player Index: {self.game.current_player_index + 1}")
        self.logger.info(f"Current Ball Number: {self.game.ball}")
        self.logger.info(f"Current Roll Number: {self.game.roll_number}")


        if self.game.roll_number == 2:
            # Increment Ball and reset roll number
            if self.game.ball < 6:
                self.game.roll_number = 1
                if self.game.current_player_index + 1 < len(self.game.players):
                    self.game.current_player_index += 1 # Increment that current Player
                else:
                    self.game.current_player_index = 0
                    self.game.ball += 1
            else:
                # END OF GAME
                self.end_game()
        else:
            self.game.roll_number += 1

        self.logger.info(f"New Player Index: {self.game.current_player_index + 1}")
        self.logger.info(f"New Ball Number: {self.game.ball}")
        self.logger.info(f"New Roll Number: {self.game.roll_number}")

    def end_game(self):
        self.logger.info("Game Ended")

        self.game.enable_flippers(enable=False)

        if len(self.game.players) == 2:
            #Set Prior Game Scores
            self.game.game_data['LastGameScores']['LastPlayer1Score'] = self.game.players[0].score
            self.game.game_data['LastGameScores']['LastPlayer2Score'] = self.game.players[1].score
            if self.game.game_data['GrandChamp']['GrandChampScore'] < self.game.players[0].score:
                self.game.game_data['GrandChamp']['GrandChampScore'] = self.game.players[0].score
            if self.game.game_data['GrandChamp']['GrandChampScore'] < self.game.players[1].score:
                self.game.game_data['GrandChamp']['GrandChampScore'] = self.game.players[1].score
        else:
            self.game.game_data['LastGameScores']['LastPlayer1Score'] = self.game.players[0].score
            self.game.game_data['LastGameScores']['LastPlayer2Score'] = ' '
            if self.game.game_data['GrandChamp']['GrandChampScore'] < self.game.players[0].score:
                self.game.game_data['GrandChamp']['GrandChampScore'] = self.game.players[0].score

        # Save the game data file
        self.game.save_game_data()

        self.game.ball = 0
        self.game.roll_number = 0
        self.game.old_players = []
        self.game.players = []
        self.game.current_player_index = 0

        self.game.modes.add(self.game.attract_mode)

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
            self.game.players[1].score = 0
            self.game.score_display_mode.updateScoreDisplays()

    # Score Holes
    def sw_rearHoleScore1_active_for_50ms(self, sw):
        if self.game.ball > 0:
            self.scoreBall(1, isExtraBall=False)

    def sw_rearHoleScore2_active_for_50ms(self, sw):
        if self.game.ball > 0:
            self.scoreBall(2, isExtraBall=False)

    def sw_rearHoleScore3_active_for_50ms(self, sw):
        if self.game.ball > 0:
            self.scoreBall(3, isExtraBall=False)

    def sw_rearHoleScore4_active_for_50ms(self, sw):
        if self.game.ball > 0:
            self.scoreBall(4, isExtraBall=False)

    def sw_rearHoleScore5_active_for_50ms(self, sw):
        if self.game.ball > 0:
            self.scoreBall(5, isExtraBall=False)

    def sw_rearHoleScore6_active_for_50ms(self, sw):
        if self.game.ball > 0:
            self.scoreBall(6, isExtraBall=False)

    def sw_centerHoleScore1_active_for_50ms(self, sw):
        if self.game.ball > 0:
            self.scoreBall(1, isExtraBall=False)

    def sw_centerHoleScore2_active_for_50ms(self, sw):
        if self.game.ball > 0:
            self.scoreBall(2, isExtraBall=False)

    def sw_centerHoleScore3_active_for_50ms(self, sw):
        if self.game.ball > 0:
            self.scoreBall(3, isExtraBall=False)

    def sw_centerHoleScore4_active_for_50ms(self, sw):
        if self.game.ball > 0:
            self.scoreBall(4, isExtraBall=False)

    def sw_centerHoleScore5_active_for_50ms(self, sw):
        if self.game.ball > 0:
            self.scoreBall(5, isExtraBall=False)

    def sw_centerHoleScore6_active_for_50ms(self, sw):
        if self.game.ball > 0:
            self.scoreBall(6, isExtraBall=False)

    def sw_rearHoleExtraBall_active_for_50ms(self, sw):
        if self.game.ball > 0:
            self.scoreBall(10, isExtraBall=True)