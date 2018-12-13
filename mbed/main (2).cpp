#include "mbed.h"
#include "Motor.h"
#include "Servo.h"
#include "SDFileSystem.h"
#include "wave_player.h"
#include "LSM9DS1.h"
#include <stdio.h>
#include <math.h>
#define PI 3.14159
#define DECLINATION -4.94
#define rturn 65.2174 //degrees/sec
#define lturn 63.1136 //degrees/sec
Serial pc(USBTX,USBRX);

DigitalOut led (LED2);
Serial blue(p13,p14); 
Motor RW(p25, p15, p16);    // pwm, fwd, rev //B
Motor LW(p26, p19, p20);     // pwm, fwd, rev //A
Servo servo(p21);
DigitalOut trigger(p17);
DigitalIn  echo(p12);
SDFileSystem sd(p5, p6, p7, p8, "sd");
AnalogOut DACout(p18);
wave_player waver(&DACout);

Timer sonar;
Timer  y;


//global variable that is used to call functions
char move = 0;
float heading = 0;
int obj_distance = 0;
int sonar_correction = 0;
char tag;
char PIVALUE;
char turn;





void printAttitude(float ax, float ay, float az, float mx, float my, float mz)
{
// touchy trig stuff to use arctan to get compass heading (scale is 0..360)
    mx = -mx;
    float heading;
    if (my == 0.0)
        heading = (mx < 0.0) ? 180.0 : 0.0;
    else
        heading = atan2(mx, my)*360.0/(2.0*PI);
    //pc.printf("heading atan=%f \n\r",heading);
    heading -= DECLINATION; //correct for geo location
    if(heading>180.0) heading = heading - 360.0;
    else if(heading<-180.0) heading = 360.0 + heading;
    else if(heading<0.0) heading = 360.0  + heading;

    //pc.printf("Pitch: %f,    Roll: %f degress\n\r",pitch,roll);
    pc.printf("H: %f",heading);
    FILE *fp = fopen("/sd/mapdata.txt", "a");
    fprintf(fp, "%f",heading);
    fclose(fp);  
    
}

void calcTurn()
{
    if (turn == 'right')
    {
        heading = heading + (y.read() * rturn);
        if (heading >= 360)
            {heading  = heading - 360;}
    }
    
    else
    {
        heading = heading - (y.read() * lturn);
        if (heading < 0)
        {heading = 360 + heading;}
        
    }
    
    turn = ' ';
}

void printToSD(){
    
    
    FILE *fp = fopen("/sd/mapdata.txt", "a");
    fprintf(fp,"%f,%f,%c,",heading, y.read(), tag);
    fclose(fp);    
    }
    
void sonarCheck(){
    sonar.reset();
// measure actual software polling timer delays
// delay used later in time correction
// start timer
    sonar.start();
// min software polling delay to read echo pin
    while (echo==2) {};
// stop timer
    sonar.stop();
// read timer
    sonar_correction = sonar.read_us();
    //pc.printf("Approximate software overhead timer delay is %d uS\n\r",sonar_correction);

//Loop to read Sonar distance values, scale, and print
    for(int y = 0; y < 6; y++){
// trigger sonar to send a ping
        trigger = 1;
        sonar.reset();
        wait_us(10.0);
        trigger = 0;
//wait for echo high
        while (echo==0) {};
//echo high, so start timer
        sonar.start();
//wait for echo low
        while (echo==1) {};
//stop timer and read value
        sonar.stop();
//subtract software overhead timer delay and scale to cm
        obj_distance = (sonar.read_us()-sonar_correction)/58.0;
        //pc.printf(" %d cm \n\r",distance);
//wait so that any echo(s) return before sending another ping
        wait(0.2);
    }
    }

void randVoice(){
    
    //pick a random wav file and play it
    int n = 0;
    const char* file;
    n = rand() % 9;
    if (n==1) file = "/sd/im_scared.wav";
    else if (n==2) file = "/sd/flying.wav";
    else if (n==3) file = "/sd/stop.wav";
    else if (n==4) file = "/sd/squish.wav";
    else if (n==5) file = "/sd/hey.wav";
    else if (n==6) file = "/sd/protect.wav";
    else if (n==7) file = "sd/feelings.wav";
    else if (n==8) file = "sd/wee.wav";
    else if (n==0) file = "sd/fire.wav";
    else file = "sd/roar.wav";
    
    
    FILE * fp = fopen(file, "r");
    if(fp != NULL) {
        waver.play(fp);
        fclose(fp);
        }
    }
void roar() {
    FILE * fp = fopen("/sd/roar.wav", "r");       
        if (fp != NULL) {
            waver.play(fp);
            fclose(fp);
        }     
    }
    
void target() {
    FILE * fp = fopen("/sd/target_acquired.wav", "r");
        if (fp != NULL) {
            waver.play(fp);
            fclose(fp);
            }
    }

