import RPi.GPIO as gpio
import time
import sys
import threading
from datetime import datetime, timedelta
import logging
from gpiozero import MCP3008
import colorsys
import os
import csv

logging.basicConfig(level=logging.DEBUG,format='%(thread)d (%(threadName)-12s) %(message)s',)

# setting GPIO to BCM
gpio.setmode(gpio.BCM)

# setting GPIO pin numbers
GPIO_BUTTON = 16

GPIO_RGB_RED = 5
GPIO_RGB_GREEN = 6
GPIO_RGB_BLUE = 13
GPIO_RGB = [GPIO_RGB_RED,GPIO_RGB_GREEN,GPIO_RGB_BLUE]

GPIO_LED = 14

GPIO_ECHO = 24
GPIO_TRIGGER = 25

GPIO_BUZZER = 18

# setting GPIO pins for input/output
gpio.setup(GPIO_BUTTON, gpio.IN, pull_up_down = gpio.PUD_UP)

gpio.setup(GPIO_LED, gpio.OUT, initial=gpio.LOW)

gpio.setup(GPIO_ECHO, gpio.IN)
gpio.setup(GPIO_TRIGGER, gpio.OUT, initial=gpio.LOW)

gpio.setup(GPIO_BUZZER, gpio.OUT, initial=gpio.LOW)

gpio.setup(GPIO_RGB, gpio.OUT, initial=gpio.HIGH)

red = gpio.PWM(GPIO_RGB_RED, 100)
green = gpio.PWM(GPIO_RGB_GREEN, 100)
blue = gpio.PWM(GPIO_RGB_BLUE, 100)

red.start(50)
green.start(50)
blue.start(50)

pot = MCP3008(0)

MODE_MS = threading.Event()
MODE_RDM = threading.Event()
MODE_ORD = threading.Event()

# global variables
stop_function = False
time_first = time.time()
time_second = time.time()
time_elapsed = 0.0
first_press = True
MODE_ORD_START = False
WAIT_BOOL = False
ELECTRONICS_ON = True
distance = 0.0
buzzer_stopped = False
frequency = 0.0
beep_active = False
stop_active = False
pot_final = 0.0
rgb_red = 0
rgb_green = 0
rgb_blue = 0
display_str = ""

def wait_user():
    # gives user 2 seconds to release button once ORD starts
    global WAIT_BOOL
    
    time_diff = 0.0
    time_start = time.time()
    
    while time_diff <= 2.0:
        time_end = time.time()
        time_diff = time_end - time_start
        
    WAIT_BOOL = False
    
    return

def button_long_press():
    # handler for long button press
    #logging.debug("starting long press method")
    global MODE_ORD_START
    global WAIT_BOOL
    
    MODE_ORD_START = True
    time_start = time.time()
    time_diff = 0.0
    
    # if ORD has been initiated, exit function
    if WAIT_BOOL:
        MODE_ORD_START = False
        return
    
    # count time for how long user presses button, if >=2, start ORDD
    while (gpio.input(GPIO_BUTTON) == gpio.LOW):
        if time_diff >= 2.0 and not WAIT_BOOL:
            WAIT_BOOL = True
            #logging.debug("button pressed for 2 seconds")
            
            MODE_MS.clear()
            MODE_RDM.clear()
            MODE_ORD.set()
            time.sleep(0.1)
            
            wait_thread = threading.Thread(target=wait_user, daemon=True)
            wait_thread.start()
            
            led_thread = threading.Thread(target=set_led, daemon=True)
            led_thread.start()
            
        else:
            time_end = time.time()
            time_diff = time_end - time_start
            
    MODE_ORD_START = False
    
    return

def calc_time(start, end):
    # calculate the time between button presses
    global first_press
    global time_elapsed
    
    if first_press:
        time_elapsed = start - end
        
    else:
        time_elapsed = end - start
        
    logging.debug(str(time_elapsed) + "\n")
                
    # reset mode states
    MODE_MS.clear()
    MODE_RDM.clear()
    MODE_ORD.clear()
    time.sleep(0.1)
    
    mode_thread = threading.Thread(target=mode_select, daemon=True)
    mode_thread.start()
    
    return

def mode_select():
    # choose mode based on button actions
    global time_elapsed
    
    # if double click button, start RDM
    if time_elapsed < 1.0:
        MODE_MS.clear()
        MODE_RDM.set()
        MODE_ORD.clear()
        
        time.sleep(0.1)
        
        led_thread = threading.Thread(target=set_led, daemon=True)
        led_thread.start()
        
    # otherwise, start MS
    else:
        MODE_MS.set()
        MODE_RDM.clear()
        MODE_ORD.clear()
        time.sleep(0.1)
        led_thread = threading.Thread(target=set_led, daemon=True)
        led_thread.start()
        
    return

