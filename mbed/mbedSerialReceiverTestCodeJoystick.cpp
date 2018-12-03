#include "mbed.h"
#include <iostream>
#include <string>
#include <stdio.h>
#include <ctype.h>
#include "mbed.h"
#include "Motor.h"
#include "rtos.h"

//Pi mbed USB Slave function
// connect mbed to Pi USB
RawSerial  pi(USBTX, USBRX);

// Use these for debugging purposes
DigitalOut led1(LED1); // Use this for color filter purposes
DigitalOut led2(LED2); // Use for left right movement
DigitalOut led3(LED3); // Use for up down movement
DigitalOut led4(LED4); // Use for servo rotation
Motor RW(p22, p7, p6); //  pwm, fwd, rev
Motor LW(p21, p8, p11);// pwm, fwd, rev



void dev_recv()
{
    char temp = 0;
    //led1 = !led1;
    while(pi.readable()) {
        temp = pi.getc();
        //string tempString(11, temp);
        pi.putc(temp);
        if (isblank(temp) == true) { print('Error with communciation')};

        elseif (isblank(temp) == false) {print('Connection successful')};
            if (temp == "Up button pressed") {

            }

            elseif (temp == "Up button let go"){

            }

            elseif (temp == "Down button pressed") {

            }

            elseif (temp == "Down button let go"){

            }

            elseif (temp == "Left button pressed") {

            }

            elseif (temp == "Left button let go"){

            }

            elseif (temp == "Right button pressed") {

            }

            elseif (temp == "Right button let go"){

            }

            elseif (temp == "Left Joystick moved up") {

            }

            elseif (temp == "Left Joystick moved down"){

            }

            elseif (temp == "Left Joystick moved left") {

            }

            elseif (temp == "Left Joystick moved right"){

            }

            elseif (temp == "Right Joystick moved up") {

            }

            elseif (temp == "Right Joystick moved down"){

            }

            elseif (temp == "Right Joystick moved left") {

            }

            elseif (temp == "Right Joystick moved right"){

            }

            elseif (temp == "X button pressed") {

            }

            elseif (temp == "X button let go"){

            }

            elseif (temp == "O button pressed") {

            }

            elseif (temp == "O button let go"){

            }

            elseif (temp == "Square button pressed") {

            }

            elseif (temp == "Square button let go"){

            }

            elseif (temp == "Triangle button pressed") {

            }

            elseif (temp == "Triangle button let go"){

            }






    }
}
int main()
{
    pi.baud(9600);
    pi.attach(&dev_recv, Serial::RxIrq);
    while(1) {
        sleep();
    }
}
