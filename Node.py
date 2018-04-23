import random

key = False

class Node:
    def __init__(self):
        self.edges = {}

    def getConnections(self):
        options = ''
        for key, value in self.edges.items():
            options += key + ' '
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
        super().__init__()
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
        super().__init__ ()

    def action(self, health):
        return 100

class End(Node):
    def __init__(self):
        super().__init__()

    def action(self, health):
        if key:
            return 101
        else:
            return health


n2 = End()
n3 = Enemy(1, False)
n1 = Node()
n4 = Enemy(1, True)
n5 = Recharge()
current = n1
health = 100

n1.setEdges({'south': n3})
n2.setEdges({'east': n3})
n3.setEdges({'south':n5, 'north': n1, 'west': n2, 'east': n4})
n4.setEdges({'west': n3})
n5.setEdges({'north': n3})

while health > 0 and health < 101:
    dir = 'weast'
    while not current.isValid(dir):
        dir = input (current.getConnections())
    current = current.edges.get(dir)
    health = current.action(health)
    print(health)

win = 0
lose = 0
