from machine import Pin
import time 

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

# Function to run the feeder for a specified duration
def run_feeder(duration=10):
    print("Feeder is running for", duration, "seconds")
    move_forward()
    time.sleep(duration)
    stop()
    print("Feeder stopped.")
