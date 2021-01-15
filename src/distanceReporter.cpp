#include <Arduino.h>

// This pin connects to the trigger pin of the HC-SR04 distance sensor.
#define TRIGGER_PIN 7

// This pin connects to the echo pin of the HC-SR04 distance sensor.
#define ECHO_PIN 8

long microsecondsToMillimeters(long duration);

// Function runs once at beginning.
void setup() {
	pinMode(TRIGGER_PIN, OUTPUT);
	pinMode(ECHO_PIN, INPUT);
	Serial.begin(9600);
	
}

// Function loops infinitely.
void loop() {

	// Clear the TRIGGER_PIN state.
	digitalWrite(TRIGGER_PIN, LOW);
	delayMicroseconds(10);

	// The sensor is triggered by a HIGH pulse of 10 or more microseconds.
	digitalWrite(TRIGGER_PIN, HIGH);
	delayMicroseconds(10);

	// The duration between transmitting the ultrasonic signal and recieving the echo.
	long duration = pulseIn(ECHO_PIN, HIGH);

	// The distance travelled in the given duration in centimeters.
	int millimeters = microsecondsToMillimeters(duration);
	
	// This is what sends the distance to the receiver.py program.
	Serial.println(millimeters);

	delay(25);
}

/*
	Converts the distance travelled in the given duration of microseconds to mm.
	The speed of sound is ~343 m/s or 2.92 microseconds/mm.
	duration is already in microseconds, so divide by 2.92.
	Then divide by 2 since to get half the distance travelled (distance between sensor to object).
*/
long microsecondsToMillimeters(long duration) {
	return duration / 2.92 / 2;
}