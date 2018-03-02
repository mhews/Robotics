import tkinter as tk
from time import sleep
import copy

class Controller:

    def __init__(self, win):
        self.win = win
        self.canvas = tk.Canvas(self.win, width = 1040, height = 720)
        self.commandList = []
        self.eyeLoc = (300,300)
        self.pupil = self.canvas.create_oval(300, 300, 550, 600, outline='blue', fill='black', width=70)
        self.botEye = self.canvas.create_rectangle(0, 720, 1040, 1500, fill='black')
        self.topEye = self.canvas.create_rectangle(0, -800, 1040, 0, fill='black')
        self.canvas.bind("<Button-1>", self.clickHandle)
        body = tk.Label(self.win, text = "BODY")
        body.place (x = 5, y = 10)
        body.pack()
        self.canvas.pack()

    def eyeMove(self):
        while(True):
            self.look(0,200)
            sleep(1)
            self.look(790,200)
            sleep(1)
            self.look(400,200)
            sleep(1)
            self.blink()

    def look(self, x, y):
        xDist = x - self.eyeLoc[0]
        yDist = y - self.eyeLoc[1]
        xStep = xDist / 100
        yStep = yDist / 100

        for i in range(100):
            self.eyeLoc = (self.eyeLoc[0] + xStep, self.eyeLoc[1] + yStep)
            self.canvas.move(self.pupil, xStep, yStep)
            self.win.update()

    def blink(self):
        step = 7

        for i in range(int(520/step)):
            self.canvas.move(self.botEye, 0, -step)
            self.canvas.move(self.topEye, 0, step)
            self.win.update()

        for i in range(int(520/step)):
            self.canvas.move(self.botEye, 0, step)
            self.canvas.move(self.topEye, 0, -step)
            self.win.update()

    def clickHandle(self, event):
        if (event.x < 50):
            self.createCommand(int(event.y/100))


    def createCommand(self, part):
        print(part)
        if (part != 5):
            c = tk.Frame(self.win, width = 50, height = 300)
        if (part == 0):
            lbl = tk.Label(c, text = "BODY")
            lbl.grid(column = 1, row = 0)
            lbl.pack()
            pos = tk.IntVar()
            left = tk.Radiobutton (c, text = "LEFT", variable = pos, value = 0)
            left.pack()
            middle = tk.Radiobutton (c, text = "MIDDLE", variable = pos, value = 1)
            middle.pack()
            right = tk.Radiobutton (c, text = "RIGHT", variable = pos, value = 2)
            right.pack()
            self.commandList.append({'body':{'pos':pos}})

        if (part == 1):
            lbl = tk.Label(c, text = "WHEELS")
            lbl.grid(column = 1, row = 0)
            lbl.pack()

            direction = tk.IntVar()
            forward = tk.Radiobutton (c, text = "FORWARD", variable = direction, value = 0)
            forward.pack()
            backward = tk.Radiobutton (c, text = "BACKWARD", variable = direction, value = 1)
            backward.pack()

            speed = tk.IntVar()
            slow = tk.Radiobutton(c, text = 'SLOW', variable = speed, value = 0)
            slow.pack()
            fast = tk.Radiobutton (c, text = "FAST", variable = speed, value = 1)
            fast.pack()

            self.commandList.append({'wheels':{'direction':direction, 'speed':speed}})

        if (part == 2):
            lbl = tk.Label(c, text = "TURN")
            lbl.grid(column = 1, row = 0)
            lbl.pack()

            direction = tk.IntVar()
            right = tk.Radiobutton (c, text = "RIGHT", variable = direction, value = 0)
            right.pack()
            left = tk.Radiobutton (c, text = "LEFT", variable = direction, value = 1)
            left.pack()

            speed = tk.IntVar()
            slow = tk.Radiobutton(c, text = 'SLOW', variable = speed, value = 0)
            slow.pack()
            fast = tk.Radiobutton (c, text = "FAST", variable = speed, value = 1)
            fast.pack()

            print(c.winfo_children())

            self.commandList.append({'turn':{'direction':direction, 'speed':speed}})
        if (part == 3):
            lbl = tk.Label(c, text = "HEAD NOD")
            lbl.grid(column = 1, row = 0)
            lbl.pack()

            pos = tk.IntVar()
            up = tk.Radiobutton (c, text = "UP", variable = pos, value = 0)
            up.pack()
            middle = tk.Radiobutton (c, text = "MIDDLE", variable = pos, value = 1)
            middle.pack()
            down = tk.Radiobutton (c, text = "DOWN", variable = pos, value = 2)
            down.pack()
            self.commandList.append({'Head Nod':{'pos':pos}})

        if (part == 4):
            lbl = tk.Label(c, text = "Head Turn")
            lbl.grid(column = 1, row = 0)
            lbl.pack()
            pos = tk.IntVar()

            left = tk.Radiobutton (c, text = "LEFT", variable = pos, value = 0)
            left.pack()
            middle = tk.Radiobutton (c, text = "MIDDLE", variable = pos, value = 1)
            middle.pack()
            right = tk.Radiobutton (c, text = "RIGHT", variable = pos, value = 2)
            right.pack()
            self.commandList.append({'Head Turn':{'pos':pos}})

        if (part == 5):
            self.commandList.pop()
            frame = self.win.winfo_children()[len(self.win.winfo_children())-1]
            frame.destroy()
            return(0)

        c.place(x = len(self.commandList)*100, y = 0)
        self.test()

    def test(self):
        for key in self.commandList:
            for k, v in key.items():
                print(k)
                for i,j in v.items():
                    print (i+',',j.get())
                print()
window = tk.Tk()
window.geometry("1040x720")
control = Controller (window)
#control.eyeMove()
window.mainloop()
