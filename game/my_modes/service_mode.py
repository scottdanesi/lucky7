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
import logging

class ServiceMode(procgame.game.Mode):
    def __init__(self, game, priority):
        super(ServiceMode, self).__init__(game=game, priority=priority)

        self.logger = logging.getLogger('game.ServiceMode')

        # self.menuList = ['VER','LED','SW','SOL','DSP','RUL'] # menuList with Ruleset section
        self.menuList = ['VER','LED','SW','SOL','DSP','RST']
        self.currentMenu = 0
        self.previousMenu = 1
        # self.game.service_mode.serviceModeActive
        self.serviceModeActive = False

        ## LED Test Variables ##########################################################################################
        self.ledTestScript = []
        self.ledTestScript.append({'color': "FFFFFF", 'time': 500, 'fade': False})
        self.ledTestScript.append({'color': "000000", 'time': 500, 'fade': False})

        ## Display Test Variables ######################################################################################
        self.displayTestText = 0
        self.displayTestDisplayNumber = 1
        self.displayTestDisplayCharacter = 0
        self.displayTestSpeedS = 0.25
        self.displayTestStage = 2 # Start on Stage 2 of Display Test

        ## Coil Test Variables #########################################################################################
        self.currentCoilIndex = 0
        self.coilTestDelay = 2
        self.coils = []
        for coil in self.game.coils:
            self.coils.append(coil)

        ## Global Switch Handler Definitions ###########################################################################
        for sw in self.game.switches:
            self.add_switch_handler(name=sw.name, event_type="active", delay=None, handler=self.switchTestActiveHandler)

        for sw in self.game.switches:
            self.add_switch_handler(name=sw.name, event_type="inactive", delay=None, handler=self.switchTestInactiveHandler)

    def mode_started(self):
        # Do not activate the service mode here.  This will be handled with the enter button.
        pass

    def mode_stopped(self):
        self.deactivateServiceMode()

    ## Activate and Deactivate Functions ###############################################################################
    def activateServiceMode(self):
        self.logger.info("###########################################")
        self.logger.info("SERVICE MODE ENTERED")
        self.logger.info("###########################################")
        self.logger.debug(f"Current Menu Index: {self.currentMenu}, Current Menu Length: {len(self.menuList)}")
        self.serviceModeActive = True
        #will need to stop all game modes too...
        self.game.reset()
        self.game.modes.remove(self.game.attract_mode)


        self.processCurrentTest()

    def deactivateServiceMode(self):
        self.logger.info("###########################################")
        self.logger.info("SERVICE MODE EXITED")
        self.logger.info("###########################################")
        self.serviceModeActive = False
        self.cancel_delayed('displayTestDelay')
        self.cancel_delayed('coilTestDelay')
        self.currentMenu = 0
        self.previousMenu = 1
        self.game.save_settings()
        self.game.reset()

    ## Change Service Menu Test Function ###############################################################################
    def changeMode(self,direction=1):
        self.logger.debug(f"Previous Menu Index: {self.currentMenu}, Previous Menu Length: {len(self.menuList)}")
        self.previousMenu = self.currentMenu
        if direction == 1:
            # Move forward
            if self.currentMenu < len(self.menuList) - 1:
                self.currentMenu += 1
        else:
            if self.currentMenu > 0:
                self.currentMenu -= 1

        self.processCurrentTest()

    ## Service Menu Processing Function ################################################################################
    def processCurrentTest(self):
        self.logger.debug(f"Current Menu Index: {self.currentMenu}, Current Menu Length: {len(self.menuList)}")
        if self.previousMenu == self.currentMenu:
            return 0

        self.game.utilities_mode.disableAllLEDs("Backglass")
        self.cancel_delayed('displayTestDelay')
        self.cancel_delayed('coilTestDelay')
        self.game.utilities_mode.disableStrobe()
        match self.menuList[self.currentMenu]:
            case 'VER':
                ########################################################################################################
                ## Version and Revision Display
                ########################################################################################################
                self.logger.info(f"SERVICE MENU VERSION ACTIVE")
                self.game.score_display_mode.updatePlayerDisplay(1,self.game.versionMajor, fade=0)
                self.game.score_display_mode.updatePlayerDisplay(2,self.game.versionMinor, fade=0)
            case 'LED':
                ########################################################################################################
                ## LED Test
                ########################################################################################################
                self.logger.info(f"SERVICE MENU LED TEST ACTIVE")
                self.game.score_display_mode.updatePlayerDisplay(1,"LED", fade=0)
                self.game.score_display_mode.updatePlayerDisplay(2,"ALL", fade=0)
                #Start up the LED all test
                for led in self.game.leds:
                    if "Backglass" in led.tags:
                        self.game.LEDs.stop_script(led.name)
                        self.game.LEDs.run_script(led.name, self.ledTestScript)
                self.game.utilities_mode.strobeBallReturnLEDs(r=255,g=255,b=255,pulseGapS=.5,pulsetimeS=.5,strobeOverExisting=False,strobeTimeS=0)
            case 'SW':
                ########################################################################################################
                ## Switch Test
                ########################################################################################################
                self.logger.info(f"SERVICE MENU SWITCH TEST ACTIVE")
                self.game.score_display_mode.updatePlayerDisplay(1,"S")
                self.game.score_display_mode.updatePlayerDisplay(2,"---")
            case 'SOL':
                ########################################################################################################
                ## Solenoid Test
                ########################################################################################################
                self.logger.info(f"SERVICE MENU SOLENOID TEST ACTIVE")
                self.game.score_display_mode.updatePlayerDisplay(1,"SOL", fade=0)
                self.game.score_display_mode.updatePlayerDisplay(2,"---", fade=0)
                # Reset Variable
                self.currentCoilIndex = 0
                # Kick off the coil test loop with a delay...
                self.delay(name='coilTestDelay', delay=self.coilTestDelay, handler=self.coilTestLoop)
            case 'DSP':
                ########################################################################################################
                ## Display Test
                ########################################################################################################
                self.logger.info(f"SERVICE MENU DISPLAY TEST ACTIVE")
                # Reset display variables.
                self.displayTestText = 0
                self.displayTestDisplayNumber = 1
                self.displayTestDisplayCharacter = 1

                # Kick off the display loop
                self.displayTestLoop()
            case 'RUL':
                ########################################################################################################
                ## Ruleset Selection
                ########################################################################################################
                self.game.score_display_mode.updatePlayerDisplay(1,"RUL", fade=0)
                self.game.score_display_mode.updatePlayerDisplay(2,str(self.game.user_settings['Standard']['RUL']), fade=0)
            case 'RST':
                ########################################################################################################
                ## Reset GC Selection
                ########################################################################################################
                self.game.score_display_mode.updatePlayerDisplay(1,"RST", fade=0)
                self.game.score_display_mode.updatePlayerDisplay(2,"HI", fade=0)

    ## Display Test Loop Function ######################################################################################
    def displayTestLoop(self):
        if not self.serviceModeActive:
            self.logger.debug(f"Display Test Loop attempted to run when service mode was not active...")
            return 0


        if self.displayTestStage == 1:
            if self.displayTestDisplayCharacter == 0:
                self.game.utilities_mode.disableAllLEDs("NumericDisplay",fade=0)
            else:
                self.game.score_display_mode.sendValueToDisplay(self.displayTestDisplayNumber,self.displayTestDisplayCharacter, str(''), fade=0)

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
                    self.displayTestDisplayCharacter = 0
                    self.displayTestStage = 2

            self.game.score_display_mode.sendValueToDisplay(self.displayTestDisplayNumber,self.displayTestDisplayCharacter, str(self.displayTestText), fade=0)
        else:
            self.game.utilities_mode.disableAllLEDs("NumericDisplay",fade=0)
            self.game.score_display_mode.sendValueToDisplay(1,1, str(self.displayTestText), fade=0)
            self.game.score_display_mode.sendValueToDisplay(1,2, str(self.displayTestText), fade=0)
            self.game.score_display_mode.sendValueToDisplay(1,3, str(self.displayTestText), fade=0)
            self.game.score_display_mode.sendValueToDisplay(2,1, str(self.displayTestText), fade=0)
            self.game.score_display_mode.sendValueToDisplay(2,2, str(self.displayTestText), fade=0)
            self.game.score_display_mode.sendValueToDisplay(2,3, str(self.displayTestText), fade=0)
            if self.displayTestText < 9:
                self.displayTestText += 1
            else:
                self.displayTestText = 0
                self.displayTestStage = 1

        self.delay(name='displayTestDelay', delay=self.displayTestSpeedS, handler=self.displayTestLoop)

    ## Coil Test Loop Function #########################################################################################
    def coilTestLoop(self):
        if not self.serviceModeActive:
            self.logger.debug(f"Coil Test Loop attempted to run when service mode was not active...")
            return 0

        self.game.utilities_mode.disableAllCoils()

        self.game.score_display_mode.updatePlayerDisplay(1,"SOL")
        self.game.score_display_mode.updatePlayerDisplay(2,str(self.coils[self.currentCoilIndex].label))
        self.coils[self.currentCoilIndex].pulse()

        if self.currentCoilIndex < len(self.coils) - 1:
            self.currentCoilIndex += 1
        else:
            self.currentCoilIndex = 0

        self.delay(name='coilTestDelay', delay=self.coilTestDelay, handler=self.coilTestLoop)

    ## Switch Handler Functions ########################################################################################
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

    ## Switch Handlers #################################################################################################
    def sw_enter_active(self, sw):
        if not self.serviceModeActive:
            self.activateServiceMode()
        else:
            # Logic for changing values in Service Mode
            match self.menuList[self.currentMenu]:
                case 'RUL':
                    ########################################################################################################
                    ## Ruleset Selection
                    ########################################################################################################
                    valid_ruleset_values = ["A", "B"]
                    current_ruleset = self.game.user_settings['Standard']['RUL']

                    if current_ruleset in valid_ruleset_values:
                        # Get the index of the current ruleset and move to the next one
                        current_index = valid_ruleset_values.index(current_ruleset)
                        next_index = (current_index + 1) % len(valid_ruleset_values)
                        self.game.user_settings['Standard']['RUL'] = valid_ruleset_values[next_index]
                    else:
                        # If the current ruleset is not valid, set it to the first valid value
                        self.game.user_settings['Standard']['RUL'] = valid_ruleset_values[0]

                    # Save the game data file
                    self.game.save_game_data()
                    self.logger.info(f"Ruleset changed to {self.game.user_settings['Standard']['RUL']}")
                    self.game.score_display_mode.updatePlayerDisplay(2,str(self.game.user_settings['Standard']['RUL']))
                case 'RST':
                    ########################################################################################################
                    ## Reset GC Selection
                    ########################################################################################################
                    self.game.game_data['GrandChamp']['GrandChampScore'] = 80
                    # Save the game data file
                    self.game.save_game_data()

                    self.game.score_display_mode.updatePlayerDisplay(1,"RST", fade=0)
                    self.game.score_display_mode.updatePlayerDisplay(2,"DON", fade=0)

    def sw_up_active(self, sw):
        if self.serviceModeActive:
            self.changeMode(1)

    def sw_down_active(self, sw):
        if self.serviceModeActive:
            self.changeMode(0)

    def sw_exit_active(self, sw):
        if self.serviceModeActive:
            self.deactivateServiceMode()

