# module to support Kegbot motion

import roboclaw
import time
PORT="/dev/serial/by-id/usb-Silicon_Labs_CP2102_USB_to_UART_Bridge_Controller_0001-if00-port0"
robot = roboclaw.Controller(PORT)


# motion constats
FORWARD=1
REVERSE=-1
STOP=3



def left(speed):
 # change speed of left motor
 # robo.M1Backward(val)
 # robo.M1Forward(val)
 # robo.M2Backward(val)
 # robo.M2Forward(val)

 # scale speed
 speed=int(speed/2)

 # change speed of right motor
 if speed>0:
  robot.M1Forward(speed)
 else:
  robot.M1Backward(-1*speed)




def right(speed):
 # change speed of right motor
 
 # scale speed
 speed=int(speed/2)

 if speed>0: 
  robot.M2Forward(speed)
 else:
  robot.M2Backward(-1*speed)


def stop():
  # stop everything
  left(0)
  right(0)

