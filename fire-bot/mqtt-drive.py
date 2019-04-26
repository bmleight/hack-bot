#!/usr/bin/python3

import paho.mqtt.client as mqtt
import roboclaw
import datetime
import json

PORT="/dev/serial/by-id/usb-Silicon_Labs_CP2102_USB_to_UART_Bridge_Controller_0001-if00-port0"
robot = roboclaw.Controller(PORT)

SPEED_RIGHT = 0
SPEED_LEFT = 0
SPEED_RIGHT_LAST = 0
SPEED_LEFT_LAST = 0

LAST_COMMAND_TIME = LAST_STATUS_SENT_TIME = datetime.datetime.now()

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe([("hackbot/drive", 0)])

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    
    global SPEED_RIGHT, SPEED_LEFT, LAST_COMMAND_TIME
    
    #print('on message ' + msg.topic);
    if msg.topic == "hackbot/drive":

        LAST_COMMAND_TIME = datetime.datetime.now()

        try:
            decodedData = json.loads(str(msg.payload)[2:-1])
        except ValueError as e:
            print("error?!?! ")
            print(e)

        SPEED_RIGHT = int(decodedData['right'])
        SPEED_LEFT = int(decodedData['left'])

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("192.168.2.128", 1883, 60)
#client.connect("iot.eclipse.org", 1883, 60)
#client.connect("kegbot.local", 1883, 60)

client.loop_start()

run = True
while run:

    #print("motor speeds: " + str(SPEED_RIGHT) + " " + str(SPEED_LEFT))

    # TODO: if wheels are moving and the timestamp of last command is greater than X seconds, start to decrease speed
    cur_time = datetime.datetime.now()

    #if (LAST_COMMAND_TIME):
    #    diff = cur_time - LAST_COMMAND_TIME

         # after .5 seconds, cut the speed in half
    #    if ((SPEED_RIGHT != 0 or SPEED_LEFT != 0) and diff.microseconds > 500000):

    #        SPEED_RIGHT = 0 if abs(SPEED_RIGHT) < 1 else int(SPEED_RIGHT/2)
    #        SPEED_LEFT = 0 if abs(SPEED_LEFT) < 1 else int(SPEED_LEFT/2)
    #        LAST_COMMAND_TIME = datetime.datetime.now()

    statusDiff = cur_time - LAST_STATUS_SENT_TIME

    if (statusDiff.seconds > 10):
        client.publish("hackbot/status", json.dumps({"battery": robot.readmainbattery()}, sort_keys=True));
        LAST_STATUS_SENT_TIME = datetime.datetime.now()


    if (SPEED_LEFT_LAST != SPEED_LEFT):
        SPEED_LEFT_LAST = SPEED_LEFT
        if (SPEED_LEFT >= 0):
            robot.M1Forward(int(SPEED_LEFT))
        else:
            robot.M1Backward(int(SPEED_LEFT*-1))

    if (SPEED_RIGHT_LAST != SPEED_RIGHT):
        SPEED_RIGHT_LAST = SPEED_RIGHT
        if (SPEED_RIGHT >= 0):
            robot.M2Forward(int(SPEED_RIGHT))
        else:
            robot.M2Backward(int(SPEED_RIGHT*-1))
