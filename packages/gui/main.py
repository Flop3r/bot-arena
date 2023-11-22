from .game_render.main import Main as GameRender
from .map_generate.map_generate_main import Main as MapGenerate
from pygame import init

from time import sleep

class Main():
    def __init__(self, log_name: str):
        init()
        sleep(1)
        MapGenerate()
        sleep(1)
        game_name = input("Game name: ")
        GameRender('example_log.txt', game_name)


        

        