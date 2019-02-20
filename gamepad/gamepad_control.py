#!/usr/bin/python3

# a crude remote control

# originally from here: http://oarkit.intelligentrobots.org/home/raspberry-pi/gamepad-controls/

import catapult
cat=catapult.Catapult()

# the robot's Hardware Abstraction Layer (HAL)
import kegbot_HAL as HAL

# support for USB gamepad
from evdev import InputDevice, categorize, ecodes, KeyEvent

# cbond sound setup
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BOARD)
GPIO.setup(40, GPIO.OUT)

p = GPIO.PWM(40, 340)  # channel=40 frequency=340Hz
p.start(0)
soundLoopCounter=0

# immediately stop motion when starting
print ("Stopping motors")
HAL.stop()


# tell the user what to do
print ("use left hat to move forward/backward")
print ("use right hat to steer left, right")

def move(a,b,c):
  # move
  print ("moving: a=%s, b=%s, c=%s"%(a,b,c))


def drive_train(direction, magnitude):
  global soundLoopCounter
  # adjust the speed of the RC drive train

  # the scaling factor for moving forward/backward
  MAX_DISTANCE=32768.0

  # uncomment to debug
  #print ("in drive_train, direction=%s and magnitude=%s"%(direction,magnitude))
  
  # if the magnitude was small, stop motion
  if abs(magnitude)<100:
    print ("stopping drive train")
    HAL.stop()
    p.ChangeDutyCycle(0)
    soundLoopCounter = 0
    return

  if (direction=="fwd"):
   new_direction=-1
   p.ChangeDutyCycle(0)
   soundLoopCounter = 0 
  elif (direction=="back"):
   new_direction=+1
   print('hi')
   if (soundLoopCounter % 300 == 0):
    p.ChangeDutyCycle(100)
   elif (soundLoopCounter % 300 == 150):
    p.ChangeDutyCycle(0)
   soundLoopCounter += 1
  else:
   soundLoopCounter = 0
   p.ChangeDutyCycle(0)
  
  #calculate relative speed
  speed_percent=int(100.0*(magnitude/MAX_DISTANCE))
  print ("speed=%s"%(speed_percent))

  # update the drive train
  HAL.left(new_direction*speed_percent)
  HAL.right(new_direction*speed_percent)





def steer(direction):
   # steer the front wheels

  # the scaling factor for moving forward/backward
  MAX_DISTANCE=32768.0

  # speed for turning
  TURN_SPEED=80

  # scaled direction
  scaled_steering=int(100.0*(direction/MAX_DISTANCE))

  if abs(scaled_steering)<10:
    # top motion if centered
    HAL.stop()
    #HAL.steering(HAL.CENTER)
    return

  if (scaled_steering<0):
    #HAL.steering(HAL.LEFT)
    # steer left by applying more speed to one motor
    HAL.left(TURN_SPEED)
    HAL.right(-TURN_SPEED)
  else:
    #HAL.steering(HAL.RIGHT)
    HAL.left(-TURN_SPEED)
    HAL.right(TURN_SPEED)

  #***
  print ("in steering,scaled_direction=%s"%(scaled_steering)) 





def find_controller():

    event0 = InputDevice('/dev/input/event0')
    #***
    gamepad=event0
    return gamepad
   
    event1 = InputDevice('/dev/input/event1')
    event2 = InputDevice('/dev/input/event2')
    event3 = InputDevice('/dev/input/event3')
    controller_list = ["Logitech Gamepad F710", "Logitech Gamepad F310"]

    for controller in controller_list:

        if event0.name == controller:

            gamepad = event0

        elif event1.name == controller:

            gamepad = event1

        elif event2.name == controller:

            gamepad = event2

        elif event3.name == controller:

            gamepad = event3

        else:

            print("controller not found")

    return gamepad

gamepad = find_controller()




for event in gamepad.read_loop():

    x = event.code
    val =event.value
      
    #print(event)

    if x == 2:

        print('left wheels fw')

    elif x == 304:
        if val==1:
          print ("fire..")
          cat.fire()

 
    elif x == 5:

        print('right wheels fw')

    elif x == 310:

        print('left wheels back')

    elif x == 311:

        print('right wheels back')

    elif x == 3:

        y = event.value

        if y > 0:
            print('pan right [y=%s]'%(y))
            steer(y)
        else:
            print('pan left [y=%s]'%(y))
            steer(y)

    elif x == 0:

        y = event.value

        if y > 0:

            print ('left +', y)
            move(y/40, 'right', False)

        elif y < 0:
            print ('right +', (y*-1))
            move((y*-1)/40, 'left', False)
    
    elif x == 1:
        y = event.value
        if y > 0:
            print ('back', y)
            drive_train('back',y)
        else:
            print ('fwd', (y*-1))
            drive_train('fwd',y*-1)

    elif x == 4:

        y = event.value

        if y > 0:

            print('tilt fwd')

        else:

                  print('tilt back')

    elif x == 314:

        print('quit')

        break

    elif x == 315:

        print('servo reset')


