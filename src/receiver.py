import serial
import re # regex
import time
from pynput.keyboard import Key, Controller

# This baudrate is set in distanceTester.cpp
BAUDRATE = 9600

# Port
PORT = "COM3"

# How long the serial waits with no input
TIMEOUT = 1

def main():
	print("--- Welcome to the Anti Infiltrator defense system. ---\n")

	# Keyboard object
	keyboard = Controller() 

	ser = serial.Serial()
	ser.baudrate = BAUDRATE
	ser.port = PORT

	ser.open()

	AUTO_THRESHOLD = input("Automatically get threshold? (y/n) ")
	if AUTO_THRESHOLD == "y":
		AUTO_THRESHOLD = True
	else:
		AUTO_THRESHOLD = False

	if(AUTO_THRESHOLD):
		THRESHOLD_DISTANCE = getAutoThreshold(ser)
	else: 
		# If something is within this distance, the defense system is executed.
		THRESHOLD_DISTANCE = float(input("Enter a threshold distance in cm: "))
	

	SHOW_DISTANCES = input("\nShow distances in real time? (y/n) ")
	if SHOW_DISTANCES == "y":
		SHOW_DISTANCES = True
	else:
		SHOW_DISTANCES = False

	print("\nReceiver activated. Press CTRL + C to quit.")

	try:
		# Infinite loop, reads serial data forever
		while(True):

			# Must extract int from the received string, since, example: 84 is received as b'84\r\n'
			distance = int(re.findall("\d+", str(ser.readline()))[0]) 

			if(distance < THRESHOLD_DISTANCE):
				showDesktop(keyboard)

			if(SHOW_DISTANCES):
				print("\tObject at distance of " + str(distance) + "cm")	

	except KeyboardInterrupt:
		print("Receiver stopped.")


# The WINDOWS + M shortcut displays the desktop
def showDesktop(keyboard):
	keyboard.press(Key.cmd)
	keyboard.press('m')
	keyboard.release(Key.cmd)
	keyboard.release('m')
	print("\tDesktop triggered! That was close.")

# Calculates an appropriate threshold using the serial object
def getAutoThreshold(ser):
	print("Retrieving appropriate threshold...");

	NUM_TESTS = 5
	PERCENT_REDUCTION = 5

	sum = 0 # Sum of distances

	for _ in range(NUM_TESTS):
		sum += int(re.findall("\d+", str(ser.readline()))[0])

	average = sum / NUM_TESTS
	
	threshold = average * ((100 - PERCENT_REDUCTION) / 100)

	print("Average distance over %d tries was %dcm. Threshold set at %d%% lower, at %.1fcm" 
		% (NUM_TESTS, average, PERCENT_REDUCTION, threshold))

	return threshold

main()