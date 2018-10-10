#!/usr/bin/python3
  
print ("stopping!")

#**** USER SETTINGS ****
#PORT="/dev/ttyUSB0"
PORT="/dev/serial/by-id/usb-Silicon_Labs_CP2102_USB_to_UART_Bridge_Controller_0001-if00-port0"

#**** USER SETTINGS ****


import roboclaw

import time

robo = roboclaw.Controller(PORT)


robo.SetM1Speed(0)
robo.SetM2Speed(0)
