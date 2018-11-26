
from picamera import picamera
from time import sleep

## Creating the camera object
camera = PiCamera()

#Setting the alpha value in order to set the transparency
alpha = 0
#rotating the image because of the camera mount
camera.rotation = 90

## initiates the start of the camera
camera.start_preview(alpha)
while(True):
    {
    pass #Runs indefinitely until Ctrl+C has been hit
    }
#sleep(10)


camera.stop_preview()
