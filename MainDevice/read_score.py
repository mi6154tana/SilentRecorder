import numpy as np
#from play_sound import PlaySound as ps

def data_conv(data):
    model = ['.', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j']
    for i in range(len(model)):
        if data == model[i]:
            return i - 1
            

def read_score(music_name):
    music_data = []
    f = open('./Score/' + music_name + '.txt','r')
    line = f.readline()
    tmp = line.split()#改行で分割
    bpm = int(tmp[0])
    NoteLength = 60/bpm
    mag = [0,4,2,3,1,1.5,0.25,0.375,0.5,0.75]#楽譜データに対応、一小節を４としている、楽譜データにあるものは配列のインデックス番号
    hRecorder = 10 #リコーダーが一秒間に送ってくるデータ数
    hScore = 32 #楽譜が一秒間に処理数データ数（最小の） 一小節のデータ数？？
    line = f.readline()
    fRecorder = open('Recorder.txt','w')#リコーダーから送られてくるデータとみなす、後々正確性診断に使う
    fScore = open('Score.txt','w')#楽譜データから音階データのみを記録
    t = 0

    music_data.append(NoteLength)
    music_data.append(int(tmp[2]))
    #sound_conv = ps()

    #デバイスから入力される信号　　ド～ミ^
    #あとでplay_sound.pyのやつをつかう
    halls = ["11111111","01111111","00111111","00011111","00001111","00000111","00000101","00000100","00111110"]

    while line:#楽譜データの行数回る
        #コメ切り
        if line == '\n' or line[0:2] == '//':
            line = f.readline()
            continue
        data = line.split()#改行を消去
        for i in range(int((hScore/4)*mag[int(data[1])])):
            fScore.write(data[0]+'\n')
            music_data.append(data_conv(data[0]))
        dt = (mag[int(data[1])]*NoteLength)#その音符の長さ（秒）
        #無音処理
        for i in np.arange(t, t+dt, (1/hRecorder)):
            scale = data[0][0]
            if scale == ".":
                fRecorder.write("0:00000000\n")#休符
                #music_data.append(sound_comp.fingering_check('00000000'))
            else :
                fRecorder.write('1:' + halls[ord(scale)-ord('a')]+'\n')
                #music_data.append(sound_comp.fingering_check(halls[ord(scale)-ord('a')]))
        t += dt
        line = f.readline()
    f.close()
    fScore.close()
    fRecorder.close()
    #del sound_comp

    return music_data