def button_detect(channel):
    # handler for button press: both rising and falling
    #logging.debug("starting button detector")
    global first_press
    global time_first
    global time_second
    global MODE_ORD_START
    global WAIT_BOOL

    # start long press sequence if haven't been started
    if not MODE_ORD_START and not WAIT_BOOL:
        press_thread = threading.Thread(target=button_long_press, daemon=True)
        press_thread.start()

    # only look for single/double clicks if a long press is not active
    if not WAIT_BOOL:
        if gpio.input(GPIO_BUTTON):
            if first_press:
                time_first = time.time()
                time_diff = threading.Thread(target=calc_time, args=[time_first, time_second])
                time_diff.start()
                first_press = False
                #print("first press")
            else:
                time_second = time.time()
                time_diff = threading.Thread(target=calc_time, args=[time_first, time_second])
                time_diff.start()
                first_press = True 
                #print("second press")
                
    return

def set_led():
    # set the LED and start mode loops
    #logging.debug("starting led control")
    
    # Monitor System
    if MODE_MS.is_set():        
        while MODE_MS.is_set():
            gpio.output(GPIO_LED, False)
            
    # Record Data and Monitor
    if MODE_RDM.is_set():
        record_thread = threading.Thread(target=record_data)
        record_thread.start()
        
        while MODE_RDM.is_set():
            gpio.output(GPIO_LED, True)
            
    # Only Record Data
    if MODE_ORD.is_set():
        record_thread = threading.Thread(target=record_data)
        record_thread.start()
        
        while MODE_ORD.is_set():
            gpio.output(GPIO_LED, True)
            time.sleep(0.5)
            gpio.output(GPIO_LED, False)
            time.sleep(0.5)
            
    return
            
    #logging.debug("closing " + str(threading.current_thread().getName()))

def ultrasonic():
    #logging.debug("starting ultrasonice sensor")
    global ELECTRONICS_ON
    global distance
    global frequency
    global buzzer_stopped
    global beep_active
    global stop_active
    
    buzzer = gpio.PWM(GPIO_BUZZER, 0.1) # default buzzer to not play anything
    buzzer.start(10)
    
    while ELECTRONICS_ON:
        if not MODE_ORD.is_set():
            if buzzer_stopped:
                buzzer.start(10)
                buzzer_stopped = False
        
        time.sleep(0.1) # sampling rate
        
        distance = get_distance() # get distance in cm
        
        if not MODE_ORD.is_set():
        # convert distance to a linear scale of frequency from 100 Hz to 2 kHz
            distance_range = 20 - 4
            frequency_range = 2000 - 100
            frequency_conv = (((distance - 4) * frequency_range) / distance_range) + 100
            frequency = round(frequency_conv, 2)
        
            # play linear scaling sound
            if distance >= 4 and distance <= 20:
                buzzer.ChangeFrequency(frequency)
                
            # play 1 Hz beep at 2 kHz
            if distance < 4:
                buzzer.stop()
                if not beep_active:
                    beep_active = True
                    beep_thread = threading.Thread(target=beep, daemon=True)
                    beep_thread.start()
                frequency = 2000
                
            # stop buzzer
            if distance > 20:
                buzzer.stop()
                if not stop_active:
                    stop_active = True
                    stop_thread = threading.Thread(target=stop_buzzer, daemon=True)
                    stop_thread.start()
                frequency = 0

        else:
            buzzer.stop()
            buzzer_stopped = True
            frequency = None
        
    return

def get_distance():
    new_reading = False
    counter = 0
    
    gpio.output(GPIO_TRIGGER, True)
    time.sleep(0.00001)
    gpio.output(GPIO_TRIGGER, False)
    
    # get first pulse, if never received exit loop
    while gpio.input(GPIO_ECHO) == 0:
        pass
        counter += 1
        if counter == 5000:
            new_reading = True
            break
    pulse_start = time.time()
        
    if new_reading:
        return False
        
    while gpio.input(GPIO_ECHO) == 1:
        pass
    pulse_end = time.time()
        
    # get pulse duration in uS
    pulse_duration = (pulse_end - pulse_start) * 1000000
    
    # convert pulse to distance in cm
    distance_meas = pulse_duration / 58.0
    distance = round(distance_meas-0.5, 2)
    
    return distance

def beep():
    # beep handler
    global distance
    global buzzer_stopped
    global beep_active
    
    buzzer = gpio.PWM(GPIO_BUZZER, 2000)
    
    while distance < 4:
        buzzer.start(10)
        time.sleep(1)
        buzzer.stop()
    
    buzzer.stop()
    buzzer_stopped = True
    beep_active = False

def stop_buzzer():
    # stop buzzer handler
    global distance
    global buzzer_stopped
    global stop_active

    buzzer = gpio.PWM(GPIO_BUZZER, 2000)
    buzzer.start(100)
    
    # keep buzzer off until distance < 20
    while distance > 20:
        continue
    
    buzzer_stopped = True
    stop_active = False

