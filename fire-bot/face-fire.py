#!/usr/bin/python3

import paho.mqtt.client as mqtt
import catapult
import roboclaw
import time

PORT="/dev/serial/by-id/usb-Silicon_Labs_CP2102_USB_to_UART_Bridge_Controller_0001-if00-port0"
robot = roboclaw.Controller(PORT)
#robot.M1Forward(speed)

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe([("hackbot/forward", 0), ("hackbot/backward", 0), ("hackbot/fire", 0), ("hackbot/left", 0), ("hackbot/right", 0)])

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    if msg.topic == "hackbot/forward":
        print("Forward")
        robot.M1Backward(20)
        robot.M2Backward(20)
        time.sleep(1)
        robot.M1Forward(0)
        robot.M2Forward(0)
        client.publish("hackbot/done", 'forward')
    elif msg.topic == "hackbot/backward":
        print("Backward")
        robot.M1Forward(20)
        robot.M2Forward(20)
        time.sleep(1)
        robot.M1Forward(0)
        robot.M2Forward(0)
        client.publish("hackbot/done", 'backward')
    elif msg.topic == "hackbot/left":
        print("left")
        robot.M1Forward(20)
        robot.M2Backward(20)
        time.sleep(1)
        robot.M1Forward(0)
        robot.M2Forward(0)
        client.publish("hackbot/done", 'left')
    elif msg.topic == "hackbot/right":
        print("right")
        robot.M1Backward(20)
        robot.M2Forward(20)
        time.sleep(1)
        robot.M1Forward(0)
        robot.M2Forward(0)
        client.publish("hackbot/done", 'right')
    elif msg.topic == "hackbot/fire":
        print("FIRE")
        c.fire()
        client.publish("hackbot/done", 'fire')

    #print(msg.topic+" "+str(msg.payload))
    #c.fire()

c=catapult.Catapult()

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

#client.connect("192.168.1.158", 1883, 60)
#client.connect("iot.eclipse.org", 1883, 60)
client.connect("kegbot.local", 1883, 60)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_forever()
