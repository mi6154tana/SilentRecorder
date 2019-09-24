# -*- coding: utf-8 -*-
#This is Prototype Silent Recorder's code.

import threading
from pygame.locals import *
import pygame
import time
import sys

class BackMetro:

    def __init__(self):
        pygame.mixer.quit()
        pygame.mixer.pre_init(44100,-16,1,512)
        pygame.mixer.init()

        self.mflag = 0
        self.sound_metro_1 = None
        self.sound_metro_2 = None
        self.metro_fname_1 = './SoundDatas/metro_1.wav'
        self.metro_fname_2 = './SoundDatas/metro_2.wav'

        self.sound_metro_1 = pygame.mixer.Sound(self.metro_fname_1)
        self.sound_metro_2 = pygame.mixer.Sound(self.metro_fname_1)

    def _play_metronome(self, tempo):
        last_time = time.perf_counter()
        ob_flag = 0
        while 1:
            if self.mflag == 0:
                break
            now_time = time.perf_counter()
            interval = now_time - last_time
            #print('BPM : ' + str(tempo))
            if interval >= tempo:
                print(interval)
                if ob_flag == 0:
                    #self.sound_metro_2.stop()
                    self.sound_metro_1.play()
                    #print("1:",self.sound_metro_1.get_length())
                elif ob_flag == 1:
                    #self.sound_metro_1.stop()
                    self.sound_metro_2.play()
                    #print("2:",self.sound_metro_2.get_length())
                ob_flag = 1- ob_flag
                    #time.sleep(self.sound_metro_1.get_length())
                last_time = time.perf_counter()

    def metro_start(self, bpm):
        self.mflag = 1
        tempo = float(60/bpm)
        thread_metro = threading.Thread(target=BackMetro._play_metronome, args=(self, tempo, ))#並行処理でメトロノームを流す
        thread_metro.start()
        time.sleep(5)
        self.metro_stop()

    def metro_stop(self):
        self.mflag = 0


def main():
    bpm = 60
    metro = BackMetro()
    #metro.s()
    metro.metro_start(bpm)
    #BackMetronome(bpm)

if __name__ == "__main__":
    main()