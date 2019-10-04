import tkinter as tk
import math
import time
import numpy as np
import read_score as rs
#from udp_com import UdpCom as uc #RaspberryPiでの動作確認 and 演奏デバイスと通信時
#from gpio_in import GpioIn as gi #RaspberryPiでの動作確認
from play_sound import PlaySound as ps
import judgement_score as j_s
from ope_recording import OpeRecording as o_re
import json

from send_damy_input import DamyInput as di #PCでの動作確認

class DrawScore:
    '''
    music_deta = [  
        1,1,0,0,1,1,2,2,
        4,4,2,2,1,1,1,1,
        2,2,4,4,5,5,4,5,
        8,8,6,6,5,5,4,4,
        2,2,4,4,5,5,5,5,
        8,8,7,7,8,8,8,8,
        2,2,4,4,5,5,4,4,
        2,2,2,4,1,1,1,1,
        5,5,7,7,8,8,8,8,
        7,7,8,8,5,5,4,4,
        5,5,4,2,1,1,1,1
    ]
    '''

    def __init__(self, music_name, cv, p_frame, mode_name):
        self.cv = cv
        self.root = p_frame
        self.music_name = music_name
        self.mode_name = mode_name
        #self.button = gi() #RaspberryPiでの動作確認

        self.music_deta = []
        self.last_time = time.time()
        self.first_roop = 1
        self.draw_point = 0
        self.seek_point = 5
        self.last_seek_point = 5#入力描画用
        self.end_flag = 0
        self.bpm = 0
        self.measure = 0

        self.music_sound = ["ド","レ","ミ","ファ","ソ","ラ","シ","ド","レ"]
        self.labals_update = -1
        self.labels = []

        # 受信の準備 #RaspberryPiでの動作確認 and 演奏デバイスと通信時
        # self.udp_data = uc()#PaspberryPiでの動作確認

        # 音を出す準備
        self.sound = ps()
        self.rcv_data_s = []

        #記録をとる準備
        self.write_rec = o_re()

        self.chan_in = 0
        self.chan_in_point = 0
        self.score_update = 1

        self.d_input = di()#PCでの動作確認

        
        if self.mode_name == "PLAY_RECORDING":
            l_music_data = rs.read_score(self.music_name)
            self.bpm = l_music_data[0]
            self.measure = l_music_data[1]
            del l_music_data[0:2]
            self.music_deta = l_music_data
            for i in self.music_deta:
                print(i)
        else:
            l_music_data = rs.read_score(self.music_name)#, self.mode_name)
            self.bpm = l_music_data[0]
            self.measure = l_music_data[1]
            del l_music_data[0:2]
            self.music_deta = l_music_data
            for i in self.music_deta:
                print(i)

    def _draw_base_line(self):
        self.cv.create_polygon(0, 0, 512, 0, 512, 300, 0, 300, fill = "white")
        #五線譜の表示
        for i in range(0,5):
            i = i * 10
            self.cv.create_line(5,80+i,505,80+i)
        #小節毎の区切りの線
        self.cv.create_line(5,80,5,120)
        self.cv.create_line(255,80,255,120)
        self.cv.create_line(505,80,505,120)

    def _reset_labels(self):
        self.labals_update = 1
        for i in range(len(self.labels)):
            self.labels[i].place_forget()
        self.labels.clear()

    def _draw_score_line(self):
        '''
        if self.button.gpio_input() == 0:#PaspberryPiでの動作確認
            self.write_rec.write_stop(self.music_name)
            self.root.quit()
            return
        '''
        if self.mode_name == 'JUDGE_PLAY':
            self.rcv_data_s.clear()
            #受信　PaspberryPiでの動作確認 and 演奏デバイスと通信時
            '''
            rcv_data = self.udp_data.rcv_input()
            self.rcv_data_s = rcv_data.split(':')
            '''
            #PCでの動作確認
            rcv_data = self.d_input.rcv_input()
            self.rcv_data_s = rcv_data.split(':')
            if int(self.rcv_data_s[1]) != self.chan_in:
                self.chan_in_point = self.last_seek_point#self.seek_point - 10
            
                
        #記録を残す
        self.write_rec.write_recording(self.rcv_data_s[0], self.rcv_data_s[1])

        x = 0
        now_time = time.time()
        interval = now_time - self.last_time
        if interval >= self.bpm*self.measure*2:
            self.draw_point += 32*2#だと思う
            #self.seek_point = 0#最も左のシーク位置
            self.last_time = time.time()
            if self.end_flag == 1:
                '''
                print("OKOKOKO")#点数を表示
                self.ans = j_s.judgement_score()
                print("ANS_e:", self.ans)
                self.label = tk.Label(self.root,text = "正答率" + str(round(self.ans,1)) + "%" ,background = "white",font = ("",20,"bold"))
                self.label.place(x = 300, y = 240)
                self.root.update()
                
                time.sleep(3)
                print("interval : " + str(interval))
                print("end of draw_score_line")
                '''
                #self.root.destroy()
                self.write_rec.write_stop(self.music_name)
                self.root.quit()
                return
            self._reset_labels()
        elif self.labals_update == -1:#要改良
            self._reset_labels()      
        else:
            self.labals_update = 0
        
        #self.seek_point = 5.0+ 500.0*float(interval/(self.bpm*self.measure*2))
        self.last_seek = time.time()

        self.cv.delete('seek_line')
        
        m_p = [127.5,122.5,117.5,112.5,107.5,102.5,97.5,92.5,87.5]#音階の描画位置
        count = 0
        old_m = -1
        old_change = 5

    
        for j in self.music_deta:#range(draw_point, draw_point + 16):
            if self.draw_point <= count and self.draw_point + 32*2 > count:
                if count > len(self.music_deta):
                    break
                #print(str(j) + ':' + str(draw_point))
                x1=x * 500/(32*2)#x1 = x * 62.5
                #self.cv.create_polygon(x1 + 10,M_s[j],72.5 + x1,M_s[j],72.5 + x1,M_s[j] + 10,x1 + 10,M_s[j] + 10 , tag ="polygon")
                if self.score_update:
                    self.cv.create_polygon(x1 + 5,m_p[j],5 + 500/(32*2) + x1,m_p[j],5 + 500/(32*2) + x1,m_p[j] + 5,x1 + 5,m_p[j] + 5 , tag = 'score_line')

                #音階が変わったかを検知
                if count == self.draw_point:
                    old_m = j
                if self.labals_update == 1:
                    if j != old_m or count == self.draw_point + 32*2-1 or count == len(self.music_deta)-1:
                        self.labels.append(tk.Label(text = self.music_sound[old_m],background = "white",font = ("",10,"bold")))
                        self.labels[len(self.labels)-1].place(x = (old_change + x1 )/2 - 5,y = 150)
                        old_m = j
                        old_change = x1 + 5

                #cv.update()
                x = x + 1
                if x == 32*2:
                    x = 0
                    #cv.delete("polygon")
            if count >= self.draw_point + 32*2:
                break
            count += 1
        
        self.score_update = 0

        self.cv.create_polygon(self.seek_point-2, 50, self.seek_point+2, 50, self.seek_point + 2, 140, self.seek_point -2, 140, fill = "red", tag = 'seek_line')#シーク線
        if self.draw_point + 32*2 >= len(self.music_deta):
            #print("flag of draw_score_line")
            self.end_flag = 1
            #self.root.quit()
            #return

        
        if self.rcv_data_s[1] == old_m:#一致しているとき
            self.cv.create_polygon(self.chan_in_point, m_p[self._data_conv(self.rcv_data_s[1])], self.seek_point, m_p[self._data_conv(self.rcv_data_s[1])], self.seek_point, m_p[self._data_conv(self.rcv_data_s[1])]-5, self.chan_in_point, m_p[self._data_conv(self.rcv_data_s[1])]-5, fill = "blue", tag = "in_score_line")#入力描画
        else:
            self.cv.create_polygon(self.chan_in_point, m_p[self._data_conv(self.rcv_data_s[1])], self.seek_point, m_p[self._data_conv(self.rcv_data_s[1])], self.seek_point, m_p[self._data_conv(self.rcv_data_s[1])]-5, self.chan_in_point, m_p[self._data_conv(self.rcv_data_s[1])]-5, fill = "red", tag = "in_score_line")#入力描画
        
        #音を出す
        #self.sound.sr_play(self.rcv_data_s[1], self.rcv_data_s[0])

        if self.first_roop:
            self.first_roop = 0
            self.last_time = time.time() + 5
            self.root.after(5000, self._draw_score_line)        
        else:
            self.last_seek_point = self.seek_point
            self.seek_point = 5 + 500.0*float(interval/(self.bpm*self.measure*2))
            #self.chan_in = int(self.rcv_data_s[1])
            if self.chan_in_point > self.seek_point:
                self.chan_in = self.seek_point
                self.cv.delete('score_line')
                self.cv.delete('in_score_line')
                self.score_update = 1
            self.root.after(100, self._draw_score_line)

    def _data_conv(self, data):
        model = [
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
        for i in range(len(model)):
            if data == model[i]:
                return i - 1

    def ds_main(self):
        if self.mode_name == 'JUDGE_PLAY':
            self.write_rec.open_file()

        self._draw_base_line()
        self._draw_score_line()
        self.root.mainloop()

if __name__ == "__main__":
    #sound_score = DrawScore('君が代')

    print('finish')