#!/usr/bin/env python


import RPi.GPIO as GPIO
import subprocess
import board
#import neopixel


# On CircuitPlayground Express, and boards with built in status NeoPixel -> board.NEOPIXEL
# Otherwise choose an open pin connected to the Data In of the NeoPixel strip, i.e. board.D1
#pixel_pin = board.NEOPIXEL

# On a Raspberry pi, use this instead, not all pins are supported
#pixel_pin = board.D18
#GPIO.setup(15, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)

# The number of NeoPixels
#num_pixels = 240

# The order of the pixel colors - RGB or GRB. Some NeoPixels have red and green reversed!
# For RGBW NeoPixels, simply change the ORDER to RGBW or GRBW.
#ORDER = neopixel.GRB #GRB

#pixels = neopixel.NeoPixel(
#    pixel_pin, num_pixels, brightness=0.2, auto_write=False, pixel_order=ORDER
#)

GPIO.setmode(GPIO.BCM)
GPIO.setup(3, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.wait_for_edge(3, GPIO.FALLING)


#pixels.fill((0,0,0))
#pixels.show()


subprocess.call(['shutdown', '-h', 'now'], shell=False)
