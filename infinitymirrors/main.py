#!/usr/bin/python


"""
Made by Bror Hjemgaard 2021 for Laplace, UiO
Bror.hjemgaard@gmail.com
"""

import RPi.GPIO as GPIO
import time
import board
import neopixel
import subprocess
import threading
import sys
import random 
import math
import serial
import datetime
from os import listdir
from os.path import isfile, join

# global analog, btn, sw
# sw = False



port = serial.Serial("/dev/ttyUSB0", 115200)


# startup time
time.sleep(1)


# lightshow_id = 0 # the initial lightshow_id which is incremented by a button press
# kill_all_threads = False # when True, all threads will halt


# num_pixels = 240 # The number of NeoPixels
# pixel_pin = board.D18 # BCM ID for data out pin connected to the neopixels


# Neopixel init setup

GPIO.setmode(GPIO.BCM)
class Lightshow:
    current_lightshow_id = 0 # the initial lightshow_id which is incremented by a button press
    kill_all_threads = False # when True, all threads will halt
    num_pixels = 240 # The number of NeoPixels
    pixel_pin = board.D18 # BCM ID for data out pin connected to the neopixels

    sw = False # switch state

    def __init__(self) -> None:

        self.pixels = neopixel.NeoPixel(
            self.pixel_pin, self.num_pixels, brightness=0.5, auto_write=False, pixel_order=neopixel.GRB
        )

        try:
        
            # find all lightshows in the ./lightshows dir
            filenames = [f.rstrip(".py") for f in listdir("/home/pi/Laplace/infinitymirrors/lightshows") if isfile(join("/home/pi/Laplace/infinitymirrors/lightshows", f))]

            self.lightshows = []
            for a in filenames:
                exec(f"import lightshows.{a}")
                self.lightshows.append(eval(f"lightshows.{a}.show"))


            # self.lightshows = lightshows
            self.num_lightshows = len(self.lightshows)
        except Exception as e:
            self.log_error(e)
            self.exit(shutdown=False)
        


    def start(self):
        """ 
        starts the ligthshow, which consists of different threads;
            - base_thread: A constant thread which checks the button panel for user input
            - lightshow_thread: There is one possible thread per ligthshow method, however only one runs at a time. When a lightshow is started/stopped the respective thread is started/stopped.
        All threads halt if self.kill_all_threads is True or an exception is thrown
        """

        # start base_thread which reads serial input
        self.base_thread = threading.Thread(target = self.read_serial,name="base_thread")
        self.base_thread.start()

        prev_val = 1#GPIO.input(button_pin)
        
        while True:
            self.pixels.fill((0,0,0)) # set all pixels blank before switching show
            self.pixels.show()

            # start lightshow_thread
            lightshow_thread = threading.Thread(target = self.lightshows[self.current_lightshow_id], args=(self, self.current_lightshow_id),name=f"lightshow_thread-{str(self.current_lightshow_id)}")
            lightshow_thread.start()

            try:
                # wait for the target function to end
                if not self.kill_all_threads:
                    lightshow_thread.join()
            except KeyboardInterrupt:
                self.exit(shutdown=False)
            except Exception as e:
                self.log_error(e)
                self.exit(shutdown=False)
                

            time.sleep(0.08)



    def exit(self, shutdown = True, *args, **kwargs):

        # safely end all threads
        self.kill_all_threads = True
        for thread in threading.enumerate():
            if thread.name == "MainThread": continue
            try:
                print(f"killing thread '{thread.name}'...")
                thread.join(timeout=1)
            except Exception as e:
                #self.log_error(e)
                print(e)

        # turn off the pixels
        self.pixels.fill((0,0,0))
        self.pixels.show()
        
        GPIO.cleanup()
        if shutdown:
            print("Shutting down ... ")
            subprocess.call(['shutdown', '-h', 'now'], shell=False)
            sys.exit(1)
        else:
            sys.exit(0)


    def change_ligthshow(self):
        self.current_lightshow_id += 1
        self.current_lightshow_id = self.current_lightshow_id % self.num_lightshows
        print(self.current_lightshow_id)
    

    def read_serial(self):
        # Reads the controll board input via arduino USB

        # global analog, btn, sw
        while True and (not self.kill_all_threads):
            # time.sleep(0.1)
            # continue
            line = port.readline().decode()
            tmpanalog, tmpbtn, tmpsw, tmpswChg = line.split(',')[:4]

            analog = int(tmpanalog)
            btn = bool(int(tmpbtn))
            sw = bool(int(tmpsw))
            swChg = bool(int(tmpswChg))

            if btn and sw:
                self.change_ligthshow()

            self.pixels.brightness = analog/1023 if sw else 0
        
    def log_error(self, err):
        with open("/home/pi/Laplace/infinitymirrors/err.txt", "w+") as file:
            file.write(f"{datetime.datetime.now()}  {err} \n")

if __name__ == "__main__":
    ligthshow = Lightshow()
    try:
        ligthshow.start()
    except Exception as e:
        if e is not KeyboardInterrupt:
            lightshow.log_error(e)



    