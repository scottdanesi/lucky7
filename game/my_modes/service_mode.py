########################################################################################################################
## This mode is the Lucky 7 Service Menu Mode.
########################################################################################################################

########################################################################################################################
## Global Imports
########################################################################################################################
import procgame.game
import pygame
from pygame.locals import *
from pygame.font import *

class ServiceMode(procgame.game.Mode):
    def __init__(self, game, priority):
        super(ServiceMode, self).__init__(game=game, priority=priority)

        self.menuList = ['VER','LED','SW','SOL','DSP']
        self.currentMenu = 0
        self.previousMenu = 1
        self.serviceModeActive = False

        ## LED Test Variables ##########################################################################################
        self.ledTestScript = []
        self.ledTestScript.append({'color': "FFFFFF", 'time': 500, 'fade': False})
        self.ledTestScript.append({'color': "000000", 'time': 500, 'fade': False})

        ## Display Test Variables ######################################################################################
        self.displayTestText = 0
        self.displayTestDisplayNumber = 1
        self.displayTestDisplayCharacter = 1
        self.displayTestSpeedS = 0.25
        self.displayTestStage = 2 # Start on Stage 2 of Display Test

        ## Global Switch Handler Definitions ###########################################################################
        for sw in self.game.switches:
            self.add_switch_handler(name=sw.name, event_type="active", delay=None, handler=self.switchTestActiveHandler)

        for sw in self.game.switches:
            self.add_switch_handler(name=sw.name, event_type="inactive", delay=None, handler=self.switchTestInactiveHandler)

    def mode_started(self):
        pass

    def mode_stopped(self):
        pass

    def processCurrentTest(self):
        self.game.logger.debug(f"Current Menu Index: {self.currentMenu}, Current Menu Length: {len(self.menuList)}")
        if self.previousMenu == self.currentMenu:
            return 0

        self.game.utilities_mode.disableAllLEDs("Backglass")
        self.cancel_delayed('displayTestDelay')
        match self.menuList[self.currentMenu]:
            case 'VER':
                ########################################################################################################
                ## Version and Revision Display
                ########################################################################################################
                self.game.score_display_mode.updatePlayerDisplay(1,self.game.versionMajor)
                self.game.score_display_mode.updatePlayerDisplay(2,self.game.versionMinor)
            case 'LED':
                ########################################################################################################
                ## LED Test
                ########################################################################################################
                self.game.score_display_mode.updatePlayerDisplay(1,"LED")
                self.game.score_display_mode.updatePlayerDisplay(2,"ALL")
                #Start up the LED all test
                for led in self.game.leds:
                    if "Backglass" in led.tags:
                        self.game.LEDs.stop_script(led.name)
                        self.game.LEDs.run_script(led.name, self.ledTestScript)
            case 'SW':
                ########################################################################################################
                ## Switch Test
                ########################################################################################################
                self.game.score_display_mode.updatePlayerDisplay(1,"S")
                self.game.score_display_mode.updatePlayerDisplay(2,"---")
            case 'SOL':
                ########################################################################################################
                ## Solenoid Test
                ########################################################################################################
                self.game.score_display_mode.updatePlayerDisplay(1,"SOL")
                self.game.score_display_mode.updatePlayerDisplay(2,"---")
            case 'DSP':
                ########################################################################################################
                ## Display Test
                ########################################################################################################
                # Reset display variables.
                self.displayTestText = 0
                self.displayTestDisplayNumber = 1
                self.displayTestDisplayCharacter = 1

                # Kick off the display loop
                self.displayTestLoop()

    def activateServiceMode(self):
        self.game.logger.debug("###########################################")
        self.game.logger.debug("SERVICE MODE ENTERED")
        self.game.logger.debug("###########################################")
        self.game.logger.debug(f"Current Menu Index: {self.currentMenu}, Current Menu Length: {len(self.menuList)}")
        self.serviceModeActive = True
        #will need to stop all game modes too...
        self.game.modes.remove(self.game.attract_mode)

        self.processCurrentTest()

    def deactivateServiceMode(self):
        self.serviceModeActive = False
        self.cancel_delayed('displayTestDelay')
        self.currentMenu = 0
        self.previousMenu = 1
        self.game.reset()

    def changeMode(self,direction=1):
        self.game.logger.debug(f"Previous Menu Index: {self.currentMenu}, Previous Menu Length: {len(self.menuList)}")
        self.previousMenu = self.currentMenu
        if direction == 1:
            # Move forward
            if (self.currentMenu < len(self.menuList) - 1):
                self.currentMenu += 1
        else:
            if (self.currentMenu > 0):
                self.currentMenu -= 1

        self.processCurrentTest()

    def displayTestLoop(self):
        if not self.serviceModeActive:
            self.game.logger.debug(f"Display Test Loop attempted to run when service mode was not active...")
            return 0

        self.game.utilities_mode.disableAllLEDs("NumericDisplay")
        if self.displayTestStage == 1:
            self.game.score_display_mode.sendValueToDisplay(self.displayTestDisplayNumber,self.displayTestDisplayCharacter, str(self.displayTestText))

            if self.displayTestDisplayCharacter < 3:
                # increment character
                self.displayTestDisplayCharacter += 1
            elif self.displayTestDisplayNumber == 1:
                # Increment Display Number and reset Character
                self.displayTestDisplayNumber = 2
                self.displayTestDisplayCharacter = 1
            else:
                self.displayTestDisplayNumber = 1
                self.displayTestDisplayCharacter = 1
                if self.displayTestText < 9:
                    self.displayTestText += 1
                else:
                    self.displayTestText = 0
                    self.displayTestStage = 2
        else:
            self.game.score_display_mode.sendValueToDisplay(1,1, str(self.displayTestText))
            self.game.score_display_mode.sendValueToDisplay(1,2, str(self.displayTestText))
            self.game.score_display_mode.sendValueToDisplay(1,3, str(self.displayTestText))
            self.game.score_display_mode.sendValueToDisplay(2,1, str(self.displayTestText))
            self.game.score_display_mode.sendValueToDisplay(2,2, str(self.displayTestText))
            self.game.score_display_mode.sendValueToDisplay(2,3, str(self.displayTestText))
            if self.displayTestText < 9:
                self.displayTestText += 1
            else:
                self.displayTestText = 0
                self.displayTestStage = 1

        self.delay(name='displayTestDelay', delay=self.displayTestSpeedS, handler=self.displayTestLoop)

    def switchTestActiveHandler(self,sw):
        if self.menuList[self.currentMenu] != 'SW':
            return 0

        self.game.score_display_mode.updatePlayerDisplay(1,"S-C")
        self.game.score_display_mode.updatePlayerDisplay(2,sw.number)

    def switchTestInactiveHandler(self,sw):
        if self.menuList[self.currentMenu] != 'SW':
            return 0

        self.game.score_display_mode.updatePlayerDisplay(1,"S-O")
        self.game.score_display_mode.updatePlayerDisplay(2,sw.number)


    def sw_enter_active(self, sw):
        if not self.serviceModeActive:
            self.activateServiceMode()

    def sw_up_active(self, sw):
        if self.serviceModeActive:
            self.changeMode(1)

    def sw_down_active(self, sw):
        if self.serviceModeActive:
            self.changeMode(0)

    def sw_exit_active(self, sw):
        if self.serviceModeActive:
            self.deactivateServiceMode()

