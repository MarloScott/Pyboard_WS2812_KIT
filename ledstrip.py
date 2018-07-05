# Written by Marlo Scott
# Class to represent an LED strip
import pyb
import ws2812
import math

class LedStrip:

    """
    Class to represent a strip of LEDs and provide basic manipulation methods.

    Attributes:
        led_number:     Number of total LEDs
        led_list:       list of each LEDs color value
        led_n_color:    Used for calculating new color values
        led_color:      Stores current color value for all LEDs
        led_pos:        Used for tracking a single LED position
        led_driver:     Instance of the ws2812 Driver
        led_intensity:  Sets main LEDs intensity (value between 0-1)
        led_direction:  Direction of movement. 1 for right, -1 for left and 0 for not moving
    """

    def __init__(self, led_number=1, init_color=(0xff,0xff,0xff), spi_bus=1, intensity=1):
        self.led_number = led_number
        self.led_color  = init_color
        self.led_list   = [(self.led_color, intensity) for i in range(led_number)]
        self.led_driver = ws2812.ws2812(spi_bus=spi_bus, led_count=led_number, intensity=1)
        self.led_pos    = 0
        self.led_intensity = intensity
        self.led_n_color    = 107
        self.update()


    def update(self):
        stripped_led_list = [self.led_list[x][0] for x in range(self.led_number)]
        self.led_driver.show(stripped_led_list)


    def init_kit_scroll(self):
        fade_amount = self.led_intensity / (self.led_number*0.6)    # This will make 60% of LEDs be on for the effect
        for x in range(self.led_number):
            self.set_led_intensity(x, self.led_color, self.led_intensity - fade_amount*x)
        self.led_pos = 0
        self.update()


    def init_single_led(self):
        self.led_list = [((0,0,0),0) for i in range(self.led_number)]
        self.set_led_intensity(0, self.led_color, self.led_intensity)
        self.led_pos = 0
        self.update()


    def shift_right(self):
        if(self.led_pos<self.led_number-1):
            self.led_list = [self.led_list[i-1]
                            for i in range(self.led_number)]
            self.led_pos += 1
            self.update()


    def shift_left(self):
        if(self.led_pos>0):
            self.led_list =[self.led_list[(i-self.led_number)+1]
                           for i in range(self.led_number)]
            self.led_pos -= 1
            self.update()




    def swap(self, led1, led2):
        temp = self.led_list[led1]
        self.led_list[led1] = self.led_list[led2]
        self.led_list[led2] = temp


    def shift_right_swap(self):
        count = self.led_pos
        while count >= 0:
            self.swap(count, count+1)
            count-=1
        self.led_pos += 1
        self.update()


    def shift_left_swap(self):
        count = self.led_pos
        while count <= self.led_number-1:
            self.swap(count, count-1)
            count+=1
        self.led_pos -= 1
        self.update()


    def scroll_right(self, delay):
        for x in range(self.led_number-1):
             #self.shift_right_swap()
             self.move_right()
             pyb.delay(delay)

    def scroll_left(self, delay):
        for x in range(self.led_number-1):
             #self.shift_left_swap()
             self.move_left()
             pyb.delay(delay)

    def move_left(self):
        if(self.led_pos>0):
            self.fade_all_led()
            self.led_pos -= 1
            self.set_led_intensity(self.led_pos, self.led_color, self.led_intensity)
            self.update()

    def move_right(self):
        if(self.led_pos<self.led_number-1):
            self.fade_all_led()
            self.led_pos += 1
            self.set_led_intensity(self.led_pos, self.led_color, self.led_intensity)
            self.update()

    def set_led_intensity(self, led, color, intensity):
        if(intensity < 0 or intensity > 1):
            self.led_list[led] = ((0,0,0),0)
        else:
            r = (int)(color[0]*intensity)
            g = (int)(color[1]*intensity)
            b = (int)(color[2]*intensity)
            self.led_list[led] = ((r,g,b),intensity)
        self.update()

    def fade_all_led(self):
        fade_amount = 0.7
        for x in range(self.led_number):
            self.set_led_intensity(x, self.led_color, self.led_list[x][1]*fade_amount)


    def change_color(self):
        r = int((1 + math.sin(self.led_n_color * 0.1324)) * 127)
        g = int((1 + math.sin(self.led_n_color * 0.1654)) * 127)
        b = int((1 + math.sin(self.led_n_color * 0.1)) * 127)
        self.led_color = (r,g,b)
        for x in range(self.led_number):
            self.set_led_intensity(x, self.led_color, self.led_list[x][1])
        self.led_n_color += 1
        self.update()
