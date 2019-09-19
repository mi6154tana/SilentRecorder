import tkinter as tk

class NormalPlay:
    def __init__(self, cv):
        self.cv = cv

    def __draw_recorder(self):
        # リコーダー本体(表)
        self.cv.create_polygon(110, 40, 110, 280, 180, 280, 180, 40, fill="blue")

        # リコーダー本体(裏)
        self.cv.create_polygon(30, 40, 30, 280, 100, 280, 100, 40, fill="blue")

        # リコーダー穴
        # for i in range()

    def npmain(self):
        self.cv.delete('select')
        self.__draw_recorder()