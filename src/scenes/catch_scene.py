import pygame as pg

from src.utils import GameSettings
from src.sprites import BackgroundSprite
from src.scenes.scene import Scene
from src.interface.components import Button
from src.core.services import scene_manager, sound_manager, input_manager,resource_manager
from typing import override
from src.interface.components.pokemon import Pokemon
from src.interface.components.wild_pokemon import WildPokemon
import time
class CatchScene(Scene):
    # Background Image
    background: BackgroundSprite
    # Buttons
    play_button: Button
    
    def __init__(self):
        self.enemy_attack_timer=0
        super().__init__()
        self.background = BackgroundSprite("backgrounds/background1.png")
        sheet = pg.image.load("assets/images/sprites/sprite5_attack.png")
        sheet_width = sheet.get_width()
        sheet_height = sheet.get_height()
        frame_width = sheet_width // 4
        frames = []
        self.leaving_timer=0
        for i in range(4):
            frame_rect = pg.Rect(i * frame_width, 0, frame_width, sheet_height)
            frame = sheet.subsurface(frame_rect).copy()
            frames.append(frame)
        self.bird=WildPokemon(frames[1],frames[0],frames[2],
                    800, 0, 500, 500,self.leave)#(x,y,w,h,hp,atk)
    @override
    def enter(self) -> None:
        sound_manager.play_bgm("RBY 107 Battle! (Trainer).ogg")
        self.leaving_timer=0
        self.bird.catched=False
    def leave(self):
        self.leaving_timer=2
        

        
        
        
    
        


    @override
    def exit(self) -> None:
        pass

    @override
    def update(self, dt: float) -> None:
        if input_manager.key_pressed(pg.K_ESCAPE):
            scene_manager.change_scene("game")
            return
        self.bird.update(dt)
        
        if self.leaving_timer>0:
            self.leaving_timer-=dt
        if self.leaving_timer<0:
            scene_manager.change_scene("game")
        print(self.leaving_timer)
            
        
        
        

    @override
    def draw(self, screen: pg.Surface) -> None:
        self.background.draw(screen)
        font = pg.font.Font("assets/fonts/Minecraft.ttf", 32)
        text_l=font.render(f"Press Esc to leave", True, (255,255,255))
        _=screen.blit(text_l,(200,600))

        if self.bird.catched:
            font = pg.font.Font("assets/fonts/Minecraft.ttf", 256)
            text_c=font.render(f"CATCH", True, (255,255,255))
            _=screen.blit(text_c,(0,300))

        
        
        
        self.bird.draw(screen)

