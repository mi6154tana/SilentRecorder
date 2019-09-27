# -*- coding: utf-8 -*-
#This is Prototype Silent Recorder's code.

import threading
from pygame.locals import *
import pygame
import time
import sys
import json

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

        self.volume_lv = 1

    def __get_volume_lv(self):
        with open('config.json', 'r') as f:
            conf_data = json.load(f)
        return conf_data
    
    def __set_volume_level(self):
        v_text = self.__get_volume_lv()
        if v_text['Volume'] == '1':
            self.volume_lv = 2
        elif v_text['Volume'] == '2':
            self.volume_lv = 3
    
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
        self.__set_volume_level()
        self.sound_metro_1.set_volume(float(1/3) * self.volume_lv)
        self.sound_metro_2.set_volume(float(1/3) * self.volume_lv)
        tempo = float(60/bpm)
        thread_metro = threading.Thread(target=BackMetro._play_metronome, args=(self, tempo, ))#並行処理でメトロノームを流す
        thread_metro.start()

    def metro_stop(self):
        self.mflag = 0


def main():
    bpm = 158
    metro = BackMetro()
    #metro.s()
    metro.metro_start(bpm)
    #BackMetronome(bpm)
    time.sleep(5)
    metro.metro_stop()

if __name__ == "__main__":
    main()