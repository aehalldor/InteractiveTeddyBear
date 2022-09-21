###This file holds all the functions used for TIT###
import RPi.GPIO as GPIO
import time
import threading
import os
import time
import busio
import digitalio
import board
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn
import adafruit_mpu6050 
import math

#####function definitions#####
'''
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
'''

