#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# This file presents an interface for interacting with the Playstation 4 Controller
# in Python. Simply plug your PS4 controller into your computer using USB and run this
# script!
#
# NOTE: I assume in this script that the only joystick plugged in is the PS4 controller.
#       if this is not the case, you will need to change the class accordingly.
#
# Copyright © 2015 Clay L. McLeod <clay.l.mcleod@gmail.com>
#
# Adjusted by adding a dictionary for each key command on a PS4 controller
# And added a new method for dealing with actions assigned to each button action
# Copyright © 2017 Nelson Raphael <NelsonRaphael27@gmail.com>
#
# Distributed under terms of the MIT license.

import os
import pprint
import pygame

class PS4Controller(object):
    """Class representing the PS4 controller. Pretty straightforward functionality."""

    controller = None
    axis_data = None
    button_data = None
    hat_data = None

    def init(self):
        """Initialize the joystick components"""

        pygame.init()
        pygame.joystick.init()
        self.controller = pygame.joystick.Joystick(0)
        self.controller.init()

    #Added methods for the axis Movement and button interaction. If they work then debugging is easier/



    def listen(self):
        """Listen for events to happen"""

        if not self.axis_data:
            self.axis_data = {}
            self.axis_dataKeyCommands ={0: 'Left Joystick (L/R)', 1: 'Left Joystick (U/D)', 2: 'L2 (H/R)', 3: 'Right Joystick (L/R)', 4: 'Right Joystick (U/D)', 5: 'R2 (H/R)'}
            #Left Joystick L(0: -1.0) R(0: 1.0) U(1: -1.0) D(1: 1.0)
            #L2hold - 2:(-1.0 to 1.0)
            #Right Joystick L(3: -1.0) R(3: 1.0) U(4: -1.0) D(4: 1.0)
            #R2hold - 5:(-1.0 to 1.0)

        if not self.button_data:
            self.button_data = {}
            for i in range(self.controller.get_numbuttons()):
                self.button_data[i] = False
                self.button_dataKeyCommandsPress = {0: 'X buttom pressed', 1: 'O button pressed', 2: 'Triangle Button pressed', 3: 'Square Button pressed', 4: 'L1 button pressed', 5: 'R1 button pressed', 6: 'L2 button pressed', 7: 'R2 button pressed', 8: 'Share button pressed', 9: 'Options button pressed' ,10: 'PS4 home button pressed', 11: 'L3 or Left Joystick Pressed', 12: 'R3 or Right Joystick Pressed'}
                self.button_dataKeyCommandsRelease = {0: 'X buttom released', 1: 'O button released', 2: 'Triangle Button released', 3: 'Square Button released', 4: 'L1 button released', 5: 'R1 button released', 6: 'L2 button released', 7: 'R2 button released', 8: 'Share button released', 9: 'Options button released' ,10: 'PS4 home button released', 11: 'L3 or Left Joystick released', 12: 'R3 or Right Joystick released'}

                #Button Mapping
                #X - 0
                #O - 1
                #Triangle - 2
                #Square - 3
                #L1 - 4
                #R1 - 5
                #L2press - 6
                #R2press - 7
                #Share - 8
                #Options - 9
                #PS4 Home Btn - 10
                #Left Joystick Click - 11
                #Right Joystick Click - 12


        if not self.hat_data:
            self.hat_data = {}
            for i in range(self.controller.get_numhats()):
                self.hat_data[i] = (0, 0)
                self.hat_dataKeyCommands = {0:'L/R button hat',1:'U/D button hat'} #Thought this indexing was intuitive
                #Up - (0,1)
                #Down - (0,-1)
                #Left - (-1,0)
                #Right - (1,0)

        while True:
            for event in pygame.event.get():
                if event.type == pygame.JOYAXISMOTION:
                    self.axis_data[event.axis] = round(event.value,2)
                    #Change action to whatever you want to happen possibly


                elif event.type == pygame.JOYBUTTONDOWN:
                    self.button_data[event.button] = True
                    #Placed the print command inside the if else so that the event member was defined
                    #pprint.pprint(self.button_dataKeyCommandsPress[int(event.button)])


                elif event.type == pygame.JOYBUTTONUP:
                    self.button_data[event.button] = False
                    #Placed the print command inside the if else so that the event member was defined
                    #pprint.pprint(self.button_dataKeyCommandsRelease[int(event.button)])


                elif event.type == pygame.JOYHATMOTION:
                    self.hat_data[event.hat] = event.value
                    #Placed the print command inside the if else so that the event member was defined
                    #pprint.pprint(self.hat_dataKeyCommands[int(event.hat)])



                if self.axis_data[0] > 0:
                    button = "Left Joystick"
                    action = "moved left"
                elif self.axis_data[0] < 0:
                    button = "Left Joystick"
                    action = "moved right"
                elif self.axis_data[1] > 0:
                    button = "Left Joystick"
                    action = "moved up"
                elif self.axis_data[1] < 0:
                    button = "Left Joystick"
                    action = "moved down"
                elif self.axis_data[2] < 0:
                    button = "L2"
                    action = "pressed down"
                elif self.axis_data[2] > 0:
                    button = "L2"
                    action = "let go"
                elif self.axis_data[3] < 0:
                    button = "Right Joystick"
                    action = "moved left"
                elif self.axis_data[3] > 0:
                    button = "Right Joystick"
                    action = "moved right"
                elif self.axis_data[4] > 0:
                    button = "Right Joystick"
                    action = "moved up"
                elif self.axis_data[4] < 0:
                    button = "Right Joystick"
                    action = "moved down"
                elif self.axis_data[5] < 0:
                    button = "R2"
                    action = "pressed down"
                elif self.axis_data[5] > 0:
                    button = "R2"
                    action = "let go"
                elif self.button_data[0] == True :
                    button = "X button"
                    action = "pressed"
                elif self.button_data[1] == True :
                    button = "O button"
                    action = "pressed"
                elif self.button_data[2] == True :
                    button = "Triangle button"
                    action = "pressed"
                elif self.button_data[3] == True :
                    button = "Square button"
                    action = "pressed"
                elif self.button_data[4] == True :
                    button = "L1 button"
                    action = "pressed"
                elif self.button_data[5] == True :
                    button = "R1 button"
                    action = "pressed"
                elif self.button_data[6] == True :
                    button = "L2 button"
                    action = "pressed"
                elif self.button_data[7] == True :
                    button = "R2 button"
                    action = "pressed"
                elif self.button_data[8] == True :
                    button = "Share button"
                    action = "pressed"
                elif self.button_data[9] == True :
                    button = "Options button"
                    action = "pressed"
                elif self.button_data[10] == True :
                    button = "PS4 Home button"
                    action = "pressed"
                elif self.button_data[11] == True :
                    button = "Left Joystick button"
                    action = "pressed"
                elif self.button_data[12] == True :
                    button = "Right Joystick button"
                    action = "pressed"
                elif self.button_data[0] == False :
                    button = "X button"
                    action = "released"
                elif self.button_data[1] == False :
                    button = "O button"
                    action = "released"
                elif self.button_data[2] == False :
                    button = "Triangle button"
                    action = "released"
                elif self.button_data[3] == False :
                    button = "Square button"
                    action = "released"
                elif self.button_data[4] == False :
                    button = "L1 button"
                    action = "released"
                elif self.button_data[5] == False :
                    button = "R1 button"
                    action = "released"
                elif self.button_data[6] == False :
                    button = "L2 button"
                    action = "released"
                elif self.button_data[7] == False :
                    button = "R2 button"
                    action = "released"
                elif self.button_data[8] == False :
                    button = "Share button"
                    action = "released"
                elif self.button_data[9] == False :
                    button = "Options button"
                    action = "released"
                elif self.button_data[10] == False :
                    button = "PS4 Home button"
                    action = "released"
                elif self.button_data[11] == False :
                    button = "Left Joystick button"
                    action = "released"
                elif self.button_data[12] == False :
                    button = "Right Joystick button"
                    action = "released"
                elif self.hat_data[0] < 0:
                    button = "Down Button"
                    action = "was pressed"
                elif self.hat_data[0] > 0:
                    button = "Up Button"
                    action = "was pressed"
                if self.hat_data[1] < 0:
                    button = "Right Button"
                    action = "was pressed"
                elif self.hat_data[1] > 0:
                    button = "Left Button"
                    action = "was pressed"
                    
                pprint.pprint("%s was %s."%(button,action))

                #Happens exteremely fast. So you may have to turn off the clear function to view it.
                #os.system('clear')
                #pprint.pprint(self.button_data)
                #pprint.pprint(self.axis_data)
                #pprint.pprint(self.hat_data)

if __name__ == "__main__":
    ps4 = PS4Controller()
    ps4.init()
    ps4.listen() #Assigns events to dictionaries
