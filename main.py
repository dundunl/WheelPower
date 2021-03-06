#import thread
import signal
import sys
import numpy
import time

from compFilterv2 import *
from driverClass import *

# Initialize driver/sensor classes
drive = driver()
compFilter = CompFilter()
ignoreAngles = 500

# Signal handler (Ctrl+C)
def signal_handler(signal, frame):
	drive.stop()
	sys.exit()

# ignore first 10 angles
def ignore_angle():
	print("Please wait for initialization")
	for x in range(ignoreAngles):
		compFilter()
# setup base angles and values
def get_base_angle():
	tempAngle = 0
	for x in range(20):
		compFilter()
		tempAngle += compFilter.angle
	global flat_thresh
	global down_thresh
	global up_thresh
	flat_thresh = tempAngle/20
	down_thresh = flat_thresh - 2
	up_thresh = flat_thresh + 2
	print("Base angle is set to: " +str(flat_thresh))
# Retrieve previous x angles and average them
def get_angle():
   # angle = numpy.mean( [compFilter() for i in range(debounce)] )
	tempAngle = 0
	for x in range(20):
		compFilter()
		tempAngle += compFilter.angle
	angle = tempAngle/20
	return angle
	
# Move chair based on angle
def move_chair(angle):
        print("Current angle is "+str(angle))
	if angle > up_thresh:
		drive.forward()
		print("Moving forward")
		while True:
			drive.forward()

	elif angle < down_thresh:
		#drive.backward()
		print("Braking")


	else:
		drive.stop()
		print("Not doing anything")
 

# Main
signal.signal(signal.SIGINT, signal_handler)
ignore_angle()
get_base_angle()
time.sleep(3)
while True:
	angle = get_angle()
	move_chair(angle)
