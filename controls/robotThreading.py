import tkinter as tk
from time import sleep
import copy

class Controller:

    def __init__(self, win):
        self.win = win
        self.canvas = tk.Canvas(self.win, width = 1040, height = 720)
        self.commandList = []
        self.eyeLoc = (300,300)
        self.pupil = 0
        self.botEye = 0
        self.topEye = 0

        body = tk.Label(self.canvas, text = "BODY", bg = "black", fg = "white", bd = 5, relief = tk.RAISED)
        body.pack()
        wheels = tk.Label(self.canvas, text = "WHEELS", bg = "black", fg = "white", bd = 5, relief = tk.RAISED)
        wheels.pack()
        turn = tk.Label(self.canvas, text = "TURN", bg = "black", fg = "white", bd = 5, relief = tk.RAISED)
        turn.pack()
        headnod = tk.Label(self.canvas, text = "HEAD NOD", bg = "black", fg = "white", bd = 5, relief = tk.RAISED)
        headnod.pack()
        headTurn = tk.Label(self.canvas, text = "HEAD TURN", bg = "black", fg = "white", bd = 5, relief = tk.RAISED)
        headTurn.pack()
        delete = tk.Label(self.canvas, text = "DELETE", bg = "black", fg = "white", bd = 5, relief = tk.RAISED)
        delete.pack()
        body.place (x = 0, y = 0, height = 110, width = 90)
        wheels.place (x = 0, y = 120, height = 110, width = 90)
        turn.place (x = 0, y = 240, height = 110, width = 90)
        headnod.place (x = 0, y = 360, height = 110, width = 90)
        headTurn.place (x = 0, y = 480, height = 110, width = 90)
        delete.place (x = 0, y = 600, height = 110, width = 90)
        body.bind("<Button-1>", self.bodyClick)
        wheels.bind("<Button-1>", self.wheelClick)
        turn.bind("<Button-1>", self.turnClick)
        headnod.bind("<Button-1>", self.nodClick)
        headTurn.bind("<Button-1>", self.headTurnClick)
        delete.bind("<Button-1>", self.deleteClick)

        start = tk.Label(self.canvas, text = "START", bg = "blue", bd = 5, relief = tk.RAISED)
        start.pack()
        start.place(x = 800, y = 600, width = 200, height = 110)
        start.bind("<Button-1>", self.test)
        self.canvas.pack()

    def eyeMove(self):
        self.canvas.create_oval(0,0,1040,720, fill = "white")
        self.pupil = self.canvas.create_oval(300, 300, 550, 600, outline='blue', fill='black', width=70)
        self.botEye = self.canvas.create_rectangle(0, 720, 1040, 1500, fill='black')
        self.topEye = self.canvas.create_rectangle(0, -800, 1040, 0, fill='black')
        while(True):
            self.look(50,200)
            sleep(1)
            self.look(740,200)
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
            self.createCommand(int(event.y/120))


    def createCommand(self, part):
        if (part != 5):
            c = tk.Frame(self.win, width = 50, height = 300)
    def bodyClick(self, event):
        c = tk.Frame(self.win, bd = 2, relief = tk.RIDGE)
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
        c.place(x = len(self.commandList)*100, y = 0, width = 95, height = 200)

    def wheelClick(self, event):
        c = tk.Frame(self.win, bd = 2, relief = tk.RIDGE)
        lbl = tk.Label(c, text = "WHEELS")
        lbl.grid(column = 1, row = 0)
        lbl.pack()

        direction = tk.IntVar()
        forward = tk.Radiobutton (c, text = "FORWARD", variable = direction, value = 0)
        forward.pack()
        backward = tk.Radiobutton (c, text = "BACK", variable = direction, value = 1)
        backward.pack()

        speed = tk.IntVar()
        slow = tk.Radiobutton(c, text = 'SLOW', variable = speed, value = 0)
        slow.pack()
        fast = tk.Radiobutton (c, text = "FAST", variable = speed, value = 1)
        fast.pack()

        self.commandList.append({'wheels':{'direction':direction, 'speed':speed}})
        c.place(x = len(self.commandList)*100, y = 0, width = 95, height = 200)


    def turnClick(self, event):
        c = tk.Frame(self.win, bd = 2, relief = tk.RIDGE)
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

        self.commandList.append({'turn':{'direction':direction, 'speed':speed}})
        c.place(x = len(self.commandList)*100, y = 0, width = 95, height = 200)

    def nodClick(self, event):
        c = tk.Frame(self.win, bd = 2, relief = tk.RIDGE)
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
        c.place(x = len(self.commandList)*100, y = 0, width = 95, height = 200)


    def headTurnClick(self, event):
        c = tk.Frame(self.win, bd = 2, relief = tk.RIDGE)
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
        c.place(x = len(self.commandList)*100, y = 0, width = 95, height = 200)

    def deleteClick(self, event):
        self.commandList.pop()
        frame = self.win.winfo_children()[len(self.win.winfo_children())-1]
        frame.destroy()

    def test(self, event):
        for item in  self.win.winfo_children():
            item.destroy()
        self.canvas = tk.Canvas(self.win, width = 1040, height = 720, bg = "black")
        self.canvas.pack()
        for key in self.commandList:
            for k, v in key.items():
                print("\n",k)
                for i,j in v.items():
                    print (i+',',j.get())

        self.eyeMove()
window = tk.Tk()
window.geometry("1040x720")
control = Controller (window)
#control.eyeMove()
window.mainloop()
