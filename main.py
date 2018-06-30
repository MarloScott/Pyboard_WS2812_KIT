# This code is based on SPI example at Https://forum.micropython.org/viewtopic.php?t=149
# Written by Marlo Scott
# K.I.T
# Compatible with Pyboard and WS2812 RGB LED
# WS2812 Datasheet: https://cdn-shop.adafruit.com/datasheets/WS2812.pdf

from pyb import Pin, Timer, Switch, SPI

# Initalise SPI to baud rate of 6.4 mHz.
# This should give us 1 byte to represent 1 LED bit.
spi = SPI(1, SPI.MASTER, baudrate=6400000, polarity=0, phase=1)


# Byte codes for LED bits
code_0 = chr(0x03)
code_1 = chr(0x0F)

brightness = 0x04

# Must be one one then actual number to remove incorrect value being sent to last LED
number_of_LEDS = 9

# This list keeps track of all the LED values
led_list = [dict({'green':0x00,'red':0x00,'blue':0x0f}) for x in range(number_of_LEDS)]


spi.send(chr(0x00000000))

# This function converts a byte to the equivilant LED bits
def byte2bits(byte):
    bits = ''
    mask = 0x80
    while mask != 0:
        bits += code_0 if ( byte & mask ) == 0 else code_1
        mask >>= 1
    return bits



def update():
    bits = ''
    spi.send(0x00)
    for x in range(number_of_LEDS):
        bits+=byte2bits(led_list[x]['green'])
        bits+=byte2bits(led_list[x]['red'])
        bits+=byte2bits(led_list[x]['blue'])
    spi.send(bits)


def red():
    for x in range(number_of_LEDS):
        led_list[x]['red'] = brightness
        led_list[x]['green'] = 0x00
        led_list[x]['blue'] = 0x00
    update()
    update()


def green():
    for x in range(number_of_LEDS):
        led_list[x]['red'] = 0x00
        led_list[x]['green'] = brightness
        led_list[x]['blue'] = 0x00
    update()
    update()


def blue():
    for x in range(number_of_LEDS):
        led_list[x]['red'] = 0x00
        led_list[x]['green'] = 0x00
        led_list[x]['blue'] = brightness
    update()
    update()


def set_led(x, color):
    led_list[x]['green'] = 0x00
    led_list[x]['red'] = 0x00
    led_list[x]['blue'] = 0x00
    led_list[x][color] = brightness
    update()
    update()


def off():
    for x in range(number_of_LEDS):
        led_list[x]['red'] = 0x00
        led_list[x]['green'] = 0x00
        led_list[x]['blue'] = 0x00
    update()
    update()

off()





n = 0
while True:
    r = int((1 + math.sin(n * 0.1324)) * 127)
    g = int((1 + math.sin(n * 0.1654)) * 127)
    b = int((1 + math.sin(n * 0.1)) * 127)
    for x in range(number_of_LEDS):
        led_list[x]['red'] = r
        led_list[x]['green'] = g
        led_list[x]['blue'] = b
    update()
    n += 1
    pyb.delay(20)
