import os
def _new_data_conv(self, data):
    new_model = [
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
    for i in range(len(new_model)):
        if data == new_model[i]:
            return model[i]
    return '00000000'

def judgement_score():
    nowDirectoryPath = os.path.dirname(os.path.abspath(__file__)) + "/"
    cnt = 0
    Standard_data = open(nowDirectoryPath + "Score.txt","r") #正解
    S_d_line = Standard_data.read().split()

    User_sound_data = open(nowDirectoryPath + "udp_input.txt","r") #ユーザー入力
    U_s_d_line = User_sound_data.read().split()
    del U_s_d_line[0:3]

    for i in range(len(U_s_line)):
        if i > len(S_d_line)-1:
            break
        fin_U_s_d_line = U_s_d_line[i].split(':')
        if S_d_line[i] == _new_data_conv(fin_U_s_d_line[1]):
            cnt += 1
    ans = float(cnt/len(S_d_line)) * 100
    return ans
