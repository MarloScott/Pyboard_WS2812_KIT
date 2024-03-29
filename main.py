# Written by Marlo Scott
# K.I.T
# Compatible with Pyboard and WS2812 RGB LED
# WS2812 Datasheet: https://cdn-shop.adafruit.com/datasheets/WS2812.pdf

import ledstrip

transition_delay = 60  # Microseconds
movement_accel_threshold = 5  # Expected absolute acceleration readings range from 0 - 25

led_strip = ledstrip.LedStrip(led_number=8, init_color=(0xff,0,0), spi_bus=1, intensity=1)

def main():

    accel = pyb.Accel()
    color_flag = 0

    while True:
        z = accel.z()
        x = accel.x()
        y = accel.y()

        # Toggles whether the lights change color.
        # Triggerd when the LEDs are tilted so that the
        # LEDs are facing horizontally length wise.
        if abs(y) > 15:
            if(color_flag == 0):
                led_strip.toggle_color_change()
                color_flag = 1
        else:
            color_flag = 0

        # Allows LED to be moved manually
        # when tilted left and right
        if abs(z) > movement_accel_threshold:
            if(z > 0):
                led_strip.shift_left()
                pyb.delay(transition_delay)
            else:
                led_strip.shift_right()
                pyb.delay(transition_delay)
            continue

        led_strip.auto_scroll(transition_delay)

main()
