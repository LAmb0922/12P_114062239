from __future__ import annotations
import pygame as pg

from src.sprites import Sprite
from src.core.services import input_manager, resource_manager
from src.utils import Logger
from typing import Callable, override
from .component import UIComponent
import time
from src.interface.components.button import Button
class ChooseYourPokemon(UIComponent):
    img_button: Sprite
    img_button_default: Sprite
    img_button_hover: Sprite
    hitbox: pg.Rect
    on_click: Callable[[], None] | None

    def __init__(
        self,
        img_normal: str, img_hover:str,
        x: int, y: int, width: int, height: int,hp:int,atk:int,
        normal_attack,super_attack,attribute,
        on_click: Callable[[], None] | None = None
        ):
        self.pose="normal"
        self.img = img_normal
        self.img_normal=img_normal
        self.img_hover=img_hover
        self.hitbox = pg.Rect(x, y, width, height)
        #[TODO HACKATHON 1]
        self.on_click = on_click
        self.w=width
        self.h=height
        self.defense=False
        self.skill=[normal_attack,super_attack]
        self.attribute=attribute
        self.chosen=False
        self.atk=atk
        self.hp=hp
        self.hov=False
        self.star= Button(
            "ingame_ui/baricon3.png", "ingame_ui/baricon3.png",
            self.hitbox[0]+50,self.hitbox[1]+50, 50, 50,
            )
    def defense_action(self):
        self.defense=True    
    def attack_action(self):
        return self.atk
    @override
    def update(self, dt: float) -> None:
        self.star.update(dt)

        if self.hitbox.collidepoint(input_manager.mouse_pos):
            self.img = self.img_hover
            self.hov=True
            
            if input_manager.mouse_pressed(1):
                self.img=self.img_hover
                self.chosen=True
        
        else:
            self.hov=False
            if not self.chosen:
                self.img=self.img_normal
    
    @override
    def draw(self, screen: pg.Surface) -> None:
        
        if self.hov:
            font = pg.font.Font("assets/fonts/Minecraft.ttf", 32)
            text_a=font.render(f"atk : {self.atk}", True, (255,255,255))
            text_h=font.render(f"hp  : {self.hp}", True, (255,255,255))
            text_attri=font.render(f"attribite :{self.attribute}", True, (255,255,255))
            text_s=font.render(f"super :{self.skill[1]}", True, (255,255,255))
            _=screen.blit(text_a,(self.hitbox[0]+50,500))
            _=screen.blit(text_h,(self.hitbox[0]+50,540))
            _=screen.blit(text_attri,(self.hitbox[0]+50,580))
            _=screen.blit(text_s,(self.hitbox[0]+50,620))
        
        screen.blit(pg.transform.scale(self.img, (self.w, self.h)), self.hitbox)
        if self.chosen:
            self.star.draw(screen)
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
