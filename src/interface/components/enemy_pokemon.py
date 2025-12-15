from __future__ import annotations
import pygame as pg

from src.sprites import Sprite
from src.core.services import input_manager, resource_manager
from src.utils import Logger
from typing import Callable, override
from .component import UIComponent
import time
import random

class EnemyPokemon(UIComponent):
    img_button: Sprite
    img_button_default: Sprite
    img_button_hover: Sprite
    hitbox: pg.Rect
    on_click: Callable[[], None] | None

    def __init__(
        self,
        img_normal: str,img_evolve:str,img_attack,
        x: int, y: int, width: int, height: int,hp:int,atk:int,
        normal_attack,super_attack,attribute,name,fly,
        on_click: Callable[[], None] | None = None
        ):
        self.pose="normal"
        self.img = img_normal
        self.img_normal=img_normal
        self.img_evolve=img_evolve
        self.img_attack=img_attack
        self.hitbox = pg.Rect(x, y, width, height)
        #[TODO HACKATHON 1]
        self.on_click = on_click
        self.w=width
        self.h=height
        self.skill=[normal_attack,super_attack]
        self.attribute=attribute
        self.chosen=False
        self.atk=atk
        self.hp=hp
        self.hov=False
        self.name=name
        self.fly=fly
        self.up=True
        self.left=True
        self.evolve=False
        self.d=True
        self.can_be_chosen=False
    def attack_action(self):
        return self.atk
    @override
    def update(self, dt: float) -> None:
        if self.hitbox.collidepoint(input_manager.mouse_pos ):
            self.hov=True
            if input_manager.mouse_pressed(1) and self.on_click is not None:
                self.on_click()
                if self.can_be_chosen:
                    self.chosen=True
        else:
            self.hov=False
        if self.fly:
            if self.up:
                if self.d:
                    self.hitbox[1]+=1
                    self.d=False
                    if self.hitbox[1]>=110:
                        self.up=False
                else:
                    self.d=True
            if not self.up:
                if self.d:
                    self.hitbox[1]-=1
                    self.d=False
                    if self.hitbox[1]<=90:
                        self.up=True
                else:
                    self.d=True
        if self.evolve:
            self.img=self.img_evolve
        else:
            self.img=self.img_normal
    @override
    def draw(self, screen: pg.Surface) -> None:
        if self.hp>0:
            if self.hov:
                font = pg.font.Font("assets/fonts/Minecraft.ttf", 24)
                text_a=font.render(f"atk : {self.atk}", True, (255,255,255))
                text_h=font.render(f"hp  : {self.hp}", True, (255,255,255))
            
                _=screen.blit(text_a,(self.hitbox[0]-50,self.hitbox[1]+130))
                _=screen.blit(text_h,(self.hitbox[0]-50,self.hitbox[1]+170))
            
            screen.blit(pg.transform.scale(self.img, (self.w, self.h)), self.hitbox)
        
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
