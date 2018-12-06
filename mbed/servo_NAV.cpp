#include "mbed.h"
#include "Servo.h"

Servo myservo(p21);
BusOut mbedleds(LED1,LED2,LED3,LED4);
//BusOut/In is faster than multiple DigitalOut/Ins

class Nav_Switch
{
public:
    Nav_Switch(PinName up,PinName down,PinName left,PinName right,PinName fire);
    int read();
//boolean functions to test each switch
    bool up();
    bool down();
    bool left();
    bool right();
    bool fire();
//automatic read on RHS
    operator int ();
//index to any switch array style
    bool operator[](int index) {
        return _pins[index];
    };
private:
    BusIn _pins;

};
Nav_Switch::Nav_Switch (PinName up,PinName down,PinName left,PinName right,PinName fire):
    _pins(up, down, left, right, fire)
{
    _pins.mode(PullUp); //needed if pullups not on board or a bare nav switch is used - delete otherwise
    wait(0.001); //delays just a bit for pullups to pull inputs high
}
inline bool Nav_Switch::up()
{
    return !(_pins[0]);
}
inline bool Nav_Switch::down()
{
    return !(_pins[1]);
}
inline bool Nav_Switch::left()
{
    return !(_pins[2]);
}
inline bool Nav_Switch::right()
{
    return !(_pins[3]);
}
inline bool Nav_Switch::fire()
{
    return !(_pins[4]);
}
inline int Nav_Switch::read()
{
    return _pins.read();
}
inline Nav_Switch::operator int ()
{
    return _pins.read();
}

Nav_Switch myNav( p9, p6, p7, p5, p8); //pin order on Sparkfun breakout'



int main()

{
    myservo.calibrate(.00085, 180.0); 
    float p = 0.5;

    
    while(1) {
        if (myNav.up())
        {   
        p = 0.0;
        myservo = p;
        wait(.2);
        }
        else if (myNav.left())
        {  
        p = .5;
        myservo = p;
       wait(.2);
        }
        else if (myNav.right())
        {   
        p = 1.0;
        myservo = p;
       wait(.2);
        }
        else if (myNav.down()) 
        {   
        myservo = p +.1;
        p = p+.1;
        wait(.2);        

        }
        else if (myNav.fire())         
        {   
        myservo = p - .1;
        p = p-.1;
        wait(.2);
        }
        
}
}