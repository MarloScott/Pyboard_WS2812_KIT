# Written by Marlo Scott
# K.I.T
# Compatible with Pyboard and WS2812 RGB LED
# WS2812 Datasheet: https://cdn-shop.adafruit.com/datasheets/WS2812.pdf

from pyb import SPI, Timer
import ledstrip

led_strip = ledstrip.LedStrip(led_number=8, init_color=(0xff,0,0), spi_bus=1, intensity=1)

led_strip.init_single_led()

delay = 60
movement_threshold = 5

accel = pyb.Accel()

def test():
    count = 0
    color_flag = 0
    while True:
        z = accel.z()
        x = accel.x()
        y = accel.y()

        # This handles moveable LED mode
        if abs(z) > movement_threshold:
            led_strip.init_single_led()
            count = 0
            led_pos = 0
            while (count < 100):
                if(z > 0):
                    led_strip.shift_left()
                    led_pos += 1
                    pyb.delay(delay)
                else:
                    led_strip.shift_right()
                    led_pos -= 1
                    pyb.delay(delay)
                z = accel.z()
                count = count+1 if abs(z) < 5 else count


        # This handles scrolling along LEDs
        if abs(x) > 20:
            count+=1
            if(count>=20):
                count = 0
                while (abs(z) < movement_threshold):
                    led_strip.scroll_right(delay)
                    #led_strip.change_color()
                    led_strip.scroll_left(delay)
                    # This handles changing colors
                    if abs(y) > 20:
                        if(color_flag == 0):
                            led_strip.toggle_color_change()
                        color_flag = 1
                    else:
                        color_flag = 0
                    x = accel.x()
                    y = accel.y()
                    z = accel.z()
            pyb.delay(100)