def potentiometer():
    global ELECTRONICS_ON
    global pot_final
    global rgb_red
    global rgb_green
    global rgb_blue
    
    while ELECTRONICS_ON:
        # get potentiometer value as a percentage
        pot_val_perc = (1 - pot.value) * 100
        pot_final = round(pot_val_perc, 2)
        
        if not MODE_ORD.is_set():
            # convert potentiometer scale to linear scale of the rainbow
            perc_conv = pot_final/100
            init_range = 360 - 0
            new_range = 270 - 0
            new_value = (((perc_conv - 0) * 270) / 360)
            color = colorsys.hsv_to_rgb(new_value,1,1)

            # convert hsv to a PWM-frienldy value
            output_red = color[0]*100
            output_green = color[1]*100
            output_blue = color[2]*100
            
            # convert hsv to rgb values
            rgb_red = round(color[0] * 255)
            rgb_green = round(color[1] * 255)
            rgb_blue = round(color[2] * 255)
        
        else:
            rgb_red = None
            rgb_green = None
            rgb_blue = None
            
            output_red = 0
            output_green = 0
            output_blue = 0
            
        # change rgb led color
        rgb_thread = threading.Thread(target=RGB_LED, args=[output_red,output_green,output_blue], daemon=True)
        rgb_thread.start()
                    
        time.sleep(0.5)

def RGB_LED(R, G, B):
    # rgb led handler
    red.ChangeDutyCycle(R)
    green.ChangeDutyCycle(G)
    blue.ChangeDutyCycle(B)

def record_data():
    global distance
    global frequency
    global pot_final
    global rgb_red
    global rgb_green
    global rgb_blue 
    
    print("Recording data...")
    
    # create file, check if file exists, if file exists, increment name by 1
    n = 0
    check_file_name = True
    file_path = "/home/pi/Documents/data{}.csv".format(n)
    while check_file_name:
        check_file_name = os.path.isfile(file_path)
        if check_file_name:
            n += 1
            file_path = "/home/pi/Documents/data{}.csv".format(n)
    
    headers = ["Timestamp", "Distance (cm)", "Frequency (Hz)", "Potentiometer %", "RGB Value"]
    file = open(file_path, 'w', newline='')
    writer = csv.writer(file, delimiter=',', quotechar='"')
    writer.writerow(headers)
    
    temp_val = distance # first value read
    while MODE_RDM.is_set() or MODE_ORD.is_set():
        time.sleep(0.001) # give small time delay to not take up memory
        
        # if distance changes (most frequently changed variable), add row to data file
        if temp_val != distance:
            timestamp = datetime.utcnow().strftime('%m-%d-%Y %H:%M:%S.%f')[:-3]
            rgb_value = str(rgb_red) + "-" + str(rgb_green) + "-" + str(rgb_blue)
            values = [timestamp, str(distance), str(frequency), str(pot_final), rgb_value]
            writer.writerow(values)
            
        temp_val = distance # store previous data point
        
    file.close()
    print("stopped recording...")

def print_data():
    global ELECTRONICS_ON
    global distance
    global frequency
    global pot_final
    global rgb_red
    global rgb_green
    global rgb_blue
    
    while ELECTRONICS_ON:
        time.sleep(1)
        output_str = "Distance: " + str(distance) + " cm | Frequency:" + str(frequency) + " Hz"
        output_str += " | Percentage turned: " + str(pot_final) + "% | RGB:" + str(rgb_red) + "-" + str(rgb_green) + "-" + str(rgb_blue)
        print(output_str)

if __name__ == '__main__':
    try:
        # set default led status
        MODE_MS.set()
        MODE_RDM.clear()
        MODE_ORD.clear()
        time.sleep(0.1)
        led_thread = threading.Thread(target=set_led, daemon=True)
        led_thread.start() 
        
        #intialize gpio events
        gpio.add_event_detect(GPIO_BUTTON, gpio.BOTH, callback=button_detect, bouncetime=200)
        
        #initialize ultrasonic and buzzer threads
        ultrasonic_thread = threading.Thread(target=ultrasonic)
        ultrasonic_thread.start()
        
        #initialize potentiometer and RGB LED threads
        pot_thread = threading.Thread(target=potentiometer) 
        pot_thread.start()
        
        #intialize print to console handler
        print_thread = threading.Thread(target=print_data, daemon=True)
        print_thread.start()
        
        while True:
            time.sleep(0.001) # small delay to not take up too much memory
            
    except KeyboardInterrupt:
        # close program gracefully
        ELECTRONICS_ON = False
        
        MODE_MS.clear()
        MODE_RDM.clear()
        MODE_ORD.clear()
        
        red.stop()
        green.stop()
        blue.stop()
        
        led_thread.join()
        server_thread.join()
        ultrasonic_thread.join()
        pot_thread.join()
        print_thread.join()

        print("Stopping MonitoringApp.py")
        
        pot.close()
        gpio.cleanup()
        sys.exit()
