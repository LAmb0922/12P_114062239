import pygame as pg
import pytmx
from src.core import GameManager
from src.utils import load_tmx, Position, GameSettings, PositionCamera, Teleport,Logger


class Map:
    # Map Properties
    path_name: str
    tmxdata: pytmx.TiledMap
    # Position Argument
    spawn: Position
    teleporters: list[Teleport]
    # Rendering Properties
    _surface: pg.Surface
    _collision_map: list[pg.Rect]

    def __init__(self, path: str, tp: list[Teleport], spawn: Position):
        self.path_name = path
        self.tmxdata = load_tmx(path)
        self.spawn = spawn
        self.teleporters = tp
        self._minimap_surface = None
        pixel_w = self.tmxdata.width * GameSettings.TILE_SIZE
        pixel_h = self.tmxdata.height * GameSettings.TILE_SIZE

        # Prebake the map
        self._surface = pg.Surface((pixel_w, pixel_h), pg.SRCALPHA)
        self._render_all_layers(self._surface)
        # Prebake the collision map
        self._collision_map = self._create_collision_map()
        self.bush=self.create_bush() 
        
        
    def update(self, dt: float):
        pass
    def create_minimap(self, mini_width: int, mini_height: int):
        minimap = pg.transform.scale(self._surface, (mini_width, mini_height))
        bordered = pg.Surface((mini_width + 4, mini_height + 4))
        bordered.fill((255, 255, 255))
        bordered.blit(minimap, (2, 2))
        self._minimap_surface = bordered

    def draw_minimap(self, screen: pg.Surface, x: int = 10, y: int = 10):
        if self._minimap_surface:
            screen.blit(self._minimap_surface, (x, y))
            
    def draw(self, screen: pg.Surface, camera: PositionCamera):
        screen.blit(self._surface, camera.transform_position(Position(0, 0)))
        
        # Draw the hitboxes collision map
        if GameSettings.DRAW_HITBOXES:
            for rect in self._collision_map:
                pg.draw.rect(screen, (255, 0, 0), camera.transform_rect(rect), 1)
        
    def check_collision(self, rect: pg.Rect) -> bool:
        '''
        [TODO HACKATHON 4]
        Return True if collide if rect param collide with self._collision_map
        Hint: use API colliderect and iterate each rectangle to check
        '''
        for collision_rect in self._collision_map:
            if rect.colliderect(collision_rect):
                return True
        return False
        
    def check_teleport(self, pos: Position) -> Teleport | None:
        '''[TODO HACKATHON 6] 
        Teleportation: Player can enter a building by walking into certain tiles defined inside saves/*.json, and the map will be changed
        Hint: Maybe there is an way to switch the map using something from src/core/managers/game_manager.py called switch_... 
        '''
        for tp in self.teleporters:
            
            if tp.pos.x-50<=pos.x and pos.x<=tp.pos.x+50 and tp.pos.y-50<=pos.y and tp.pos.y+50>=pos.y:
                self.spawn=Position(pos.x,pos.y)
                return tp
        return None
        

    def _render_all_layers(self, target: pg.Surface) -> None:
        for layer in self.tmxdata.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                self._render_tile_layer(target, layer)
            # elif isinstance(layer, pytmx.TiledImageLayer) and layer.image:
            #     target.blit(layer.image, (layer.x or 0, layer.y or 0))

    def _render_tile_layer(self, target: pg.Surface, layer: pytmx.TiledTileLayer) -> None:
        for x, y, gid in layer:
            if gid == 0:
                continue
            image = self.tmxdata.get_tile_image_by_gid(gid)
            if image is None:
                continue

            image = pg.transform.scale(image, (GameSettings.TILE_SIZE, GameSettings.TILE_SIZE))
            target.blit(image, (x * GameSettings.TILE_SIZE, y * GameSettings.TILE_SIZE))
    
    def _create_collision_map(self) -> list[pg.Rect]:
        rects = []
        for layer in self.tmxdata.visible_layers:
            
            if isinstance(layer, pytmx.TiledTileLayer) and ("collision" in layer.name.lower() or "house" in layer.name.lower()):
                for x, y, gid in layer:
                    if gid != 0:
                        '''
                        [TODO HACKATHON 4]
                        rects.append(pg.Rect(...))
                        Append the collision rectangle to the rects[] array
                        Remember scale the rectangle with the TILE_SIZE from settings
                        '''
                        rects.append(pg.Rect(x * GameSettings.TILE_SIZE,y * GameSettings.TILE_SIZE,GameSettings.TILE_SIZE,GameSettings.TILE_SIZE))
        return rects
    def create_bush(self):
        bush=[]
        for layer in  self.tmxdata.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer) and "PokemonBush" in layer.name:
                for x, y, gid in layer:
                    if gid != 0:
                        bush.append(pg.Rect(x * GameSettings.TILE_SIZE,y * GameSettings.TILE_SIZE,GameSettings.TILE_SIZE,GameSettings.TILE_SIZE))
        return bush
    @classmethod
    def from_dict(cls, data: dict) -> "Map":
        tp = [Teleport.from_dict(t) for t in data["teleport"]]
        pos = Position(data["player"]["x"] * GameSettings.TILE_SIZE, data["player"]["y"] * GameSettings.TILE_SIZE)
        return cls(data["path"], tp, pos)

    def to_dict(self):
        return {
            "path": self.path_name,
            "teleport": [t.to_dict() for t in self.teleporters],
            "player": {
                "x": self.spawn.x // GameSettings.TILE_SIZE,
                "y": self.spawn.y // GameSettings.TILE_SIZE,
            }
        }
