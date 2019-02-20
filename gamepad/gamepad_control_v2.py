#!/usr/bin/python3

# a crude remote control

# originally from here: http://oarkit.intelligentrobots.org/home/raspberry-pi/gamepad-controls/

import catapult
cat=catapult.Catapult()

# the robot's Hardware Abstraction Layer (HAL)
import kegbot_HAL as HAL

# support for USB gamepad
from evdev import InputDevice, categorize, ecodes, KeyEvent

# for delays
import time

# immediately stop motion when starting
print ("Stopping motors")
HAL.stop()


# tell the user what to do
print ("use left hat to move forward/backward")
print ("use right hat to steer left, right")



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


# control mappings, mapping event codes to inputs
ctl_map={304:'Y_BUTTON', 306: 'A_BUTTON', 16:'LEFT_HAT_X', 17:'LEFT_HAT_Y'}

for event in gamepad.read_loop():

         
    # ***
    #print (event.code)
    print ("Categorized:",categorize(event))
 
    # process the event if its been mapped
    if event.code in ctl_map.keys():
     mapped_event=ctl_map[event.code]

     print ("Mapped event=%s, value=%s"%(mapped_event,event.value))

     if (mapped_event in ['Y_BUTTON', 'A_BUTTON']):
       # fire catapult on button press only (not release)
       if event.value==1:
        cat.fire()

        # wait a bit (0.1 seconds)  between fire commands, otherwise can fill up the que
        time.sleep(0.1)


     # process joystick events (absolute position)
     #if event.type==ecodes.EV_ABS:
     if event.type==ecodes.EV_REL:  
      print ("absolute event:",event)
