from __future__ import annotations
import pygame as pg
from src.interface.components.button import Button
from src.sprites import Sprite
from src.core.services import input_manager, resource_manager
from src.utils import Logger
from typing import Callable, override
from .component import UIComponent
import time
import random

class BattlePokemon(UIComponent):
    img_button: Sprite
    img_button_default: Sprite
    img_button_hover: Sprite
    hitbox: pg.Rect
    on_click: Callable[[], None] | None

    def __init__(
        self,
        img_normal: str,img_atk:list[str],
        x: int, y: int, width: int, height: int,hp:int,atk:int,
        normal_attack,super_attack,attribute,name,max,
        on_click: Callable[[], None] | None = None
        ):
        self.pose="normal"
        self.max_hp=max
        self.img = img_normal
        self.img_normal=img_normal
        self.img_attack=img_atk
        self.hitbox = pg.Rect(x, y, width, height)
        #[TODO HACKATHON 1]
        self.on_click = on_click
        self.w=width
        self.h=height
        self.defense=False
        self.skill=[normal_attack,super_attack]
        self.attribute=attribute
        self.can_be_chosen=False
        self.chosen=False
        self.atk=atk
        self.hp=hp
        self.animate_timer=0
        self.hov=False
        self.can_be_hov=False
        self.name=name
        self.defense_buff=0
        self.berserker=False
        self.change_frame=True
        self.fire=self.make_pokemon_image("assets/images/attack/attack5.png")
        self.star= Button(
            "ingame_ui/baricon3.png", "ingame_ui/baricon3.png",
            self.hitbox[0]+50,self.hitbox[1]+50, 50, 50,
            )
        self.shield=Button(
            "ingame_ui/options2.png", "ingame_ui/options2.png",
            self.hitbox[0],self.hitbox[1]+150, 50, 50,
            )
        
        self.fire1= [pg.transform.scale(f, (160, 160)) for f in self.fire]
        self.fire2= [pg.transform.scale(f, (50, 50)) for f in self.fire]
        self.fire3= [pg.transform.scale(f, (100, 100)) for f in self.fire]
    def attack_action(self):
        return self.atk
    def make_pokemon_image(self,path):
        sheet = pg.image.load(path)
        sheet_width = sheet.get_width()
        sheet_height = sheet.get_height()
        frame_width = sheet_width // 4
        frames = []
        for i in range(4):
            frame_rect = pg.Rect(i * frame_width, 0, frame_width, sheet_height)
            frame = sheet.subsurface(frame_rect).copy()
            frames.append(frame)
        return frames
    @override
    def update(self, dt: float) -> None:
        self.star= Button(
            "ingame_ui/baricon3.png", "ingame_ui/baricon3.png",
            self.hitbox[0]+50,self.hitbox[1]+50, 50, 50,
            )
        self.shield=Button(
            "ingame_ui/options2.png", "ingame_ui/options2.png",
            self.hitbox[0]-30,self.hitbox[1]+150, 50, 50,
            )
        if self.hitbox.collidepoint(input_manager.mouse_pos ):
            self.hov=True
            if input_manager.mouse_pressed(1) and self.on_click is not None:
                self.on_click()
                if self.can_be_chosen:
                    self.chosen=True
        else:
            self.img_button = self.img_normal
            self.hov=False
    @override
    def draw(self, screen: pg.Surface) -> None:
        
        
        if self.hp>0:    
            screen.blit(pg.transform.scale(self.img, (self.w, self.h)), self.hitbox)
        
            if self.chosen:
                self.star.draw(screen)
            if self.defense:
                self.shield.draw(screen)
            if self.berserker:
                if self.animate_timer<=4:
                    if self.change_frame:
                        size=random.randint(30,150)
                        self.frames=[pg.transform.scale(f, (size,size )) for f in self.fire]
                        self.fire_dx=random.randint(75,150)
                        self.fire_dy=random.randint(150,200)
                        self.change_frame=False
                    speed=random.random()*0.2
                    screen.blit(self.frames[int(self.animate_timer)], (self.hitbox[0]+self.fire_dx, self.hitbox[1]+self.fire_dy))
                    self.animate_timer+=speed
                else:
                    self.change_frame=True
                    self.animate_timer=0
            if self.hov:
                font = pg.font.Font("assets/fonts/Minecraft.ttf", 24)
                text_a=font.render(f"atk : {self.atk}", True, (255,255,255))
                text_h=font.render(f"hp  : {self.hp}", True, (255,255,255))
                
                _=screen.blit(text_a,(self.hitbox[0]-20,self.hitbox[1]+5))
                _=screen.blit(text_h,(self.hitbox[0]-20,self.hitbox[1]+45))
            
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
