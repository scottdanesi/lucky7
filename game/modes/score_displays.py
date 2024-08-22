################################################################################################
## This mode is used to control the score displays on the backglass.  Player 1 is Display #2
## and Player 2 is Display #2.
################################################################################################

###############################
## Global Imports
###############################
import procgame.game
from procgame.game import AdvancedMode
import pygame
from pygame.locals import *
from pygame.font import *
from random import *

COLOR_WHITE = "FFFFFF"
COLOR_BLACK = "000000"

class ScoreDisplaysMode(procgame.game.AdvancedMode):
    def __init__(self, game):
        super(ScoreDisplaysMode, self).__init__(game=game, priority=2, mode_type=AdvancedMode.Game) # 2 is higher than BGM

        # Global Variables
        self.enableScript = self.create_script(COLOR_WHITE, 100)
        self.disableScript = self.create_script(COLOR_BLACK, 100)
        self.testScript = self.create_script(COLOR_WHITE, 1000) + self.create_script(COLOR_BLACK, 1000)
        self.animationScript = []  # This will be built in the function below

        # Player 1 Segment List
        self.player1SegmentList = [
            "Player1_1A", "Player1_1B", "Player1_1C", "Player1_1D", "Player1_1E", "Player1_1F", "Player1_1G", "Player1_1DP",
            "Player1_2A", "Player1_2B", "Player1_2C", "Player1_2D", "Player1_2E", "Player1_2F", "Player1_2G", "Player1_2DP",
            "Player1_3A", "Player1_3B", "Player1_3C", "Player1_3D", "Player1_3E", "Player1_3F", "Player1_3G", "Player1_3DP"
        ]

        # Player 2 Segment List
        self.player2SegmentList = [
            "Player2_1A", "Player2_1B", "Player2_1C", "Player2_1D", "Player2_1E", "Player2_1F", "Player2_1G", "Player2_1DP",
            "Player2_2A", "Player2_2B", "Player2_2C", "Player2_2D", "Player2_2E", "Player2_2F", "Player2_2G", "Player2_2DP",
            "Player2_3A", "Player2_3B", "Player2_3C", "Player2_3D", "Player2_3E", "Player2_3F", "Player2_3G", "Player2_3DP"
        ]

        # Mapping of digits to segments (A-G, DP)
        self.segment_map = {
            "0": ["A", "B", "C", "D", "E", "F"],
            "1": ["B", "C"],
            "2": ["A", "B", "D", "E", "G"],
            "3": ["A", "B", "C", "D", "G"],
            "4": ["B", "C", "F", "G"],
            "5": ["A", "C", "D", "F", "G"],
            "6": ["A", "C", "D", "E", "F", "G"],
            "7": ["A", "B", "C"],
            "8": ["A", "B", "C", "D", "E", "F", "G"],
            "9": ["A", "B", "C", "D", "F", "G"]
        }

    def create_script(self, color, time, fade=True):
        return [{'color': color, 'time': time, 'fade': fade}]

    def mode_started(self):
        self.disableDisplay(1)
        self.disableDisplay(2)

    def mode_stopped(self):
        pass

    def updatePlayerDisplay(self, displayNum=1, value=0):
        # Ensure value is positive and within the range for display
        if value < 0:
            self.startAnimationScript(displayNum=displayNum)
            return

        # Convert value to a string, pad with leading zeros if necessary
        str_value = str(value).zfill(3)

        # Check for leading zeros and disable the display if necessary
        if str_value[0] == "0":
            self.sendValueToDisplay(displayNum=str(displayNum), digitNum="1", displayDigit=" ", displayDP=False)  # Disable first digit
            if str_value[1] == "0":
                self.sendValueToDisplay(displayNum=str(displayNum), digitNum="2", displayDigit=" ", displayDP=False)  # Disable second digit
                self.sendValueToDisplay(displayNum=str(displayNum), digitNum="3", displayDigit=str_value[2])  # Show only third digit
            else:
                self.sendValueToDisplay(displayNum=str(displayNum), digitNum="2", displayDigit=str_value[1])  # Show second digit
                self.sendValueToDisplay(displayNum=str(displayNum), digitNum="3", displayDigit=str_value[2])  # Show third digit
        else:
            # No leading zeros, display all digits
            self.sendValueToDisplay(displayNum=str(displayNum), digitNum="1", displayDigit=str_value[0])
            self.sendValueToDisplay(displayNum=str(displayNum), digitNum="2", displayDigit=str_value[1])
            self.sendValueToDisplay(displayNum=str(displayNum), digitNum="3", displayDigit=str_value[2])

    def startAnimationScript(self, displayNum=1):
        self.animationSpeed = 100
        self.disableDisplay(displayNum)

        segmentList = self.player1SegmentList if displayNum == 1 else self.player2SegmentList

        for i in range(24):
            self.animationScript = [
                {'color': COLOR_BLACK, 'time': self.animationSpeed * i, 'fade': True},
                {'color': COLOR_WHITE, 'time': self.animationSpeed, 'fade': True},
                {'color': COLOR_BLACK, 'time': self.animationSpeed * 4, 'fade': True},
                {'color': COLOR_BLACK, 'time': self.animationSpeed * (23 - i), 'fade': True}
            ]
            self.game.LEDs.run_script(segmentList[i], self.animationScript)

    def disableDisplay(self, displayNum=1):
        segmentList = {
            1: self.player1SegmentList,
            2: self.player2SegmentList
        }.get(displayNum, [])

        for ledName in segmentList:
            self.game.LEDs.stop_script(ledName)
            self.game.LEDs.disable(ledName)

    def sendValueToDisplay(self, displayNum="1", digitNum="1", displayDigit="0", displayDP=False):
        prefix = f"Player{displayNum}_{digitNum}"
        segments = self.segment_map.get(displayDigit, [])

        # Enable the necessary segments
        for segment in "ABCDEFG":
            if segment in segments:
                self.game.LEDs.enable(f"{prefix}{segment}", color=COLOR_WHITE)
            else:
                self.game.LEDs.disable(f"{prefix}{segment}")

        # Handle the decimal point
        if displayDP:
            self.game.LEDs.enable(f"{prefix}DP", color=COLOR_WHITE)
        else:
            self.game.LEDs.disable(f"{prefix}DP")
