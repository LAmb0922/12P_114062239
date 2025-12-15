from __future__ import annotations
import pygame as pg
from typing import Protocol

class UIComponent(Protocol):
    def update(self, dt: float) -> None: ...
    def draw(self, screen: pg.Surface) -> None: ...

MonsterInfoType = UIComponent
ItemInfoType = UIComponent

import pygame as pg

from src.sprites import Sprite
from src.core.services import input_manager
from src.core.services import sound_manager
from src.utils import Logger
from typing import Callable, override
from .component import UIComponent
from src.utils import GameSettings

class Slider(UIComponent):
    
    def __init__(
        self,
        img_path: str, img_hovered_path:str,max_x: int, min_x:int,
        x: int, y: int, width: int, height: int,
        on_click: Callable[[], None] | None = None
    ):
        self.img_button_default = Sprite(img_path, (width, height))
        self.hitbox = pg.Rect(x, y, width, height)
        self.x=x
        self.y=y
        self.min_x=min_x
        self.max_x=max_x
        self.w=width
        self.h=height
        #[TODO HACKATHON 1]
        self.dragging=False
        
        self.img_button_hover = Sprite(img_hovered_path,(width,height))
        self.img_button = self.img_button_default
        self.on_click = on_click
        

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

        if self.hitbox.collidepoint(input_manager.mouse_pos ):
            self.img_button = self.img_button_hover
            if input_manager.mouse_down(1):
                self.dragging=True
                if  self.on_click is not None:
                    self.on_click()
                
                    
        else:
            self.img_button = self.img_button_default
        if input_manager.mouse_released(1):
            self.dragging=False
        
        if self.dragging:
            self.hitbox.x=max(self.min_x,min(self.max_x,input_manager.mouse_pos[0]-20))
        GameSettings.change_volume((self.hitbox.x-self.min_x)/(self.max_x-self.min_x))
        if sound_manager.current_bgm:
            sound_manager.current_bgm.set_volume(GameSettings.AUDIO_VOLUME)
        
    @override
    def draw(self, screen: pg.Surface) -> None:
        '''
        [TODO HACKATHON 1]
        You might want to change this too
        '''
        _=screen.blit(self.img_button.image, self.hitbox)
        


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
class Switch(UIComponent):
    
    def __init__(
        self,
        img_path: str, img_on_path:str,
        x: int, y: int, width: int, height: int,
        on_click: Callable[[], None] | None = None
    ):
        self.img_button_off = Sprite(img_path, (width, height))
        self.img_button_on=Sprite(img_on_path,(width, height))
        self.hitbox = pg.Rect(x, y, width, height)
        self.x=x
        self.y=y
        
        self.w=width
        self.h=height
        #[TODO HACKATHON 1]
        self.dragging=False
        
        
        self.img_button = self.img_button_off
        self.on_click = on_click
        
    
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

        if self.hitbox.collidepoint(input_manager.mouse_pos ):
            if input_manager.mouse_pressed(1):
                if self.img_button==self.img_button_off:
                    self.img_button=self.img_button_on
                    sound_manager.stop_all_sounds()
                else:
                    self.img_button=self.img_button_off
                    sound_manager.play_bgm("RBY 103 Pallet Town.ogg")
                
                    
        
        
        
        
        
        
        
    @override
    def draw(self, screen: pg.Surface) -> None:
        '''
        [TODO HACKATHON 1]
        You might want to change this too
        '''
        _=screen.blit(self.img_button.image, self.hitbox)
        


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
