import os
import json
import random

class BOT():
    def __init__(self): 
        game_timeout, move_timeout, ready_timeout, side = input().split()
        self.game_timeout = game_timeout
        self.move_timeout = move_timeout
        self.ready_timeout = ready_timeout
        self.side = side

        map_name = input()
        map = os.path.dirname(__file__)
        map = os.path.dirname(map)
        map = os.path.join(map, "maps", map_name)
        map = json.load(open(map, "r"))
        self.map = map

        self.preprocess()

        print("READY")

        while True:
            move = self.make_move()
            print(move)
            message = input()

            if message == "END":
                break

            self.update(message)

    # user defined functions  
    def preprocess(self):
        pass

    def update(self, message):
        pass

    def make_move(self):
        x = random.randint(0, self.map["MAP_SIZE_X"] - 1)
        y = random.randint(0, self.map["MAP_SIZE_Y"] - 1)

        move = random.choice(['W', 'T', 'F', 'S'])
        import sys 
        print("RAND", file=sys.stderr)
        if move == 'W':
            return f'W'
        elif move == 'T':
            return f'T {x} {y}'
        elif move == 'F':
            return f'F {x} {y}'
        elif move == 'S':
            return f'S {random.choice(["swordsman", "archer"])}'
        else:
            return f'W'

while True:
    BOT()