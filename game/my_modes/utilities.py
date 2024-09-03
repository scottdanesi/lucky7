################################################################################################
## This mode is the Lucky 7 Utilities Mode.
################################################################################################

###############################
## Global Imports
###############################
import procgame.game
import pygame
from pygame.locals import *
from pygame.font import *
import math
import logging

class UtilitiesMode(procgame.game.Mode):
    def __init__(self, game, priority):
        super(UtilitiesMode, self).__init__(game=game, priority=priority)
        self.logger = logging.getLogger('game.UtilitiesMode')

        ## RGB Drivers Global Variables ###################################################
        self.previousR = -1
        self.previousG = -1
        self.previousB = -1

    def mode_started(self):
        pass

    def mode_stopped(self):
        pass

    ####################################################################################################################
    ## LED UTILITIES
    ####################################################################################################################
    ## self.game.utilities_mode.disableAllLEDs(tagFilter=None)

    def disableAllLEDs(self, tagFilter=None):
        # This function will stop and disable ALL LEDs in the system and clear the entire queue.
        # use the tagFilter to only disable LEDs with a specific tag in the YAML definition file.
        for led in self.game.leds:
            if tagFilter is None or tagFilter in led.tags:
                self.game.LEDs.stop_script(led.name)
                # Disable by setting all LEDs to 000000, since these are most likely stuck on by default upon boot up.
                self.game.LEDs.enable(led.name, color="000000")
                # Remove from the internal queue list
                self.game.LEDs.disable(led.name)

    ####################################################################################################################
    ## COIL UTILITIES
    ####################################################################################################################
    ## self.game.utilities_mode.disableAllCoils(tagFilter=None)

    def disableAllCoils(self, tagFilter=None):
        # This function will stop and disable ALL Coils in the system.
        # use the tagFilter to only disable Coils with a specific tag in the YAML definition file.
        for coil in self.game.coils:
            if tagFilter is None or tagFilter in coil.tags:
                self.game.coils[coil.name].disable()

    ####################################################################################################################
    ## BALL RETURN LED UTILITIES
    ####################################################################################################################
    ## self.game.utilities_mode.flashBallReturnLEDs(flashTimeS=0.100,r=255,g=255,b=255)
    ## self.game.utilities_mode.disableBallReturnLEDs()
    ## self.game.utilities_mode.disableStrobe()
    ## self.game.utilities_mode.strobeBallReturnLEDs(r,g,b,pulseGapS,pulsetimeS,strobeOverExisting=False,strobeTimeS=0)
    ## self.game.utilities_mode.pulseAndFadeBallReturnLEDs(r=255,g=0,b=255,pulse_ms=100,fade_ms=800,step_size_ms=30.0,refreshAfter=False)
    ## self.game.utilities_mode.setBallReturnLED(r=0,g=0,b=0,pulsetime=0)

    def flashBallReturnLEDs(self,flashTimeS=0.100,r=255,g=255,b=255):
        self.setBallReturnLED(r=r,g=g,b=b)
        self.previousR = 255
        self.previousG = 255
        self.previousB = 255
        self.delay(name='speakerRGBResume',delay=flashTimeS,handler=self.resumeBallReturnLEDs)

    def resumeBallReturnLEDs(self):
        self.game.utilities_mode.update_lamps()

    def disableBallReturnLEDs(self):
        self.game.coils.BallReturnRedLED.disable()
        self.game.coils.BallReturnGreenLED.disable()
        self.game.coils.BallReturnBlueLED.disable()
        self.previousR = 0
        self.previousG = 0
        self.previousB = 0
        self.disableStrobe()
        self.fade_in_progress = False
        self.cancel_delayed('startFade')
        self.cancel_delayed('continueFade')


    def disableStrobe(self):
        ## self.game.utilities_mode.disableStrobe()
        self.strobeActive = False
        self.cancel_delayed('strobeLoopDelay')


    def update_lamps(self):
        self.updateRGBBallReturn()

    def updateRGBBallReturn(self):
        self.disableStrobe()
        self.disableBallReturnLEDs()

        if self.game.attract_mode in self.game.modes:
            self.setBallReturnLED(r=255,g=0,b=0)


    def strobeBallReturnLEDs(self,r,g,b,pulseGapS,pulsetimeS,strobeOverExisting=False,strobeTimeS=0):
        self.strobeActive = True
        self.previousR = 0
        self.previousG = 0
        self.previousB = 0
        self.strobeCurValR = r
        self.strobeCurValG = g
        self.strobeCurValB = b
        self.strobeCurpulseGapS = pulseGapS
        self.strobeCurpulsetimeS = pulsetimeS
        self.strobeBallReturnLEDsLoop()
        if strobeTimeS > 0:
            self.delay(name='strobeDisable', delay=strobeTimeS, handler=self.updateRGBBallReturn)

    def strobeBallReturnLEDsLoop(self):
        if self.strobeActive:
            self.setBallReturnLED(r=self.strobeCurValR, g=self.strobeCurValG, b=self.strobeCurValB)
            self.delay(name='strobeStopDelay', delay=self.strobeCurpulsetimeS, handler=self.strobeBallReturnLEDsOff)
            self.delay(name='strobeLoopDelay', delay=self.strobeCurpulseGapS + self.strobeCurpulsetimeS, handler=self.strobeBallReturnLEDsLoop)

    def strobeBallReturnLEDsOff(self):
        self.setBallReturnLED(r=0, g=0, b=0)

    def pulseAndFadeBallReturnLEDs(self,r=255,g=0,b=255,pulse_ms=100,fade_ms=800,step_size_ms=30.0,refreshAfter=False):
        # Stop current Fade
        self.abortCurrentFade()

        # Get variables
        self.fade_in_progress = True
        self.fade_total_ms = fade_ms
        self.fade_step_size_ms = step_size_ms
        self.fade_step_count = int(fade_ms / step_size_ms)
        self.fade_r_reduction_per_step = int(r / self.fade_step_count)
        self.fade_g_reduction_per_step = int(g / self.fade_step_count)
        self.fade_b_reduction_per_step = int(b / self.fade_step_count)
        self.current_r = r
        self.current_g = g
        self.current_b = b

        self.disableStrobe()

        #start with full value
        self.setBallReturnLED(r=self.current_r, g=self.current_g, b=self.current_b)

        if pulse_ms > 0:
            self.delay(name='startFade', delay=pulse_ms/1000.0, handler=self.fadeLoop, param=refreshAfter)
        else:
            self.fadeLoop(refreshAfter=refreshAfter)

    def fadeLoop(self,refreshAfter=False):
        if self.fade_in_progress and (self.current_r > 0 or self.current_g > 0 or self.current_b > 0):
            self.setBallReturnLED(r=self.current_r, g=self.current_g, b=self.current_b)
            if self.current_r >= self.fade_r_reduction_per_step:
                self.current_r = self.current_r - self.fade_r_reduction_per_step
            else:
                self.current_r = 0
            if self.current_g >= self.fade_g_reduction_per_step:
                self.current_g = self.current_g - self.fade_g_reduction_per_step
            else:
                self.current_g = 0
            if self.current_b >= self.fade_b_reduction_per_step:
                self.current_b = self.current_b - self.fade_b_reduction_per_step
            else:
                self.current_b = 0

            self.delay(name='continueFade', delay=self.fade_step_size_ms/1000.0, handler=self.fadeLoop, param=refreshAfter)
        else:
            self.fade_in_progress = False
            if refreshAfter:
                self.updateRGBBallReturn()

    def abortCurrentFade(self):
        self.fade_in_progress = False
        #cancel delay here

    def setBallReturnLED(self,r=0,g=0,b=0,pulsetime=0):

        if r == self.previousR and g == self.previousG and b == self.previousB:
            #Do not update, just return
            return

        #Global Constants
        self.totalResolutionMS = 10
        self.divisor = 255 / self.totalResolutionMS
        #Check for Reset
        if(r==0 and g==0 and b==0):
            self.game.coils.BallReturnRedLED.disable()
            self.game.coils.BallReturnGreenLED.disable()
            self.game.coils.BallReturnBlueLED.disable()
            self.previousR = 0
            self.previousG = 0
            self.previousB = 0
            return
        #RED Color Evaluation
        self.rOn = int(math.floor(r/self.divisor))
        self.rOff = self.totalResolutionMS - self.rOn
        if(self.rOn == self.totalResolutionMS):
            if(pulsetime == 0):
                self.game.coils.BallReturnRedLED.enable()
            else:
                self.game.coils.BallReturnRedLED.pulse(pulsetime)
        elif(self.rOn == 0):
            self.game.coils.BallReturnRedLED.disable()
        else:
            if(pulsetime == 0):
                self.game.coils.BallReturnRedLED.patter(self.rOn,self.rOff,now=True)
            else:
                self.game.coils.BallReturnRedLED.pulsed_patter(self.rOn,self.rOff,run_time=pulsetime,now=False)
        #GREEN Color Evaluation
        self.gOn = int(math.floor(g/self.divisor))
        self.gOff = self.totalResolutionMS - self.gOn
        if(self.gOn == self.totalResolutionMS):
            if(pulsetime == 0):
                self.game.coils.BallReturnGreenLED.enable()
            else:
                self.game.coils.BallReturnGreenLED.pulse(pulsetime)
        elif(self.gOn == 0):
            self.game.coils.BallReturnGreenLED.disable()
        else:
            if(pulsetime == 0):
                self.game.coils.BallReturnGreenLED.patter(self.gOn,self.gOff,now=True)
            else:
                self.game.coils.BallReturnGreenLED.pulsed_patter(self.gOn,self.gOff,run_time=pulsetime)
        #BLUE Color Evaluation
        self.bOn = int(math.floor(b/self.divisor))
        self.bOff = self.totalResolutionMS - self.bOn
        if(self.bOn == self.totalResolutionMS):
            if(pulsetime == 0):
                self.game.coils.BallReturnBlueLED.enable()
            else:
                self.game.coils.BallReturnBlueLED.pulse(pulsetime)
        elif(self.bOn == 0):
            self.game.coils.BallReturnBlueLED.disable()
        else:
            if(pulsetime == 0):
                self.game.coils.BallReturnBlueLED.patter(self.bOn,self.bOff,now=True)
            else:
                self.game.coils.BallReturnBlueLED.pulsed_patter(self.bOn,self.bOff,run_time=pulsetime)

        self.previousR = r
        self.previousG = g
        self.previousB = b