void icu() {
    FILE * fp = fopen("/sd/icu.wav", "r");     
        if (fp != NULL) {
            waver.play(fp);
            fclose(fp);
        }
    
    }
void hey() {
    
    FILE * fp = fopen("/sd/hey.wav", "r");     
        if (fp != NULL) {
            waver.play(fp);
            fclose(fp);
        }
    
    }
    
void readPi(){
    
    
    tag = '0';
    char temp = 0;
    while(pc.readable()) {
        temp = pc.getc();
        pc.putc(temp);
        
        if (temp == '0') led = 1;
        
        else {    
        //motor movement
        if (temp == '!') 
        {
            PIVALUE = 'N';
            tag = '0';
            printToSD();
            
        }
        else if (temp == '*') 
        {
            tag = '1';
            PIVALUE = 'Y';
            printToSD();
        }
        else 
        {
            PIVALUE = 'N';
            }
            
            
        
        
        }
        
    }

    
}

//bot movement using bluetooth thread
int main()
{
 
    FILE *fp = fopen("/sd/mapdata.txt", "w");
    fclose(fp); 
    servo.calibrate(.00085, 180.0);
    float p = 0.5;
    char previousButton='0';
    char current;
    led=0;
    pc.printf("in main\n\r");
    char bnum=0;
    char bhit=0;

 
    
    while(1) {
        
    if (p < 0.0)
    p=0.0;
    else if (p > 1.0)
    p=1.0;     
    if(blue.readable()==1){
        if (blue.getc()=='!') {
            if (blue.getc()=='B') { //button data packet
                bnum = blue.getc(); //button number
                bhit = blue.getc(); //1=hit, 0=release
                current=bnum;  
                previousButton = current; 
                if (blue.getc()==char(~('!' + 'B' + bnum + bhit))) { 
                    switch (bnum) {
                        case '1': //number button 1
                            if (bhit=='1') {
                                //led = 1;
                                servo = p - .1;
                                p = p-.1;
                                wait(.2);
                            } else {
                                //add release code here
                            break;
                        case '2': //number button 2
                            if (bhit=='1') {
                                //led1 = 1;
                                servo = p +.1;
                                p = p+.1;
                                wait(.2);
                                //add hit code here
                            } else {
                                //add release code here
                            }
                            break;
                        case '3': //number button 3
                            if (bhit=='1') {
                                randVoice();
                            } else {
                                //add release code here
                            }
                            break;
                        case '4': //number button 4
                            if (bhit=='1') {
                                sonarCheck();
                                if(obj_distance < 15) //we are close enough to tag
                                    {
                                        icu();
                                         //printAttitude(IMU.calcAccel(IMU.ax), IMU.calcAccel(IMU.ay), IMU.calcAccel(IMU.az), IMU.calcMag(IMU.mx),IMU.calcMag(IMU.my), IMU.calcMag(IMU.mz));
                                        
                                        for (int j=0; j<100; j++)
                                        {pc.printf("*");}
                                         
                                        readPi();
                                        if(PIVALUE == 'Y')
                                            target();
                                        else if (PIVALUE == 'N')
                                            hey();
                                        printToSD();

                                                                                                  
                                    }
                                    else if (obj_distance > 15) //get closer to tag
                                    {
                                        roar();
                                        
                                        for (int j=0; j<100; j++)
                                        {pc.printf("*");}
                                        
                                       
                                    }
                            } else {
                                //add release code here
                            }
                            break;
                        case '5': //button 5 up arrow
                            if (bhit=='1') {
                                tag = 'm';
                                y.reset();
                                y.start();
                                RW.speed(.45);
                                LW.speed(.39);  
                            } else {
                                y.stop();
                                RW.speed(0); 
                                LW.speed(0); 
                                printToSD();
                            }
                            break;
                        case '6': //button 6 down arrow
                            if (bhit=='1') {
                                tag = 'm';
                                RW.speed(-.47);
                                LW.speed(-.39);  
                                //add hit code here
                            } else {
                                RW.speed(0);
                                LW.speed(0);
                            }
                            break;
                        case '7': //button 7 left arrow
                            if (bhit=='1') {
                                tag = 'm';
                                y.reset();
                                y.start();
                                RW.speed(-.47);
                                LW.speed(.39);
                                turn = 'left';
                            } else {
                                y.stop();
                                
                                calcTurn();
                            
                                printToSD();
                                RW.speed(0);
                                LW.speed(0);
                            }
                            break;
                        case '8': //button 8 right arrow
                            if (bhit=='1') {
                                tag = 'm';
                                y.reset();
                                y.start();
                                RW.speed(.47);
                                LW.speed(-.39);
                                turn = 'right';
                            } else {
                                y.stop();
                                
                                calcTurn();
                                printToSD();
                                RW.speed(0);
                                LW.speed(0);
                            }
                            break;
                        default:
                            break;
                    }
                    }
                    }
                }
          
            }
           
            
            
        }
    }
   } 