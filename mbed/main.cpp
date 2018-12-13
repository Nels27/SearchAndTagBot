#include "mbed.h"
#include <iostream>
#include <string>
#include <stdio.h>
#include <ctype.h>
//Pi mbed USB Slave function
// connect mbed to Pi USB
Serial  pi(USBTX, USBRX);
//Serial pc(USBTX, USBRX);

DigitalOut led1(LED1);
DigitalOut led2(LED2);
DigitalOut led3(LED3);
DigitalOut led4(LED4);

/*
void dev_tag()
{
    
pc.printf("tag\n");
    
}
*/
void dev_recv()
{
    char temp = 0;
    if(pi.readable()){ led3 = !led3;}
    else if (!pi.readable()){led4 = !led4;}
    //led3 = !led3;
    while(pi.readable()) {
        temp = pi.getc();
        //led3 = !led3;
        //string tempString(11, temp);
        //pi.putc(temp);
        if (temp == '*') {
            // Army man is present!
            //led1 = 1;
            led1 = !led1;
            wait(0.5);
       } else if (temp == '!') {
            //Threat is not present
            led2 = !led2;
            wait(0.5);
            //led2 = !led2;
            }
    }
}
int main()
{
    pi.baud(9600);
    //pc.baud(9600);
    //pi.attach(&dev_recv, Serial::RxIrq);
    //pc.attach(&dev_tag, Serial::RxIrq);
    
    
    for (int j = 1; j < 100; j++) { 
    pi.printf("*");
    //wait(0.45);
    }
    
    while(1) {
        //sleep();
        dev_recv();
    }
}
