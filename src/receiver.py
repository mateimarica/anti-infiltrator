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

	# Serial object
	ser = serial.Serial()
	ser.baudrate = BAUDRATE
	ser.port = PORT
	ser.timeout = TIMEOUT

	# Tries to open serial port. If failed to open, allows user to retry.
	while(True):
		try:
			ser.open()
			break
		except serial.serialutil.SerialException:
			print("Couldn't open the %s port for serial communication. Is your Arduino connected properly?" % PORT)
			input("\tPress ENTER to retry...")


	# The threshold is the minimum distance at which the safety mechanism isn't triggered.
	AUTO_THRESHOLD = (input("Automatically get threshold? (y/n) ") == "y")
	if(AUTO_THRESHOLD):
		THRESHOLD_DISTANCE = getAutoThreshold(ser)
	else: 
		while(True):
			# If something is within this distance, the defense system is executed.
			THRESHOLD_DISTANCE = float(input("Enter a threshold distance in cm: "))

			# Checks if the user's threshold is already breached and offers a retry.
			ser.reset_input_buffer()
			testDistance = float(re.findall("\d+", str(ser.readline()))[0]) / 10
			if(THRESHOLD_DISTANCE > testDistance):
				if(input("There is already an object closer than %.1fcm. Do you want to proceed? (y/n) " % THRESHOLD_DISTANCE) == "y"):
					break
				continue # Restarts loop
			break 			
	
	# If the user wants to constantly see the distances
	SHOW_DISTANCES = (input("\nShow distances in real time? (y/n) ") == "y")

	print("\nReceiver activated. You are now safe. Press CTRL+C to quit.")

	try:
		# Clear any 
		ser.reset_input_buffer()

		# Infinite loop, reads serial data forever
		while(True):

			# Must extract int from the received string, since, example: 84 is received as b'84\r\n'
			distance = float(re.findall("\d+", str(ser.readline()))[0]) / 10

			if(distance < THRESHOLD_DISTANCE):
				showDesktop(keyboard)

			if(SHOW_DISTANCES):
				print("\tObject at distance of " + str(distance) + "cm")	

	except KeyboardInterrupt:
		ser.close()
		print("Receiver stopped. You are no longer safe.")


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

	# The number of distance tests that will be done to get an average distance.
	# The higher this is, the more precise the average distance
	NUM_TESTS = 10

	# Time between tests, in seconds. Example: If NUM_TESTS = 10, getting threshold will be 1 second.
	# Unused
	#TIME_BTWN_TESTS = 0.1

	# The percent reduction of the average distance to get the threshold.
	# The closer to zero, the more sensitive the trigger will be.
	PERCENT_REDUCTION = 5

	PERCENT_UNDER = ((100 - PERCENT_REDUCTION) / 100) # Example: 0.95 if PERCENT_REDUCTION = 5
	PERCENT_OVER = ((100 + PERCENT_REDUCTION) / 100)  # Example: 1.05 if PERCENT_REDUCTION = 5

	sum = 0 # Sum of distances
	lastDistanceCm = None # The last measured distance
	ser.reset_input_buffer() # Clear any old values in the buffer

	i = 0 # Counter variable
	retries = 0 # The number of times the threshold-getting has failed

	while(i < NUM_TESTS):

		currentDistanceCm = float(re.findall("\d+", str(ser.readline()))[0]) / 10
		

		# If the current distance is too different than the previous distance, restart the whole process
		if((lastDistanceCm is not None) and
			(currentDistanceCm * PERCENT_UNDER > lastDistanceCm or 
			 currentDistanceCm * PERCENT_OVER < lastDistanceCm)):

			# Reset everything
			ser.reset_input_buffer()
			i = 0
			sum = 0
			lastDistanceCm = None
			retries += 1

			# Lets the user know that they suck
			if(retries % 2 == 0):
				print("Can't get a steady reading. Retrying...")

			continue
		
		lastDistanceCm = currentDistanceCm	# Save the current distance
		sum += currentDistanceCm			# Adds to sum
		i += 1								# Increment count

		#time.sleep(TIME_BTWN_TESTS)			# Wait between tests. Unused

	# Get average distance
	average = sum / NUM_TESTS
	
	# Get an appropriate threshold for the current distance
	threshold = average * PERCENT_UNDER

	print("Average distance over %d tries was %.1fcm. Threshold set at %d%% lower, at %.1fcm" 
		% (NUM_TESTS, average, PERCENT_REDUCTION, threshold))

	return threshold

main()