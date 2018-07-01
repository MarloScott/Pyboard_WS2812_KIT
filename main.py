# Written by Marlo Scott
# K.I.T
# Compatible with Pyboard and WS2812 RGB LED
# WS2812 Datasheet: https://cdn-shop.adafruit.com/datasheets/WS2812.pdf

from pyb import Pin, Timer, Switch, SPI
import ws2812
import math

brightness_mask = 0x0F

r = 0xFF
g = 0
b = 0

color = 0

number_of_LEDS = 8

fade_bit_shift = 1

# This list keeps track of all the LED values
led_list = [(r,g,b) for x in range(number_of_LEDS)]

chain = ws2812.ws2812(spi_bus=1, led_count=number_of_LEDS)

chain.show(led_list)

# Initailise LEDs for scrolling side to side like KIT
def init_kit_scroll():
    global led_list
    led_list = [(r>>(fade_bit_shift*x),g>>(fade_bit_shift*x),b>>(fade_bit_shift*x)) for x in range(int(number_of_LEDS))]
    chain.show(led_list)

def init_moveable_LED():
    global led_list
    led_list = [(r>>(6*x),g>>(6*x),b>>(6*x)) for x in range(int(number_of_LEDS))]
    chain.show(led_list)

#[0,1,2,3,4] -> [4,0,1,2,3]
# Simple shift to the right with loop around
def shift_right():
    global led_list
    led_list =[led_list[i-1] for i in range(int(number_of_LEDS))]
    chain.show(led_list)

#[0,1,2,3,4] -> [1,2,3,4,0]
# Simple shift to the left with loop around
def shift_left():
    global led_list
    led_list =[led_list[(i-number_of_LEDS)+1] for i in range(int(number_of_LEDS))]
    chain.show(led_list)

#Swap two LEDs with each other
def swap(led1, led2):
    global led_list
    temp = led_list[led1]
    led_list[led1] = led_list[led2]
    led_list[led2] = temp


# Shifts all LEDs by looping them back on themselfs
def shift_right_swap(led):
    while led >= 0:
        swap(led, led+1)
        led-=1
    chain.show(led_list)

def shift_left_swap(led):
    while led <= number_of_LEDS-1:
        swap(led, led-1)
        led+=1
    chain.show(led_list)

# Performs complete scroll from one side to the other using the
# shift_<direction>_swap() method.
def scroll_right(delay):
    for x in range(number_of_LEDS-1):
         shift_right_swap(x)
         pyb.delay(delay)

def scroll_left(delay):
    for x in range(number_of_LEDS-1):
         shift_left_swap((number_of_LEDS-1)-x)
         pyb.delay(delay)

def change_color():
    global color, r, g, b
    r = int((1 + math.sin(color * 0.1324)) * 127)
    g = int((1 + math.sin(color * 0.1654)) * 127)
    b = int((1 + math.sin(color * 0.1)) * 127)
    for x in range(number_of_LEDS):
        led_list[x] = (r,g,b)
    color += 1
    chain.show(led_list)


delay = 50
accel = pyb.Accel()
movement_threshold = 10

def test():
    init_kit_scroll()
    count = 0

    while True:
        z = accel.z()
        x = accel.x()
        y = accel.y()

        # This handles moveable LED mode
        if abs(z) > movement_threshold:
            init_moveable_LED()
            count = 0
            led_pos = 0
            while (count < 100):
                if(z > 0):
                    if(led_pos > number_of_LEDS):
                        shift_left()
                        led_pos += 1
                        pyb.delay(delay)
                else:
                    if(led_pos < number_of_LEDS):
                        shift_right()
                        led_pos -= 1
                        pyb.delay(delay)
                z = accel.z()
                count = count+1 if abs(z) < 5 else count

        # This handles changing colors
        if abs(y) > 20:
            change_color()
            pyb.delay(50)

        # This handles scrolling along LEDs
        if abs(x) > 20:
            count+=1
            if(count>=20):
                count = 0
                init_kit_scroll()
                while (abs(x) > movement_threshold):
                    scroll_right(40)
                    scroll_left(40)
                    x = accel.x()
            pyb.delay(100)
