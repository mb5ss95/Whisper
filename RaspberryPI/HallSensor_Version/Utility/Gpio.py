from RPi import GPIO as gpio
from .AudioPlayer import audioPlayer

import threading
import time

class myGpio(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        
        #16, 23, 24, 25 interrupt

        self.DeadOrAlive = True
        self.val_rotary = list()
        self.player = audioPlayer()
        self.gpio_Setup()

    def vibe_Start(self, long=1):    
        time.sleep(long)
        gpio.output(self.vibePin, gpio.HIGH)
        time.sleep(long)
        gpio.output(self.vibePin, gpio.LOW)
            
    def rotary_Handler(self, ch):
        val_left = gpio.input(23)
        val_right = gpio.input(22)    
        
        time.sleep(0.5)
        if val_left == 0 and val_right == 1:
            if self.val_rotary.count(0) > 3:
                temp =  self.audio_get_volume() - 15
                print(temp)
                self.audio_set_volume(temp)
                self.val_rotary.clear()
            else:
                self.val_rotary.append(0)
        elif val_left == 1 and val_right == 0:
            if self.val_rotary.count(1) > 3:
                if  self.audio_get_volume() <= 130:
                    temp =  self.audio_get_volume() + 15
                    print(temp)
                    self.audio_set_volume(temp)
                self.val_rotary.clear()
            else:
                self.val_rotary.append(1)

    def effect_Handler(self, ch):
        self.player.set_Level((16, 23, 24, 25).index(ch))
        self.player.start_Audio()

    def gpio_Setup(self):
        gpio.setmode(gpio.BCM)
        gpio.setwarnings(False)

        #Vibe Pin
        gpio.setup(17, gpio.OUT)
        gpio.output(17, 0)

        #Rotary Pin
        for i in (23, 22):
            gpio.setup(i, gpio.IN)
            gpio.add_event_detect(i, gpio.BOTH, callback=self.rotary_Handler, bouncetime=100)

        #Effect Pin
        '''
        for i in (16, 23, 24, 25):
            gpio.setup(i, gpio.IN)
            gpio.add_event_detect(i, gpio.BOTH, callback=self.effect_Handler, bouncetime=1000)
        '''
        
    def set_PlayList(self, level):
        self.player.set_PlayList(level)

    def DeadOrAlive(self):
        gpio.clean()
        self.DeadOrAlive = False

    def run(self):       
        while(self.DeadOrAlive):
            pass