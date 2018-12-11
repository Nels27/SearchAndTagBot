import paho.mqtt.client as mqtt
import time
import serial
import pdb

broker = "143.215.98.134"
port = 1883
topic = "controller"
global controllerOutput
controllerOutput = ""
#global tempMsg
tempMsg = ''
addr = "/dev/ttyACM0"
def on_connect(client, userdata, rc):
	print("Connected with result code "+str(rc))
	
	client.subscribe(broker)
	
def on_message(client, userdata, msg):
	global controllerOutput
	global tempMsg
	
	#print("message received"+" "+str(msg.payload))
	#print("message topic =",msg.topic)
	#print("message qos=",msg.qos)
	#print("message retain flag=",msg.retain)
	
	controllerOutput = str(msg.payload)
	print("controller " + controllerOutput)
	print("msg: " + tempMsg)
	
	if tempMsg.__eq__(controllerOutput):
		
		time.sleep(0.7)
		ser.write('z')
		print('I write in if')

		#tempMsg = controllerOutput
	else:
		print(controllerOutput)
		ser.write(controllerOutput)
		print('I write in else')
		tempMsg = controllerOutput
		
	read_val = ser.read()	
	print ("line 45")
	print read_val
	

ser = serial.Serial('/dev/ttyACM0',9600)
print(ser.name)
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect(broker,port)
client.subscribe(topic)
client.on_message
print('I get here')

client.loop_forever()






	
