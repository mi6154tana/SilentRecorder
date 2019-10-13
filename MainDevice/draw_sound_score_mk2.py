# -*- coding: utf-8 -*-
#This is Silent Recorder's code. I hope this works the way I want.
import tkinter as tk
import math
import time
import numpy as np
import read_score as rs
from udp_com import UdpCom as uc #RaspberryPiでの動作確認 and 演奏デバイスと通信時
from gpio_in import GpioIn as gi #RaspberryPiでの動作確認
from play_sound import PlaySound as ps
import judgement_score as j_s
from ope_recording import OpeRecording as o_re
from back_metro import BackMetro as bm
import json
import os

from send_damy_input import DamyInput as di #PCでの動作確認

class DrawScore:
    def __init__(self, music_name, cv, p_frame, mode_name):
        self.damy_mode = 0 #演奏デバイスと通信せずに動かす
        self.center_adj = 100 #中央寄せ調整用
        self.draw_mag = 2.0 #フルスクリーン時、表示するディスプレイに合わせるため
        self.cv = cv
        self.root = p_frame
        self.music_name = music_name
        self.mode_name = mode_name
        self.button = gi() #RaspberryPiでの動作確認

        self.music_deta = []
        self.last_time = time.time()
        self.last_input_time = time.time()
        self.start_time = time.time()
        self.first_roop = 1
        #self.draw_point = 0
        self.seek_point = 5
        self.last_seek_point = 5#入力描画用
        self.end_flag = 0

        self.music_sound = ["ド","レ","ミ","ファ","ソ","ラ","シ","ド","レ"]
        self.labels = []

        self.m_p = [127.5,122.5,117.5,112.5,107.5,102.5,97.5,92.5,87.5]#音階の描画位置

        # 受信の準備 #RaspberryPiでの動作確認 and 演奏デバイスと通信時
        if not self.damy_mode:
            self.udp_data = uc()#PaspberryPiでの動作確認

        # PCでの動作確認
        self.d_input = di()

        # 音を出す準備
        self.sound = ps()
        self.rcv_data_s = ['0', '00000000']

        #記録をとる準備
        self.write_rec = o_re()

        #お手本を読む
        if self.mode_name == 'JUDGE_PLAY':
            l_music_data = rs.read_score(self.music_name)
        else:
            l_music_data = rs.read_recording(self.music_name)
        noteLength = l_music_data[0]
        self.radix = l_music_data[1]
        self.bpm = 60/noteLength
        del l_music_data[0:2]
        self.exa_music_datas = l_music_data
        self.exa_counter = 0

        #カタカナデータを読む
        self._read_scale_kana()
        self.kana_last_write = 0
        self.kana_num = 0
        self.drawing_kana = self.kana_lines[self.kana_num]#.split(':')

        self.seek_limit = noteLength*self.radix*2 #2小説の演奏にかかる時間7
        print('self.seek_limit : ', self.seek_limit)
        self.num_measure_data = self.seek_limit/0.05 #二小説の描画に必要なデータ数
        print('self.num_measure_data : ', self.num_measure_data)
        #print('self.num_measure_data to int: ', int(self.num_measure_data))
        self.draw_min_size = 500*self.draw_mag/self.num_measure_data

        #実験用
        self.input_counter = 0
        self.reflesh = 1

        #メトロノームの準備
        self.b_metro = bm(self.root,self.bpm)
    
    def _draw_base_line(self):# 五線譜の描画
        self.cv.create_polygon(self.center_adj + 0,0, self.center_adj + 512*self.draw_mag,0, self.center_adj + 512*self.draw_mag,300*self.draw_mag, self.center_adj + 0,300*self.draw_mag, fill = "white", tag = 'back_ground')
        #五本線
        for i in range(0,5):
            i = i * 10
            self.cv.create_line(self.center_adj + 5*self.draw_mag,(80+i)*self.draw_mag, self.center_adj + 505*self.draw_mag,(80+i)*self.draw_mag, tag = 'base_line')
        #小節毎の区切りの線
        self.cv.create_line(self.center_adj + 5*self.draw_mag,80*self.draw_mag,  self.center_adj + 5*self.draw_mag,120*self.draw_mag, tag = 'base_line')
        self.cv.create_line(self.center_adj + 255*self.draw_mag,80*self.draw_mag,self.center_adj + 255*self.draw_mag,120*self.draw_mag, tag = 'base_line')
        self.cv.create_line(self.center_adj + 505*self.draw_mag,80*self.draw_mag,self.center_adj + 505*self.draw_mag,120*self.draw_mag, tag = 'base_line')

    def _draw_score_line(self):
        #PaspberryPiでの動作確認
        #中断して戻る
        if self.button.gpio_input() == 0:
            if self.mode_name == 'JUDGE_PLAY':
                self.udp_data.play_stop()
                self.write_rec.write_stop(self.music_name)
                self.b_metro.metro_stop()
            self.root.quit()
            return
        
        now_time = time.time()
        interval = now_time - self.last_time
        rcv_data = '0:00000000'
        if self.first_roop != 1:# 入力を受け付ける
            if (now_time-self.start_time) - self.input_counter*0.05 >= 0.05:# 0.05秒おきに入力を受け付ける
                self.rcv_data_s.clear()
                if self.mode_name == 'JUDGE_PLAY':
                    if not self.damy_mode:
                        rcv_data = self.udp_data.rcv_input()# 受信 PaspberryPiでの動作確認 and 演奏デバイスと通信時
                    else:
                        rcv_data = self.d_input.rcv_input()# PCでの動作確認
                else:
                    if self.input_counter < len(self.exa_music_datas)-1:
                        rcv_data = self.exa_music_datas[self.input_counter]# exaを入力とする
                self.rcv_data_s = rcv_data.split(':')
                self.last_input_time = time.time()
                self.input_counter += 1
                # 記録を残す
                if self.mode_name == 'JUDGE_PLAY':
                    self.write_rec.write_recording(self.rcv_data_s[0], self.rcv_data_s[1])

        if interval >= self.seek_limit or self.first_roop:# シークバーが右端に行った 画面の更新
            #print('interval ', interval)
            print('self.input_counter : ', self.input_counter)
            if self.end_flag:#終了
                if self.mode_name == 'JUDGE_PLAY':
                    self.write_rec.write_stop(self.music_name)
                    self.cv.create_text(self.center_adj + (242 + len(self.music_name)*2)*self.draw_mag, 225*self.draw_mag, font = ('Purisa', int(25*self.draw_mag)), text = '正確率 : ' + str(round(j_s.judgement_score(), 1)) + '%')
                    self.b_metro.metro_stop()
                self.root.quit()
                return
            self.last_time = now_time
            # 古い描画を消す
            self._reset_scale_labels()
            self.cv.delete('score_line')
            self.cv.delete('in_score_line')

            scale_change_point = 5
            for i in range(int(self.num_measure_data)):# お手本を二小節分描画
                x0 = i*self.draw_min_size + 5*self.draw_mag
                x1 = i*self.draw_min_size + self.draw_min_size + 5*self.draw_mag
                if self.mode_name == 'JUDGE_PLAY':
                    drawing_scale = int(self.exa_music_datas[self.exa_counter])
                else:
                    rec_tmp_s = self.exa_music_datas[self.exa_counter].split(':')
                    drawing_scale = self._data_conv(rec_tmp_s[1])
                if drawing_scale != -1:
                    self.cv.create_polygon(self.center_adj + x0,self.m_p[drawing_scale]*self.draw_mag, self.center_adj + x1,self.m_p[drawing_scale]*self.draw_mag, self.center_adj + x1,(self.m_p[drawing_scale] + 5)*self.draw_mag, self.center_adj + x0,(self.m_p[drawing_scale] + 5)*self.draw_mag , tag = 'score_line')
                self.exa_counter += 1

                if self.exa_counter > len(self.exa_music_datas)-1:#お手本楽譜の最後まで来たら
                    if self.mode_name == 'JUDGE_PLAY':
                        self._draw_scale_label(drawing_scale, scale_change_point, x1)
                    self.end_flag = 1
                    break
                
                #print(self.drawing_kana[1], ' ', self.exa_counter)
                if self.mode_name == 'JUDGE_PLAY' and int(self.drawing_kana) == self.exa_counter - self.kana_last_write:
                    self._draw_scale_label(drawing_scale, scale_change_point, x1)#カタカナ音階の表示
                    self.kana_last_write = self.exa_counter
                    self.kana_num += 1
                    if self.kana_num < len(self.kana_lines):
                        self.drawing_kana = self.kana_lines[self.kana_num]#.split(':')
                    scale_change_point = x1
                
                '''
                elif self.mode_name == 'PLAY_RECORDING':
                    next_rec_tmp_s = self.exa_music_datas[self.exa_counter].split(':')
                    if drawing_scale != self._data_conv(next_rec_tmp_s[1]):
                        self._draw_scale_label(drawing_scale, scale_change_point, x1)#カタカナ音階の表示
                        self.kana_last_write = self.exa_counter
                        self.kana_num += 1
                        if self.kana_num < len(self.kana_lines):
                            self.drawing_kana = self.kana_lines[self.kana_num]#.split(':')
                        scale_change_point = x1
                '''

            if self.num_measure_data - int(self.num_measure_data) > 0:
                self.exa_counter += 1
        
        elif self.mode_name == 'JUDGE_PLAY':# 入力描画
            if self.last_seek_point > self.seek_point:
                self.cv.delete('in_score_line')
                self.last_seek_point = 5*4
            if self._new_data_conv(self.rcv_data_s[1]) != -1 and int(self.rcv_data_s[0])>2000:
                if self._new_data_conv(self.rcv_data_s[1]) == self.exa_music_datas[self.input_counter - 1]:
                    self.cv.create_polygon(self.center_adj + self.last_seek_point*self.draw_mag,self.m_p[self._new_data_conv(self.rcv_data_s[1])]*self.draw_mag, self.center_adj + self.seek_point*self.draw_mag,self.m_p[self._new_data_conv(self.rcv_data_s[1])]*self.draw_mag, self.center_adj + self.seek_point*self.draw_mag,(self.m_p[self._new_data_conv(self.rcv_data_s[1])] + 5)*self.draw_mag, self.center_adj + self.last_seek_point*self.draw_mag,(self.m_p[self._new_data_conv(self.rcv_data_s[1])] + 5)*self.draw_mag, fill = "blue", tag = "in_score_line")
                else:
                    self.cv.create_polygon(self.center_adj + self.last_seek_point*self.draw_mag,self.m_p[self._new_data_conv(self.rcv_data_s[1])]*self.draw_mag, self.center_adj + self.seek_point*self.draw_mag,self.m_p[self._new_data_conv(self.rcv_data_s[1])]*self.draw_mag, self.center_adj + self.seek_point*self.draw_mag,(self.m_p[self._new_data_conv(self.rcv_data_s[1])] + 5)*self.draw_mag, self.center_adj + self.last_seek_point*self.draw_mag,(self.m_p[self._new_data_conv(self.rcv_data_s[1])] + 5)*self.draw_mag, fill = "red", tag = "in_score_line")
        

        #シーク線
        self.cv.delete('seek_line')
        self.cv.create_polygon(self.center_adj + (self.seek_point-2)*self.draw_mag,50*self.draw_mag, self.center_adj + (self.seek_point+2)*self.draw_mag,50*self.draw_mag, self.center_adj + (self.seek_point+2)*self.draw_mag,140*self.draw_mag, self.center_adj + (self.seek_point-2)*self.draw_mag,140*self.draw_mag, fill = "red", tag = 'seek_line')

        #音を出す
        if self.mode_name == 'JUDGE_PLAY':
            self.sound.sr_play(self.rcv_data_s[1], self.rcv_data_s[0])
        else:
            self.sound.sr_play(self.rcv_data_s[1], self.rcv_data_s[0])

        #再起ループ
        if self.first_roop:# 第一回目のループは5秒後
            self.first_roop = 0
            self.last_time = time.time() + 5
            self.start_time = self.last_time
            self.last_input_time = self.last_time
            self.root.after(3000, self._draw_score_line)        
        else:
            self.last_seek_point = self.seek_point
            self.seek_point = (5 + 500.0)*float(interval/self.seek_limit)
            self.root.after(30, self._draw_score_line)

    def _read_scale_kana(self):
        nowDirectoryPath = os.path.dirname(os.path.abspath(__file__)) + "/"
        f = open(nowDirectoryPath + 'ScaleKana.txt', 'r')
        self.kana_lines = f.readlines()
        for i in range(len(self.kana_lines)):
            self.kana_lines[i] = self.kana_lines[i].strip()
        

    def _reset_scale_labels(self):
        self.labals_update = 1
        for i in range(len(self.labels)):
            self.labels[i].place_forget()
        self.labels.clear()

    def _draw_scale_label(self, scale, x0, x1):
        if scale != -1:
            self.labels.append(tk.Label(text = self.music_sound[scale],background = "white",font = ("",int(10*self.draw_mag),"bold")))
            self.labels[len(self.labels)-1].place(x = self.center_adj + ((x0 + x1 )/2 - 5),y = 150*self.draw_mag)

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
                return i
        return -1

    def _new_data_conv(self, data):
        model = [
            '11111111',#do
            '01111111',#re
            '00111111',#mi
            '00011111',#fa
            '00001111',#sol
            '00000111',#la
            '00001011',#si
            '00001101',#do8va
            '00001100',#re8va
            '00111110' #mi8va
        ]
        for i in range(len(model)):
            if data == model[i]:
                return i
        return -1

    def __get_mode_flag(self):
        nowDirectoryPath = os.path.dirname(os.path.abspath(__file__)) + "/"
        with open(nowDirectoryPath + 'config.json', 'r') as f:
            conf_data = json.load(f)
        return conf_data

    def dss_main(self):
        if self.mode_name == 'JUDGE_PLAY':
            self.write_rec.open_file()
            self.write_rec.write_head_data(str(self.bpm), '4', str(self.radix))

            mode_text = self.__get_mode_flag()
            if not self.damy_mode:
                #演奏デバイスに送信指示 PaspberryPiでの動作確認
                if mode_text['Mode'] == 'B':
                    self.udp_data.zero_start(2)
                else:
                    self.udp_data.zero_start(1)
                
        self._draw_base_line()# 五線譜を描画
        self._draw_score_line()
        if self.mode_name == 'JUDGE_PLAY':
            if mode_text['metronom'] == 'ON':
                self.b_metro.metro_start()
            title_y = 20
        else:
            title_y = 225
        #題名表示
        self.cv.create_text(self.center_adj + (242 + len(self.music_name)*2)*self.draw_mag, title_y*self.draw_mag, font = ('Purisa', int(25*self.draw_mag)), text = self.music_name)
        self.root.mainloop()
