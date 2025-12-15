'''
[TODO HACKATHON 5]
Try to mimic the menu_scene.py or game_scene.py to create this new scene
'''
import pygame as pg

from src.utils import GameSettings
from src.sprites import BackgroundSprite
from src.scenes.scene import Scene
from src.interface.components import Button
from src.core.services import scene_manager, sound_manager, input_manager 
from typing import override
from src.interface.components.component import Slider , Switch
class SettingScene(Scene):
    # Background Image
    background: BackgroundSprite
    # Buttons
    settingbutton_button: Button
    
    def __init__(self):
        super().__init__()
        self.background = BackgroundSprite("backgrounds/background1.png")

        px, py = GameSettings.SCREEN_WIDTH // 2, GameSettings.SCREEN_HEIGHT * 3 // 4
        self.back_button = Button(
            "UI/button_back.png", "UI/button_back_hover.png",
            px -200, py, 100, 100,
            lambda: scene_manager.change_scene("menu")
        )
        mx, my = GameSettings.SCREEN_WIDTH // 2, GameSettings.SCREEN_HEIGHT * 3 // 4
        self.board_button = Button(
            "UI/raw/UI_Flat_Frame03a.png", "UI/raw/UI_Flat_Frame03a.png",
            px -450, py-500, 800, 500,
           # lambda: scene_manager.change_scene("menu")
        )
        self.slider_bar=Slider(
            "UI/raw/UI_Flat_ToggleOff02a.png","UI/raw/UI_Flat_ToggleOn01a.png",
            px+200,px-350,px-350+GameSettings.AUDIO_VOLUME*(550), py-300,50,20,
            
        )
        self.line_bar = Button(
            "UI/raw/UI_Flat_BarFill01f.png", "UI/raw/UI_Flat_BarFill01f.png",
            px -320, py-300, 550, 20,
            #lambda: scene_manager.change_scene("game")
        )
        self.mute_switch = Switch(
            "UI/raw/UI_Flat_ToggleOff03a.png", "UI/raw/UI_Flat_ToggleOn03a.png",
            px-330 , py-200, 50, 30,
            #self.backpack_overlay_click
            )
    @override
    def enter(self) -> None:
        sound_manager.play_bgm("RBY 101 Opening (Part 1).ogg")
        pass

    @override
    def exit(self) -> None:
        pass

    @override
    def update(self, dt: float) -> None:
        if input_manager.key_pressed(pg.K_SPACE):
            scene_manager.change_scene("setting")
            return
        self.back_button.update(dt)
        self.board_button.update(dt)
        self.line_bar.update(dt)
        self.slider_bar.update(dt)
        self.mute_switch.update(dt)
    @override
    def draw(self, screen: pg.Surface) -> None:
        self.background.draw(screen)
        self.back_button.draw(screen)
        self.board_button.draw(screen)
        font = pg.font.Font("assets/fonts/Minecraft.ttf", 24)
        text_v=font.render(f"Volume", True, (255,255,255))
        text_m=font.render(f"Mute", True, (255,255,255))
        _=screen.blit(text_v, (230, 240))
        _=screen.blit(text_m,(250,345))
        self.line_bar.draw(screen)
        self.mute_switch.draw(screen)
        self.slider_bar.draw(screen)

    