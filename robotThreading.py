import Tkinter as tk
from time import sleep
import copy
from Maestro import Controller
import thread
from math import floor, fmod
import socket
import sys
import threading

class Controllers:

    def __init__(self, win):
        self.looking = True
        self.data = None;
        self.win = win
        self.canvas = tk.Canvas(self.win, width = 800, height = 480)
        self.commandList = []
        self.eyeLoc = (300,300)
        self.pupil = 0
        self.botEye = 0
        self.response = ''
        self.speaking = False
        self.topEye = 0

##        thread.start_new_thread(self.send,())
        thread.start_new_thread(self.receive,())
        
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
        body.place (x = 0, y = 0, height = 60, width = 90)
        wheels.place (x = 0, y = 70, height = 60, width = 90)
        turn.place (x = 0, y = 140, height = 60, width = 90)
        headnod.place (x = 0, y = 210, height = 60, width = 90)
        headTurn.place (x = 0, y = 280, height = 60, width = 90)
        delete.place (x = 0, y = 350, height = 60, width = 90)
        body.bind("<Button-1>", self.bodyClick)
        wheels.bind("<Button-1>", self.wheelClick)
        turn.bind("<Button-1>", self.turnClick)
        headnod.bind("<Button-1>", self.nodClick)
        headTurn.bind("<Button-1>", self.headTurnClick)
        delete.bind("<Button-1>", self.deleteClick)

        start = tk.Label(self.canvas, text = "START", bg = "cyan", bd = 5, relief = tk.RAISED)
        start.pack()
        start.place(x = 700, y = 380, width = 80, height = 50)
        start.bind("<Button-1>", self.test)
        self.canvas.pack()

    def eyeMove(self):
         
        c = tk.Canvas(self.canvas, width = 800, height = 480)
        c.configure(background = 'black')
        c.pack()
        c.create_oval(0,0,800,480, fill = "white")
        self.pupil = c.create_oval(150, 150, 275, 300, outline='blue', fill='black', width=70)
        self.botEye = c.create_rectangle(0, 480, 800, 1500, fill='black')
        self.topEye = c.create_rectangle(0, -800, 1040, 0, fill='black')
        while(self.looking):
            self.look(200,300,c)
            sleep(1)
            self.look(650,250,c)
            sleep(1)
            self.look(400,240,c)
            sleep(1)
            self.blink(c)
        c.destroy()
    def look(self, x, y, c):
        xDist = x - self.eyeLoc[0]
        yDist = y - self.eyeLoc[1]
        xStep = xDist / 100
        yStep = yDist / 100

        for i in range(100):
            self.eyeLoc = (self.eyeLoc[0] + xStep, self.eyeLoc[1] + yStep)
            c.move(self.pupil, xStep, yStep)
            self.win.update()

    def blink(self, c):
        step = 7

        for i in range(int(520/step)):
            c.move(self.botEye, 0, -step)
            c.move(self.topEye, 0, step)
            self.win.update()

        for i in range(int(520/step)):
            c.move(self.botEye, 0, step)
            c.move(self.topEye, 0, -step)
            self.win.update()

    def bodyClick(self, event):
        c = tk.Frame(self.canvas, bd = 2, relief = tk.RIDGE)
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
        c.place(x = (fmod(len(self.commandList),7) + 1)*100, y = floor(len(self.commandList)/7) * 210, width = 95, height = 200)
        self.commandList.append({'body':{'pos':pos}})
        
    def wheelClick(self, event):
        c = tk.Frame(self.canvas, bd = 2, relief = tk.RIDGE)
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

        time = tk.DoubleVar()
        choice = tk.Scale(c, label = "TIME (S)", from_ = 0, to = 3, resolution = .25, variable = time, sliderlength = 10, orient = tk.HORIZONTAL)
        choice.pack()

        c.place(x = (fmod(len(self.commandList),7) + 1)*100, y = floor(len(self.commandList)/7) * 210, width = 95, height = 200)
        self.commandList.append({'wheels':{'direction':direction, 'speed':speed, 'time':time}})
        

    def turnClick(self, event):
        c = tk.Frame(self.canvas, bd = 2, relief = tk.RIDGE)
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

        time = tk.DoubleVar()
        choice = tk.Scale(c, label = "TIME (S)", from_ = 0, to = 3, resolution = .25, variable = time, sliderlength = 10, orient = tk.HORIZONTAL)
        choice.pack()

        c.place(x = (fmod(len(self.commandList),7) + 1)*100, y = floor(len(self.commandList)/7) * 210, width = 95, height = 200)
        self.commandList.append({'turn':{'direction':direction, 'speed':speed, 'time':time}})
        
    def nodClick(self, event):
        c = tk.Frame(self.canvas, bd = 2, relief = tk.RIDGE)
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
        c.place(x = (fmod(len(self.commandList),7) + 1)*100, y = floor(len(self.commandList)/7) * 210, width = 95, height = 200)
        self.commandList.append({'Head Nod':{'pos':pos}})
        

    def headTurnClick(self, event):
        c = tk.Frame(self.canvas, bd = 2, relief = tk.RIDGE)
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
        c.place(x = (fmod(len(self.commandList),7) + 1)*100, y = floor(len(self.commandList)/7) * 210, width = 95, height = 200)
        self.commandList.append({'Head Turn':{'pos':pos}})
        
    def deleteClick(self, event):
        self.commandList.pop()
        frame = self.win.winfo_children()[len(self.win.winfo_children())-1]
        frame.destroy()
    def newTest(self):
        self.looking = True;
                # for key in self.commandList:
        #     for k, v in key.items():
        #         print("\n",k)
        #         for i,j in v.items():
        #             print (i+',',j.get())
        try:
            thread.start_new_thread(self.action,())
        except:
            print('Error1')
        try:
            thread.start_new_thread(self.eyeMove,())
        except:
            print('Error2')
        
    def test(self, event):
        self.newTest()
        

    def action(self):
        for key in self.commandList:
            for k, v in key.items():
                if k == 'body':
                    for i,j in v.items():
                        self.moveBody(j.get())
                elif k == 'wheels':
                    self.moveWheels(v.items())
                elif k == 'turn':
                    self.turn(v.items())
                elif k == 'Head Nod':
                    for i,j in v.items():
                        self.headNod(j.get())
                elif k == 'Head Turn':
                    for i,j in v.items():
                        self.headTurn(j.get())
        self.looking = False;

    def moveBody(self, bodVal):
        if bodVal == 0:
            x.setTarget(0,5000)
        elif bodVal == 1:
            x.setTarget(0,6000)
        else:
            x.setTarget(0,7000)

    def moveWheels(self, params):
        dir = 1
        for k, v in params:
            print(k)
            if k == 'direction':
                if v.get() == 0:
                    dir = -1
                else:
                    dir = 1
            if k == 'speed':
                if v.get() == 0:
                    x.setTarget(1,6000 + (800 * dir))
                else:
                    x.setTarget(1,6000 + (1300 * dir))
            if k == 'time':
                sleep(v.get())
        x.setTarget(1,6000)

    def turn(self, params):
        dir = 1
        for k, v in params:
            print(k)
            if k == 'direction':
                print(v.get())
                if v.get() == 0:
                    dir = -1
                else:
                    dir = 1
            if k == 'speed':
                if v.get() == 0:
                    x.setTarget(2,6000 + (800 * dir))
                else:
                    x.setTarget(2,6000 + (1300 * dir))
            if k == 'time':
                sleep(v.get())
        x.setTarget(2,6000)

    def headNod(self, nodVal):
        if nodVal == 0:
            print(nodVal)
            x.setTarget(4,7000)
        elif nodVal == 1:
            x.setTarget(4,6000)
        else:
            x.setTarget(4,5000)

    def headTurn(self, turnVal):
        if turnVal == 0:
            x.setTarget(3,7000)
        elif turnVal == 1:
            x.setTarget(3,6000)
        else:
            x.setTarget(3,5000)
        sleep(.5)
    def receive(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        commands = {'hello':'hey friend', 'bye':'peace', 'weather':'look outside', 'name':'none ya business', 'cats':'fuck the griz'}
        try:
            self.sock.connect(('10.200.5.97', 8080))
##            print(self.s.recv(1024))
        except:
            print('bind fail')
        while(True):
##            self.sock.connect(('10.200.5.97',8080))
            try:
                  input = self.sock.recv(1024)
                  input = str.decode(input)
                  print(input)
                  if input == 'start':
                      self.newTest()
                  elif commands.get(input) != None:
                      response = commands.get(input)
                      print('hi')
                      self.send(response)
##                      self.sock.close()
##                      self.sock.connect(('10.200.5.97',8080))
##                  self.sock.close()
                   
            except:
                  print('WOOW')
    def send(self, response):
##            self.s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
##            try:
##                self.s.connect(('10.200.5.97', 8080))
##            except:
##                print('connection failed')
        
##                    self.s.connect(('10.200.5.97', 8080))

            try:
                 my_str = response
                 my_str_as_bytes=str.encode(my_str)
                 self.sock.send(my_str_as_bytes)
            except:
                 print('NOO')
            self.sock.close()
            self.sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            self.sock.connect(('10.200.5.97', 8080))


window = tk.Tk()
window.geometry("1040x720")
control = Controllers (window)
x = Controller()
##try:
##    thread.start_new_thread(test,())
##except:
##    print('error')
##control.eyeMove()
window.mainloop()
