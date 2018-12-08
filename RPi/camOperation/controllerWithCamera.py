
import serial
import time
import os
import pprint
import pygame
import argparse
import base64
import picamera
import json

from googleapiclient import discovery
from oauth2client.client import GoogleCredentials
from imgIdentify import imgIdentify


class PS4Controller(object):
    """Class representing the PS4 controller. Pretty straightforward functionality."""

    controller = None
    axis_data = None
    button_data = None
    hat_data = None
    global camera
    camera = picamera.PiCamera()
    imgId = imgIdentify()


    def init(self):
        """Initialize the joystick components"""

        pygame.init()
        pygame.joystick.init()
        self.controller = pygame.joystick.Joystick(0)
        self.controller.init()
    
    #def checkMbedResponse()
    
    def listen(self):
        """Listen for events to happen"""

        #button = ""
        #action = ""
        buttonAction = ''
        tempAction = ''
        ser = serial.Serial('/dev/ttyACM0',9600)
        print(ser.name)

        if not self.axis_data:
            self.axis_data = {}
            #Left Joystick L(0: -1.0) R(0: 1.0) U(1: -1.0) D(1: 1.0)
            #L2hold - 2:(-1.0 to 1.0)
            #Right Joystick L(3: -1.0) R(3: 1.0) U(4: -1.0) D(4: 1.0)
            #R2hold - 5:(-1.0 to 1.0)

        if not self.button_data:
            self.button_data = {}
            for i in range(self.controller.get_numbuttons()):
                self.button_data[i] = False

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
                    #Change action to whatever you want to happen hardware wise
                    if event.axis == 0 and self.axis_data[event.axis] > 0:
                        #"Left Joystick moved right"
                        buttonAction = 'o'
                    elif event.axis == 0 and self.axis_data[event.axis] < 0:
                        #button = "Left Joystick"
                        #action = "moved left"
                        buttonAction = 'p'
                    elif event.axis == 1 and self.axis_data[event.axis] > 0:
                        #button = "Left Joystick"
                        #action = "moved down"
                        buttonAction = 'n'
                    elif event.axis == 1 and self.axis_data[event.axis] < 0:
                        #button = "Left Joystick"
                        #action = "moved up"
                        buttonAction = 'm'
                    elif event.axis == 1 and self.axis_data[event.axis] == 0:
                        #Left Joystick moved to the center
                        buttonAction = 'S'
                    elif event.axis == 2 and self.axis_data[event.axis] < 0:
                        #button = "L2"
                        #action = "let go"
                        buttonAction = 'I'
                    elif event.axis == 2 and self.axis_data[event.axis] > 0:
                        #button = "L2"
                        #action = "pressed down"
                        buttonAction = 'i'
                    elif event.axis == 3 and self.axis_data[event.axis] < 0:
                        #button = "Right Joystick"
                        #action = "moved left"
                        buttonAction = 'u'
                    elif event.axis == 3 and self.axis_data[event.axis] > 0:
                        #button = "Right Joystick"
                        #action = "moved right"
                        buttonAction = 't'
                    elif event.axis == 4 and self.axis_data[event.axis] > 0:
                        #button = "Right Joystick"
                        #action = "moved down"
                        buttonAction = 's'
                    elif event.axis == 4 and self.axis_data[event.axis] < 0:
                        #button = "Right Joystick"
                        #action = "moved up"
                        buttonAction = 'r'
                    elif event.axis == 4 and self.axis_data[event.axis] == 0:
                        #Right Joystick moved to the center
                        buttonAction = 'S'
                    elif event.axis == 5 and self.axis_data[event.axis] < 0:
                        #button = "R2"
                        #action = "let go"
                        buttonAction = 'j'
                    elif event.axis == 5 and self.axis_data[event.axis] > 0:
                        #button = "R2"
                        #action = "pressed down"
                        imgId.analyzePic()
                        buttonAction = 'J'

                elif event.type == pygame.JOYBUTTONDOWN:
                    self.button_data[event.button] = True
                    #Change action to whatever you want to happen hardware wise
                    if event.button == 0 and self.button_data[event.button] == True :
                        #button = "X button"
                        #action = "pressed"
                        buttonAction = 'a'
                    elif event.button == 1 and self.button_data[event.button] == True :
                        #button = "O button"
                        #action = "pressed"
                        buttonAction = 'c'
                    elif event.button == 2 and self.button_data[event.button] == True :
                        #button = "Triangle button"
                        #action = "pressed"
                        buttonAction = 'd'
                    elif event.button == 3 and self.button_data[event.button] == True :
                        #button = "Square button"
                        #action = "pressed"
                        buttonAction = 'b'
                    elif event.button == 4 and self.button_data[event.button] == True :
                        #button = "L1 button"
                        #action = "pressed"
                        buttonAction = 'k'
                    elif event.button == 5 and self.button_data[event.button] == True :
                        #button = "R1 button"
                        #action = "pressed"
                        buttonAction = 'l'
                    elif event.button == 6 and self.button_data[event.button] == True :
                        #button = "L2 button"
                        #action = "pressed"
                        buttonAction = 'i'
                    elif event.button == 7 and self.button_data[event.button] == True :
                        #button = "R2 button"
                        #action = "pressed"
                        buttonAction = 'j'
                    elif event.button == 8 and self.button_data[event.button] == True :
                        #button = "Share button"
                        #action = "pressed"
                        buttonAction = 'x'
                    elif event.button == 9 and self.button_data[event.button] == True :
                        #button = "Options button"
                        #action = "pressed"
                        buttonAction = 'y'
                    elif event.button == 10 and self.button_data[event.button] == True :
                        #button = "PS4 Home button"
                        #action = "pressed"
                        buttonAction = 'S'
                    elif event.button == 11 and self.button_data[event.button] == True :
                        #button = "Left Joystick button"
                        #action = "pressed"
                        buttonAction = 'q'
                    elif event.button == 12 and self.button_data[event.button] == True :
                        #button = "Right Joystick button"
                        #action = "pressed"
                        buttonAction = 'v'
                elif event.type == pygame.JOYBUTTONUP:
                    self.button_data[event.button] = False
                    #Placed the print command inside the if else so that the event member was defined
                    #pprint.pprint(self.button_dataKeyCommandsRelease[int(event.button)])
                    if event.button == 0 and self.button_data[event.button] == False :
                        #button = "X button"
                        #action = "let go"
                        buttonAction = 'A'
                    elif event.button == 1 and self.button_data[event.button] == False :
                        #button = "O button"
                        #action = "let go"
                        buttonAction = 'C'
                    elif event.button == 2 and self.button_data[event.button] == False :
                        #button = "Triangle button"
                        #action = "let go"
                        buttonAction = 'D'
                    elif event.button == 3 and self.button_data[event.button] == False :
                        #button = "Square button"
                        #action = "let go"
                        buttonAction = 'B'
                    elif event.button == 4 and self.button_data[event.button] == False :
                        #button = "L1 button"
                        #action = "let go"
                        buttonAction = 'K'
                    elif event.button == 5 and self.button_data[event.button] == False :
                        #button = "R1 button"
                        #action = "let go"
                        buttonAction = 'L'
                    elif event.button == 6 and self.button_data[event.button] == False :
                        #button = "L2 button"
                        #action = "let go"
                        buttonAction = 'I'
                    elif event.button == 7 and self.button_data[event.button] == False :
                        #button = "R2 button"
                        #action = "let go"
                        buttonAction = 'J'
                    elif event.button == 8 and self.button_data[event.button] == False :
                        #button = "Share button"
                        #action = "let go"
                        buttonAction = 'X'
                    elif event.button == 9 and self.button_data[event.button] == False :
                        #button = "Options button"
                        #action = "let go"
                        buttonAction = 'Y'
                    elif event.button == 10 and self.button_data[event.button] == False :
                        #button = "PS4 Home button"
                        #action = "let go"
                        buttonAction = 'S'
                    elif event.button == 11 and self.button_data[event.button] == False :
                        #button = "Left Joystick button"
                        #action = "let go"
                        buttonAction = 'Q'
                    elif event.button == 12 and self.button_data[event.button] == False :
                        #button = "Right Joystick button"
                        #action = "let go"
                        buttonAction = 'V'

                elif event.type == pygame.JOYHATMOTION:
                    self.hat_data[event.hat] = event.value
                    #Change action to whatever you want to happen hardware wise
                    if event.value == (1,0):
                        #button = "Right Button"
                        #action = "was pressed"
                        buttonAction = 'h'
                    elif event.value == (-1,0):
                        #button = "Left Button"
                        #action = "was pressed"
                        buttonAction = 'g'
                    elif event.value == (0,-1):
                        #button = "Down Button"
                        #action = "was pressed"
                        buttonAction = 'f'
                    elif event.value == (0,1):
                        #button = "Up Button"
                        #action = "was pressed"
                        buttonAction = 'e'
                    elif event.value == (0,0):
                        #Stops all motion
                        buttonAction = 'H'


                #pprint.pprint("%s was %s."%(button,action))
                #controllerAction = button + ' ' +  action
                controllerAction = buttonAction
                if tempAction != controllerAction:
                    ser.write(controllerAction)
                    tempAction = controllerAction
                else:
                    time.sleep(0.7)
                    ser.write('z')
                #	tempAction = buttonAction
                #else:
                #    print(tempAction,buttonAction)
                #print(controllerAction)   #left for debugging purposes
                read_val = ser.read_until(controllerAction,1)
                #print read_val

                #Happens exteremely fast. So you may have to turn off the clear function to view it.
                #os.system('clear')
                #pprint.pprint(self.button_data)
                #pprint.pprint(self.axis_data)
                #pprint.pprint(self.hat_data)

if __name__ == "__main__":
    ps4 = PS4Controller()
    ps4.init()
    ps4.listen() #Assigns events to dictionaries
