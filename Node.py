import random
import socket
import thread
import Tkinter as tk
from time import sleep
from itertools import cycle
from Maestro import Controller


key = False
input = ''
class Node(object):
    def __init__(self, type):
        self.edges = {}
        self.type = type

    def getConnections(self):
        saying = {'North' : 'N', 'South': 'S', 'East': 'E', 'West':'W'}
        options = ''
        for key, value in self.edges.items():
            options += saying[key] + ' '
        return options

    def isValid(self, direction):
        if(self.edges.get(direction)):
            return True
        return False

    def setEdges(self, edges):
        self.edges = edges

    def action(self, health):
        return health

class Enemy(Node):
    def __init__(self, difficulty, k):
        super(Enemy,self).__init__('enemy')
        self.key = k
        self.mult = difficulty
        self.health = 10 * self.mult
    def action(self, health):
        while health > 0 and self.health > 0:
            health += (-random.randint(0, 10))
            self.health += -random.randint(0, 6)
        if (self.key):
            global key
            key = True
        return health

class Recharge(Node):
    def __init__(self):
        super(Recharge,self).__init__ ('recharge')

    def action(self, health):
        return 100

class End(Node):
    def __init__(self):
        super(End, self).__init__('end')

    def action(self, health):
        if key:
            return 101
        else:
            return health
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
def receive():
    global sock
    commands = {'hello':'hey there friend', 'bye':'peace', 'weather':'look outside', 'name':'none ya business', 'cats':'fuck the griz'}
    n2 = End()
    n3 = Enemy(1, False)
    n1 = Node('start')
    n4 = Enemy(1, True)
    n5 = Recharge()
    
    health = 100

    startpos = [Node('start'),End()]
    places = [Enemy(1,False),Enemy(1,False),Enemy(1,False),Enemy(1,False),Enemy(2,True),Enemy(2,False),Recharge()]
    a = random.sample(range(7),7)
    b = random.sample(range(4),4)

    random.shuffle(places)
    
    startpos.append(places.pop())
    startpos.append(places.pop())
    random.shuffle(startpos)
    m1 = startpos.pop()
    if(m1.type == 'start'):
        current = m1
    m6 = startpos.pop()
    if(m6.type == 'start'):
        current = m6
    m7 = startpos.pop()
    if(m7.type == 'start'):
        current = m7
    m9 = startpos.pop()
    if(m9.type == 'start'):
        current = m9
    
    m2 = places.pop()
    m3 = places.pop()
    m4 = places.pop()
    m5 = places.pop()
    m8 = places.pop()
    
    m1.setEdges({'East': m2})
    m2.setEdges({'West': m1,'East':m3,'South':m5})
    m3.setEdges({'South': m6, 'West':m2})
    m4.setEdges({'East': m5, 'South': m7})
    m5.setEdges({'South': m8,'West':m4,'North':m2})
    m6.setEdges({'North': m3})
    m7.setEdges({'North': m4})
    m8.setEdges({'North': m5,'East':m9})
    m9.setEdges({'West':m8})

       
    directions = ['North', 'West', 'South', 'East']
    pool = cycle(directions)
    n1.setEdges({'South': n3})
    n2.setEdges({'East': n3})
    n3.setEdges({'South':n5, 'North': n1, 'West': n2, 'East': n4})
    n4.setEdges({'West': n3})
    n5.setEdges({'North': n3})

    curdir = 'Weast'
    
    try:
       sock.connect(('10.200.35.31', 8080))
    except:
        print('bind fail')
    global input
    global key
    while health > 0 and health < 101:
        dir = ''
        response = 'there is a path to the ' + current.getConnections()
        
        print(response)
        send(response)
        while not current.isValid(dir):
            try:
                  input = sock.recv(1024)
                  input = str.decode(input)
                  print(input)
                  
            except:
                  pass
            dir = input

        if(curdir == 'Weast'):
            curdir = dir
    
        current = current.edges.get(dir)
        if(directions[(directions.index(curdir) + 1) % len(directions)] == dir):
            curdir = dir
            x.setTarget(2,7500)
            sleep(.5)
            x.setTarget(2,6000)
            sleep(.5)
            x.setTarget(1,5000)
            sleep(1)
            x.setTarget(1,6000)
            print('right')
        elif(directions[(directions.index(curdir) + 3) % len(directions)] == dir):
            curdir = dir
            x.setTarget(2,4500)
            sleep(.5)
            x.setTarget(2,6000)
            sleep(1)
            x.setTarget(1,5000)
            sleep(1)
            x.setTarget(1,6000)
            print('left')
        elif(directions[directions.index(curdir) % len(directions)] == dir):
            x.setTarget(1,5000)
            sleep(1)
            x.setTarget(1,6000)
            print('forward')
        elif(directions[(directions.index(curdir) + 2) % len(directions)] == dir):
            x.setTarget(1,7000)
            sleep(1)
            x.setTarget(1,6000)
            print('backward')

        tempkey = key

        if(current.type == 'enemy'):
            if(current.health > 0):
                sleep(0.5)
                response=('You encountered an enemy. What should I do?')
                print(response)
                send(response)
                while input != 'run' and input != 'fight':
                    try:
                          input = sock.recv(1024)
                          input = str.decode(input)
                          print(input)
                          
                    except:
                          pass
                if(input == 'fight'):
                    x.setTarget(6,8000)
                    x.setTarget(12,4000)
                    x.setTarget(7,5000)    
                    x.setTarget(13,4000)
                    sleep(.1)
                    x.setTarget(14,5000)
                    x.setTarget(8,4000)
                    sleep(.6)
                    x.setTarget(14,7000)
                    x.setTarget(6,5000)
                    sleep(.1)
                    x.setTarget(12,6000)
                    x.setTarget(8,6000)
                    x.setTarget(7,6000)
                    x.setTarget(13,5800)
                    sleep(.6)
                    x.setTarget(6,0)
                    x.setTarget(7,0)
                    x.setTarget(8,0)
                    x.setTarget(12,0)
                    x.setTarget(13,0)
                    x.setTarget(14,0)

                    health = current.action(health)
                    response = 'you fought a level ' + str(current.mult) +' enemy. you have ' + str(health) + ' health'
                    send(response)
                elif(input == 'run'):
                    response = 'you ran away'
                    send(response)
                    print('ran away')
        else:
            health = current.action(health)
                
        if current.type == 'end' and not key:
            response = 'you need a key'
            send(response)
        if current.type == 'recharge':
            response = 'you recharged your health'
            send (response)
