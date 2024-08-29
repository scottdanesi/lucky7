################################################################################################
## This mode is used to control the score displays on the backglass.  Player 1 is Display #2
## and Player 2 is Display #2.
################################################################################################

###############################
## Global Imports
###############################
import procgame.game
# from procgame.game import AdvancedMode
import pygame
from pygame.locals import *
from pygame.font import *
from random import *

COLOR_WHITE = "FFFFFF"
COLOR_BLACK = "000000"

class ScoreDisplaysMode(procgame.game.Mode):
    def __init__(self, game, priority):
        super(ScoreDisplaysMode, self).__init__(game=game, priority=priority) # 2 is higher than BGM

        # Global Variables
        #self.enableScript = self.create_script(COLOR_WHITE, 100)
        #self.disableScript = self.create_script(COLOR_BLACK, 100)
        #self.testScript = self.create_script(COLOR_WHITE, 1000) + self.create_script(COLOR_BLACK, 1000)
        #self.animationScript = []  # This will be built in the function below

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
            "9": ["A", "B", "C", "D", "F", "G"],
            "A": ["A", "B", "C", "E", "F", "G"],
            "B": ["C", "D", "E", "F", "G"],
            "C": ["A", "D", "E", "F"],
            "D": ["B", "C", "D", "E", "G"],
            "E": ["A", "D", "E", "F", "G"],
            "F": ["A", "E", "F", "G"],
            "G": ["A", "B", "C", "D", "F", "G"],
            "H": ["B", "C", "E", "F", "G"],
            "I": ["B", "C"],
            "J": ["B", "C", "D", "E"],
            "K": ["B", "C", "G"],
            "L": ["D", "E", "F"],
            "M": ["A", "B", "C", "E", "F"],
            "N": ["C", "E", "G"],
            "O": ["A", "B", "C", "D", "E", "F"],
            "P": ["A", "B", "E", "F", "G"],
            "Q": ["A", "B", "D", "E", "F"],
            "R": ["E", "G"],
            "S": ["A", "C", "D", "F", "G"],
            "T": ["A", "E", "F"],
            "U": ["C", "D", "E"],
            "V": ["C", "D", "E"],
            "W": ["B", "C", "D", "E", "F"],
            "X": ["B", "C", "E", "F"],
            "Y": ["B", "E", "F", "G"],
            "Z": ["A", "B", "D", "E", "G"],
            "-": ["G"],
            "_": ["D"],
            "!": ["B", "C", "DP"],
            ".": ["DP"],
            "0.": ["A", "B", "C", "D", "E", "F", "DP"],
            "1.": ["B", "C", "DP"],
            "2.": ["A", "B", "D", "E", "G", "DP"],
            "3.": ["A", "B", "C", "D", "G", "DP"],
            "4.": ["B", "C", "F", "G", "DP"],
            "5.": ["A", "C", "D", "F", "G", "DP"],
            "6.": ["A", "C", "D", "E", "F", "G", "DP"],
            "7.": ["A", "B", "C", "DP"],
            "8.": ["A", "B", "C", "D", "E", "F", "G", "DP"],
            "9.": ["A", "B", "C", "D", "F", "G", "DP"],
            "A.": ["A", "B", "C", "E", "F", "G", "DP"],
            "B.": ["C", "D", "E", "F", "G", "DP"],
            "C.": ["A", "D", "E", "F", "DP"],
            "D.": ["B", "C", "D", "E", "G", "DP"],
            "E.": ["A", "D", "E", "F", "G", "DP"],
            "F.": ["A", "E", "F", "G", "DP"],
            "G.": ["A", "B", "C", "D", "F", "G", "DP"],
            "H.": ["B", "C", "E", "F", "G", "DP"],
            "I.": ["B", "C", "DP"],
            "J.": ["B", "C", "D", "E", "DP"],
            "K.": ["B", "C", "G", "DP"],
            "L.": ["D", "E", "F", "DP"],
            "M.": ["A", "B", "C", "E", "F", "DP"],
            "N.": ["C", "E", "G", "DP"],
            "O.": ["A", "B", "C", "D", "E", "F", "DP"],
            "P.": ["A", "B", "E", "F", "G", "DP"],
            "Q.": ["A", "B", "D", "E", "F", "DP"],
            "R.": ["E", "G", "DP"],
            "S.": ["A", "C", "D", "F", "G", "DP"],
            "T.": ["A", "E", "F", "DP"],
            "U.": ["C", "D", "E", "DP"],
            "V.": ["C", "D", "E", "DP"],
            "W.": ["B", "C", "D", "E", "F", "DP"],
            "X.": ["B", "C", "E", "F", "DP"],
            "Y.": ["B", "E", "F", "G", "DP"],
            "Z.": ["A", "B", "D", "E", "G", "DP"],
            "-.": ["G", "DP"],
            "_.": ["D", "DP"],
        }

    def mode_started(self):
        self.game.utilities_mode.disableAllLEDs("NumericDisplay")
        self.displayVersionInfo()

    def mode_stopped(self):
        pass

    def displayVersionInfo(self):
        self.updatePlayerDisplay(1,self.game.versionMajor)
        self.updatePlayerDisplay(2,self.game.versionMinor)

    def disableDisplay(self, displayNum=1):
        segmentList = {
            1: self.player1SegmentList,
            2: self.player2SegmentList
        }.get(displayNum, [])

        for ledName in segmentList:
            self.game.LEDs.stop_script(ledName)
            self.game.LEDs.disable(ledName)

    def updatePlayerDisplay(self, displayNum=1, value=""):
        self.disableDisplay(displayNum)
        # Convert value to a string and handle justification
        str_value = str(value).upper()

        if str_value.isdigit():
            # Right justify if it's a numeric value, with spaces for leading zeros
            str_value = str_value.rjust(3, " ")
        else:
            # Left justify if it contains any characters
            str_value = str_value.ljust(3)

        # Handle up to 3 characters, accounting for any decimal point
        digit_num = 1
        i = 0
        while i < len(str_value) and digit_num <= 3:
            displayDigit = str_value[i]
            next_char = str_value[i+1] if i + 1 < len(str_value) else ""
            if next_char == ".":
                displayDigit += "."
                i += 1  # Skip the decimal point character in the loop

            self.sendValueToDisplay(displayNum=str(displayNum), digitNum=str(digit_num), displayDigit=displayDigit)
            digit_num += 1
            i += 1

    def sendValueToDisplay(self, displayNum="1", digitNum="1", displayDigit="0"):
        prefix = f"Player{displayNum}_{digitNum}"
        segments = self.segment_map.get(displayDigit, [])

        # Enable the necessary segments
        for segment in "ABCDEFG":
            if segment in segments:
                self.game.LEDs.enable(f"{prefix}{segment}", color=COLOR_WHITE)
            else:
                self.game.LEDs.disable(f"{prefix}{segment}")

        # Handle the decimal point (DP)
        if "DP" in segments:
            self.game.LEDs.enable(f"{prefix}DP", color=COLOR_WHITE)
        else:
            self.game.LEDs.disable(f"{prefix}DP")
