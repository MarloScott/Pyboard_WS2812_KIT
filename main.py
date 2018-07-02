# Written by Marlo Scott
# K.I.T
# Compatible with Pyboard and WS2812 RGB LED
# WS2812 Datasheet: https://cdn-shop.adafruit.com/datasheets/WS2812.pdf

from pyb import SPI
import ledstrip

led_strip = ledstrip.LedStrip(led_number=8, init_color=(0xff,0,0), spi_bus=1, intensity=0.1)

led_strip.init_kit_scroll()

delay = 100
accel = pyb.Accel()
movement_threshold = 5

def test():
    led_strip.init_kit_scroll()
    count = 0

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

        # This handles changing colors
        if abs(y) > 20:
            led_strip.change_color()
            pyb.delay(50)

        # This handles scrolling along LEDs
        if abs(x) > 20:
            count+=1
            if(count>=20):
                count = 0
                led_strip.init_kit_scroll()
                while (abs(x) > movement_threshold):
                    led_strip.scroll_right(40)
                    led_strip.scroll_left(40)
                    x = accel.x()
            pyb.delay(100)
