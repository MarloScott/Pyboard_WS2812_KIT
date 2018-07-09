# Written by Marlo Scott
# Class to control LED strip

import pyb
import ws2812
import math

class LedStrip:

    """
    Class to controll a strip of RGB ws2812 LEDs.
    Provides basic manipulation methods for creating a pattern
    similar to "KIT" from the tv series night rider.

    Example KIT pattern:

        led_strip = LedStrip(led_number=8, init_color=(0xff,0,0), spi_bus=1, intensity=1)
        while(True):
            led_strip.auto_scroll(50)

    """

    def __init__(self, led_number=1, init_color=(0xff,0xff,0xff), spi_bus=1, intensity=1):
        """
        params:
            led_number: Total number of LEDs
            init_color: Initial color of all LEDs. Format: (R,G,B), each value between 0-255
            spi_bus:    SPI bus that LEDs are connected to (only MOSI pin required)
            intensity:  value between 0-1, with 1 being brightest
        """
        self.led_number = led_number
        self.led_color = init_color
        self.led_list = [(self.led_color, intensity) for i in range(led_number)]
        self.led_driver = ws2812.ws2812(spi_bus=spi_bus, led_count=led_number, intensity=1)
        self.led_pos = 0
        self.led_intensity = intensity
        self.led_n_color = 107  # Used for calculating new color values
        self.led_color_change_enable = 0
        self.update()

    def update(self):
        """
        Updates all LEDs, called automatically.
        """
        stripped_led_list = [self.led_list[x][0] for x in range(self.led_number)]
        self.led_driver.show(stripped_led_list)

    def init_single_led(self):
        """
        Sets the first LED to led_color and turns off
        the rest.
        """
        self.led_list = [((0,0,0),0) for i in range(self.led_number)]
        self.set_led(0, self.led_color, self.led_intensity)
        self.led_pos = 0
        self.update()

    def shift_left(self):
        """
        Shifts the LED at led_pos left by one and then
        resets that LEDs intensity to led_intensity.
        This also fades all other LEDs.
        """
        self.fade_all_led()
        if(self.led_pos>0):
            self.led_pos -= 1
            self.set_led(self.led_pos, self.led_color, self.led_intensity)
            self.update()

    def shift_right(self):
        self.fade_all_led()
        if(self.led_pos<self.led_number-1):
            self.led_pos += 1
            self.set_led(self.led_pos, self.led_color, self.led_intensity)
            self.update()

    def scroll_right(self, delay):
        """
        Shifts the left most LED right untill
        it reaches the end.
        Also updates color if flag is set.
        Delay specifies how long to wait between each shift
        in microseconds.
        """
        if(self.led_color_change_enable == 1):
            self.change_color()
        for x in range(self.led_number-1):
             self.shift_right()
             pyb.delay(delay)

    def scroll_left(self, delay):
        if(self.led_color_change_enable == 1):
            self.change_color()
        for x in range(self.led_number-1):
             self.shift_left()
             pyb.delay(delay)

    def auto_scroll(self,delay):
        """
        Rather than call scroll_left and then scroll_right
        this function automatically scrolls to the opposite
        side based on led_pos.
        Delay specifies how long to wait between each shift
        in microseconds.
        """
        if(self.led_pos == 0):
            self.scroll_right(delay)
        else:
            self.scroll_left(delay)

    def set_led(self, led, color, intensity):
        """
        This sets an LEDs color and intensity.
        led values between 0 - led_number.
        Color should be in the form: (R,G,B), between 0-255.
        Intensity should be between 0-1.
        """
        if(intensity < 0 or intensity > 1):
            self.led_list[led] = ((0,0,0),0)
        else:
            r = (int)(color[0]*intensity)
            g = (int)(color[1]*intensity)
            b = (int)(color[2]*intensity)
            self.led_list[led] = ((r,g,b),intensity)
        self.update()

    def fade_all_led(self):
        """
        Decreases all LED values by ((1-fade_amount)*100)%.
        """
        fade_amount = 0.92
        for x in range(self.led_number):
            self.set_led(x, self.led_list[x][0], self.led_list[x][1]*fade_amount)

    def toggle_color_change(self):
        """
        Used to toggle the color change flag.
        """
        self.led_color_change_enable = 1 if self.led_color_change_enable == 0 else 0

    def change_color(self):
        """
        Calculates new color values based on led_n_color.
        """
        r = int((1 + math.sin(self.led_n_color * 0.1324)) * 127)
        g = int((1 + math.sin(self.led_n_color * 0.1654)) * 127)
        b = int((1 + math.sin(self.led_n_color * 0.1)) * 127)
        self.led_color = (r,g,b)
        self.set_led(self.led_pos,(r,g,b),self.led_intensity)
        self.led_n_color += 1
        self.update()
