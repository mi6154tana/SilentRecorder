# -*- coding: utf-8 -*-
#This is Prototype Silent Recorder's code.
import RPi.GPIO as GPIO

class GpioIn:

    def __init__(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(4,GPIO.OUT)
        GPIO.setup(18,GPIO.IN,pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(23,GPIO.IN,pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(24,GPIO.IN,pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(25,GPIO.IN,pull_up_down=GPIO.PUD_DOWN)

    def gpio_input(self):
        if GPIO.input(18) == GPIO.HIGH:
            print(0)
            return 0
        elif GPIO.input(23) == GPIO.HIGH:
            print(1)
            return 1
        elif GPIO.input(24) == GPIO.HIGH:
            print(2)
            return 2
        elif GPIO.input(25) == GPIO.HIGH:
            print(3)
            return 3
        else:
            print(-1)
            return -1
