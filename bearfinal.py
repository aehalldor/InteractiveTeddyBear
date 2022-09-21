#!/usr/bin/python3
import RPi.GPIO as GPIO
import time
import threading
import os
import random
import time
import busio
import digitalio
import board
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn
import adafruit_mpu6050 
import math
import pygame
import numpy as np
import sounddevice as sd

# perf_counter is more precise than time() for dt calculation 
from time import sleep, perf_counter 
 
#accelermeter
i2c = busio.I2C(board.SCL, board.SDA) 
mpu = adafruit_mpu6050.MPU6050(i2c)

MOVE_AVERAGE_CONST = 5 #number of points saved for moving average

x_vals = [0] * MOVE_AVERAGE_CONST
y_vals = [0] * MOVE_AVERAGE_CONST
z_vals = [0] * MOVE_AVERAGE_CONST

####analog to digital stuff#####
# create the spi bus
spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)
# create the cs (chip select)
cs = digitalio.DigitalInOut(board.D22)
# create the mcp object
mcp = MCP.MCP3008(spi, cs)
# create an analog input channel on pin 0
chan0 = AnalogIn(mcp, MCP.P0)


###Buttons####
GPIO.setmode(GPIO.BCM)

LeftHand = 6
RightHand = 5


GPIO.setwarnings(False)
GPIO.setup(LeftHand, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(RightHand, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

###Eyes###
LED_R = 13
LED_G = 19
LED_B = 26

GPIO.setup([LED_R], GPIO.OUT, initial=GPIO.LOW)
GPIO.setup([LED_G], GPIO.OUT, initial=GPIO.LOW)
GPIO.setup([LED_B], GPIO.OUT, initial=GPIO.LOW) 

###state declarations###
state_change = True
prev_eye_state = 'RGB'
eye_state = 'RGB'
blinking = False

### Audio file paths ###
happy = [['voices/happy1.mp3',1.3],['voices/happy2.mp3',1.3],['voices/iwuvu.mp3',1.3]]
sad = [['voices/sad1.mp3',1.3],['voices/crying.mp3',1.5],['voices/wah.mp3',1.3]]
special = [['voices/whoop.mp3',1.4],['voices/gigem.mp3',1.2]]
scared = [['voices/surprise0.mp3',0.5],['voices/surprise1.mp3',0.5],['voices/scream2.mp3',0.7]]


###functions###
def EyeState(color):
	if color == 'R':
		GPIO.setup([LED_R], GPIO.OUT, initial=GPIO.LOW)
		GPIO.setup([LED_G], GPIO.OUT, initial=GPIO.HIGH)
		GPIO.setup([LED_B], GPIO.OUT, initial=GPIO.HIGH)
	elif color == 'B':
		GPIO.setup([LED_R], GPIO.OUT, initial=GPIO.HIGH)
		GPIO.setup([LED_G], GPIO.OUT, initial=GPIO.HIGH)
		GPIO.setup([LED_B], GPIO.OUT, initial=GPIO.LOW)
	elif color == 'G':
		GPIO.setup([LED_R], GPIO.OUT, initial=GPIO.HIGH)
		GPIO.setup([LED_G], GPIO.OUT, initial=GPIO.LOW)
		GPIO.setup([LED_B], GPIO.OUT, initial=GPIO.HIGH)
	elif color == 'RB' or color == 'BR':
		GPIO.setup([LED_R], GPIO.OUT, initial=GPIO.LOW)
		GPIO.setup([LED_G], GPIO.OUT, initial=GPIO.HIGH)
		GPIO.setup([LED_B], GPIO.OUT, initial=GPIO.LOW)
	elif color == 'BG' or color == 'GB':
		GPIO.setup([LED_R], GPIO.OUT, initial=GPIO.HIGH)
		GPIO.setup([LED_G], GPIO.OUT, initial=GPIO.LOW)
		GPIO.setup([LED_B], GPIO.OUT, initial=GPIO.LOW)
	elif color == 'RG' or color == 'GR':
		GPIO.setup([LED_R], GPIO.OUT, initial=GPIO.LOW)
		GPIO.setup([LED_G], GPIO.OUT, initial=GPIO.LOW)
		GPIO.setup([LED_B], GPIO.OUT, initial=GPIO.HIGH)
	elif color == 'RGB':
		GPIO.setup([LED_R], GPIO.OUT, initial=GPIO.LOW)
		GPIO.setup([LED_G], GPIO.OUT, initial=GPIO.LOW)
		GPIO.setup([LED_B], GPIO.OUT, initial=GPIO.LOW)
	else:
		GPIO.setup([LED_R], GPIO.OUT, initial=GPIO.HIGH)
		GPIO.setup([LED_G], GPIO.OUT, initial=GPIO.HIGH)
		GPIO.setup([LED_B], GPIO.OUT, initial=GPIO.HIGH)

def PlaySound(emotion):
	num = random.randint(0, len(emotion)-1)
	path = emotion[num][0]
	print('playing',path)
	####insert actual sound being played
	t = emotion[num][1]
	pygame.mixer.init()
	pygame.mixer.music.load("/home/pi/final/" + path)
	pygame.mixer.music.play()
	###while pygame.mixer.music.get_busy() == True:
	###	continue
	return t

def Blink(t,color, color2 = 'null', off = 0.09, on = 1.75):
	total_time = 0
	global blinking 
	blinking = True
	if color2 == 'null': #only one color given
		while total_time < t:
			EyeState('off')
			total_time += off
			time.sleep(off)
			
			EyeState(color)
			total_time += on
			time.sleep(on)
	else:
		while total_time < t:
			EyeState('off')
			total_time += off
			time.sleep(off)
			
			EyeState(color)
			total_time += on
			time.sleep(on)
			
			EyeState('off')
			total_time += off
			time.sleep(off)
			
			EyeState(color2)
			total_time += on
			time.sleep(on)
			
		EyeState('off')
		time.sleep(off)
		blinking = False
		return

def Falling():
	print('Fell')
	
	t = PlaySound(scared)
	Blink(t,'RB','null', 0, 0.5)
	EyeState('RGB')
	

###Handlers###
def hand_handler(pin):
	print('hand touched')
	count = 0
	left = False
	right = False
	while count < 20:
		if GPIO.input(LeftHand):
			left = True
		if GPIO.input(RightHand):
			right = True
		count += 1
		time.sleep(0.02)
		
	if right and left:
		print('both hands touched')
		t =PlaySound(special)
		Blink(t,'RB')
	elif left:
		print('left hand touch')
		t = PlaySound(happy)
		Blink(t,'RG','null',0.05,0.8)
	elif right:
		print('right handtouch')
		t = PlaySound(sad)
		Blink(t,'B','null',0)
	EyeState('RGB')
	global blinking
	blinking = False
		
be_quiet_count = 0

cool_down = False
cool_down_count = 0

def audio_callback (indata, frames, time, status):
	volume_norm = np.linalg.norm(indata) * 10
	vol = int(volume_norm)
	#print(vol)
	global be_quiet_count
	global cool_down_count
	global cool_down
	if cool_down_count > 50:
		cool_down = True
	cool_down_count += 1
	if be_quiet_count > 1000:
		#play be quiet
		pygame.mixer.init()
		pygame.mixer.music.load("/home/pi/final/" + 'voices/bequiet.mp3')
		pygame.mixer.music.play()
		be_quiet_count = 0
		
	if vol > 400 and cool_down:
		cool_down = False
		cool_down_count = 0
		print(volume_norm,"|" * vol)
		#include interrupt
		print('loud noise')
		t = PlaySound(scared)
		Blink(t,'G')
		EyeState('RGB')
		#print(volume_norm,"|" * vol)
		global blinking
		blinking = False
	elif vol > 20:
		be_quiet_count += 1
		#include interrupt
	

	

####Events###

GPIO.add_event_detect(LeftHand,GPIO.BOTH,hand_handler)
GPIO.add_event_detect(RightHand,GPIO.BOTH,hand_handler)

####Main Loop###
count = 0 
mov = 0
y = 0
FALL_THRESHOLD = 0.6 #when acceleration falls below this amount, the bear is detecting falling
static_blink_count = 400
blink_count = 0
fall_cool_down = 30 #cycles
fell = -100


stream = sd.InputStream(callback=audio_callback)

with stream:
	while True:
		count += 1
		blink_count+= 1
		fell += 1
		
		if blink_count > static_blink_count and not blinking:
			interval = random.randint(3, 5)
			if interval >= 5 and not blinking:
				EyeState('off')
				time.sleep(0.04)
				EyeState('RGB')
				time.sleep(0.2)
				EyeState('off')
				time.sleep(0.04)
				EyeState('RGB')
			elif not blinking:
				EyeState('off')
				time.sleep(0.06)
				EyeState('RGB')
			blink_count = 0
			static_blink_count = interval * 100
			
				
		if False: #count > 5:
			#print(mov)
			#print(y)
			count = 0
			if chan0.value != 0:
				print('Raw ADC Value: ', math.log(10,chan0.value))
			
		if mov < FALL_THRESHOLD and fell > fall_cool_down:
			print('FALLING')
			Falling()	
			fell = 0
		
			
			
			
		sleep(0.001) 
		
		#GET FILTERED POINTS#
		x_curr = mpu.acceleration[0]
		y_curr = mpu.acceleration[1]
		z_curr = mpu.acceleration[2]
		
		#moves values back
		for i in range(1, MOVE_AVERAGE_CONST):
			x_vals[i-1] = x_vals[i]
			y_vals[i-1] = y_vals[i]
			z_vals[i-1] = z_vals[i]
			
		#updating with curr values
		x_vals[MOVE_AVERAGE_CONST-1] = x_curr
		y_vals[MOVE_AVERAGE_CONST-1] = y_curr
		z_vals[MOVE_AVERAGE_CONST-1] = z_curr
		
		#get move averages
		x = sum(x_vals)/MOVE_AVERAGE_CONST
		y = sum(y_vals)/MOVE_AVERAGE_CONST
		z = sum(z_vals)/MOVE_AVERAGE_CONST
		   
		mov = math.sqrt(x**2 + y**2 +z**2)
		
    

    
		
	
		
		




###Tests
###light functions###
'''
print('light red')
EyeState('R')
time.sleep(1)
print('blue')
EyeState('B')
time.sleep(1)
print('RB')
EyeState('RB')
time.sleep(1)
print('off')
EyeState('off')
time.sleep(2)
EyeState('RGB')
'''


while False: ###button tests
	
	if GPIO.input(LeftHand):
		print("LeftHand works")
		GPIO.output(LED_R, True)
		GPIO.output(LED_G, True)
		GPIO.output(LED_B, True)
	if GPIO.input(RightHand):
		print("RightHand works")
		GPIO.output(LED_R, False)
		GPIO.output(LED_G, False)
		GPIO.output(LED_B, False)
	

while False: ###accelerometer tests
    sleep(0.0001) 
    
    #GET FILTERED POINTS#
    x_curr = mpu.acceleration[0]
    y_curr = mpu.acceleration[1]
    z_curr = mpu.acceleration[2]
    
    #moves values back
    for i in range(1, MOVE_AVERAGE_CONST):
        x_vals[i-1] = x_vals[i]
        y_vals[i-1] = y_vals[i]
        z_vals[i-1] = z_vals[i]
        
    #updating with curr values
    x_vals[MOVE_AVERAGE_CONST-1] = x_curr
    y_vals[MOVE_AVERAGE_CONST-1] = y_curr
    z_vals[MOVE_AVERAGE_CONST-1] = z_curr
    
    #get move averages
    x = sum(x_vals)/MOVE_AVERAGE_CONST
    y = sum(y_vals)/MOVE_AVERAGE_CONST
    z = sum(z_vals)/MOVE_AVERAGE_CONST
    
    
    
    print(x, y, z)

while False: ###analog signal test
	time.sleep(0.001)
	print('Raw ADC Value: ', chan0.value)



###sound
