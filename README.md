Are you worried your boss will catch you watching YouTube during work hours? If so, here's a setup for you!

This program will return you to your desktop when a distance sensor is triggered. This way, to a third party, it would appear that you were just passionately inspecting your wallpaper.

<br>

# Using the program
<i>This program has two parts: the code running on the Arduino and the code running on your PC.</i>


### <b>Arduino</b>

* Requires an Arduino UNO or an equivalent microcontroller and a HC-SR04 sensor. Connect like below. 

* Using the [Arduino IDE](https://www.arduino.cc/en/software) or the [PlatformIO IDE](https://platformio.org/platformio-ide) VSCode extension, open the `/src/distanceReporter.cpp` file and upload it to the board.  Position the board by your door.

![Contraption anatomy](https://raw.githubusercontent.com/mateimarica/public/master/anti-infiltrator/anti_infiltrator_1.png)

![](https://raw.githubusercontent.com/mateimarica/public/master/anti-infiltrator/anti_infiltrator_2.png)


### <b>Python</b>

* Must have [Python](https://www.python.org/downloads) installed.

* Requires the [pyserial](https://pythonhosted.org/pyserial) and the [pynput](https://pynput.readthedocs.io) libraries.<br>
Run `python -m pip install -r requirements.txt` to install them.

* Open the `receiver.py` file or run `python /src/receiver.py` to run the receiver program. 
