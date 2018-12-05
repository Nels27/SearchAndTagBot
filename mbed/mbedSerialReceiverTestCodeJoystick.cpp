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
//Motor RW(p22, p7, p6); //  pwm, fwd, rev
//Motor LW(p21, p8, p11);// pwm, fwd, rev



void dev_recv()
{
    char temp = '0';
    //led1 = !led1;
    while(pi.readable()) {
        temp = pi.getc();
        //string tempString(11, temp);
        pi.putc(temp);
        if (isblank(temp) == '1')  led2 = 1;

        else if (isblank(temp) == '0') led3 = 1;

            if(temp == 'e') led1 = 1;

            else if(temp == 'E') led1 = 0;

            else if(temp == 'f') led2 = 1;

            else if(temp == 'F') led2 = 0;

            else if(temp == 'g') led3 = 1;

            else if(temp == 'G') led3 = 0;

            else if(temp == 'h') led4 = 1;

            else if(temp == 'H') led4 = 0;

            else if(temp == 'z'){
                led1 = 0;
                led2 = 0;
                led3 = 0;
                led4 = 0;
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
