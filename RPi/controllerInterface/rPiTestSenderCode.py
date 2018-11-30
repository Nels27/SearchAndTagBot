import serial
import time

ser = serial.Serial('/dev/ttyACM0',9600)
print(ser.name)
ser.write("hello")
read_val = ser.read_until("hello",5)
print read_val
ser.close()
