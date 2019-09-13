# GUIを扱う
import tkinter as tk
import time
from PIL import Image, ImageTk
from create_page import CreatePage as cp

root = None

pages = []
home_cons = ['通常演奏', '正確性診断', '記録', '設定']
test_cons = ['A', 'B', 'C']

p_flag = 0

def change_page():
    global p_flag
    if p_flag == 1:
        pages[0].raise_page()
    else:
        pages[1].raise_page()
    p_flag = 1 - p_flag

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
    pages.append(cp(root, 'HOME', home_cons))
    pages.append(cp(root, 'TEST', test_cons))

    pages[0].raise_page()

    root.after(1000, change_page)
    #change_page()
    #test_p.raise_page()
    root.mainloop()

if __name__ == '__main__':
    main()