#!/usr/bin/python3

import paho.mqtt.client as mqtt
#import catapult
#import roboclaw
import datetime
import json

PORT="/dev/serial/by-id/usb-Silicon_Labs_CP2102_USB_to_UART_Bridge_Controller_0001-if00-port0"
#robot = roboclaw.Controller(PORT)
#robot.M1Forward(speed)

SPEED_RIGHT = 0
SPEED_LEFT = 0

LAST_COMMAND_TIME = datetime.datetime.now()

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe([("hackbot/drive", 0), ("hackbot/fire", 0)])

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):

    global SPEED_RIGHT, SPEED_LEFT, LAST_COMMAND_TIME

    if msg.topic == "hackbot/fire":

        print("FIRE")
        #c.fire()
        client.publish("hackbot/done", 'fire')

    elif msg.topic == "hackbot/drive":

        LAST_COMMAND_TIME = datetime.datetime.now()
        decodedData = json.loads(str(msg.payload))

        SPEED_RIGHT = decodedData['right']
        SPEED_LEFT = decodedData['left']

#c=catapult.Catapult()

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

#client.connect("192.168.1.158", 1883, 60)
client.connect("iot.eclipse.org", 1883, 60)
#client.connect("kegbot.local", 1883, 60)

client.loop_start()

run = True
while run:

    # print()
    print("motor speeds: " + str(SPEED_RIGHT) + " " + str(SPEED_LEFT))

    # TODO: if wheels are moving and the timestamp of last command is greater than X seconds, start to decrease speed
    cur_time = datetime.datetime.now()

    if (LAST_COMMAND_TIME):
        diff = cur_time - LAST_COMMAND_TIME

        # after .5 seconds, cut the speed in half
        if ((SPEED_RIGHT != 0 or SPEED_LEFT != 0) and diff.microseconds > 500000):

            SPEED_RIGHT = 0 if abs(SPEED_RIGHT) < 1 else SPEED_RIGHT/2
            SPEED_LEFT = 0 if abs(SPEED_LEFT) < 1 else SPEED_LEFT/2
            LAST_COMMAND_TIME = datetime.datetime.now()

    # TODO: send speeds to the motors -- please be careful when testing this!!!!!!
    # robot.M1Forward(SPEED_LEFT)
    # robot.M2Forward(SPEED_RIGHT)
