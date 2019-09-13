# -*- coding: utf-8 -*-
#This is Prototype Silent Recorder's code.

import threading
from  play_sound import PlaySound
from back_metro import BackMetro
import time

def main():
    fin_tmp = -1

    bpm = int(input('BPM >> '))
    metronome = BackMetro()
    if bpm != 0:
        metronome.metro_start(bpm)

    sound = PlaySound()
    try:
        while True:#メインループ
            #keybord input!
            '''
            fin_tmp = int(input('>>'))
            if fin_tmp == 7777:
                break
            fin_tmp -= 1
            if fin_tmp < 0 or fin_tmp > 8:
                fin_tmp = -1
            '''
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
            
            time.sleep(0.03)
    except KeyboardInterrupt:
        pass
    #GPIO.cleanup()
    metronome.metro_stop()

if __name__ == "__main__":
    main()