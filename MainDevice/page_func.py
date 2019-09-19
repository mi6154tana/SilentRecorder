# -*- coding: utf-8 -*-
#This is Prototype Silent Recorder's code.

import threading
from  play_sound import PlaySound as ps
from back_metro import BackMetro as bm
import time

def select_func(p_position, select_con):
    if p_position == 1:#通常演奏
        play_sound_start()

def play_sound_start():
    sound = ps()
    try:
        while True:#メインループ
            #keybord input!
            
            fin_tmp = int(input('ps >>'))
            if fin_tmp == 7777:
                break
            fin_tmp -= 1
            if fin_tmp < 0 or fin_tmp > 8:
                fin_tmp = -1
            
            #data_input!
            '''
            f = open('./input_data.txt', 'r')
            lines = f.readlines()
            for l in lines:
                i_data = l.split(':')
                print(i_data[1])
                fin_tmp = sound.fingering_check(i_data[1].strip())
                print(fin_tmp)
                sound.sr_play(int(fin_tmp))
                time.sleep(0.1)
            '''

            #device input!
            #fin_tmp = int(ps.FingeringCheck(ifingering)) 
            sound.sr_play(fin_tmp)
            
            time.sleep(0.1)
    except KeyboardInterrupt:
        pass
