'''
Server that controls LEDs and sends LED state to client
To exit server, use CTRL + C
SW1/Red LED blinks once per second, SW2/Green LED blinks twice per second
Releasing the button will turn off the LED immediately
'''

import RPi.GPIO as gpio
import time
import threading
import logging
import os
import socket
import sys
import _thread

########## GPIO Stuff ##########
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

reply = ""

red_led_bool_list = []
red_led_bool_counter = 0
green_led_bool_list = []
green_led_bool_counter = 0
red_loop_bool = True
green_loop_bool = True
red_led_bool = True
green_led_bool = True
red_threads = []
red_threads_counter = 0
green_threads = []
green_threads_counter = 0

logging.basicConfig(level=logging.DEBUG,format='%(thread)d (%(threadName)-12s) %(message)s',)

# function to turn on LED if button is pressed
def set_led(led, t, sw):
    input_state = gpio.input(sw)
    if led == GREEN_LED:
        green_led_bool = True
        logging.debug("starting green led " + globals()["green_threads"][globals()["green_threads_counter"]].getName())
        while(green_led_bool):
            if (gpio.input(sw) == gpio.LOW):
                logging.debug("pressing " + str(led))
                gpio.output(led, True)
                time.sleep(t)
                gpio.output(led, False)
                time.sleep(t)
        logging.debug("exit green loop")
    if led == RED_LED:
        red_led_bool = True
        logging.debug("starting red led " + globals()["red_threads"][globals()["red_threads_counter"]].getName())
        while(red_led_bool):
            if (gpio.input(sw) == gpio.LOW):
                logging.debug("pressing " + str(led))
                gpio.output(led, True)
                time.sleep(t)
                gpio.output(led, False)
                time.sleep(t)
        logging.debug("exit red loop")

# function to turn off LED once button is released
def red_led_off(channel):
    logging.debug("turning off " + globals()["red_threads"][globals()["red_threads_counter"]].getName())
    gpio.output(RED_LED, False)
    gpio.cleanup(RED_LED)
    gpio.setup(RED_LED, gpio.OUT, initial=gpio.LOW)
    globals()["red_threads_counter"] += 1
    new_red_thread = threading.Thread(target=set_led, args=(RED_LED, 1, SW1))
    new_red_thread.setDaemon = True
    globals()["red_threads"].append(new_red_thread)
    globals()["red_threads"][globals()["red_threads_counter"]].start()
    
def green_led_off(channel):
    logging.debug("turning off " + globals()["green_threads"][globals()["green_threads_counter"]].getName())
    gpio.output(GREEN_LED, False)
    gpio.cleanup(GREEN_LED)
    gpio.setup(GREEN_LED, gpio.OUT, initial=gpio.LOW)
    globals()["green_threads_counter"] += 1
    new_green_thread = threading.Thread(target=set_led, args=(GREEN_LED, 0.5, SW2))
    new_green_thread.setDaemon = True
    globals()["green_threads"].append(new_green_thread)
    globals()["green_threads"][globals()["green_threads_counter"]].start()       
        
# function to set GPIO pins to safe, close threads, and turn off pi
def turn_off_pi(channel):
    i = 0
    while (gpio.input(SW3) == gpio.LOW):
        if i == 3:
            print("button pressed for 3 seconds - shutting down")
            globals()["reply"] = "SW3 pressed, server shutting down.."
            try:
                conn.sendall(globals()["reply"].encode())
            except (BrokenPipeError, NameError):
                logging.debug("Closing connection...")
                pass
            
            search_clients = False
            client_connect = False
            gpio.cleanup()
            try:
                conn.close()
            except NameError:
                pass
            s.close()
            os.system("sudo shutdown -h now")
        else:
            time.sleep(1)
            i += 1
            print("button pressed for " + str(i) + " seconds")
            
