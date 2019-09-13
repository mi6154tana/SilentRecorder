import tkinter as tk
import math
import time
import numpy as np
import read_score as rs

from play_sound import PlaySound as ps

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
    music_deta = []
    root = tk.Tk("1024x600")
    last_time = time.time()
    draw_point = 0
    seek_point = 10
    end_flag = 0
    bpm = 0
    measure = 0

    music_sound = ["ド","レ","ミ","ファ","ソ","ラ","シ","ド","レ"]
    labals_update = -1
    labels = []
    cv = tk.Canvas(root,width = 1024,height = 600)
    sound = ps()

    def __init__(self, music_name):
        self.cv.pack()
        l_music_data = rs.read_score(music_name)
        self.bpm = l_music_data[0]
        self.measure = l_music_data[1]
        del l_music_data[0:2]
        self.music_deta = l_music_data
        for i in self.music_deta:
            print(i)
        self.root.after(10, self._draw_score_line)
        self.root.mainloop()

    def _reset_labels(self):
        self.labals_update = 1
        for i in range(len(self.labels)):
            self.labels[i].place_forget()
        self.labels.clear()

    def _draw_score_line(self):
        x = 0
        now_time = time.time()
        interval = now_time - self.last_time
        if interval >= self.bpm*self.measure*2:
            self.draw_point += 32*2#だと思う
            seek_point = 10#最も左のシーク位置
            self.last_time = time.time()
            if self.end_flag == 1:
                print("interval : " + str(interval))
                print("end of draw_score_line")
                self.root.destroy()
                return
            self._reset_labels()
        elif self.labals_update == -1:#要改良
            self._reset_labels()      
        else:
            self.labals_update = 0
        
        seek_point = 10.0+ 1000.0*float(interval/(self.bpm*self.measure*2))
        self.last_seek = time.time()

        self.cv.delete("all")
        self.cv.create_polygon(0, 0, 1024, 0, 1024, 600, 0, 600, fill = "white")
        #五線譜の表示
        #五線譜の表示
        for i in range(0,5):
            i = i * 20
            self.cv.create_line(10,160+i,1010,160+i)
        #小節毎の区切りの線
        self.cv.create_line(10,160,10,240)
        self.cv.create_line(510,160,510,240)
        self.cv.create_line(1010,160,1010,240)

        m_p = [255,245,235,225,215,205,195,185,175]#音階の描画位置
        count = 0
        old_m = -1
        old_change = 10
        for j in self.music_deta:#range(draw_point, draw_point + 16):
            if self.draw_point <= count and self.draw_point + 32*2 > count:
                if count > len(self.music_deta):
                    break
                #print(str(j) + ':' + str(draw_point))
                x1=x * 1000/(32*2)#x1 = x * 62.5
                #self.cv.create_polygon(x1 + 10,M_s[j],72.5 + x1,M_s[j],72.5 + x1,M_s[j] + 10,x1 + 10,M_s[j] + 10 , tag ="polygon")
                self.cv.create_polygon(x1 + 10,m_p[j],10 + 1000/(32*2) + x1,m_p[j],10 + 1000/(32*2) + x1,m_p[j] + 10,x1 + 10,m_p[j] + 10 , tag ="polygon")

                #音階が変わったかを検知
                if count == self.draw_point:
                    old_m = j
                if self.labals_update == 1:
                    if j != old_m or count == self.draw_point + 32*2-1 or count == len(self.music_deta)-1:
                        self.labels.append(tk.Label(text = self.music_sound[old_m],background = "white",font = ("",20,"bold")))
                        self.labels[len(self.labels)-1].place(x = (old_change + x1 )/2 - 10,y = 300)
                        old_m = j
                        old_change = x1 + 10

                #cv.update()
                x = x + 1
                if x == 32*2:
                    x = 0
                    #cv.delete("polygon")
            if count >= self.draw_point + 32*2:
                break
            count += 1
    
        self.cv.create_polygon(seek_point-2, 100, seek_point+2, 100, seek_point + 2, 280, seek_point -2, 280, fill = "red")#シーク線
        if self.draw_point + 32*2 >= len(self.music_deta):
            #print("flag of draw_score_line")
            self.end_flag = 1
        
        self.root.after(10, self._draw_score_line)

if __name__ == "__main__":
    sound_score = DrawScore('君が代')

    print('finish')