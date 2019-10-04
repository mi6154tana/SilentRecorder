def judgement_score():
    cnt = 0
    Standard_data = open("Recorder.txt","r") #正解
    S_d_line = Standard_data.read().split()

    User_sound_data = open("./udp_input.txt","r") #ユーザー入力
    U_s_d_line = User_sound_data.read().split()

    for i in range(len(S_d_line)):
        if S_d_line[i] == U_s_d_line[i]:
            cnt += 1
    ans = cnt/len(S_d_line) * 100
    return ans
