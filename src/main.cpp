#include <Arduino.h>

// This pin connects to the trigger pin of the HC-SR04 distance sensor.
#define TRIGGER_PIN 7

// This pin connects to the echo pin of the HC-SR04 distance sensor.
#define ECHO_PIN 8

long microsecondsToCentimeters(long duration);

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

	// The sensor is triggered by a HIGH pulse of 10 or more microseconds. Using 1 millisecond to be safe.
	digitalWrite(TRIGGER_PIN, HIGH);
	delayMicroseconds(10);

	// The duration between transmitting the ultrasonic signal and recieving the echo.
	long duration = pulseIn(ECHO_PIN, HIGH);

	//The distance travelled in the given duration in centimeters.
	float centimeters = microsecondsToCentimeters(duration);
	
	Serial.print("Object is at a distance of ");
	Serial.print(centimeters);
	Serial.println(" centimeters.");

	delay(500);
}

// Converts the distance travelled in the given duration of microseconds to cm.
// The speed of sound is 340 m/s or 29 microseconds/cm.
// duration is already in microseconds, so divide by 29.
// Then divide by 2 since to get half the distance travelled (distance between sensor to object).
long microsecondsToCentimeters(long duration) {
	return duration / 29 / 2;
}