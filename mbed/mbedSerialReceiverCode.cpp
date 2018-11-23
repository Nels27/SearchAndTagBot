

// mbed serial connection receiver code for servo commands


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

int main()
{
    pi.baud(9600);
    pi.attach(&dev_recv, Serial::RxIrq);
    while(1) {

        char temp = 0;

        while(pi.readable()) {
            temp = pi.getc();
            pi.putc(temp);
            if (temp=="Up button was pressed")
            {   led3 = !led3;
                LW.speed(1.0);
                RW.speed(1.0);
            }
            else if (temp == "Down button was pressed" )
            {   led3 = !led3;
                RW.speed(-1.0);
                LW.speed(-1.0);
            }
            else if (temp == "Left button was pressed")
            {   led2 = !led2;
                RW.speed(-1.0);
                LW.speed(1.0);
            }
            else if (temp == "Right button was pressed")
            {   led2 = !led2;
                RW.speed(1.0);
                LW.speed(-1.0);
            }
            else if (temp == "Left Joystick was moved left")
            {
                //Rotate camera servo
                led4 = !led4;
            }
            else if (temp == "Left Joystick was moved right")
            {
                led1 = !led1;
            }
        }
        sleep();
    }
}