##        if health < temp:
##            response = 'you fought a level ' + str(current.mult) +' enemy. you have ' + str(health) + ' health'
##            send(response)
        if (not tempkey and key):
            response = 'you picked up a key'
            send(response)
        
        print(health)
    if(health == 101):
        response = 'you win'
    else:
        response = 'you lose'
    send(response)
        

def send(response):
        global sock  

        try:
             my_str = response
             my_str_as_bytes=str.encode(my_str)
             sock.send(my_str_as_bytes)
        except:
             print('NOO')
        sock.close()
        sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        sock.connect(('10.200.35.31', 8080))

class Controllers:

    def __init__(self, win):
        self.looking = True
        self.win = win
        self.canvas = tk.Canvas(self.win, width = 800, height = 480)
        self.commandList = []
        self.eyeLoc = (300,300)
        self.pupil = 0
        self.botEye = 0
        self.eyeMove()
        self.canvas.pack()

    def eyeMove(self):
         
        c = self.canvas
        c.configure(background = 'black')
        c.pack()
        c.create_oval(0,0,800,480, fill = "white")
        self.pupil = self.canvas.create_oval(150, 150, 275, 300, outline='blue', fill='black', width=70)
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

x = Controller()
thread.start_new_thread(receive,())
window = tk.Tk()
window.geometry("1040x720")
control = Controllers (window)
window.mainloop()

game()

win = 0
lose = 0
