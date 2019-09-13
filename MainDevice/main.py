# GUIを扱う
#import RPi.GPIO as GPIO
import tkinter as tk
import time
from PIL import Image, ImageTk
from create_page import CreatePage as cp

root = None
pages = []
page_names = [
    'HOME',
    'NORAL_PLAY',
    'SCORE_LIST',
    'JUDGE_PLAY',
    'RECORDING_LIST',
    'PLAY_RECORDING',
    'SETTING'
]
page_cons = [
    ['通常演奏', '正確性診断', '記録', '設定'],
    ['A', 'B', 'C'],
    ['君が代', '体の芯からまだ燃えているんだ'],
    ['E', 'F'],
    ['G'],
    ['H', 'I'],
    ['J']
]
trans_list = [#行はpagesに格納されているインデックス番号に対応、配列の中身は移動先のページのインデックス番号
        [0, 1, 2, 4, 6],#0:ホーム　最左列は戻る（左ボタン）での対応先、コンテンツは１～番号が振られており、選択されていればそこに移動
        [0],            #1:通常演奏　用意されていなければ、先に進めない
        [0, 3],         #2:楽譜リスト
        [2],            #3:正確性診断
        [0, 5],            #4:演奏記録一覧
        [4],          #5:演奏記録再生
        [0]             #6:設定
    ]

p_position = 0

def change_page():
    global p_position
    
    gpio_in = int(input('>>'))#PCでの動作確認 4という入力があった場合は、コンテンツ４が選択された状態で右ボタンが押されたとき
    if gpio_in + 1 <= len(trans_list[p_position]):
        pages[trans_list[p_position][gpio_in]].raise_page()
        p_position = trans_list[p_position][gpio_in]
    if gpio_in == 7777:
        root.destroy()
    else:
        root.after(1000, change_page)

def main():
    global root, pages
    root = tk.Tk()

    # ウィンドウタイトルを決定
    root.title("SilentRecorder")
    # ウィンドウの大きさを決定
    root.geometry("1024x600")
    #window.attributes("-fullscreen", True)

    # ウィンドウのグリッドを 1x1 にする
    root.grid_rowconfigure(0, weight=1)
    root.grid_columnconfigure(0, weight=1)

    #home = cp(root, 'HOME', home_cons)
    for i in range(len(page_names)):
        pages.append(cp(root, page_names[i], page_cons[i]))

    pages[0].raise_page()

    root.after(1000, change_page)
    #change_page()
    #test_p.raise_page()
    root.mainloop()

if __name__ == '__main__':
    main()