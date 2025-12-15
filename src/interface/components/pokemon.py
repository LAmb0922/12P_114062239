from __future__ import annotations
import pygame as pg

from src.sprites import Sprite
from src.core.services import input_manager, resource_manager
from src.utils import Logger
from typing import Callable, override
from .component import UIComponent
import time

class Pokemon(UIComponent):
    img_button: Sprite
    img_button_default: Sprite
    img_button_hover: Sprite
    hitbox: pg.Rect
    on_click: Callable[[], None] | None

    def __init__(
        self,
        img_normal: str, img_attack:str,img_being_attack:str,
        x: int, y: int, width: int, height: int,hp:int,atk:int,
        on_click: Callable[[], None] | None = None
        ):
        self.pose="normal"
        self.img = img_normal
        self.img_normal=img_normal
        self.hitbox = pg.Rect(x, y, width, height)
        self.attack_pose=img_attack
        self.attacked_pose=img_being_attack
        #[TODO HACKATHON 1]
        self.on_click = on_click
        self.hp=hp
        self.atk=atk
        self.pose_timer=0
        self.w=width
        self.h=height
    
        title = ''
        parameter_name = ''
    
        def lookups(self, request, model_admin):
            pass
    
        def queryset(self, request, queryset):
            return queryset
    def attack_player(self):
        self.img=self.attack_pose
        self.pose="attack"
        self.pose_timer=0.5
        return self.atk
    def being_attack(self,val):
        self.hp=max(0,self.hp-val)
        self.img=self.attacked_pose
        self.pose="attacked"
        self.pose_timer=0.5
    @override
    def update(self, dt: float) -> None:
        '''
        [TODO HACKATHON 1]
        Check if the mouse cursor is colliding with the button, 
        1. If collide, draw the hover image
        2. If collide & clicked, call the on_click function
        
        if self.hitbox.collidepoint(input_manager.mouse_pos):
            ...
            if input_manager.mouse_pressed(1) and self.on_click is not None:
                ...
        else:
            ...
        '''

        if self.pose!="normal":
            self.pose_timer-=dt
            if self.pose_timer<=0:
                self.img=self.img_normal
                self.pose="normal"
    
    @override
    def draw(self, screen: pg.Surface) -> None:
        '''
        [TODO HACKATHON 1]
        You might want to change this too
        '''
        _=screen.blit(pg.transform.scale(self.img, (self.w, self.h)), self.hitbox)
        


def main():
    import sys
    import os
    
    pg.init()

    WIDTH, HEIGHT = 800, 800
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    pg.display.set_caption("Button Test")
    clock = pg.time.Clock()
    
    bg_color = (0, 0, 0)
    def on_button_click():
        nonlocal bg_color
        if bg_color == (0, 0, 0):
            bg_color = (255, 255, 255)
        else:
            bg_color = (0, 0, 0)
        
    
    
    running = True
    dt = 0
    
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            input_manager.handle_events(event)
        
        dt = clock.tick(60) / 1000.0
        
        input_manager.reset()
        
        _ = screen.fill(bg_color)
        

        
        pg.display.flip()
    
    pg.quit()


if __name__ == "__main__":
    main()
