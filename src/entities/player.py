from __future__ import annotations
import pygame as pg
from .entity import Entity_one
from src.core.services import input_manager
from src.utils import Position, PositionCamera, GameSettings, Logger
from src.core import GameManager
import math
from typing import override
from src.utils import Position, PositionCamera, Direction, GameSettings 

class Player(Entity_one):
    speed: float = 4.0 * GameSettings.TILE_SIZE
    game_manager: GameManager

    def __init__(self, x: float, y: float, game_manager: GameManager) -> None:
        super().__init__(x, y, game_manager)
        self.on_ice=False
    @override
    def update(self, dt: float) -> None:
        
        dis = Position(0, 0)
        if input_manager.key_down(pg.K_LEFT) or input_manager.key_down(pg.K_a):
            dis.x -= self.speed
            self.direction="left"
            self.animation.switch("left")
            self.animation.walk()
        if input_manager.key_down(pg.K_RIGHT) or input_manager.key_down(pg.K_d):
            dis.x += self.speed
            self.animation.switch("right")
            self.direction="right"
            self.animation.walk()
        if input_manager.key_down(pg.K_UP) or input_manager.key_down(pg.K_w):
            dis.y -= self.speed
            self.animation.switch("up")
            self.direction="up"
            self.animation.walk()
        if input_manager.key_down(pg.K_DOWN) or input_manager.key_down(pg.K_s):
            dis.y += self.speed
            self.animation.switch("down")
            self.direction="down"
            self.animation.walk()
        if not(input_manager.key_down(pg.K_DOWN) or input_manager.key_down(pg.K_s) or input_manager.key_down(pg.K_UP) or input_manager.key_down(pg.K_w) or input_manager.key_down(pg.K_RIGHT) or input_manager.key_down(pg.K_d) or input_manager.key_down(pg.K_LEFT) or input_manager.key_down(pg.K_a)):
            self.animation.moving=False
        dis.x *= dt
        dis.y *= dt
        if dis.x != 0 and dis.y != 0:
            norm = (dis.x ** 2 + dis.y ** 2) ** 0.5
            dis.x = (dis.x / norm) * self.speed * dt
            dis.y = (dis.y / norm) * self.speed * dt
        self.position.x += dis.x*0.3
        self.position.y += dis.y*0.3

        

        '''
        [TODO HACKATHON 2]
        Calculate the distance change, and then normalize the distance
        
        [TODO HACKATHON 4]
        Check if there is collision, if so try to make the movement smooth
        Hint #1 : use entity.py _snap_to_grid function or create a similar function
        Hint #2 : Beware of glitchy teleportation, you must do
                    1. Update X
                    2. If collide, snap to grid
                    3. Update Y
                    4. If collide, snap to grid
                instead of update both x, y, then snap to grid
        
        if input_manager.key_down(pg.K_LEFT) or input_manager.key_down(pg.K_a):
            dis.x -= ...
        if input_manager.key_down(pg.K_RIGHT) or input_manager.key_down(pg.K_d):
            dis.x += ...
        if input_manager.key_down(pg.K_UP) or input_manager.key_down(pg.K_w):
            dis.y -= ...
        if input_manager.key_down(pg.K_DOWN) or input_manager.key_down(pg.K_s):
            dis.y += ...
        
        self.position = ... 
        
        '''
        rect = pg.Rect(self.position.x, self.position.y, GameSettings.TILE_SIZE, GameSettings.TILE_SIZE)
        rect.x += dis.x
        if self.game_manager.check_collision(rect):
            if dis.x > 0:
                rect.right = (rect.right//64)*64
            elif dis.x < 0:
                rect.left = (rect.left//64+1)*64
            dis.x = 0
        self.position.x = float(rect.x)
        rect.y += dis.y
        if self.game_manager.check_collision(rect):
            if dis.y > 0:
                rect.bottom = (rect.bottom//64)*64
            elif dis.y < 0:
                rect.top = (rect.top//64 + 1)*64
            dis.y = 0
        self.position.y = float(rect.y)

    # --- Check teleportation ---
        tp = self.game_manager.current_map.check_teleport(self.position)
        if tp:
            dest = tp.destination
            self.game_manager.switch_map(dest)

        super().update(dt)
        
        # Check teleportation
        
        
    @override
    def draw(self, screen: pg.Surface, camera: PositionCamera) -> None:
        super().draw(screen, camera)
        
    @override
    def to_dict(self) -> dict[str, object]:
        return super().to_dict()
    
    @classmethod
    @override
    def from_dict(cls, data: dict[str, object], game_manager: GameManager) -> Player:
        return cls(data["x"] * GameSettings.TILE_SIZE, data["y"] * GameSettings.TILE_SIZE, game_manager)

