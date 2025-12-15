from __future__ import annotations
import pygame as pg
import copy
from src.sprites import Sprite
from src.core.services import input_manager
from src.utils import Logger
from typing import Callable, override
from .component import UIComponent
import random
class SpecialButton(UIComponent):
    img_button: Sprite
    img_button_default: Sprite
    img_button_hover: Sprite
    hitbox: pg.Rect
    on_click: Callable[[], None] | None

    def __init__(
        self,
        img_path: str, img_hovered_path:str,
        x: int, y: int, width: int, height: int,massage:str,
        on_click: Callable[[], None] | None = None
    ):
        
        self.img_button_default = Sprite(img_path, (width, height)).image
        self.hitbox = pg.Rect(x, y, width, height)
        self.massage=massage
        #[TODO HACKATHON 1]
        dark = pg.Surface(self.img_button_default.get_size(), pg.SRCALPHA)
        dark.fill((0, 0, 0, 120))  
        
        self.img_button_cd = self.img_button_default.copy()
        self.img_button_cd.blit(dark, (0, 0))
        self.img_button_hover = Sprite(img_hovered_path,(width,height)).image
        self.img_button = self.img_button_default
        self.on_click = on_click
        if self.massage=="ice sword rain" or self.massage=="digger steal" or self.massage=="fire berserker" or self.massage=="forest legacy":
            self.cd=random.randint(1,3)
        else:
            self.cd=0
        self.font_size=36
        self.click_move=0
        self.count=1
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
        if self.cd>0 or self.count<=0:
            self.img_button=self.img_button_cd
        elif self.hitbox.collidepoint(input_manager.mouse_pos ):
            self.img_button = self.img_button_hover
            self.click_move=-6
            if input_manager.mouse_pressed(1) and self.on_click is not None:
                self.on_click()
        else:
            self.click_move=0
            self.img_button = self.img_button_default
    
    @override
    def draw(self, screen: pg.Surface) -> None:
        '''
        [TODO HACKATHON 1]
        You might want to change this too
        '''
        _=screen.blit(self.img_button, self.hitbox)
        font = pg.font.Font("assets/fonts/Minecraft.ttf", self.font_size)
        
        text=font.render(f"{self.massage}", True, (0,0,0))
        text_length=text.get_width()
        text_height=text.get_height()
        get_to_middle=[(self.hitbox[2]-text_length)//2,(self.hitbox[3]-text_height)//2]
        _=screen.blit(text,(self.hitbox[0]+get_to_middle[0]+5,self.hitbox[1]+get_to_middle[1]+self.click_move+5))
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
