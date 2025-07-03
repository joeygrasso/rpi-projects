###
# l298n.py
# A simple demo/poc for the L298N Stepper Motor Drive Controller
###

from machine import Pin
import time #importing time for delay

# RPI LED Status blink
led_pin = Pin("LED", Pin.OUT)

# Defining motor pins
# OUT1 & OUT2
In1=Pin(6,Pin.OUT)
In2=Pin(7,Pin.OUT)
EN_A=Pin(8,Pin.OUT)
EN_A.high()

# Forward
def move_forward():
    In1.high()
    In2.low()

# Backward
def move_backward():
    In1.low()
    In2.high()

# Stop
def stop():
    In1.low()
    In2.low()

while True:

    # toggle on/off LED
    led_pin.toggle()

    move_forward()
    time.sleep(5)
    stop()
    time.sleep(3)
    move_backward()
    time.sleep(5)
    stop()
    time.sleep(3)
