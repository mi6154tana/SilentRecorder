# -*- coding: utf-8 -*-
#This is Prototype Silent Recorder's code.

#import RPi.GPIO as GPIO
from pygame.locals import *
import pygame
import time
import sys

class PlaySound:

    def __init__(self):
        #pygame.init()
        pygame.mixer.quit()
        pygame.mixer.init()

        self.sound_list = []
        self.sound_fname = [#サンプリング音源のファイル名
            './SoundDatas/do.wav',
            './SoundDatas/re.wav',
            './SoundDatas/mi.wav',
            './SoundDatas/fa.wav',
            './SoundDatas/sol.wav',
            './SoundDatas/la.wav',
            './SoundDatas/si.wav',
            './SoundDatas/do8va.wav',
            './SoundDatas/re8va.wav'
        ]
        self.ingering_models = [
            '11111111',#do
            '01111111',#re
            '00111111',#mi
            '00011111',#fa
            '00001111',#sol
            '00000111',#la
            '00000101',#si
            '00000100',#do8va
            '00111110' #re8va
        ]

        #in_gpiopin = [4, 17, 27, 22, 5, 6, 13, 19]#GPIO運指検知テスト用ピン
        self.last_fin = -1
        self.now_fin = -1

        for i in range(9):
            self.sound_list.append(None)
            self.sound_list[i] = pygame.mixer.Sound(self.sound_fname[i])
    
        '''
        GPIO.setmode(GPIO.BCM)
        for i in range(8):#プロトタイプ(優先接続式)のみ
            GPIO.setup(in_gpiopin[i], GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        '''

    '''
    def ProtoFingeringCheck():#プロトタイプ(優先接続式)のみ
        ifingering = ''
        count = 0
        for i in range(8):
            if GPIO.input(in_gpiopin[i]) == GPIO.HIGH:
                ifingering += '1'
            else:
                ifingering += '0'
        print(ifingering)
        for m in fingering_models:
            if m == ifingering:
                print('play sound !!')
                return str(count)
            count += 1
        return '-1'# NoHit
    '''

    def fingering_check(self, ifingering):
        count = 0
        for m in self.fingering_models:
            if m == ifingering:
                print('play sound !!')
                return str(count)
            count += 1
        return '-1'# NoHit

    def _change_sound(self, last_fin, now_fin):
        if(last_fin != now_fin):
            if last_fin != -1:
                self.sound_list[last_fin].stop()
            if now_fin != -1:
                self.sound_list[now_fin].play(-1)
                volume = self.sound_list[now_fin].get_volume() # 音量取得
                print(volume)
            else:
                self.sound_list[last_fin].stop()

    '''
    def ChangeVolume():
        volume = channel.get_volume() # 音量取得
        print(volume)
        channel.set_volume(0.5)
    '''

    def sr_play(self, fin_tmp):#モジュールとして呼び出されたとき
        self.last_fin = self.now_fin
        self.now_fin = fin_tmp
        self._change_sound(self.last_fin, self.now_fin)

    def __del__(self):
        self._change_sound(self.now_fin, -1)


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

    #GPIO.cleanup()

if __name__ == "__main__":
    main()