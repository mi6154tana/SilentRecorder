import os
def judgement_score():
    nowDirectoryPath = os.path.dirname(os.path.abspath(__file__)) + "/"
    cnt = 0
    Standard_data = open(nowDirectoryPath + "Score.txt","r") #正解
    S_d_line = Standard_data.read().split()

    User_sound_data = open(nowDirectoryPath + "udp_input.txt","r") #ユーザー入力
    U_s_d_line = User_sound_data.read().split()
    del U_s_d_line[0:3]

    for i in range(len(S_d_line)):
        fin_U_s_d_line = U_s_d_line[i].split(':')
        if S_d_line[i] == fin_U_s_d_line[1]:
            cnt += 1
    ans = float(cnt/len(S_d_line)) * 100
    return ans
