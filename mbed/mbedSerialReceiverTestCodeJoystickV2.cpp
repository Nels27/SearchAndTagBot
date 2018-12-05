#include "mbed.h"
#include <iostream>
#include <ctype.h>
#include <stdio.h>
#include "Motor.h"
#include "HALLFX_ENCODER.h"
#include "Servo.h"
#include "letters.h"

#include <math.h>
#include <string.h>

#define SPEED 0.66
#define BCKSPEED -0.66
#define TICKSPERREV 390
#define DISTPERREV 8.25         // 8.25 inches per revolution
#define TicksPerDeg 2.42

#define PI 3.1415926535
#define abs(X) ((X < 0) ? -1 * X : X)

DigitalOut led(LED1);
DigitalOut led1(LED2);
Motor RW(p25, p15, p16);    // pwm, fwd, rev
Motor LW(p26, p19, p20);     // pwm, fwd, rev

HALLFX_ENCODER leftEnc(p22);
HALLFX_ENCODER rightEnc(p21);
      
Serial blue(p13,p14);
RawSerial  pi(USBTX, USBRX);

char move = 0;

//need an update command that recieves joystick commands from pi
void getCommand(){
    
    
    char temp = 0;
    while(pi.readable()) {
        temp = pi.getc();
        pi.putc(temp);
        
        if (isblank(temp) =='1') led = 1;
        else {
        if (temp=='e') move = 'f';
        if (temp == 'f') move = 'b';
        if (temp == 'g') move = 'l';
        if (temp == 'h') move = 'r';
         //uppercase character for button released
        if (temp == 'H') move = 's';
        if (temp=='S')  led1=0;
        if (temp == 'z') led1 =1 ;
        }
    }
    }


//data that needs to be sent to the pi for mapping (IMU data and IR sensor data) 
void sendPi(){
    
    
    pi.printf("");
    }

void stop() {
    
   RW.speed(0.0);
    LW.speed(0.0);
}

void forward() {

    RW.speed(SPEED);
    LW.speed(SPEED);
}

void backwards() {
    
    RW.speed(BCKSPEED);
    LW.speed(BCKSPEED);
    
}

void turnRight(){

        RW.speed(BCKSPEED);
        LW.speed(SPEED);
        
    }
    
void turnLeft(){
    
    RW.speed(SPEED);
    LW.speed(BCKSPEED);
 
    }

int main() {
    
 
    
    
    while (1) {
       getCommand();
        
        switch (move) {
            case 'f':
                forward(); 
                break;
            case 's':
                stop();
                break;
            case 'b':
                backwards();
                break;
            case 'r':
                turnRight();
                break;
            case 'l':
                turnLeft();
                break;
        

    }
}
}