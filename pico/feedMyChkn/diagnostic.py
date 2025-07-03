import time

from machine import Pin

led = Pin("LED", Pin.OUT)

def led_on():
    led.value(1)

def led_off():
    led.value(0)

def toggle_status_led():
    led.toggle()

def blink_status_led(duration=1):
    for i in range(duration):
        led.value(i % 2)
        time.sleep(1)
