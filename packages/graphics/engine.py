from pygame import Surface, SRCALPHA, Rect
from pygame import Vector2
from pygame.draw import rect as draw_rect

from .const import DRAW_SCREEN_SIZE, DRAW_SCREEN_SIZE_X, DRAW_SCREEN_SIZE_Y, \
    TILE_SIZE, SHOW_SOLDIERS_REAL_POS, SHOW_FARMS_REAL_POS, \
    SPRITE_SIZE, SHOW_TURRETS_REAL_POS, MOUSE_TARGET_RADIUS, INFO_TAB_SHOW_TIME, SHOW_REAL_POS
from .camera import Camera
from .assets_loader import AssetsLoader
from .map_renderer import MapRenderer
from ..game_logic.game import Game
from .soldier_rt import SoldierRT
from .object_rt import ObjectRT
from .soldier_tracker import SoldierTracker
from .turret_rt import TurretRT
from .turret_tracker import TurretTracker
from .farm_rt import FarmRT
from .farm_tracker import FarmTracker
from .particle import ParticleController, Particle, BloodParticle
from .font_renderer import FontRenderer

class Engine():
    '''Main graphics class.
    '''

    def __init__(self, game: Game):

        # render surface
        self.__draw_screen = Surface(DRAW_SCREEN_SIZE)
        
        # initialize modules
        self.__map_renderer = MapRenderer(game)
        self.__soldier_tracker = SoldierTracker(game.get_path())
        self.__turret_tracker = TurretTracker()
        self.__farm_tracker = FarmTracker()
        self.__particle_controller = ParticleController()
        self.__font_renderer = FontRenderer()
        self.__camera = Camera(game.get_map_size())

        # assets
        self.__assets_loader = AssetsLoader()
        path = "/".join([dir for dir in __file__.split('\\') if dir != ''][:-1]) + '/' + 'textures'
        self.__assets = self.__assets_loader.load(path, '.png')

        # first render
        self.__map_texture = self.__map_renderer.render(self.__assets, game)

    def render(self, game: Game, game_speed: float) -> Surface:
        '''Main rendering function.

        Refereshes once per frame.
        '''

        # update staff
        self.__camera.update()
        self.__soldier_tracker.update_tracker(game.get_soldiers(), self.__particle_controller)
        self.__soldier_tracker.update_soldiers(game_speed, self.__camera.get_mouse_pos())
        self.__turret_tracker.update_tracker(game.get_turrets())
        self.__turret_tracker.update_turrets(game_speed, self.__camera.get_mouse_pos())
        self.__farm_tracker.update_tracker(game.get_farms())
        self.__farm_tracker.update_farms(game_speed, self.__camera.get_mouse_pos())
        self.__particle_controller.update_particles(game_speed)

        # reset frame
        self.__draw_screen.fill((0, 0, 0))
        self.__draw_screen.blit(self.__map_texture, self.__camera.get_offset())

        # drawing soldiers and their health bars
        for soldier in self.__soldier_tracker.get_soldiers():
            self.__draw_object_rt(soldier)

        # drawing turrets
        for turret in self.__turret_tracker.get_turrets():    
            self.__draw_object_rt(turret)

        # drawing farms
        for farm in self.__farm_tracker.get_farms():
            self.__draw_object_rt(farm)

        # drawing particles
        for particle in self.__particle_controller.get_particles():
            self.__draw_particle(particle)
        
        return self.__draw_screen

    def __draw_object_rt(self, object: ObjectRT):
        
        if object.__class__ == SoldierRT:
            direction = {
                (0, 0):    'bot',
                (0, -1):   'top',
                (0, 1):    'bot',
                (-1, 0):   'left',
                (1, 0):    'right'
            }[(int(object.direction.x), int(object.direction.y))]

            texture = self.__assets['soldiers'][object.name] \
            [object.animation][direction][object.frame]
        elif object.__class__ == FarmRT:
            texture = self.__assets["farms"]["farm"]
        elif object.__class__ == TurretRT:
            texture = self.__assets["turrets"]["turret"]

        size = texture.get_size()

        self.__draw(
            texture,
            object.cords + \
            Vector2(TILE_SIZE // 2, TILE_SIZE - size[1]) \
            - Vector2(size[0], 0) // 2
        )
        
        if object.__class__ == SoldierRT:
            size = texture.get_size()[0] // 2
            bar = Surface((size, 1))
            bar.fill((255, 0, 0))
            self.__draw(bar, object.cords - Vector2(-1, 4))

            bar = Surface((object.actual_hp_rate * size, 1))
            bar.fill((0, 255, 0))
            self.__draw(bar, object.cords - Vector2(-1, 4))

        if object.select_time > 0:
            infos = object.stats
            text_surfaces = [
                self.__font_renderer.render(f'{name}: {info}', 'small')
                for name, info in infos.items()
            ]
            info_tab = Surface((
                max(s.get_size()[0] for s in text_surfaces),
                sum((s.get_size()[1] for s in text_surfaces))
            ), SRCALPHA)
            info_tab.fill((0, 0, 0, 255))
            [
                info_tab.blit(s, (0, sum(s.get_size()[1] for s in text_surfaces[:i])))
                for i, s in enumerate(text_surfaces)
            ]

            draw_rect(info_tab, (0, 0, 0, 0), Rect(
                0, 0, 
                info_tab.get_size()[0] * (1 - min(1, object.select_time / INFO_TAB_SHOW_TIME)),
                info_tab.get_size()[1]
            ))

            self.__draw(
                info_tab,
                object.cords - Vector2(info_tab.get_size()[0], 0)
            )

        # real pos
        if SHOW_REAL_POS:
            surf = Surface((1, 1))
            surf.fill((255, 0, 0))
            self.__draw(surf, object.cords)

    def __draw_particle(self, particle: Particle):
        pos, color, size = particle.get_data()
        surf = Surface((size, size), SRCALPHA)
        surf.fill(color)
        self.__draw(surf, pos)

    def __draw(self, texture: Surface, pos: Vector2) -> None:
        '''Draw texture with camera offset.

        Function only draw objects, which are visible on the screen.
        '''

        size = Vector2(texture.get_size())
        if -size.x <= pos.x + self.__camera.get_offset().x <= DRAW_SCREEN_SIZE_X and \
            -size.y <= pos.y + self.__camera.get_offset().y <= DRAW_SCREEN_SIZE_Y:
            self.__draw_screen.blit(texture, pos + self.__camera.get_offset())