#Function for handling connections. This will be used to create threads
def clientthread(conn):
    #Sending message to connected client
    conn.send("Welcome to LEDServer".encode()) 
    
    client_connect = True
    #infinite loop so that function do not terminate and thread do not end.
    while client_connect:
         
        #Receiving from client
        #data = conn.recv(1024)
        #print(data)
        try:
            if (gpio.input(SW1) == gpio.LOW):
                logging.debug("SW1 Pressed")
                SW1_STATUS = "Pressed"
            else:
                SW1_STATUS = "Released"
                
            if (gpio.input(SW2) == gpio.LOW):
                logging.debug("SW2 Pressed")
                SW2_STATUS = "Pressed"
            else:
                SW2_STATUS = "Released"    
            
            globals()["reply"] = "{{SW1: {0}, SW2: {1}}}".format(SW1_STATUS, SW2_STATUS)
            print(reply)
            
            try:
                conn.sendall(reply.encode())
            except BrokenPipeError:
                print("Closing connection with " + addr[0] + ':' + str(addr[1]))
                break
            
            time.sleep(0.5)
        except KeyboardInterrupt:
            logging.debug("Closing connection with " + addr[0] + ':' + str(addr[1]))
            break
     
    #came out of loop
    conn.close()
    logging.debug("closing conn")
    
SW1_ON_THREAD = threading.Thread(target=set_led, args=(RED_LED, 1, SW1))
#SW1_OFF_THREAD = threading.Thread(target=led_off, args=(RED_LED, 2, SW1))
SW2_ON_THREAD = threading.Thread(target=set_led, args=(GREEN_LED, 0.5, SW2))
#SW2_OFF_THREAD = threading.Thread(target=led_off, args=(GREEN_LED, 1, SW2))
gpio.add_event_detect(SW1, gpio.RISING, callback=red_led_off, bouncetime=100)
gpio.add_event_detect(SW2, gpio.RISING, callback=green_led_off, bouncetime=100)

# set on/off functions to daemon so in the even the pi is shut off in the middle of an LED blink
SW1_ON_THREAD.setDaemon(True)
#SW1_OFF_THREAD.setDaemon(True)
SW2_ON_THREAD.setDaemon(True)
#SW2_OFF_THREAD.setDaemon(True)

globals()["red_threads"].append(SW1_ON_THREAD)
globals()["green_threads"].append(SW2_ON_THREAD)

globals()["red_threads"][globals()["red_threads_counter"]].start()
globals()["green_threads"][globals()["green_threads_counter"]].start()

#SW1_ON_THREAD.start()
#SW1_OFF_THREAD.start()
#SW2_ON_THREAD.start()
#SW2_OFF_THREAD.start()

SW3_EVENT = gpio.add_event_detect(SW3, gpio.BOTH, callback=turn_off_pi, bouncetime=100)

########## Server Stuff ##########
PORT = 8888 # Arbitrary non-privileged port
 
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
print('Socket created')
 
#Bind socket to local host and port
try:
    s1 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s1.connect(("8.8.8.8", 80))
    ip_address = s1.getsockname()[0]
    print("Retrieving IPv4 Address...")
    s1.close()
    s.bind((ip_address, PORT))
    print("Host IP: " + ip_address + ", " + "Port: " + str(PORT))
    #s.bind(("192.168.1.229", PORT))
except (socket.error, OSError) as msg:
    print('Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1])
    sys.exit()
     
print('Socket bind complete')
 
#Start listening on socket
s.listen(10)
print('Socket now listening')

search_clients = True
#now keep talking with the client
while search_clients:
    try:
        #wait to accept a connection - blocking call
        conn, addr = s.accept()
        print ('Connected with ' + addr[0] + ':' + str(addr[1]))
         
        #start new thread takes 1st argument as a function name to be run, second is the tuple of arguments to the function.
    #    start_new_thread(clientthread ,(conn,))
        _thread.start_new_thread(clientthread, (conn,))
    except KeyboardInterrupt:
        print("Closing LEDServer...")
        s.close()
        gpio.cleanup()
        sys.exit()