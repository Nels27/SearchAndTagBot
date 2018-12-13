

"""
Google Vision API Tutorial with a Raspberry Pi and Raspberry Pi Camera.  See more about it here:  https://www.dexterindustries.com/howto/use-google-cloud-vision-on-the-raspberry-pi/

Use Google Cloud Vision on the Raspberry Pi to take a picture with the Raspberry Pi Camera and classify it with the Google Cloud Vision API.   First, we'll walk you through setting up the Google Cloud Platform.  Next, we will use the Raspberry Pi Camera to take a picture of an object, and then use the Raspberry Pi to upload the picture taken to Google Cloud.  We can analyze the picture and return labels (what's going on in the picture), logos (company logos that are in the picture) and faces.

This script uses the Vision API's label detection capabilities to find a label
based on an image's content.

"""

import argparse
import base64
import picamera
import json
import math
import serial
import io

from googleapiclient import discovery
from oauth2client.client import GoogleCredentials



def takephoto():
	camera = picamera.PiCamera()
	camera.capture('image.jpg')

def main():
	tagObject = ''
	check = "Nothing sent yet"
	takephoto() # First take a picture
	"""Run a label request on a single image"""
	credentials = GoogleCredentials.get_application_default()
	service = discovery.build('vision', 'v1', credentials=credentials)
	
	ser = serial.Serial('/dev/ttyACM0',9600)
	
	#sio = io.TextIOWrapper(io.BufferedRWPair(ser, ser))
	#print(check)
	check = ser.read()
	
	print check
	print(ser.name)
	if(check == '*'):
		with open('image.jpg', 'rb') as image:
			image_content = base64.b64encode(image.read())
			service_request = service.images().annotate(body={
				'requests': [{
					'image': {
						'content': image_content.decode('UTF-8')
					},
					'features': [{
						'type': 'LABEL_DETECTION',
						'maxResults': 10
					}]
				}]
			})
			response = service_request.execute()
			#json_data = json.loads("description")
			msg =  json.dumps(response)
					#print(msg)
			testA = msg.count("military")
			testB = msg.count("army men")
			testC = msg.count("soldier")
			testD = msg.count("gun")
			total = testA + testB + testC + testD
			#print(total)
			if (total >= 1):
				print("%d :Total threats detected" %(total))
				tagObject ='*!'
				for w in range(0,100):					
					readVal = ser.write(tagObject)
				print readVal
			else:
				print("No threat found")
				tagObject = '!'
				for w in range(0,100):
					readVal = ser.write(tagObject)
				print readVal
	else:
		print("Nothing was sent from mbed")			
		
			
			#print json.dumps(response, indent=4, sort_keys=True)	#Print it out and make it somewhat pretty.

#def printResponse():
#	toParse = json.dumps(reponse,indent = 4, sort_keys=True)
#	print(toParse)


if __name__ == '__main__':

    main()
 #   printResponse()

