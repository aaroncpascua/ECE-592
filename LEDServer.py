import RPi.GPIO as gpio
import time
import threading
import logging
import os

# set switch pins
SW1 = 8
SW2 = 10
SW3 = 12

# set LED pins
RED_LED = 16
GREEN_LED = 18

# initialize GPIO and switches/LEDs
SWs = [SW1, SW2, SW3]
LEDs = [RED_LED, GREEN_LED]

gpio.setwarnings(False)
gpio.setmode(gpio.BOARD)
gpio.setup(SWs, gpio.IN, pull_up_down=gpio.PUD_UP)
gpio.setup(LEDs, gpio.OUT, initial=gpio.LOW)

logging.basicConfig(level=logging.DEBUG, format='%(thread)d (%(threadName)-12s) %(message)s',)

program_state = True

# function to turn on LED if button is pressed
def set_led(led, t, sw):
    logging.debug("Starting set_led " + str(led))
    input_state = gpio.input(sw)
    while(True):
        if (gpio.input(sw) == gpio.LOW):
            gpio.output(led, True)
            time.sleep(t)
            gpio.output(led, False)
            time.sleep(t)

# function to turn off LED once button is released
def led_off(led, t, sw):
    logging.debug("Starting led_off " + str(led))
    while(True):
        if (gpio.input(sw) == gpio.HIGH):
            gpio.output(led, False)


# function to set GPIO pins to safe, close threads, and turn off pi
def turn_off_pi(channel):
    i = 0
    while (gpio.input(SW3) == gpio.LOW):
        time.sleep(1)
        i += 1
        if i == 3:
            print("button pressed for 3 seconds - shutting down")
            SW1_ON_THREAD.join()
            SW1_OFF_THREAD.join()
            SW2_ON_THREAD.join()
            SW2_OFF_THREAD.join()
            gpio.cleanup()
            os.system("sudo shutdown -h now")
        else:
            print("button pressed for " + str(i) + " seconds")
    return

SW1_ON_THREAD = threading.Thread(name="red LED on", target=set_led, args=(RED_LED, 1, SW1))
SW1_OFF_THREAD = threading.Thread(name="red LED off", target=led_off, args=(RED_LED, 2, SW1))
SW2_ON_THREAD = threading.Thread(name="green LED on", target=set_led, args=(GREEN_LED, 0.5, SW2))
SW2_OFF_THREAD = threading.Thread(name="green LED off", target=led_off, args=(GREEN_LED, 1, SW2))

# set on/off functions to daemon so in the even the pi is shut off in the middle of an LED blink
SW1_ON_THREAD.setDaemon(True)
SW1_OFF_THREAD.setDaemon(True)
SW2_ON_THREAD.setDaemon(True)
SW2_OFF_THREAD.setDaemon(True)

SW1_ON_THREAD.start()
SW1_OFF_THREAD.start()
SW2_ON_THREAD.start()
SW2_OFF_THREAD.start()

SW3_EVENT = gpio.add_event_detect(SW3, gpio.BOTH, callback=turn_off_pi, bouncetime=100)