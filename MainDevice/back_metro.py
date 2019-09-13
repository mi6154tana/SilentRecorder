# -*- coding: utf-8 -*-
#This is Prototype Silent Recorder's code.

import threading
from pygame.locals import *
import pygame
import time
import sys

class BackMetro:
    mflag = 0
    sound_metro_1 = None
    sound_metro_2 = None
    metro_fname_1 = './SoundDatas/metro_1.wav'
    metro_fname_2 = './SoundDatas/metro_2.wav'

    def __init__(self):
        pygame.mixer.quit()
        pygame.mixer.init()
        self.sound_metro_1 = pygame.mixer.Sound(self.metro_fname_1)
        self.sound_metro_2 = pygame.mixer.Sound(self.metro_fname_1)

    def _play_metronome(self, tempo):
        last_time = time.time()
        ob_flag = 0
        while 1:
            if self.mflag == 0:
                break
            now_time = time.time()
            interval = now_time - last_time
            #print('BPM : ' + str(tempo))
            if interval >= tempo:
                print(interval)
                if ob_flag == 0:
                    #self.sound_metro_2.stop()
                    self.sound_metro_1.play()
                elif ob_flag == 1:
                    #self.sound_metro_1.stop()
                    self.sound_metro_2.play()
                ob_flag = 1- ob_flag
                #time.sleep(self.sound_metro_1.get_length())
                last_time = time.time()

    def metro_start(self, bpm):
        self.mflag = 1
        tempo = float(60/bpm)
        thread_metro = threading.Thread(target=BackMetro._play_metronome, args=(self, tempo, ))#並行処理でメトロノームを流す
        thread_metro.start()

    def metro_stop(self):
        self.mflag = 0

def main():
    bpm = 120
    metro = BackMetro()
    metro.metro_start(bpm)
    #BackMetronome(bpm)

if __name__ == "__main__":
    main()