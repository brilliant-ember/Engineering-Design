##Code by Brilliant Ember, Shed  Automation (TeamMembers: Classified)
## University of Ottawa; GNG1103
##plz run with Python 3

import RPi.GPIO as GPIO
from time import sleep
import os
import glob
import time
DEBUG = 1

GPIO.setwarnings(False)
# The script as below using BCM GPIO 00..nn numbers
GPIO.setmode(GPIO.BCM)

# Set relay pins as output
GPIO.setup(12, GPIO.OUT) #relay in3 (Fan)
GPIO.setup(16, GPIO.OUT) #relay in4 (Bulb)
GPIO.setup(17, GPIO.IN)  #Read output from PIR motion sensor

#preps the one wire interface for the temp sensor

os.system('modprobe w1-gpio')  # Turns on the GPIO module
os.system('modprobe w1-therm') # Turns on the Temperature module

# Finds the correct device file that holds the temperature data
base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28*')[0]
device_file = device_folder + '/w1_slave'

# A function that reads the sensors data
def read_temp_raw():
    f = open(device_file, 'r') # Opens the temperature device file
    lines = f.readlines() # Returns the text
    f.close()
    return lines

# Convert the value of the sensor into a temperature
def read_temp():
    lines = read_temp_raw() # Read the temperature 'device file'

# While the first line does not contain 'YES', wait for 0.2s
# and then read the device file again.
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw()

# Look for the position of the '=' in the second line of the
# device file.
    equals_pos = lines[1].find('t=')

# If the '=' is found, convert the rest of the line after the
# '=' into degrees Celsius
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string) / 1000.0
     
    return temp_c


#####end of temp code####

################PhotoCell code#########

def RCtime (RCpin):
        reading = 0
        GPIO.setup(RCpin, GPIO.OUT)
        GPIO.output(RCpin, GPIO.LOW)
        time.sleep(0.1)

        GPIO.setup(RCpin, GPIO.IN)
        # This takes about 1 millisecond per loop cycle
        while (GPIO.input(RCpin) == GPIO.LOW):
                reading += 1
        return reading


######end of photocell#########

while (True): #main loop
    ##Bulb Control
    PhotoCell=RCtime(18)
    def Cell():
        if PhotoCell>15000:
            return True #dark
        elif PhotoCell<15000:
            return False #light
    i=GPIO.input(17)
    if i==1 and Cell():       #When output from motion sensor is LOW and cell drk
        GPIO.output(16, GPIO.HIGH) #turn the bulb on
        time.sleep(0.1)
        print("introder")
             
    elif i==0 or not(Cell()):#cell is on or When output from motion sensor is HIGH
        GPIO.output(16, GPIO.LOW) #turn the bulb off
        time.sleep(0.1)
        print("no introder yay")
    
    ## Fan Control the fan is a heating system so when temp is low turn it on
    if read_temp() >= 26:
        print (read_temp(),"C")
        GPIO.output(12, GPIO.LOW)
    elif read_temp()<26:
        GPIO.output(12, GPIO.HIGH)
        print (read_temp(),"C")
             
    
    
