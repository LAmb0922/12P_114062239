import pygame as pg
from src.core.managers import GameManager
from src.utils import GameSettings
from src.sprites import BackgroundSprite
from src.scenes.scene import Scene
from src.interface.components import Button
from src.core.services import scene_manager, sound_manager, input_manager,resource_manager
from typing import override
from src.interface.components.choose_your_pokemon import ChooseYourPokemon
from src.interface.components.enemy_pokemon import EnemyPokemon
import time
from src.interface.components.battle_pokemon import BattlePokemon
from src.interface.components.special_button import SpecialButton
import random
class ChooseScene(Scene):
    # Background Image
    background: BackgroundSprite
    # Buttons
    play_button: Button
    
    def __init__(self):
        super().__init__()
        self.button_not_clicked_yet=True
        self.stage="choose"
        self.turn="player"
        self.player_already_attack=False
        self.player_turn_tree=["choose action",["use item",["use ball"],["use potion"]],["attack",["choose attacker",["choose skill",["choose enemy",["actual attack"]]]]],["defend"]]
        self.player_action_record=["choose action"]
        self.player_step=None
        self.player_selection=None
        self.game_manager=GameManager.load("saves/game0.json")
        self.background = BackgroundSprite("backgrounds/background1.png")
        self.selection=[]
        self.make_all_frames()
        self.make_pokemon()
        self.make_button()
        self.my_mons=[self.grass_lion,self.fire_bird,self.ice_deer,self.ground_rat]
        self.wording=True
        self.text_x=-500
        self.attacker=None
        self.attackeder=None
        self.animate_timer=0
        self.play_super_animation=False
        self.super_animation_x=-500
        self.speed=0
        self.leaving_text=False
        self.texing=False
        self.text_record=0
        self.text_timer=0
        self.mask=pg.Surface((GameSettings.SCREEN_WIDTH,GameSettings.SCREEN_HEIGHT),pg.SRCALPHA)
        self.mask.fill((255,255,255,50))
        self.times=0
        self.heart=pg.image.load("assets/images/ingame_ui/baricon2.png").convert_alpha()
        self.coin=pg.image.load("assets/images/ingame_ui/coin.png").convert_alpha()
        self.coin=pg.transform.scale(self.coin, (50, 50))
        self.size=50
        self.dy=0
        self.vector=(0,0)
        self.ball=pg.image.load("assets/images/ingame_ui/ball.png").convert_alpha()
        self.ball=pg.transform.scale(self.ball, (30, 30))
        self.enemies=[self.happy_dolphin,self.angry_turtle,self.green_bug]
        self.new_text="welcome to battle field"
        self.line1=""
        self.line2=""
        self.should_change_line=False
    def make_pokemon(self):
        self.grass_lion=ChooseYourPokemon(
            self.frames1[1],self.frames1[2],
            0,200,300,300,self.game_manager.bag._monsters_data[0]["hp"],100,"hit","forest legacy","grass",           )
        self.fire_bird=ChooseYourPokemon(
            self.frames2[1],self.frames2[2],
            310,200,300,300,self.game_manager.bag._monsters_data[2]["hp"],100,"hit","fire berserker","fire",           )
        self.ice_deer=ChooseYourPokemon(
            self.frames3[1],self.frames3[2],
            620,200,300,300,self.game_manager.bag._monsters_data[1]["hp"],100,"hit","ice sword rain","water",           )
        self.ground_rat=ChooseYourPokemon(
            self.frames4[1],self.frames4[2],
            930,200,300,300,self.game_manager.bag._monsters_data[3]["hp"],100,"money hit","digger steal","None", )
        self.battle_grass_lion=BattlePokemon(
            self.frames11[1],self.attack3,
            0,275,300,300,self.game_manager.bag._monsters_data[0]["hp"],100,
            "hit","forest legacy","grass","grass lion",self.game_manager.bag._monsters_data[0]["max_hp"],self.grass_lion_selected)
        self.battle_ice_deer=BattlePokemon(
            self.frames13[1],self.attack1,
            0,275,300,300,self.game_manager.bag._monsters_data[1]["hp"],100,
            "hit","ice sword rain","water","ice deer",self.game_manager.bag._monsters_data[1]["max_hp"],self.ice_deer_selected)
        self.battle_fire_bird=BattlePokemon(
            self.frames12[1],self.attack2,
            0,275,300,300,self.game_manager.bag._monsters_data[2]["hp"],100,
            "hit","fire berserker","fire","fire bird",self.game_manager.bag._monsters_data[2]["max_hp"],self.fire_bird_selected)
        self.battle_ground_rat=BattlePokemon(
            self.frames14[1],self.attack4,
            0,275,300,300,self.game_manager.bag._monsters_data[3]["hp"],100,
            "hit","digger steal","None","ground rat",self.game_manager.bag._monsters_data[3]["max_hp"],self.ground_rat_selected)
        self.happy_dolphin=EnemyPokemon(
            self.frames5[1],self.frames6[1],self.attack6,
            250,150,150,150,500,150,
            "hit","drowning water prison","water","happy dolphin",False,self.happy_dolphin_selected)
        self.angry_turtle=EnemyPokemon(
            self.frames7[1],self.frames8[1],self.attack5,
            600,150,150,150,500,150,
            "hit","inferno bomb","fire","angry turtle",False,self.angry_turtle_selected)
        self.green_bug=EnemyPokemon(
            self.frames9[1],self.frames10[1],self.attack3,
            950,100,150,150,500,150,
            "hit","vine trap","grass","green bug",True,self.green_bug_selected)
    def new_sentence(self,new):
        self.new_text=new
        self.text_timer=0
        self.should_change_line=False
        self.line1=""
        self.line2=""
    def reset_turn(self):
        
        if self.turn=="enemy":
            for mons in self.nakama:
                mons.defense=False
                mons.defense_buff=0
            self.turn="player"
        elif self.turn=="player":
            self.turn="enemy"
            self.ice_sword_rain_button.cd-=1
            self.forest_legacy_button.cd-=1
            self.fire_berserker_button.cd-=1
            self.digger_steal_button.cd-=1
        self.player_action_record=["choose action"]
        self.player_step="choose action"
        self.wording=True
        self.text_x = -500    
        self.player_already_attack=False
        self.animate_timer=0
        self.play_super_animation=False
        self.times=0
        self.heart=pg.image.load("assets/images/ingame_ui/baricon2.png").convert_alpha()
        self.size=50
        self.dy=0
        for mons in self.nakama:
            mons.chosen=False
    def super_animation_draw(self,screen: pg.Surface,attacker:BattlePokemon,picture):
        pass
    def make_all_frames(self):
        self.frames1=self.make_pokemon_image("assets/images/sprites/sprite3_attack.png")#grass lion
        self.frames2=self.make_pokemon_image("assets/images/sprites/sprite5_attack.png")#fire bird
        self.frames3=self.make_pokemon_image("assets/images/sprites/sprite6_attack.png")#ice deer
        self.frames4=self.make_pokemon_image("assets/images/sprites/sprite4_attack.png")#ground rat
        self.frames5=self.make_pokemon_image("assets/images/sprites/sprite13_attack.png")#happy_dolphin
        self.frames6=self.make_pokemon_image("assets/images/sprites/sprite14_attack.png")#happy_dolphin_evolved
        self.frames7=self.make_pokemon_image("assets/images/sprites/sprite8_attack.png")#angry_turtle
        self.frames8=self.make_pokemon_image("assets/images/sprites/sprite9_attack.png")#angry_turtle_evolved
        self.frames9=self.make_pokemon_image("assets/images/sprites/sprite15_attack.png")#green_bug
        self.frames10=self.make_pokemon_image("assets/images/sprites/sprite16_attack.png")#green_bug_evolved
        self.frames11=self.make_2_frames("assets/images/sprites/sprite3.png")#grass lion back
        self.frames12=self.make_2_frames("assets/images/sprites/sprite5.png")#fire bird back
        self.frames13=self.make_2_frames("assets/images/sprites/sprite6.png")#ice deer back
        self.frames14=self.make_2_frames("assets/images/sprites/sprite4.png")#ground rat back
        self.attack1=self.make_pokemon_image("assets/images/attack/attack1.png")# ice
        self.attack2=self.make_pokemon_image("assets/images/attack/attack5.png")#fire
        self.attack3=self.make_pokemon_image("assets/images/attack/attack6.png")#grass
        self.attack4=self.make_pokemon_image("assets/images/attack/attack7.png")#scratch
        self.attack5=self.make_pokemon_image("assets/images/attack/attack4.png")#bomb
        self.attack6=self.make_pokemon_image("assets/images/attack/attack1.png")#water
        size=160
        self.attack1= [pg.transform.scale(f, (size, size)) for f in self.attack1]
        self.attack2=[pg.transform.scale(f, (size, size)) for f in self.attack2]
        self.attack3=[pg.transform.scale(f, (size, size)) for f in self.attack3]
        self.attack4=[pg.transform.scale(f, (size, size)) for f in self.attack4]
        self.attack5=[pg.transform.scale(f, (size, size)) for f in self.attack5]
        self.attack6=[pg.transform.scale(f, (size, size)) for f in self.attack6]
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
    def make_2_frames(self,path):
        sheet = pg.image.load(path)
        sheet_width = sheet.get_width()
        sheet_height = sheet.get_height()
        frame_width = sheet_width // 2
        frames = []
        for i in range(2):
            frame_rect = pg.Rect(i * frame_width, 0, frame_width, sheet_height)
            frame = sheet.subsurface(frame_rect).copy()
            frames.append(frame)
        return frames   
    def make_button(self):   #two:200,780  three:90,490,890   four:,,,
        self.hit_button=SpecialButton(
            "UI/raw/UI_Flat_Banner04a.png","UI/raw/UI_Flat_Banner03a.png",
            200,200,300,90,"normal hit",self.go_to_choose_enemy)
        self.defend_button=SpecialButton(
            "UI/raw/UI_Flat_Banner04a.png","UI/raw/UI_Flat_Banner03a.png",
            890,200,300,90,"defend",self.team_defend)
        self.attack_button=SpecialButton(
            "UI/raw/UI_Flat_Banner04a.png","UI/raw/UI_Flat_Banner03a.png",
            90,200,300,90,"attack",self.declare_attack)
        self.use_item_button=SpecialButton(
            "UI/raw/UI_Flat_Banner04a.png","UI/raw/UI_Flat_Banner03a.png",
            490,200,300,90,"use item",self.use_item)
        self.use_heal_potion_button=SpecialButton(
            "UI/raw/UI_Flat_Banner04a.png","UI/raw/UI_Flat_Banner03a.png",
            10,200,300,90,"heal potion",self.use_heal_potion)
        self.use_strength_potion_button=SpecialButton(
            "UI/raw/UI_Flat_Banner04a.png","UI/raw/UI_Flat_Banner03a.png",
            330,200,300,90,"strength potion",self.use_strength_potion)
        self.use_defense_potion_button=SpecialButton(
            "UI/raw/UI_Flat_Banner04a.png","UI/raw/UI_Flat_Banner03a.png",
            650,200,300,90,"defense potion",self.use_defense_potion)
        self.use_ball_button=SpecialButton(
            "UI/raw/UI_Flat_Banner04a.png","UI/raw/UI_Flat_Banner03a.png",
            970,200,300,90,"pokeball ball",self.use_pokeball)
        self.forest_legacy_button=SpecialButton(
            "UI/raw/UI_Flat_Banner04a.png","UI/raw/UI_Flat_Banner03a.png",
            780,200,300,90,"forest legacy",self.forest_legacy)
        self.ice_sword_rain_button=SpecialButton(
            "UI/raw/UI_Flat_Banner04a.png","UI/raw/UI_Flat_Banner03a.png",
            780,200,300,90,"ice sword rain",self.ice_sword_rain)
        self.fire_berserker_button=SpecialButton(
            "UI/raw/UI_Flat_Banner04a.png","UI/raw/UI_Flat_Banner03a.png",
            780,200,300,90,"fire berserker",self.fire_berserker)
        self.digger_steal_button=SpecialButton(
            "UI/raw/UI_Flat_Banner04a.png","UI/raw/UI_Flat_Banner03a.png",
            780,200,300,90,"digger steal",self.digger_steal)
    def grass_lion_selected(self):
        if self.button_not_clicked_yet:
            self.button_not_clicked_yet=False
            if self.player_step=="use heal potion":
                self.game_manager.bag._items_data[0]["count"]-=1
                self.game_manager.bag._monsters_data[0]["hp"]+=100
                self.new_sentence(f"Why didn't you use my super!? I can heal too !!! But thanks...you're a nice guy.")
                
                self.reset_turn()
            if self.player_step=="use strength potion":
                self.game_manager.bag._items_data[1]["count"]-=1
                self.battle_grass_lion.atk+=30
                self.new_sentence(f"Grass lion becomes more aggressive, increase 50 atk. Remaining {self.game_manager.bag._items_data[1]["count"]} strength potion")
                self.reset_turn()
            if self.player_step=="use defense potion":
                self.battle_grass_lion.defense_buff+=50
                self.game_manager.bag._items_data[2]["count"]-=1
                self.new_sentence(f"Grass lion gets stronger, increasing 50 defense buff. Remaining {self.game_manager.bag._items_data[2]["count"]} defense potion")
                self.reset_turn()
            if self.player_step=="declare attack":
                self.player_step="choose skill"
                self.player_action_record.append("choose skill")
                self.attacker=self.battle_grass_lion
    def ice_deer_selected(self):
        if self.button_not_clicked_yet:
            self.button_not_clicked_yet=False
            if self.player_step=="use heal potion":
                self.game_manager.bag._items_data[0]["count"]-=1
                self.game_manager.bag._monsters_data[0]["hp"]+=100
                self.new_sentence(f"You heal ice deer, increasing 100 hp. Remaining {self.game_manager.bag._items_data[0]["count"]} heal potion")
                self.reset_turn()
            if self.player_step=="use strength potion":
                self.game_manager.bag._items_data[1]["count"]-=1
                self.battle_ice_deer.atk+=30
                self.new_sentence(f"Ice deer become brutal, increasing 50 atk. Remaining {self.game_manager.bag._items_data[1]["count"]} strength potion")
                self.reset_turn()
            if self.player_step=="use defense potion":
                self.battle_ice_deer.defense_buff+=50
                self.game_manager.bag._items_data[2]["count"]-=1
                self.new_sentence(f"Getting defense buff from you, ice deer is happy. \"DO you want some ice scream later? It's on me!\", ice deer said.")
                self.reset_turn()
            if self.player_step=="declare attack":
                self.player_step="choose skill"
                self.player_action_record.append("choose skill")
                self.attacker=self.battle_ice_deer
        
    def fire_bird_selected(self):
        if self.button_not_clicked_yet:
            self.button_not_clicked_yet=False
            if self.player_step=="use heal potion":
                self.game_manager.bag._items_data[0]["count"]-=1
                self.game_manager.bag._monsters_data[2]["hp"]+=100
                self.new_sentence(f"You heal fire bird, increasing 100 hp. Remaining {self.game_manager.bag._items_data[0]["count"]} heal potion")
                self.reset_turn()
            if self.player_step=="use strength potion":
                self.game_manager.bag._items_data[1]["count"]-=1
                self.battle_fire_bird.atk+=30
                self.new_sentence(f"\"I don't need your help!!\", fire bird said. But he's power still getting stronger")
                self.reset_turn()
            if self.player_step=="use defense potion":
                self.battle_fire_bird.defense_buff+=50
                self.game_manager.bag._items_data[2]["count"]-=1
                self.new_sentence(f"\"Defense? I don't need that!\", fire bird said. Well...the potion still worked.")
                self.reset_turn()
            if self.player_step=="declare attack":
                self.player_step="choose skill"
                self.player_action_record.append("choose skill")
                self.attacker=self.battle_fire_bird
    def ground_rat_selected(self):
        if self.button_not_clicked_yet:
            self.button_not_clicked_yet=False
            if self.player_step=="use heal potion":
                self.game_manager.bag._items_data[0]["count"]-=1
                self.game_manager.bag._monsters_data[3]["hp"]+=100
                self.new_sentence(f"You heal ground rat, increase 100 hp. Remaining {self.game_manager.bag._items_data[0]["count"]} heal potion")
                self.reset_turn()
            if self.player_step=="use strength potion":
                self.game_manager.bag._items_data[1]["count"]-=1
                self.battle_ground_rat.atk+=30
                self.new_sentence(f"\"Give me more!!\", ground rat said.")
                self.reset_turn()
            if self.player_step=="use defense potion":
                self.battle_ground_rat.defense_buff+=50
                self.game_manager.bag._items_data[2]["count"]-=1
                self.new_sentence(f"\"I will be happier if you give money...\", ground rat said")
                self.reset_turn()
            if self.player_step=="declare attack":
                self.player_step="choose skill"
                self.player_action_record.append("choose skill")
                self.attacker=self.battle_ground_rat
    def happy_dolphin_selected(self):
        if self.button_not_clicked_yet:
            self.button_not_clicked_yet=False
            if self.player_step=="choose enemy":
                self.attackeder=self.happy_dolphin
                self.player_step="actual attack"
                self.player_action_record.append("actual attack")    
                self.happy_dolphin.can_be_chosen=False
                self.angry_turtle.can_be_chosen=False
                self.green_bug.can_be_chosen=False
    def angry_turtle_selected(self):
        if self.button_not_clicked_yet:
            self.button_not_clicked_yet=False
            if self.player_step=="choose enemy":
                self.attackeder=self.angry_turtle
                self.player_step="actual attack"
                self.player_action_record.append("actual attack")
                self.happy_dolphin.can_be_chosen=False
                self.angry_turtle.can_be_chosen=False
                self.green_bug.can_be_chosen=False
    def green_bug_selected(self):
        if self.button_not_clicked_yet:
            self.button_not_clicked_yet=False
            if self.player_step=="choose enemy":
                self.attackeder=self.green_bug
                self.player_step="actual attack"
                self.player_action_record.append("actual attack")
                self.happy_dolphin.can_be_chosen=False
                self.angry_turtle.can_be_chosen=False
                self.green_bug.can_be_chosen=False
    def team_defend(self):
        print(self.nakama)
        for mons in self.nakama:
            
            mons.defense=True
            print(mons.name,mons.defense)
            self.new_sentence("\"Yes sir\", your pokemon said. They turn to defense mode")
        self.reset_turn()
    def choose_action(self):
        pass
    def go_to_choose_enemy(self):
        if self.player_step=="choose skill":
            self.player_step="choose enemy"
            self.player_action_record.append("choose enemy")
    def declare_attack(self):
        self.player_step="declare attack"
        self.player_action_record.append("declare attack")
    def use_item(self):
        if not self.wording :
            self.player_step="use item"
            self.button_not_clicked_yet=False
            self.player_action_record.append("use item")
    def use_heal_potion(self):
        if self.game_manager.bag._items_data[0]["count"]>0 and self.player_step=="use item" and self.button_not_clicked_yet:
            self.player_step="use heal potion"
            self.button_not_clicked_yet=False
            self.player_action_record.append("use heal potion")
    def use_strength_potion(self):
        if self.game_manager.bag._items_data[1]["count"]>0 and self.player_step=="use item" and self.button_not_clicked_yet:
            self.player_step="use strength potion"
            self.button_not_clicked_yet=False
            self.player_action_record.append("use strength potion")
    def use_defense_potion(self):
        if self.game_manager.bag._items_data[2]["count"]>0 and self.player_step=="use item" and self.button_not_clicked_yet:
            self.button_not_clicked_yet=False
            self.player_step="use defense potion"
            self.player_action_record.append("use defense potion")
    def use_pokeball(self):
        if self.game_manager.bag._items_data[4]["count"]>1:
            self.game_manager.bag._items_data[4]["count"]-=1
            self.player_step="use pokeball"
            self.player_action_record.append("use pokeball")
            
    def ice_sword_rain(self):
        if self.attacker==self.battle_ice_deer:
            if self.button_not_clicked_yet:
                self.button_not_clicked_yet=False
                if self.player_step=="choose skill":
                    self.player_step="ice sword rain"
            
                
    def fire_berserker(self):
        if self.attacker==self.battle_fire_bird:
            if self.button_not_clicked_yet:
                self.button_not_clicked_yet=False
            if self.attacker==self.battle_fire_bird:
                self.battle_fire_bird.berserker=True
                self.player_step="fire berserker"
            
    def forest_legacy(self):
        if self.attacker==self.battle_grass_lion:
            if self.button_not_clicked_yet:
                self.button_not_clicked_yet=False
            if self.attacker==self.battle_grass_lion:
                for mons in self.nakama:
                    mons.hp+=100
                self.player_step="forest legacy"
                
    def digger_steal(self):
        if self.attacker==self.battle_ground_rat:
            if self.button_not_clicked_yet:
                self.button_not_clicked_yet=False
            if self.attacker==self.battle_ground_rat:
                self.game_manager.bag._items_data[3]["count"]+=60
                self.player_step="digger steal"
            
    def maintain_hp(self):
        for mons in self.nakama:
            mons.hp=min(max(0,mons.hp),mons.max_hp)
        self.happy_dolphin.hp=max(0,self.happy_dolphin.hp)
        self.green_bug.hp=max(0,self.green_bug.hp)
        self.angry_turtle.hp=max(0,self.angry_turtle.hp)
    def enemy_decide_attacker_and_skill(self):
        alive_enemy=list(filter(lambda x:x.hp>0,self.enemies))
        alive_pokemon=[mons for mons in self.nakama if mons.hp>0]
        self.attackeder=random.choice(alive_pokemon)
        if len(alive_enemy)>=2:
            self.attacker=random.choice(alive_enemy)
            self.player_step="enemy attack"
        elif len(alive_enemy)==1 and not alive_enemy[0].evolve:
            self.attacker=alive_enemy[0]# evolve
            self.player_step="evolve"
            self.new_sentence(f"Your rival sacrifice two corpses. Summo...I mean {self.attacker.name} evolve to super {self.attacker.name}. Recover hp and increase atk. Be careful.")
        elif len(alive_enemy)==0:
            self.player_step="you win" #you win
        else:
            self.attacker=random.choice(alive_enemy)
            self.player_step="enemy attack"
    def choose_enemy(self):
        pass
    def actual_attack(self):
        pass
    def defend(self):
        pass
    def making_player_select(self,now_tree):
        self.player_step=now_tree[0]
        selection=[x[0] for x in now_tree if  isinstance(x,list)]
        return selection
    @override
    def enter(self) -> None:
        sound_manager.play_bgm("RBY 131 Trainers_ Eyes Meet (Bad Guy).ogg")
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
        print(self.player_step)
        if input_manager.key_pressed(pg.K_ESCAPE):
            scene_manager.change_scene("game")
            return
        if input_manager.key_pressed(pg.K_r) and self.turn=="player":
            self.player_action_record.remove(self.player_step)
            self.player_step=self.player_action_record[-1]
        if self.stage=="choose":
            self.fire_bird.update(dt)
            self.grass_lion.update(dt)
            self.ice_deer.update(dt)
            self.ground_rat.update(dt)
            for mons in self.my_mons:
                if mons not in self.selection and mons.chosen:
                    self.selection.append(mons)
            if len(self.selection)==3:
                self.stage="battle"
                sound_manager.play_bgm("RBY 107 Battle! (Trainer).ogg")
                self.nakama=[]
                if self.fire_bird in self.selection:
                    self.nakama.append(self.battle_fire_bird)
                if self.ice_deer in self.selection:
                    self.nakama.append(self.battle_ice_deer)
                if self.grass_lion in self.selection:
                    self.nakama.append(self.battle_grass_lion)
                if self.ground_rat in self.selection:
                    self.nakama.append(self.battle_ground_rat)
                x=30
                for mons in self.nakama:
                    mons.hitbox[0]=x
                    x+=400
        elif self.stage=="battle":
            self.maintain_hp()
            alive_pokemon=[mons for mons in self.nakama if mons.hp!=0]
            if len(alive_pokemon)==0:
                self.player_step="you lose"
                
            self.use_ball_button.count=self.game_manager.bag._items_data[4]["count"]
            self.use_defense_potion_button.count=self.game_manager.bag._items_data[2]["count"]
            self.use_heal_potion_button.count=self.game_manager.bag._items_data[0]["count"]
            self.use_strength_potion_button.count=self.game_manager.bag._items_data[1]["count"]
            for mons in self.nakama:
                mons.update(dt)
            self.happy_dolphin.update(dt)
            self.angry_turtle.update(dt)
            self.green_bug.update(dt)
            
            if self.turn=="player" and not self.wording:
                if self.player_step==None:
                    self.player_step="choose action"
                elif self.player_step=="choose action":
                    self.use_item_button.update(dt)
                    self.attack_button.update(dt)
                    self.defend_button.update(dt)
                elif self.player_step=="use item":
                    self.use_ball_button.update(dt)
                    self.use_defense_potion_button.update(dt)
                    self.use_strength_potion_button.update(dt)
                    self.use_heal_potion_button.update(dt)
                elif self.player_step=="declare attack":
                    for mons in self.nakama:
                        mons.can_be_chosen=True
                elif self.player_step=="choose skill":
                    for mons in self.nakama:
                        mons.can_be_chosen=False
                    self.hit_button.update(dt)
                    self.ice_sword_rain_button.update(dt)
                    self.fire_berserker_button.update(dt)
                    self.forest_legacy_button.update(dt)
                    self.digger_steal_button.update(dt)
                    
                elif self.player_step=="choose enemy":
                    self.happy_dolphin.can_be_chosen=True
                    self.angry_turtle.can_be_chosen=True
                    self.green_bug.can_be_chosen=True
        self.button_not_clicked_yet=True  #last line
    @override
    def draw(self, screen: pg.Surface) -> None:
        
        self.background.draw(screen)
        font = pg.font.Font("assets/fonts/Minecraft.ttf", 100)
        if self.stage=="choose":
            self.fire_bird.draw(screen)
            self.grass_lion.draw(screen)
            self.ice_deer.draw(screen)
            self.ground_rat.draw(screen)
            text_c=font.render(f"choose your pokemon ! ! {3-len(self.selection)} left", True, (255,255,255))
            _=screen.blit(text_c,(20,80))
        elif self.stage=="battle":  #leaving
            if self.player_step=="you win" or self.player_step=="you lose":
                self.times+=1
                if not self.leaving_text:
                    if self.player_step=="you lose":
                        self.new_sentence(f"you lose. No one like you, including yourself.")
                        self.leaving_text=True
                    else:
                        self.new_sentence("congratulations!!")
                        self.leaving_text=True
                if self.times>=300:
                    self.game_manager.bag._items_data[0]=self.use_heal_potion_button.count
                    self.game_manager.bag._items_data[1]=self.use_strength_potion_button.count
                    self.game_manager.bag._items_data[2]=self.use_defense_potion_button.count
                    self.game_manager.bag._items_data[4]=self.use_ball_button.count
                    self.game_manager.bag._monsters_data[0]["hp"]=self.battle_grass_lion.hp
                    self.game_manager.bag._monsters_data[1]["hp"]=self.battle_ice_deer.hp
                    self.game_manager.bag._monsters_data[2]["hp"]=self.battle_fire_bird.hp
                    self.game_manager.bag._monsters_data[3]["hp"]=self.battle_ground_rat.hp
                    scene_manager.change_scene("game")
            for mons in self.nakama:
                mons.draw(screen)
            
            
            self.angry_turtle.draw(screen)
            self.happy_dolphin.draw(screen)
            self.green_bug.draw(screen)
            self.draw_interacter(screen)
            if self.wording and self.turn=="player":
                text_Y=font.render(f"YOU TURN !", True, (255,255,255))
                self.text_x+=10
                _=screen.blit(text_Y,(self.text_x,200))
                if self.text_x>1200:
                    self.wording=False
                    self.text_x=-500
            elif not self.wording and self.turn=="player":
                if self.player_step=="choose action":
                    self.use_item_button.draw(screen)
                    self.attack_button.draw(screen)
                    self.defend_button.draw(screen)
                elif self.player_step=="use item":
                    self.use_ball_button.draw(screen)
                    self.use_heal_potion_button.draw(screen)
                    self.use_strength_potion_button.draw(screen)
                    self.use_defense_potion_button.draw(screen)
                    
                
                elif self.player_step=="choose skill":
                    self.hit_button.draw(screen)
                    if self.attacker==self.battle_ice_deer:
                        self.ice_sword_rain_button.draw(screen)
                    elif self.attacker==self.battle_fire_bird:
                        self.fire_berserker_button.draw(screen)
                    elif self.attacker==self.battle_grass_lion:
                        self.forest_legacy_button.draw(screen)
                    elif self.attacker==self.battle_ground_rat:
                        self.digger_steal_button.draw(screen)
                elif self.player_step=="use pokeball":
                    if self.dy<200:
                        self.dy+=10
                        _=screen.blit(self.ball,(self.angry_turtle.hitbox[0]+20,450-self.dy))
                        _=screen.blit(self.ball,(self.happy_dolphin.hitbox[0]+20,450-self.dy))
                        _=screen.blit(self.ball,(self.green_bug.hitbox[0]+20,450-self.dy))
                    elif self.times<100:
                        self.times+=1
                        pos=random.randint(-5,5)
                        _=screen.blit(self.ball,(self.angry_turtle.hitbox[0]+20+pos,450-self.dy))
                        _=screen.blit(self.ball,(self.happy_dolphin.hitbox[0]+20+pos,450-self.dy))
                        _=screen.blit(self.ball,(self.green_bug.hitbox[0]+20+pos,450-self.dy))
                    elif self.animate_timer<=4:
                        frames=self.attack5
                        speed=0.1
                        screen.blit(frames[int(self.animate_timer)], (self.angry_turtle.hitbox[0]-20, 350-self.dy))
                        screen.blit(frames[int(self.animate_timer)], (self.happy_dolphin.hitbox[0]-20, 350-self.dy))
                        screen.blit(frames[int(self.animate_timer)], (self.green_bug.hitbox[0]-20,350-self.dy))
                        self.animate_timer+=speed
                    else:
                        self.angry_turtle.hp-=100
                        self.happy_dolphin.hp-=100
                        self.green_bug.hp-=100
                        self.new_sentence(f"What the heck is that!?  Pokeb...omb!! Remaining {self.use_ball_button.count} pokeball.")
                        self.reset_turn()
                    
                    
                elif self.player_step=="actual attack":
                    if self.animate_timer<=4:
                        frames=self.attacker.img_attack
                        speed=0.15
                        screen.blit(frames[int(self.animate_timer)], (self.attackeder.hitbox[0], self.attackeder.hitbox[1]))
                        self.animate_timer+=speed
                    else:
                        if self.player_already_attack==False:
                            if (self.attackeder.attribute=="grass" and self.attacker.attribute=="fire") or (self.attackeder.attribute=="fire" and self.attacker.attribute=="water") or (self.attackeder.attribute=="water" and self.attacker.attribute=="grass"):#counter
                                damage=self.attacker.atk*2
                                if self.attacker.berserker:
                                    damage=int(damage*1.5)
                                    if (self.attackeder.hp-damage)<=0:
                                        self.new_sentence(f"{self.attacker.name} attack {self.attackeder.name}, causing {self.attacker.atk}*2(counter)*1.5(berserker) damage. {self.attackeder.name} dies.")
                                    else:
                                        self.new_sentence(f"{self.attacker.name} attack {self.attackeder.name}, causing {self.attacker.atk}*2(counter)*1.5(berserker) damage.")
                                else:
                                    if (self.attackeder.hp-damage)<=0:
                                        self.new_sentence(f"{self.attacker.name} attack {self.attackeder.name}, causing {self.attacker.atk}*2(counter) damage. {self.attackeder.name} dies.")
                                    else:
                                        self.new_sentence(f"{self.attacker.name} attack {self.attackeder.name}, causing {self.attacker.atk}*2(counter) damage.")
                                self.attackeder.hp-=damage
                                self.player_already_attack=True
                            elif (self.attackeder.attribute=="fire" and self.attacker.attribute=="grass") or (self.attackeder.attribute=="grass" and self.attacker.attribute=="water") or (self.attackeder.attribute=="water" and self.attacker.attribute=="fire"):
                                damage=self.attacker.atk*0.5
                                if self.attacker.berserker:
                                    damage=int(damage*1.5)
                                    if (self.attackeder.hp-damage)<=0:
                                        self.new_sentence(f"{self.attacker.name} attack {self.attackeder.name}, causing {self.attacker.atk}*0.5(countered)*1.5(berserker) damage. {self.attackeder.name} dies.")
                                    else:
                                        self.new_sentence(f"{self.attacker.name} attack {self.attackeder.name}, causing {self.attacker.atk}*0.5(countered)*1.5(berserker) damage.")
                                else:
                                    if (self.attackeder.hp-damage)<=0:
                                        self.new_sentence(f"{self.attacker.name} attack {self.attackeder.name}, causing {self.attacker.atk}*0.5(countered) damage. {self.attackeder.name} dies.")
                                    else:
                                        self.new_sentence(f"{self.attacker.name} attack {self.attackeder.name}, causing {self.attacker.atk}*0.5(countered) damage.")
                                self.attackeder.hp-=damage
                                self.player_already_attack=True
                            else:
                                damage=self.attacker.atk
                                if self.attacker.berserker:
                                    damage=int(damage*1.5)
                                    if (self.attackeder.hp-damage)<=0:
                                        self.new_sentence(f"{self.attacker.name} attack {self.attackeder.name}, causing {self.attacker.atk}*1.5(berserker) damage. {self.attackeder.name} dies.")
                                    else:
                                        self.new_sentence(f"{self.attacker.name} attack {self.attackeder.name}, causing {self.attacker.atk}*1.5(berserker) damage.")
                                else:
                                    if (self.attackeder.hp-damage)<=0:
                                        self.new_sentence(f"{self.attacker.name} attack {self.attackeder.name}, causing {self.attacker.atk} damage. {self.attackeder.name} dies.")
                                    else:
                                        self.new_sentence(f"{self.attacker.name} attack {self.attackeder.name}, causing {self.attacker.atk} damage.")
                                self.attackeder.hp-=damage
                                self.player_already_attack=True
                        
                        self.reset_turn()
                elif self.player_step=="fire berserker":
                    if not self.play_super_animation:
                        
                        size=1200
                        self.super_animation_picture=pg.transform.scale(self.frames12[0],(size,size))
                        _=screen.blit(self.mask,(0,0))
                        screen.blit(self.super_animation_picture, (self.super_animation_x, -300))
                        if self.super_animation_x<100:
                            
                            self.speed=50
                        elif 100<=self.super_animation_x<=300:
                            self.speed=2
                        elif self.super_animation_x>300:
                            self.speed=60
                        if self.super_animation_x>700:
                            self.play_super_animation=True
                            self.super_animation_x=-500
                            self.new_sentence(f"I WILL BURN THEM TO ASHHHHH!!!!!, fire roared and transformed into a berserker. Getting more aggressive but vulnerable.")
                            self.fire_berserker_button.cd=3
                            self.reset_turn()
                        self.super_animation_x+=self.speed
                elif self.player_step=="forest legacy":
                    if self.play_super_animation:
                        if self.size>5:
                            self.heart=pg.transform.scale(self.heart,(self.size,self.size))
                            self.size-=0.5
                            self.dy+=2
                        else:
                            self.new_sentence("The grace of forest heal all your pokemon.Wind blow on your face, so comfortable!")
                            self.forest_legacy_button.cd=3
                            self.reset_turn()
                        for mons in self.nakama:
                            screen.blit(self.heart,(mons.hitbox[0],mons.hitbox[1]-self.dy))
                    elif not self.play_super_animation:
                        size=1200
                        self.super_animation_picture=pg.transform.scale(self.frames11[0],(size,size))
                        _=screen.blit(self.mask,(0,0))
                        screen.blit(self.super_animation_picture, (self.super_animation_x, -300))
                        if self.super_animation_x<100:
                            
                            self.speed=50
                        elif 100<=self.super_animation_x<=300:
                            self.speed=2
                        elif self.super_animation_x>300:
                            self.speed=60
                        if self.super_animation_x>700:
                            self.play_super_animation=True
                            self.super_animation_x=-500
                        self.super_animation_x+=self.speed
                elif self.player_step=="digger steal":
                    if self.play_super_animation:
                    
                        if 0<=self.times<=40:
                            self.times+=1
                            self.vector1=((self.battle_ground_rat.hitbox[0]+150-self.happy_dolphin.hitbox[0])/40,(self.battle_ground_rat.hitbox[1]+150-self.happy_dolphin.hitbox[1])/40)
                            self.vector2=((self.battle_ground_rat.hitbox[0]+150-self.angry_turtle.hitbox[0])/40,(self.battle_ground_rat.hitbox[1]+150-self.angry_turtle.hitbox[1])/40)
                            self.vector3=((self.battle_ground_rat.hitbox[0]+150-self.green_bug.hitbox[0])/40,(self.battle_ground_rat.hitbox[1]+150-self.green_bug.hitbox[1])/40)
                            _=screen.blit(self.coin,(self.angry_turtle.hitbox[0]+self.vector2[0]*self.times,self.angry_turtle.hitbox[1]+self.vector2[1]*self.times))
                            _=screen.blit(
                                self.coin,(self.happy_dolphin.hitbox[0]+self.vector1[0]*self.times,self.happy_dolphin.hitbox[1]+self.vector1[1]*self.times))
                            _=screen.blit(self.coin,(self.green_bug.hitbox[0]+self.vector3[0]*self.times,self.green_bug.hitbox[1]+self.vector3[1]*self.times))
                        elif self.times==-1:
                            self.new_sentence(f"Theft is immoral and illegal, but you pretended that you didn't see the crime. Shame of you.")
                            self.digger_steal_button.cd=3
                            self.reset_turn()
                        elif self.times>=40:
                            if self.dy>-250:
                                self.dy-=10
                                self.size-=2
                                picture=pg.transform.scale(self.coin, (self.size, self.size))
                                _=screen.blit(picture,(self.battle_ground_rat.hitbox[0]+150,self.battle_ground_rat.hitbox[1]+150+self.dy))
                            else:
                                self.times=-1
                        
                    elif not self.play_super_animation:
                        size=1200
                        self.super_animation_picture=pg.transform.scale(self.frames14[0],(size,size))
                        _=screen.blit(self.mask,(0,0))
                        screen.blit(self.super_animation_picture, (self.super_animation_x, -300))
                        if self.super_animation_x<100:
                            
                            self.speed=50
                        elif 100<=self.super_animation_x<=300:
                            self.speed=2
                        elif self.super_animation_x>300:
                            self.speed=60
                        if self.super_animation_x>700:
                            self.play_super_animation=True
                            self.super_animation_x=-500
                        self.super_animation_x+=self.speed
                elif self.player_step=="ice sword rain":
                    if self.play_super_animation:
                        if self.animate_timer<=4 and self.times<=3:
                            frames=self.attacker.img_attack
                            speed=0.1
                            screen.blit(frames[int(self.animate_timer)], (self.happy_dolphin.hitbox[0]-30, self.happy_dolphin.hitbox[1]))
                            screen.blit(frames[int(self.animate_timer)], (self.angry_turtle.hitbox[0]-30, self.angry_turtle.hitbox[1]))
                            screen.blit(frames[int(self.animate_timer)], (self.green_bug.hitbox[0]-30, self.green_bug.hitbox[1]))
                            self.animate_timer+=speed
                        else:
                            self.times+=1
                            self.animate_timer=0
                        
                        if self.times==3:
                            if self.player_already_attack==False:
                                self.green_bug.hp-=self.battle_ice_deer.atk*0.5
                                self.happy_dolphin.hp-=self.battle_ice_deer.atk*1
                                self.angry_turtle.hp-=self.battle_ice_deer.atk*2
                                self.player_already_attack=True
                            self.new_sentence(f"Ice deer produce a lot of icicle. Causing damage to every enemy. The battle field is so cold now that you really need a coat.")
                            self.ice_sword_rain_button.cd=3
                            self.reset_turn()
                    elif not self.play_super_animation:
                        size=1200
                        self.super_animation_picture=pg.transform.scale(self.frames13[0],(size,size))
                        _=screen.blit(self.mask,(0,0))
                        screen.blit(self.super_animation_picture, (self.super_animation_x, -300))
                        if self.super_animation_x<100:
                            
                            self.speed=50
                        elif 100<=self.super_animation_x<=300:
                            self.speed=2
                        elif self.super_animation_x>300:
                            self.speed=60
                        if self.super_animation_x>700:
                            self.play_super_animation=True
                            self.super_animation_x=-500
                        self.super_animation_x+=self.speed
                        
            elif self.wording and self.turn=="enemy":
                text_Y=font.render(f"ENEMY TURN !", True, (255,255,255))
                self.text_x+=10
                _=screen.blit(text_Y,(self.text_x,200))
                if self.text_x>1200:
                    self.wording=False
                    self.text_x=-500
            elif not self.wording and self.turn=="enemy":
                if self.times<=150:  #waiting
                    self.times+=1
                else:
                    if self.player_step=="choose action":
                        self.enemy_decide_attacker_and_skill()
                if self.player_step=="enemy attack":
                    if self.animate_timer<=4:
                        frames=[pg.transform.scale(f,(250,250)) for f in self.attacker.img_attack]
                        speed=0.1
                        screen.blit(frames[int(self.animate_timer)], (self.attackeder.hitbox[0]+50, self.attackeder.hitbox[1]+50))
                        self.animate_timer+=speed
                    else:
                        if self.player_already_attack==False:
                            if (self.attackeder.attribute=="grass" and self.attacker.attribute=="fire") or (self.attackeder.attribute=="fire" and self.attacker.attribute=="water") or (self.attackeder.attribute=="water" and self.attacker.attribute=="grass"):#counter
                                damage=self.attacker.atk*2
                                if (self.attackeder.defense or self.attackeder.defense_buff):
                                    if self.attackeder.defense:
                                        damage=int(damage*1.5*0.5)
                                        if (self.attackeder.hp-damage)<=0:
                                            self.new_sentence(f"{self.attacker.name} attack {self.attackeder.name}, causing {self.attacker.atk}*2(counter)*0.5(defense) damage. {self.attackeder.name} dies.")
                                        else:
                                            self.new_sentence(f"{self.attacker.name} attack {self.attackeder.name}, causing {self.attacker.atk}*2(counter)*0.5(defense) damage.")
                                    else:
                                        damage=int(damage*1.5)-self.attackeder.defense_buff
                                        if (self.attackeder.hp-damage)<=0:
                                            self.new_sentence(f"{self.attacker.name} attack {self.attackeder.name}, causing {self.attacker.atk}*2(counter)-{self.attackeder.defense_buff}(defense potion) damage. {self.attackeder.name} dies.")
                                        else:
                                            self.new_sentence(f"{self.attacker.name} attack {self.attackeder.name}, causing {self.attacker.atk}*2(counter)-{self.attackeder.defense_buff}(defense potion) damage.")
                                
                                else:
                                    damage=damage*1
                                    if (self.attackeder.hp-damage)<=0:
                                        self.new_sentence(f"{self.attacker.name} attack {self.attackeder.name}, causing {self.attacker.atk}*2(counter) damage. {self.attackeder.name} dies.")
                                    else:
                                        self.new_sentence(f"{self.attacker.name} attack {self.attackeder.name}, causing {self.attacker.atk}*2(counter) damage.")
                                self.attackeder.hp-=damage
                                self.player_already_attack=True
                            elif (self.attackeder.attribute=="fire" and self.attacker.attribute=="grass") or (self.attackeder.attribute=="grass" and self.attacker.attribute=="water") or (self.attackeder.attribute=="water" and self.attacker.attribute=="fire"):
                                damage=self.attacker.atk*0.5
                                if (self.attackeder.defense or self.attackeder.defense_buff):
                                    if self.attackeder.defense:
                                        damage=int(damage*1.5*0.5)
                                        if (self.attackeder.hp-damage)<=0:
                                            self.new_sentence(f"{self.attacker.name} attack {self.attackeder.name}, causing {self.attacker.atk}*0.5(countered)*0.5(defense) damage. {self.attackeder.name} dies.")
                                        else:
                                            self.new_sentence(f"{self.attacker.name} attack {self.attackeder.name}, causing {self.attacker.atk}*0.5(countered)*0.5(defense) damage.")

                                    else:
                                        damage=int(damage*1.5)-self.attackeder.defense_buff
                                        if (self.attackeder.hp-damage)<=0:
                                            self.new_sentence(f"{self.attacker.name} attack {self.attackeder.name}, causing {self.attacker.atk}*0.5(countered)-{self.attackeder.defense_buff}(defense potion) damage. {self.attackeder.name} dies.")
                                        else:
                                            self.new_sentence(f"{self.attacker.name} attack {self.attackeder.name}, causing {self.attacker.atk}*0.5(countered)-{self.attackeder.defense_buff}(defense potion) damage.")
                                
                                else:
                                    damage=damage*1
                                    if (self.attackeder.hp-damage)<=0:
                                        self.new_sentence(f"{self.attacker.name} attack {self.attackeder.name}, causing {self.attacker.atk}*0.5(countered) damage. {self.attackeder.name} dies.")
                                    else:
                                        self.new_sentence(f"{self.attacker.name} attack {self.attackeder.name}, causing {self.attacker.atk}*0.5(countered) damage.")
                                self.attackeder.hp-=damage
                                self.player_already_attack=True    
                            else:
                                damage=self.attackeder.atk
                                if (self.attackeder.defense or self.attackeder.defense_buff):
                                    if self.attackeder.defense:
                                        damage=int(damage*1.5*0.5)
                                        if (self.attackeder.hp-damage)<=0:
                                            self.new_sentence(f"{self.attacker.name} attack {self.attackeder.name}, causing {self.attacker.atk}*0.5(defense) damage. {self.attackeder.name} dies.")
                                        else:
                                            self.new_sentence(f"{self.attacker.name} attack {self.attackeder.name}, causing {self.attacker.atk}*0.5(defense) damage.")
                                    else:
                                        damage=int(damage*1.5)-self.attackeder.defense_buff
                                        if (self.attackeder.hp-damage)<=0:
                                            self.new_sentence(f"{self.attacker.name} attack {self.attackeder.name}, causing {self.attacker.atk}-{self.attackeder.defense_buff}(defense potion) damage. {self.attackeder.name} dies.")
                                        else:
                                            self.new_sentence(f"{self.attacker.name} attack {self.attackeder.name}, causing {self.attacker.atk}-{self.attackeder.defense_buff}(defense potion) damage.")
                                else:
                                    damage=damage*1
                                    if (self.attackeder.hp-damage)<=0:
                                        self.new_sentence(f"{self.attacker.name} attack {self.attackeder.name}, causing {self.attacker.atk} damage. {self.attackeder.name} dies.")
                                    else:
                                        self.new_sentence(f"{self.attacker.name} attack {self.attackeder.name}, causing {self.attacker.atk} damage.")
                                self.attackeder.hp-=damage
                                self.player_already_attack=True    
                        self.reset_turn()
                        
                elif self.player_step=="evolve":
                    if self.animate_timer<=800:
                        self.animate_timer+=1
                        self.mask.fill((255,255,255,255-255*(self.animate_timer/800)))
                        screen.blit(self.mask,(0,0))
                    else:
                        #self.new_sentence(f"Your rival sacrifice two corpses. Summo...I mean {self.attacker.name} evolve to super {self.attacker.name}. Recover hp and increase atk. Be careful.")
                        self.reset_turn()
                        self.attacker.hp+=300
                        self.attacker.atk+=100
                        
                    self.attacker.evolve=True
                    
            font = pg.font.Font("assets/fonts/Minecraft.ttf", 32)    #the text generator
            if self.text_timer<len(self.new_text):
                if int(self.text_timer)==len(self.line1)+len(self.line2):
                    if not self.should_change_line:
                        if font.render(self.line1+self.new_text[int(self.text_timer)],True,(255,255,255)).get_width()>1230 and self.new_text[int(self.text_timer)]==" ":
                            self.line2+=self.new_text[int(self.text_timer)]
                            self.should_change_line=True
                        elif font.render(self.line1+self.new_text[int(self.text_timer)],True,(255,255,255)).get_width()>1230 and self.new_text[int(self.text_timer)]!=" ":
                            self.should_change_line=True
                            tup=tuple(self.line1.split())
                            self.line1=str(self.line1[:len(tup[-1])*(-1)])
                            self.line2=tup[-1]+self.new_text[int(self.text_timer)]
                        else:
                            self.line1+=self.new_text[int(self.text_timer)]
                    else:
                        self.line2+=self.new_text[int(self.text_timer)]
                self.text1=font.render(self.line1,True,(255,255,255))
                self.text2=font.render(self.line2,True,(255,255,255))
            screen.blit(self.text1,(30,610))
            screen.blit(self.text2,(30,660))
            speed=0.8
            self.text_timer+=speed
            
            
            
            