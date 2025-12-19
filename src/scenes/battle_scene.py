import pygame as pg

from src.utils import GameSettings
from src.sprites import BackgroundSprite
from src.scenes.scene import Scene
from src.interface.components import Button
from src.core.services import scene_manager, sound_manager, input_manager,resource_manager
from typing import override
from src.interface.components.pokemon import Pokemon
import time
class BattleScene(Scene):
    # Background Image
    background: BackgroundSprite
    # Buttons
    play_button: Button
    
    def __init__(self):
        self.enemy_attack_timer=0
        super().__init__()
        self.background = BackgroundSprite("backgrounds/background1.png")
        self.win=None
        sheet = pg.image.load("assets/images/sprites/sprite5_attack.png")
        sheet_width = sheet.get_width()
        sheet_height = sheet.get_height()
        frame_width = sheet_width // 4
        frames = []
        self.hp=200
        self.atk=50
        self.bird_attack=True
        self.flashing_timer=0
        self.leaving_timer=0
        
        for i in range(4):
            frame_rect = pg.Rect(i * frame_width, 0, frame_width, sheet_height)
            frame = sheet.subsurface(frame_rect).copy()
            frames.append(frame)
        self.bird=Pokemon(frames[1],frames[2],frames[0],
                    800, 0, 500, 500,300,30)#(x,y,w,h,hp,atk)
    def battle(self):
        
        if input_manager.key_released(pg.K_a) and self.bird_attack:
            self.bird.being_attack(self.atk)
            self.bird_attack=False
            self.enemy_attack_timer = 1.5
        
        if self.bird.hp<=0 and self.win==None:
            self.win=True
            self.leaving_timer=2
            return True
        if self.hp<=0 and self.win==None:
            self.win=False
            self.leaving_timer=2
            
    @override
    def enter(self) -> None:
        sound_manager.play_bgm("RBY 107 Battle! (Trainer).ogg")
        
        self.hp = 200
        self.bird.hp = 300
        self.win = None  
        self.flash_red = False
        self.flash_timer = 0.0
        self.enemy_attack_timer = 0.0
        self.bird_attack=True
        self.flashing_timer=0
        self.hp=200
        self.atk=50
    
        


    @override
    def exit(self) -> None:
        pass

    @override
    def update(self, dt: float) -> None:
        if input_manager.key_pressed(pg.K_ESCAPE):
            scene_manager.change_scene("game")
            return
        self.bird.update(dt)
        self.battle()
        if self.enemy_attack_timer > 0 and self.win==None:
            self.enemy_attack_timer -= dt  
            if self.enemy_attack_timer <= 0 and self.bird.hp > 0 :
                self.bird_attack=True
                self.flashing_timer=0.5
                self.hp = max(0, self.hp - self.bird.attack_player())
        if self.flashing_timer>0:
            self.flashing_timer-=dt
        if self.leaving_timer>0:
            self.leaving_timer-=dt
        if self.leaving_timer<=0 and self.win!=None:
            scene_manager.change_scene("game")
            
        
        
        

    @override
    def draw(self, screen: pg.Surface) -> None:
        self.background.draw(screen)
        font = pg.font.Font("assets/fonts/Minecraft.ttf", 32)
        text_e=font.render(f"Press Esc to escape", True, (255,255,255))
        text_a=font.render(f"Press A to attack", True, (255,255,255))
        text_bird_hp=font.render(f"enemy_hp:{self.bird.hp}",True,(255,255,255))
        text_your_hp=font.render(f"your_hp:{self.hp}",True,(255,255,255))
        text_w=font.render(f"your win",True,(255,255,255))
        text_l=font.render(f"your lose",True,(255,255,255))
        _=screen.blit(text_e,(200,400))
        _=screen.blit(text_a,(200,500))
        _=screen.blit(text_bird_hp,(200,600))
        _=screen.blit(text_your_hp,(200,650))
        if self.flashing_timer > 0:
            flash_surface = pg.Surface(screen.get_size())
            flash_surface.fill((255, 0, 0))
            flash_surface.set_alpha(128)  
            screen.blit(flash_surface, (0, 0))
        if self.win==True:
            _=screen.blit(text_w,(300,300))
        elif self.win==False:
            _=screen.blit(text_l,(300,300))
        self.bird.draw(screen)

