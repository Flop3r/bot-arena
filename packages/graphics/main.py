from pygame import init, WINDOWCLOSE
from pygame.display import set_mode as display_set_mode, update as display_update
from pygame.time import Clock
from pygame.event import get as get_event
from pygame.transform import scale 

from .const import SCREEN_SIZE, FRAMERATE, STANDARD_FRAMERATE
from .engine import Engine
from ..game_logic.game import Game

class Main:
    def __init__(self):
        init()
        self.screen = display_set_mode(SCREEN_SIZE)
        self.is_running = True
        self.dt = 1
        self.clock = Clock()
        self.game = Game()
        self.engine = Engine(self.game)
        

        while self.is_running:
            self.is_running = WINDOWCLOSE not in map(lambda e: e.type, get_event())
            # self.game.update()
            self.__screen_update()

    def __screen_update(self):
        '''Refreshes screen and update frame clock.
        '''

        self.dt = self.clock.tick(FRAMERATE) * STANDARD_FRAMERATE / 1000
        self.screen.blit(scale(self.engine.render(self.game), SCREEN_SIZE), (0, 0))
        display_update()

    

if __name__ == "__main__":
    Main()
