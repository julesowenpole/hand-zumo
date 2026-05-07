# hand-zumo
This project allows you to control a Pololu Zumo robot using hand gestures, tracked via webcam. A fist stops the robot, an open hand drives it forward, and tilting your wrist left or right steers.

This was built using [libmapper](https://github.com/libmapper/libmapper), [mp-hands-libmapper](https://github.com/peacheym/mp-hands-libmapper), and [Webmapper](https://github.com/libmapper/webmapper).

I built this project during winter semester of 2025/26, alongside my second year courseload. Although it does not extend my work in any particular class, I had fun applying libmapper and Webmapper in a different field. 

## Hardware
- Arduino Uno
- Pololu Zumo Shield
- Mac with webcam
- USB cable (Arduino to Mac)

## Software dependencies
Install the following before running:
pip install libmapper
pip install pyserial
pip install mappersession

## How to run
1. Upload Arduino sketch to Uno (zumo_ctrl/zumo_ctrl.ino)
2. Find your serial port by running ls /dev/tty.usb* in terminal. Copy the port name and paste it into zumo_ctrl.py where it says SERIAL_PORT
3. Follow instructions in mp-hands-libmapper to start hand tracking.
4. Start Webmapper.
5. Run the python bridge (zumo_ctrl.py)
6. Create the mappings in Webmapper
7. Control the robot!

## Tuning
OPEN_THRESHOLD can be adjusted if gesture detection feels off. 

## Future Ideas
- Wireless control via bluetooth or WiFi
- Additional gestures
- Save Webmapper session so mappings don't need to be recreated each time

## Acknowledgements
- Matthew Peachey, Dr Joe Malloch, and the rest of the team at the GEM lab at Dalhousie University in Halifax, Nova Scotia for libmapper, mp-hands-libmapper and Webmapper.