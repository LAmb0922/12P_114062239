import pygame as pg
from src.core.managers import GameManager
from src.utils import GameSettings
from src.sprites import BackgroundSprite
from src.scenes.scene import Scene
from src.interface.components import Button
from src.core.services import scene_manager, sound_manager, input_manager,resource_manager
from typing import override
from src.interface.components.pokemon import Pokemon
import time
from src.scenes.choose_scene import ChooseScene
class NewBattleScene(Scene):
    # Background Image
    background: BackgroundSprite
    # Buttons
    play_button: Button
    
    def __init__(self):
        super().__init__()
        self.background = BackgroundSprite("backgrounds/background1.png")
        self.states=["use item","attack","defend"]
        self.state=None  
        self.game_manager=GameManager.load("./saves/game0.json")
        
    @override
    def enter(self) -> None:
        sound_manager.play_bgm("RBY 107 Battle! (Trainer).ogg")
        self.game_manager=GameManager.load("./saves/game0.json")
    def draw_interacter(self,screen:pg.Surface):
        width, height = screen.get_size()
        mask_rect = pg.Rect(0,height*(4/5),width,height/5)
        pg.draw.rect(screen,(0,0,0),mask_rect)
        pg.draw.rect(screen,(255,255,255),mask_rect,width=4)    


    @override
    def exit(self) -> None:
        self.game_manager.save("./saves/game0.json")

    @override
    def update(self, dt: float) -> None:
        if input_manager.key_pressed(pg.K_ESCAPE):
            scene_manager.change_scene("game")
            return
        
            
        
        

    @override
    def draw(self, screen: pg.Surface) -> None:
        self.background.draw(screen)
        font = pg.font.Font("assets/fonts/Minecraft.ttf", 32)
        self.draw_interacter(screen)

