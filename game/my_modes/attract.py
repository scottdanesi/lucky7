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
import logging

class L7AttractMode(procgame.game.Mode):
    def __init__(self, game, priority):
        super(L7AttractMode, self).__init__(game=game, priority=priority)
        self.logger = logging.getLogger('game.L7AttractMode')
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
        self.startButtonBlinkDelay = 500
        self.startButtonLEDStatus = False
        self.beaconOnSeconds = 10
        self.beaconOffSeconds = 120
        self.robAnimationFlag = True

        ## Attract Mode Display Frame list
        self.currentAttractDisplayFrame = 0
        self.attractDisplayFrameTypeList = ['LS','GC','LO']
        # self.attractDisplayFrameTypeList = ['LS','GC','HS1','HS2','HS3','HS4'] # Backup for full HS Table
        self.attractDisplayFrameDelayTimeList = [6,3,3]
        self.attractDisplayFrameDisplay1 = ''
        self.attractDisplayFrameDisplay2 = ''

        ###############################################################################################################
        ## BIG 7 Lightshow Script
        ###############################################################################################################
        self.Big7LEDScriptFade = 200

        # Define the patterns for each script
        self.Big7Lightshows = {
            'A': ['FFFFFF', 'FFFFFF', 'FFFFFF', '000000', '000000', '000000', '000000', '000000'],
            'B': ['000000', 'FFFFFF', 'FFFFFF', 'FFFFFF', '000000', '000000', '000000', '000000'],
            'C': ['000000', '000000', 'FFFFFF', 'FFFFFF', 'FFFFFF', '000000', '000000', '000000'],
            'D': ['000000', '000000', '000000', 'FFFFFF', 'FFFFFF', 'FFFFFF', '000000', '000000'],
            'E': ['000000', '000000', '000000', '000000', 'FFFFFF', 'FFFFFF', 'FFFFFF', '000000'],
            'F': ['000000', '000000', '000000', '000000', '000000', 'FFFFFF', 'FFFFFF', 'FFFFFF'],
            'G': ['FFFFFF', '000000', '000000', '000000', '000000', '000000', 'FFFFFF', 'FFFFFF'],
            'H': ['FFFFFF', 'FFFFFF', '000000', '000000', '000000', '000000', '000000', 'FFFFFF'],
        }

        ###############################################################################################################
        ## LUCKY Lightshow Script
        ###############################################################################################################
        self.LUCKYScriptFade = 175

        self.LUCKYLightshows = {
            'A': ['FFFFFF', '000000', '000000', '000000', '000000', '000000', '000000', '000000'],
            'B': ['000000', 'FFFFFF', '000000', '000000', '000000', '000000', '000000', 'FFFFFF'],
            'C': ['000000', '000000', 'FFFFFF', '000000', '000000', '000000', 'FFFFFF', '000000'],
            'D': ['000000', '000000', '000000', 'FFFFFF', '000000', 'FFFFFF', '000000', '000000'],
            'E': ['000000', '000000', '000000', '000000', 'FFFFFF', '000000', '000000', '000000'],
        }

        ###############################################################################################################
        ## Score Numbers Lightshow Scripts
        ###############################################################################################################
        self.ScoreNumberScriptFade = 220

        self.ScoreNumbersLightshows = {
            'A': ['FFFFFF', '000000', '000000', '000000', '000000', '000000', '000000', '000000', '000000', '000000', '000000', '000000', '000000', '000000', '000000', '000000'],
            'B': ['000000', 'FFFFFF', '000000', '000000', '000000', '000000', '000000', '000000', '000000', '000000', '000000', '000000', '000000', '000000', '000000', '000000'],
            'C': ['000000', '000000', 'FFFFFF', '000000', '000000', '000000', '000000', '000000', '000000', '000000', '000000', '000000', '000000', '000000', '000000', '000000'],
            'D': ['000000', '000000', '000000', 'FFFFFF', '000000', '000000', '000000', '000000', '000000', '000000', '000000', '000000', '000000', '000000', '000000', '000000'],
            'E': ['000000', '000000', '000000', '000000', 'FFFFFF', '000000', '000000', '000000', '000000', '000000', '000000', '000000', '000000', '000000', '000000', '000000'],
            'F': ['000000', '000000', '000000', '000000', '000000', 'FFFFFF', '000000', '000000', '000000', '000000', '000000', '000000', '000000', '000000', '000000', '000000'],
            'G': ['000000', '000000', '000000', '000000', '000000', '000000', 'FFFFFF', '000000', 'FFFFFF', '000000', 'FFFFFF', '000000', '000000', '000000', '000000', '000000'],
            'H': ['000000', '000000', '000000', '000000', '000000', '000000', '000000', '000000', '000000', '000000', '000000', 'FFFFFF', '000000', '000000', '000000', '000000'],
            'I': ['000000', '000000', '000000', '000000', '000000', '000000', '000000', '000000', '000000', '000000', '000000', '000000', 'FFFFFF', '000000', '000000', '000000'],
            'J': ['000000', '000000', '000000', '000000', '000000', '000000', '000000', '000000', '000000', '000000', '000000', '000000', '000000', 'FFFFFF', '000000', '000000'],
            'K': ['000000', '000000', '000000', '000000', '000000', '000000', '000000', '000000', '000000', '000000', '000000', '000000', '000000', '000000', 'FFFFFF', '000000'],
            'L': ['000000', '000000', '000000', '000000', '000000', '000000', '000000', '000000', '000000', '000000', '000000', '000000', '000000', '000000', '000000', 'FFFFFF'],
        }

        ###############################################################################################################
        ## Player 1 and 2 Lightshow Scripts
        ###############################################################################################################
        self.Player1Player2ScriptFade = 905

        self.Player1Player2Lightshows = {
            'A': ['FFFFFF', '000000'],
            'B': ['000000', 'FFFFFF'],
        }

        ###############################################################################################################
        ## Frame Numbers Lightshow Scripts
        ###############################################################################################################
        self.FrameNumberScriptFade = 90

        self.FrameNumbersLightshows = {
            'A': ['FFFFFF', '000000', '000000', '000000', '000000', '000000', '000000', '000000', '000000', '000000', '000000', '000000', '000000', '000000', '000000', '000000'],
            'B': ['000000', 'FFFFFF', '000000', '000000', '000000', '000000', '000000', '000000', '000000', '000000', '000000', '000000', '000000', '000000', '000000', '000000'],
            'C': ['000000', '000000', 'FFFFFF', '000000', '000000', '000000', '000000', '000000', '000000', '000000', '000000', '000000', '000000', '000000', '000000', '000000'],
            'D': ['000000', '000000', '000000', 'FFFFFF', '000000', '000000', '000000', '000000', '000000', '000000', '000000', '000000', '000000', '000000', '000000', '000000'],
            'E': ['000000', '000000', '000000', '000000', 'FFFFFF', '000000', '000000', '000000', '000000', '000000', '000000', '000000', '000000', '000000', '000000', '000000'],
            'F': ['000000', '000000', '000000', '000000', '000000', 'FFFFFF', '000000', '000000', '000000', '000000', '000000', '000000', '000000', '000000', '000000', '000000'],
            'G': ['000000', '000000', '000000', '000000', '000000', '000000', 'FFFFFF', 'FFFFFF', '000000', '000000', 'FFFFFF', 'FFFFFF', '000000', '000000', 'FFFFFF', 'FFFFFF'],
        }

        ###############################################################################################################
        ## Score Numbers Lightshow Scripts
        ###############################################################################################################
        self.BonusNumberScriptFade = 160

        self.BonusNumbersLightshows = {
            'A': ['FFFFFF', '000000', '000000', '000000', '000000', '000000', '000000', '000000', '000000', '000000', '000000', '000000', '000000'],
            'B': ['000000', 'FFFFFF', '000000', '000000', '000000', '000000', '000000', '000000', '000000', '000000', '000000', '000000', '000000'],
            'C': ['000000', '000000', 'FFFFFF', '000000', '000000', '000000', '000000', '000000', '000000', '000000', '000000', '000000', '000000'],
            'D': ['000000', '000000', '000000', 'FFFFFF', '000000', '000000', '000000', '000000', '000000', '000000', '000000', '000000', '000000'],
            'E': ['000000', '000000', '000000', '000000', 'FFFFFF', '000000', '000000', '000000', '000000', '000000', '000000', '000000', '000000'],
            'F': ['000000', '000000', '000000', '000000', '000000', 'FFFFFF', '000000', '000000', '000000', '000000', '000000', '000000', '000000'],
            'G': ['000000', '000000', '000000', '000000', '000000', '000000', 'FFFFFF', '000000', '000000', '000000', '000000', '000000', '000000'],
            'H': ['000000', '000000', '000000', '000000', '000000', '000000', '000000', 'FFFFFF', '000000', '000000', '000000', '000000', '000000'],
            'I': ['000000', '000000', '000000', '000000', '000000', '000000', '000000', '000000', 'FFFFFF', '000000', '000000', '000000', '000000'],
        }

    def mode_started(self):
        self.logger.debug("L7 Attract mode started")
        self.set_items(self.game.leds)
        self.game.utilities_mode.disableAllLEDs("Backglass")
        self.startLightshow1()
        self.game.coils.StartButtonLED.schedule(schedule=0x0F0F0F0F, cycle_seconds=0, now=True)
        # self.game.utilities_mode.setBallReturnLED(r=255,g=0,b=0,pulsetime=0)
        self.game.coils.BallReturnRedLED.schedule(schedule=0xFF00FFFF, cycle_seconds=0, now=True)
        self.game.coils.BallReturnGreenLED.schedule(schedule=0x0000FFFF, cycle_seconds=0, now=True)
        self.game.coils.BallReturnBlueLED.schedule(schedule=0x00FF00FF, cycle_seconds=0, now=True)
        # self.game.score_display_mode.updateScoreDisplays()
        self.currentAttractDisplayFrame = 0
        self.attractModeFrameAdvance()

        self.enableBeaconAttractLoop()

    def mode_stopped(self):
        self.logger.debug("L7 Attract mode stopped")
        self.game.utilities_mode.disableAllLEDs("Backglass")
        self.game.coils.StartButtonLED.disable()
        self.game.utilities_mode.setBallReturnLED(r=0,g=0,b=0,pulsetime=0)
        self.stopAttractModeFrameAdvance()
        self.disableBeaconLoop()
        self.robAnimationFlag = True
        self.cancel_delayed(name='attractFrameAdvance')
        self.cancel_delayed(name='toggleRobAnimation')

    def create_led_script(self, fade_time, pattern):
        script = []
        for color in pattern:
            script.append({'color': color, 'time': fade_time, 'fade': True})
        return script

    def set_items(self, item_list):
        if(len(item_list)>0):
            for self.item in sorted(item_list,key=lambda s: s.label):
                self.items.append(self.item)

    def startLightshow1(self):
        self.game.LEDs.run_script("Big7A", self.create_led_script(self.Big7LEDScriptFade, self.Big7Lightshows['A']))
        self.game.LEDs.run_script("Big7B", self.create_led_script(self.Big7LEDScriptFade, self.Big7Lightshows['B']))
        self.game.LEDs.run_script("Big7C", self.create_led_script(self.Big7LEDScriptFade, self.Big7Lightshows['C']))
        self.game.LEDs.run_script("Big7D", self.create_led_script(self.Big7LEDScriptFade, self.Big7Lightshows['D']))
        self.game.LEDs.run_script("Big7E", self.create_led_script(self.Big7LEDScriptFade, self.Big7Lightshows['E']))
        self.game.LEDs.run_script("Big7F", self.create_led_script(self.Big7LEDScriptFade, self.Big7Lightshows['F']))
        self.game.LEDs.run_script("Big7G", self.create_led_script(self.Big7LEDScriptFade, self.Big7Lightshows['G']))
        self.game.LEDs.run_script("Big7H", self.create_led_script(self.Big7LEDScriptFade, self.Big7Lightshows['H']))

        self.game.LEDs.run_script("LUCKY_LA", self.create_led_script(self.LUCKYScriptFade, self.LUCKYLightshows['A']))
        self.game.LEDs.run_script("LUCKY_LB", self.create_led_script(self.LUCKYScriptFade, self.LUCKYLightshows['A']))
        self.game.LEDs.run_script("LUCKY_UA", self.create_led_script(self.LUCKYScriptFade, self.LUCKYLightshows['B']))
        self.game.LEDs.run_script("LUCKY_UB", self.create_led_script(self.LUCKYScriptFade, self.LUCKYLightshows['B']))
        self.game.LEDs.run_script("LUCKY_CA", self.create_led_script(self.LUCKYScriptFade, self.LUCKYLightshows['C']))
        self.game.LEDs.run_script("LUCKY_CB", self.create_led_script(self.LUCKYScriptFade, self.LUCKYLightshows['C']))
        self.game.LEDs.run_script("LUCKY_KA", self.create_led_script(self.LUCKYScriptFade, self.LUCKYLightshows['D']))
        self.game.LEDs.run_script("LUCKY_KB", self.create_led_script(self.LUCKYScriptFade, self.LUCKYLightshows['D']))
        self.game.LEDs.run_script("LUCKY_YA", self.create_led_script(self.LUCKYScriptFade, self.LUCKYLightshows['E']))
        self.game.LEDs.run_script("LUCKY_YB", self.create_led_script(self.LUCKYScriptFade, self.LUCKYLightshows['E']))

        self.game.LEDs.run_script("Score1", self.create_led_script(self.ScoreNumberScriptFade, self.ScoreNumbersLightshows['A']))
        self.game.LEDs.run_script("Score2", self.create_led_script(self.ScoreNumberScriptFade, self.ScoreNumbersLightshows['B']))
        self.game.LEDs.run_script("Score3", self.create_led_script(self.ScoreNumberScriptFade, self.ScoreNumbersLightshows['C']))
        self.game.LEDs.run_script("Score4", self.create_led_script(self.ScoreNumberScriptFade, self.ScoreNumbersLightshows['D']))
        self.game.LEDs.run_script("Score5", self.create_led_script(self.ScoreNumberScriptFade, self.ScoreNumbersLightshows['E']))
        self.game.LEDs.run_script("Score6", self.create_led_script(self.ScoreNumberScriptFade, self.ScoreNumbersLightshows['F']))
        self.game.LEDs.run_script("Score7A", self.create_led_script(self.ScoreNumberScriptFade, self.ScoreNumbersLightshows['G']))
        self.game.LEDs.run_script("Score7B", self.create_led_script(self.ScoreNumberScriptFade, self.ScoreNumbersLightshows['G']))
        self.game.LEDs.run_script("Score8", self.create_led_script(self.ScoreNumberScriptFade, self.ScoreNumbersLightshows['H']))
        self.game.LEDs.run_script("Score9", self.create_led_script(self.ScoreNumberScriptFade, self.ScoreNumbersLightshows['I']))
        self.game.LEDs.run_script("Score10", self.create_led_script(self.ScoreNumberScriptFade, self.ScoreNumbersLightshows['J']))
        self.game.LEDs.run_script("Score11", self.create_led_script(self.ScoreNumberScriptFade, self.ScoreNumbersLightshows['K']))
        self.game.LEDs.run_script("Score12", self.create_led_script(self.ScoreNumberScriptFade, self.ScoreNumbersLightshows['L']))

        self.game.LEDs.run_script("Player1A", self.create_led_script(self.Player1Player2ScriptFade, self.Player1Player2Lightshows['A']))
        self.game.LEDs.run_script("Player1B", self.create_led_script(self.Player1Player2ScriptFade, self.Player1Player2Lightshows['A']))
        self.game.LEDs.run_script("Player2A", self.create_led_script(self.Player1Player2ScriptFade, self.Player1Player2Lightshows['B']))
        self.game.LEDs.run_script("Player2B", self.create_led_script(self.Player1Player2ScriptFade, self.Player1Player2Lightshows['B']))
        self.game.LEDs.run_script("1stRoll", self.create_led_script(self.Player1Player2ScriptFade, self.Player1Player2Lightshows['B']))
        self.game.LEDs.run_script("2ndRoll", self.create_led_script(self.Player1Player2ScriptFade, self.Player1Player2Lightshows['A']))

        self.game.LEDs.run_script("Frame1A", self.create_led_script(self.FrameNumberScriptFade, self.FrameNumbersLightshows['A']))
        self.game.LEDs.run_script("Frame1B", self.create_led_script(self.FrameNumberScriptFade, self.FrameNumbersLightshows['A']))
        self.game.LEDs.run_script("Frame2A", self.create_led_script(self.FrameNumberScriptFade, self.FrameNumbersLightshows['B']))
        self.game.LEDs.run_script("Frame2B", self.create_led_script(self.FrameNumberScriptFade, self.FrameNumbersLightshows['B']))
        self.game.LEDs.run_script("Frame3A", self.create_led_script(self.FrameNumberScriptFade, self.FrameNumbersLightshows['C']))
        self.game.LEDs.run_script("Frame3B", self.create_led_script(self.FrameNumberScriptFade, self.FrameNumbersLightshows['C']))
        self.game.LEDs.run_script("Frame4A", self.create_led_script(self.FrameNumberScriptFade, self.FrameNumbersLightshows['D']))
        self.game.LEDs.run_script("Frame4B", self.create_led_script(self.FrameNumberScriptFade, self.FrameNumbersLightshows['D']))
        self.game.LEDs.run_script("Frame5A", self.create_led_script(self.FrameNumberScriptFade, self.FrameNumbersLightshows['E']))
        self.game.LEDs.run_script("Frame5B", self.create_led_script(self.FrameNumberScriptFade, self.FrameNumbersLightshows['E']))
        self.game.LEDs.run_script("Frame6A", self.create_led_script(self.FrameNumberScriptFade, self.FrameNumbersLightshows['F']))
        self.game.LEDs.run_script("Frame6B", self.create_led_script(self.FrameNumberScriptFade, self.FrameNumbersLightshows['F']))
        self.game.LEDs.run_script("GameOverA", self.create_led_script(self.FrameNumberScriptFade, self.FrameNumbersLightshows['G']))
        self.game.LEDs.run_script("GameOverB", self.create_led_script(self.FrameNumberScriptFade, self.FrameNumbersLightshows['G']))

        self.game.LEDs.run_script("RedBonus50", self.create_led_script(self.BonusNumberScriptFade, self.BonusNumbersLightshows['A']))
        self.game.LEDs.run_script("RedBonus20", self.create_led_script(self.BonusNumberScriptFade, self.BonusNumbersLightshows['B']))
        self.game.LEDs.run_script("RedBonus10", self.create_led_script(self.BonusNumberScriptFade, self.BonusNumbersLightshows['C']))
        self.game.LEDs.run_script("BlueBonus20", self.create_led_script(self.BonusNumberScriptFade, self.BonusNumbersLightshows['D']))
        self.game.LEDs.run_script("BlueBonus50", self.create_led_script(self.BonusNumberScriptFade, self.BonusNumbersLightshows['E']))
        self.game.LEDs.run_script("BlueBonus100", self.create_led_script(self.BonusNumberScriptFade, self.BonusNumbersLightshows['F']))
        self.game.LEDs.run_script("YellowBonus10", self.create_led_script(self.BonusNumberScriptFade, self.BonusNumbersLightshows['G']))
        self.game.LEDs.run_script("YellowBonus20", self.create_led_script(self.BonusNumberScriptFade, self.BonusNumbersLightshows['H']))
        self.game.LEDs.run_script("YellowBonus50", self.create_led_script(self.BonusNumberScriptFade, self.BonusNumbersLightshows['I']))

        ## Enable Static Backbox Inserts
        self.game.LEDs.enable("BallScoreA", color="FFFFFF")
        self.game.LEDs.enable("BallScoreB", color="FFFFFF")
        self.game.LEDs.enable("BallScoreC", color="FFFFFF")

        self.game.LEDs.enable("ScoreInstA", color="FFFFFF")
        self.game.LEDs.enable("ScoreInstB", color="FFFFFF")
        self.game.LEDs.enable("ScoreInstC", color="FFFFFF")
        self.game.LEDs.enable("ScoreInstD", color="FFFFFF")

        self.game.LEDs.run_script('ShootUnder7A', self.game.utilities_mode.generateRandomBlinkSpeedScript(minspeed=100, maxspeed=500, length=50))
        self.game.LEDs.run_script('ShootUnder7B', self.game.utilities_mode.generateRandomBlinkSpeedScript(minspeed=100, maxspeed=500, length=50))
        self.game.LEDs.run_script('ShootUnder7C', self.game.utilities_mode.generateRandomBlinkSpeedScript(minspeed=100, maxspeed=500, length=50))
        self.game.LEDs.run_script('ShootUnder7D', self.game.utilities_mode.generateRandomBlinkSpeedScript(minspeed=100, maxspeed=500, length=50))

        self.game.LEDs.run_script('ShootOver7A', self.game.utilities_mode.generateRandomBlinkSpeedScript(minspeed=100, maxspeed=500, length=50))
        self.game.LEDs.run_script('ShootOver7B', self.game.utilities_mode.generateRandomBlinkSpeedScript(minspeed=100, maxspeed=500, length=50))
        self.game.LEDs.run_script('ShootOver7C', self.game.utilities_mode.generateRandomBlinkSpeedScript(minspeed=100, maxspeed=500, length=50))

        self.game.LEDs.run_script('BlueBonusMadeA', self.game.utilities_mode.generateRandomBlinkSpeedScript(minspeed=100, maxspeed=500, length=50))
        self.game.LEDs.run_script('BlueBonusMadeB', self.game.utilities_mode.generateRandomBlinkSpeedScript(minspeed=100, maxspeed=500, length=50))
        self.game.LEDs.run_script('BlueBonusMadeC', self.game.utilities_mode.generateRandomBlinkSpeedScript(minspeed=100, maxspeed=500, length=50))

        self.game.LEDs.run_script('RedBonusMadeA', self.game.utilities_mode.generateRandomBlinkSpeedScript(minspeed=100, maxspeed=500, length=50))
        self.game.LEDs.run_script('RedBonusMadeB', self.game.utilities_mode.generateRandomBlinkSpeedScript(minspeed=100, maxspeed=500, length=50))
        self.game.LEDs.run_script('RedBonusMadeC', self.game.utilities_mode.generateRandomBlinkSpeedScript(minspeed=100, maxspeed=500, length=50))

        self.game.LEDs.run_script('YellowBonusMadeA', self.game.utilities_mode.generateRandomBlinkSpeedScript(minspeed=100, maxspeed=500, length=50))
        self.game.LEDs.run_script('YellowBonusMadeB', self.game.utilities_mode.generateRandomBlinkSpeedScript(minspeed=100, maxspeed=500, length=50))

        self.game.LEDs.enable('7ScoresBonusOfA',color='FFFFFF')
        self.game.LEDs.enable('7ScoresBonusOfB',color='FFFFFF')
        self.game.LEDs.enable('7ScoresBonusOfC',color='FFFFFF')
        self.game.LEDs.enable('7ScoresBonusOfD',color='FFFFFF')

        self.game.LEDs.enable('ExtraBallA',color='FFFFFF')
        self.game.LEDs.enable('ExtraBallB',color='FFFFFF')
        self.game.LEDs.enable('ExtraBallC',color='FFFFFF')
        self.game.LEDs.enable('ExtraBallD',color='FFFFFF')

        self.game.LEDs.enable('FramesA',color='FFFFFF')
        self.game.LEDs.enable('FramesB',color='FFFFFF')
        self.game.LEDs.enable('FramesC',color='FFFFFF')
        self.game.LEDs.enable('FramesD',color='FFFFFF')


    def attractModeFrameAdvance(self):

        self.cancel_delayed(name='toggleRobAnimation')

        # Get the length of the list
        list_length = len(self.attractDisplayFrameTypeList)

        # Set the current frame to the corresponding item in the list
        current_frame = self.attractDisplayFrameTypeList[self.currentAttractDisplayFrame]

        match current_frame:
            case 'LS':
                if self.game.game_data['LastGameScores']['LastPlayer1Score'] == 41 or self.game.game_data['LastGameScores']['LastPlayer2Score'] == 41:
                    self.toggleRobAnimation()
                else:
                    self.attractDisplayFrameDisplay1 = self.game.game_data['LastGameScores']['LastPlayer1Score']
                    self.attractDisplayFrameDisplay2 = self.game.game_data['LastGameScores']['LastPlayer2Score']
            case 'GC':
                self.attractDisplayFrameDisplay1 = ' HI'
                self.attractDisplayFrameDisplay2 = self.game.game_data['GrandChamp']['GrandChampScore']
            case 'LO':
                self.attractDisplayFrameDisplay1 = ' LO'
                self.attractDisplayFrameDisplay2 = self.game.game_data['LowScoreChamp']['LowScore']
            #case 'HS1':
            #    self.attractDisplayFrameDisplay1 = 'HS1'
            #    self.attractDisplayFrameDisplay2 = self.game.game_data['HighScore1']['HighScore1Score']
            #case 'HS2':
            #    self.attractDisplayFrameDisplay1 = 'HS2'
            #    self.attractDisplayFrameDisplay2 = self.game.game_data['HighScore2']['HighScore2Score']
            #case 'HS3':
            #    self.attractDisplayFrameDisplay1 = 'HS3'
            #    self.attractDisplayFrameDisplay2 = self.game.game_data['HighScore3']['HighScore3Score']
            #case 'HS4':
            #    self.attractDisplayFrameDisplay1 = 'HS4'
            #    self.attractDisplayFrameDisplay2 = self.game.game_data['HighScore4']['HighScore4Score']

        self.game.score_display_mode.updatePlayerDisplay(1, self.attractDisplayFrameDisplay1)
        self.game.score_display_mode.updatePlayerDisplay(2, self.attractDisplayFrameDisplay2)

        self.delay(name='attractFrameAdvance',delay=self.attractDisplayFrameDelayTimeList[self.currentAttractDisplayFrame],handler=self.attractModeFrameAdvance)

        self.logger.debug(f"Current Attract Frame: {current_frame}")

        # Advance to the next frame, wrapping around using modulus
        self.currentAttractDisplayFrame = (self.currentAttractDisplayFrame + 1) % list_length

    def toggleRobAnimation(self):
        if self.robAnimationFlag:
            self.game.score_display_mode.updatePlayerDisplay(1, self.game.game_data['LastGameScores']['LastPlayer1Score'])
            self.game.score_display_mode.updatePlayerDisplay(2, self.game.game_data['LastGameScores']['LastPlayer2Score'])
        else:
            self.game.score_display_mode.updatePlayerDisplay(1, "HA")
            self.game.score_display_mode.updatePlayerDisplay(2, "ROB")
        self.robAnimationFlag = not self.robAnimationFlag
        self.delay(name='toggleRobAnimation',delay=.5,handler=self.toggleRobAnimation)

    def stopAttractModeFrameAdvance(self):
        self.currentAttractDisplayFrame = 0
        self.cancel_delayed(name='attractFrameAdvance')

    def enableBeaconAttractLoop(self):
        self.cancel_delayed(name='disableBeacon')
        self.cancel_delayed(name='enableBeacon')
        self.game.coils['beacon'].enable()
        self.delay(name='disableBeacon',delay=self.beaconOnSeconds,handler=self.disableBeaconAttractLoop)

    def disableBeaconAttractLoop(self):
        self.cancel_delayed(name='disableBeacon')
        self.cancel_delayed(name='enableBeacon')
        self.game.coils['beacon'].disable()
        self.delay(name='enableBeacon',delay=self.beaconOffSeconds,handler=self.enableBeaconAttractLoop)

    def disableBeaconLoop(self):
        self.cancel_delayed(name='disableBeacon')
        self.cancel_delayed(name='enableBeacon')
        self.game.coils['beacon'].disable()