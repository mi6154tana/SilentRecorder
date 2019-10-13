# -*- coding: utf-8 -*-
#This is Silent Recorder's code.
from pygame.locals import *
import pygame
import time
import sys
import json
import os

class PlaySound:

    def __init__(self):
        #pygame.init()
        pygame.mixer.quit()
        pygame.mixer.pre_init(44100,-16,1,512)
        pygame.mixer.init()

        nowDirectoryPath = os.path.dirname(os.path.abspath(__file__)) + "/"

        self.sound_list = []
        self.sound_fname = [#サンプリング音源のファイル名
            nowDirectoryPath + 'SoundDatas/do.wav',
            nowDirectoryPath + 'SoundDatas/re.wav',
            nowDirectoryPath + 'SoundDatas/mi.wav',
            nowDirectoryPath + 'SoundDatas/fa.wav',
            nowDirectoryPath + 'SoundDatas/sol.wav',
            nowDirectoryPath + 'SoundDatas/la.wav',
            nowDirectoryPath + 'SoundDatas/si.wav',
            nowDirectoryPath + 'SoundDatas/do8va.wav',
            nowDirectoryPath + 'SoundDatas/re8va.wav',
            nowDirectoryPath + 'SoundDatas/mi8va.wav'
        ]
        self.fingering_models = [
            '11111111',#do
            '01111111',#re
            '00111111',#mi
            '00011111',#fa
            '00001111',#sol
            '00000111',#la
            '00000011',#si
            '00000101',#do8va
            '00000100',#re8va
            '00111110' #mi8va
        ]

        #in_gpiopin = [4, 17, 27, 22, 5, 6, 13, 19]#GPIO運指検知テスト用ピン
        self.last_fin = -1
        self.now_fin = -1

        self.volume_max = 4096 #4096 ,200 in test
        self.volume_lv = 1.0
        self.__set_volume_level()

        for i in range(10):
            self.sound_list.append(None)
            self.sound_list[i] = pygame.mixer.Sound(self.sound_fname[i])

    def __get_volume_lv(self):
        nowDirectoryPath = os.path.dirname(os.path.abspath(__file__)) + "/"
        with open(nowDirectoryPath + 'config.json', 'r') as f:
            conf_data = json.load(f)
        return conf_data
    
    def __set_volume_level(self):
        v_text = self.__get_volume_lv()
        if v_text['Volume'] == '1':
            self.volume_lv = 2.0
        elif v_text['Volume'] == '2':
            self.volume_lv = 3.0


    def fingering_check(self, ifingering):
        count = 0
        for m in self.fingering_models:
            if m == ifingering:
                # print('play sound !!')
                return str(count)
            count += 1
        return '-1'# NoHit

    def _change_sound(self, last_fin, now_fin, volume):
        volume_sr = float(1/(self.volume_max - 1000)) * float(volume)/3 * self.volume_lv
        #volume_sr = float(1/(self.volume_max)) * float(volume)/3 * self.volume_lv
        if volume_sr < 0:
            volume_sr = 0
        if(last_fin != now_fin):
            if last_fin != -1:
                self.sound_list[last_fin].stop()
            if now_fin != -1:
                #pygame.mixer.music.set_volume(volume)
                self.sound_list[now_fin].set_volume(volume_sr)
                #self.sound_list[now_fin].set_volume(float(1/3) * self.volume_lv)
                #self.sound_list[now_fin].set_volume(1)
                self.sound_list[now_fin].play(-1)
                #p_volume = self.sound_list[now_fin].get_volume() # 音量取得
                #print(p_volume)
            else:
                self.sound_list[last_fin].stop()
        else:
            self.sound_list[now_fin].set_volume(volume_sr)
            #self.sound_list[now_fin].set_volume(float(1/3) * self.volume_lv)
            p_volume = self.sound_list[now_fin].get_volume() # 音量取得
            #print(p_volume)

    def sr_play(self, i_fin, volume):#呼び出されたとき
        #data = rcv_data.split(':')
        #self.__set_volume_level()
        fin_tmp = int(self.fingering_check(i_fin))
        self.last_fin = self.now_fin
        self.now_fin = fin_tmp
        self._change_sound(self.last_fin, self.now_fin, volume)

    def __del__(self):
        self._change_sound(self.now_fin, -1, 0)


def main():

    sound = PlaySound()
    fin_tmp = -1
    try:
        while True:#メインループ
            #keybord input!
            fin_tmp = int(input('>>'))
            if fin_tmp == 7777:
                break
            fin_tmp -= 1
            if fin_tmp < 0 or fin_tmp > 8:
                fin_tmp = -1
            
            #device input!
            #fin_tmp = int(ProtoFingeringCheck()) 

            sound.sr_play(fin_tmp)
            
            time.sleep(0.03)
    except KeyboardInterrupt:
        pass

if __name__ == "__main__":
    main()
