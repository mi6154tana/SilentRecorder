import datetime
import math

def trans_record2score(music_name):
    hRecorder = 10 #リコーダーが一秒間に送ってくるデータ数
    hScore = 32 #一小節のデータ数
    #dt_now = datetime.datetime.now()
    #timeStr = dt_now.strftime('%Y%m%d%H%M%S')
    playScoreFileName = './Recorder_sample.txt' #リコーダーの演奏した結果のファイル名
    musicScoreFileName = './Score/' + music_name + '.txt' #楽譜データ(bpmとかよむために)
    outputFileName = './convertDraw.txt' #出力ファイル
    playScoreFile = open(playScoreFileName,'r')
    musicScoreFile = open(musicScoreFileName,'r')
    outputFile = open(outputFileName,'w')

    line = musicScoreFile.readline()
    metaData = line.split()#改行で分割
    baseNote = int(metaData[0])
    bpm = int(metaData[1])
    beat_numerator = int(metaData[2])#拍子(分子)
    beat_denominator = int(metaData[3])#拍子(分母)

    mag = [0,4,2,3,1,1.5,0.25,0.375,0.5,0.75]#楽譜データに対応、一小節を４としている、楽譜データにあるものは配列のインデックス番号
    NoteLength = (60/bpm) / (mag[baseNote])#4分音符の長さ
    _1_32_NoteLength = NoteLength / (32/4)
    musicScoreFile.close()

    line = playScoreFile.readline()
    timeCnt = 0
    numberOfNote = -1

    #print(_1_32_NoteLength)
    while line:#楽譜データの行数回る
        nowNumberOfNote = math.floor(timeCnt / _1_32_NoteLength)
        if nowNumberOfNote > numberOfNote:
            for i in range(nowNumberOfNote - numberOfNote):
                outputFile.write(line)
            numberOfNote = nowNumberOfNote
        timeCnt += (1/hRecorder)
        timeCnt = round(timeCnt,1)
        line = playScoreFile.readline()

    playScoreFile.close()
    outputFile.close()
