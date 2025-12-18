import pygame as pg
import threading
import time
from src.sprites import BackgroundSprite
from src.core.services import scene_manager, sound_manager, input_manager
from src.scenes.scene import Scene
from src.core import GameManager, OnlineManager
from src.utils import Logger, PositionCamera, GameSettings, Position ,Direction
from src.core.services import sound_manager
from src.sprites import Sprite
from typing import override
from src.interface.components.component import Slider ,Switch
from src.utils.definition import Monster
from src.entities.shop import Shop
from src.entities.entity import Entity_one 
from src.maps.map import Map
from collections import deque
from src.interface.components import Button
# from src.interface.components.chat_overlay import ChatOverlay
class GameScene(Scene):
    game_manager: GameManager
    online_manager: OnlineManager | None
    sprite_online: Entity_one
    
    def __init__(self):
        self.setting_overlay_clicked=False
        self.slider_dragging=False
        self.backpack_overlay_clicked=False
        self.leading_system_clicked=False
        super().__init__()
        # Game Manager
        self.game_manager = GameManager.load("saves/game0.json")
        self.shop = list(self.game_manager.shop.values())[0][0]
        self.navigation_path = []
        self.navigating=False
        if self.game_manager is None:
            Logger.error("Failed to load game manager")
            exit(1)
        self.mask=pg.Surface((GameSettings.SCREEN_WIDTH,GameSettings.SCREEN_HEIGHT),pg.SRCALPHA)
        self.mask.fill((0,0,0,180))
        
        # Online Manager
        if GameSettings.IS_ONLINE:
            self.online_manager = OnlineManager()
            self.online_manager.start()
            # self.chat_overlay = ChatOverlay(
            #     send_callback=..., <- send chat method
            #     get_messages=..., <- get chat messages method
            # )
        else:
            self.online_manager = None
        self.sprite_online = Entity_one(self.game_manager.player.position.x,self.game_manager.player.position.y,self.game_manager)
        #self.player_id=self.online_manager.player_id
        px, py = GameSettings.SCREEN_WIDTH // 2, GameSettings.SCREEN_HEIGHT * 3 // 4
        self.overlay_button = Button(
            "UI/button_setting.png", "UI/button_setting_hover.png",
            px +450, py-500, 50, 50,
            self.setting_overlay_click)
        rx, ry = GameSettings.SCREEN_WIDTH // 2, GameSettings.SCREEN_HEIGHT * 3 // 4
        self.backpack_button = Button(
            "UI/button_backpack.png", "UI/button_backpack_hover.png",
            rx +500, ry-500, 50, 50,
            self.backpack_overlay_click)
        
        self.board_button = Button(
            "UI/raw/UI_Flat_Frame03a.png", "UI/raw/UI_Flat_Frame03a.png",
            px -450, py-500, 800, 500,
            #lambda: scene_manager.change_scene("game")
        )
        self.leading_system_button=Button(
            "UI/button_play.png","UI/button_play_hover.png",
            px+400,py-500,50,50,
            self.leading_system_click)
        self.lead_to_riddle_end_button=Button(
            "UI/button_play.png","UI/button_play_hover.png",
            px-400,py-400,50,50,self.go_to_end
        )
        self.lead_to_riddle_start_button=Button(
            "UI/button_play.png","UI/button_play_hover.png",
            px-400,py-300,50,50,self.go_to_start
        )
        self.lead_to_gym_button=Button(
            "UI/button_play.png","UI/button_play_hover.png",
            px-400,py-200,50,50,self.go_to_gym)
        self.slider_bar=Slider(
            "UI/raw/UI_Flat_ToggleOff02a.png","UI/raw/UI_Flat_ToggleOn01a.png",
            px+200,px-350,px-350+GameSettings.AUDIO_VOLUME*(550), py-300,50,20,
            
        )
        self.save_button = Button(
            "UI/button_save.png", "UI/button_save_hover.png",
            px +200, py-400, 50, 50,
            lambda: self.game_manager.save("./saves/game0.json")
        )
        self.load_button = Button(
            "UI/button_load.png", "UI/button_load_hover.png",
            px +100, py-400, 50, 50,
            lambda: self.load()
        )
        self.line_bar = Button(
            "UI/raw/UI_Flat_BarFill01f.png", "UI/raw/UI_Flat_BarFill01f.png",
            px -320, py-300, 550, 20,
            #lambda: scene_manager.change_scene("game")
        )
        self.mute_switch = Switch(
            "UI/raw/UI_Flat_ToggleOff03a.png", "UI/raw/UI_Flat_ToggleOn03a.png",
            rx-330 , ry-200, 50, 30,
            #self.backpack_overlay_click
            )
        self.potion_button=Button(
            "ingame_ui/potion.png","ingame_ui/potion.png",
            rx-350,ry-400,50,50)
        self.ball_button=Button(
            "ingame_ui/ball.png","ingame_ui/ball.png",
            rx-350,ry-300,50,50)
        self.coin_button=Button(
            "ingame_ui/coin.png","ingame_ui/coin.png",
            rx+100,ry-100,50,50)
        self.buy_potion_button=Button(
            "UI/button_save.png", "UI/button_save_hover.png",
            rx+250,130,50,50,self.buy_potion)
        self.buy_ball_button=Button(
            "UI/button_save.png", "UI/button_save_hover.png",
            rx+250,230,50,50,self.buy_ball)
        self.sell_potion_button=Button(
            "UI/button_load.png", "UI/button_load_hover.png",
            px +150, 130, 50, 50,self.sell_potion)
        self.sell_ball_button=Button(
            "UI/button_load.png", "UI/button_load_hover.png",
            px +150, 230, 50, 50,self.sell_ball)
        for map in self.game_manager.maps.values():
            map.create_minimap(240, 135)
    def go_to_start(self):
        self.leading_system_clicked=False
        if self.navigating:
            self.navigating=False
        else:
            self.navigating=True
        player_tile = (
        self.game_manager.player.position.x // GameSettings.TILE_SIZE,
        self.game_manager.player.position.y // GameSettings.TILE_SIZE)
        self.navigation_path = self.bfs_path(player_tile,(29,18),self.game_manager.current_map)
    def go_to_gym(self):
        self.leading_system_clicked=False
        if self.navigating:
            self.navigating=False
        else:
            self.navigating=True
        player_tile = (
        self.game_manager.player.position.x // GameSettings.TILE_SIZE,
        self.game_manager.player.position.y // GameSettings.TILE_SIZE)
        self.navigation_path = self.bfs_path(player_tile,(24,25),self.game_manager.current_map)
    def go_to_end(self):
        self.leading_system_clicked=False
        if self.navigating:
            self.navigating=False
        else:
            self.navigating=True
        player_tile = (
        self.game_manager.player.position.x // GameSettings.TILE_SIZE,
        self.game_manager.player.position.y // GameSettings.TILE_SIZE)
        self.navigation_path = self.bfs_path(player_tile,(2,6),self.game_manager.current_map)
    def get_walkable_road(self,x, y, game_map:Map):
        neighbors = []
        directions = [(0,1), (1,0), (0,-1), (-1,0)]  # down, right, up, left
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < game_map.tmxdata.width and 0 <= ny <  game_map.tmxdata.height:
                rect = pg.Rect(nx*GameSettings.TILE_SIZE,ny*GameSettings.TILE_SIZE, GameSettings.TILE_SIZE, GameSettings.TILE_SIZE)
                if not game_map.check_collision(rect):  # implement is_blocked for your map
                    neighbors.append((nx, ny))
        return neighbors
    

    def bfs_path(self,start, goal, game_map):
        queue = deque([start])
        visited = set()
        visited.add(start)
        parent = {start: None}
        while queue:
            current = queue.popleft()
            if current == goal:
                break
            neighbors= self.get_walkable_road(current[0], current[1], game_map)
            for neighbor in neighbors:
                if neighbor not in visited:
                    visited.add(neighbor)
                    parent[neighbor] = current
                    queue.append(neighbor)
        path = []
        current = goal
        while current and current in parent:
            path.append(current)
            current = parent[current]
        path.reverse()
        return path

    def load(self):
        tmp=self.game_manager.load("./saves/game0.json")
        self.game_manager=tmp
    def check_bush(self):
        for b in self.game_manager.current_map.bush:
            if self.game_manager.player.animation.rect.colliderect(b) and input_manager.key_released(pg.K_SPACE):
                scene_manager.change_scene("catch")
                self.game_manager.bag._monsters_data.append(Monster({"name": "Song bird",
    "hp": 300,
    "max_hp": 300,
    "level": 5,
    "sprite_path": "sprites\sprite5.png"}))
    def buy_potion(self):
        if self.game_manager.bag._items_data[3]["count"]>=25: #the price of potion is 30
            self.game_manager.bag._items_data[3]["count"]-=25
            self.game_manager.bag._items_data[0]["count"]+=1
            self.game_manager.bag._items_data[1]["count"]+=1
            self.game_manager.bag._items_data[2]["count"]+=1
    def buy_ball(self):
        if self.game_manager.bag._items_data[3]["count"]>=5: #the price of ball is 5
            self.game_manager.bag._items_data[3]["count"]-=5
            self.game_manager.bag._items_data[4]["count"]+=1
    def sell_potion(self):
        if self.game_manager.bag._items_data[0]["count"]>=1 and self.game_manager.bag._items_data[1]["count"]>=1 and self.game_manager.bag._items_data[2]["count"]>=1: #the price of potion is 10
            self.game_manager.bag._items_data[0]["count"]-=1
            self.game_manager.bag._items_data[2]["count"]-=1
            self.game_manager.bag._items_data[1]["count"]-=1
            self.game_manager.bag._items_data[3]["count"]+=20
    def sell_ball(self):
        if self.game_manager.bag._items_data[4]["count"]>=1: #the price of potion is 10
            self.game_manager.bag._items_data[4]["count"]-=1
            self.game_manager.bag._items_data[3]["count"]+=4
    def slider_clicked(self):
        self.slider_dragging=True
    def setting_overlay_click(self):
        if self.setting_overlay_clicked==0:
            self.setting_overlay_clicked=1
        else:
            self.setting_overlay_clicked=0
    def backpack_overlay_click(self):
        if self.backpack_overlay_clicked==0:
            self.backpack_overlay_clicked=1
        else:
            self.backpack_overlay_clicked=0        
    def leading_system_click(self):
        if self.leading_system_clicked==0:
            self.leading_system_clicked=1
        else:
            self.leading_system_clicked=0 
    def draw_triangle_prepare(self,x, y,direction: str):
        size=12
        if direction == "up":
            points = [(x,y-1.5*size),(x-size, y+size),(x+size,y+size)]
        elif direction == "down":
            points = [(x,y+1.5*size),(x-size,y-size),(x+size,y-size)]
        elif direction == "left":
            points = [(x-1.5*size,y),(x+size,y-size),(x+size,y+size)]
        elif direction == "right":
            points = [(x+1.5*size,y),(x-size,y-size),(x-size,y+size)]
        return points
    @override
    def enter(self) -> None:
        sound_manager.play_bgm("RBY 103 Pallet Town.ogg")
        self.game_manager.current_map.create_minimap(240, 135)
        if self.online_manager:
            self.online_manager.start()
        
    @override
    def exit(self) -> None:
        if self.online_manager:
            self.online_manager.exit()
        self.game_manager.save("./saves/game0.json")
        
    @override
    def update(self, dt: float):
        # Check if there is assigned next scene
        self.game_manager.try_switch_map()
        
        self.sprite_online.update(dt)
        
        # Update player and other data 
        if self.game_manager.player:
            self.game_manager.player.update(dt)
        for enemy in self.game_manager.current_enemy_trainers:
            enemy.update(dt)
        for shop in self.game_manager.current_shop:
            shop.update(dt)
            
        if input_manager.key_pressed(pg.K_ESCAPE):
            for shop in self.game_manager.current_shop:
                shop.close = True
        
        self.game_manager.bag.update(dt)
        if  pg.mouse.get_pressed()[0]==0:     #slider dragging and change volume
            self.slider_dragging = False
        if self.slider_dragging:
            mx = input_manager.mouse_pos[0]
            self.slider_bar.x = mx
        if self.game_manager.player is not None and self.online_manager is not None:
            _ = self.online_manager.update(
                self.game_manager.player.position.x, 
                self.game_manager.player.position.y,
                self.game_manager.current_map.path_name,
                self.game_manager.player.animation.moving
            )
        #print(self.game_manager.player.animation.moving)
        #print(self.game_manager.player.direction.name)
        self.overlay_button.update(dt)
        self.save_button.update(dt)
        self.load_button.update(dt)
        self.backpack_button.update(dt)
        self.board_button.update(dt)
        self.slider_bar.update(dt)
        self.line_bar.update(dt)
        self.mute_switch.update(dt)
        self.potion_button.update(dt)
        self.ball_button.update(dt)
        self.coin_button.update(dt)
        self.buy_ball_button.update(dt)
        self.buy_potion_button.update(dt)
        self.sell_ball_button.update(dt)
        self.sell_potion_button.update(dt)
        self.check_bush() 
        self.leading_system_button.update(dt)
        self.lead_to_riddle_end_button.update(dt)
        self.lead_to_gym_button.update(dt)
        self.lead_to_riddle_start_button.update(dt)
        """
        TODO: UPDATE CHAT OVERLAY:

        # if self._chat_overlay:
        #     if _____.key_pressed(...):
        #         self._chat_overlay.____
        #     self._chat_overlay.update(____)
        # Update chat bubbles from recent messages

        # This part's for the chatting feature, we've made it for you.
        # if self.online_manager:
        #     try:
        #         msgs = self.online_manager.get_recent_chat(50)
        #         max_id = self._last_chat_id_seen
        #         now = time.monotonic()
        #         for m in msgs:
        #             mid = int(m.get("id", 0))
        #             if mid <= self._last_chat_id_seen:
        #                 continue
        #             sender = int(m.get("from", -1))
        #             text = str(m.get("text", ""))
        #             if sender >= 0 and text:
        #                 self._chat_bubbles[sender] = (text, now + 5.0)
        #             if mid > max_id:
        #                 max_id = mid
        #         self._last_chat_id_seen = max_id
        #     except Exception:
        #         pass
        """
    @override
    def draw(self, screen: pg.Surface):
        if self.game_manager.player:
            '''
            [TODO HACKATHON 3]
            Implement the camera algorithm logic here
            Right now it's hard coded, you need to follow the player's positions
            you may use the below example, but the function still incorrect, you may trace the entity.py
            
            camera = self.game_manager.player.camera
            '''
            
            camera = PositionCamera(16 * GameSettings.TILE_SIZE, 30 * GameSettings.TILE_SIZE)
            
            camera.x=self.game_manager.player.position.x-int(0.5*screen.get_width())
            camera.y=self.game_manager.player.position.y-int(0.5*screen.get_height())
            camera.x = max(0, min(camera.x, 64*64 - screen.get_width()))
            camera.y = max(0, min(camera.y, 64*64 - screen.get_height()))
            self.game_manager.current_map.draw(screen, camera)
            self.game_manager.player.draw(screen, camera)
        else:
            camera = PositionCamera(0, 0)
            self.game_manager.current_map.draw(screen, camera)
        for enemy in self.game_manager.current_enemy_trainers:
            enemy.draw(screen, camera)
        for shop in self.game_manager.current_shop:
            shop.draw(screen,camera)

        
        
        
                    
        
        self.game_manager.current_map.draw_minimap(screen, 0, 0)
        map_w = self.game_manager.current_map.tmxdata.width * GameSettings.TILE_SIZE
        map_h = self.game_manager.current_map.tmxdata.height * GameSettings.TILE_SIZE
        px = int(self.game_manager.player.position.x/ map_w * 240)  +5.5
        py = int(self.game_manager.player.position.y/ map_h * 135) +5.5
        pg.draw.circle(screen, (0, 0, 0), (px, py), 3)
        # if self._chat_overlay:
        #     self._chat_overlay.draw(screen)
        if self.setting_overlay_clicked:
            font = pg.font.Font("assets/fonts/Minecraft.ttf", 24)
            text_v=font.render(f"Volume", True, (255,255,255))
            text_m=font.render(f"Mute",True, (255,255,255))
            _=screen.blit(self.mask,(0,0))
            self.board_button.draw(screen)
            _=screen.blit(text_v, (230, 240))
            _=screen.blit(text_m,(250,345))
            self.line_bar.draw(screen)
            self.slider_bar.draw(screen)
            self.save_button.draw(screen)
            self.load_button.draw(screen)
            self.mute_switch.draw(screen)
        
        elif self.backpack_overlay_clicked:
            
            _=screen.blit(self.mask,(0,0))
            self.board_button.draw(screen)
            self.game_manager.bag.draw(screen)
        elif self.leading_system_clicked:   ### make the navigate system
            font = pg.font.Font("assets/fonts/Minecraft.ttf", 24)
            self.board_button.draw(screen)
            self.lead_to_riddle_end_button.draw(screen)
            self.lead_to_gym_button.draw(screen)
            self.lead_to_riddle_start_button.draw(screen)
            text_g=font.render(f"If you want some exercise.",True,(255,255,255))
            text_s=font.render(f"Just in case you forget the way to go home.",True,(255,255,255))
            text_e=font.render(f"Why not make some effort first?",True,(255,255,255))
            _=screen.blit(text_g,(300,350))
            _=screen.blit(text_e,(300,150))
            _=screen.blit(text_s,(300,250))
        self.overlay_button.draw(screen)
        self.backpack_button.draw(screen)
        self.leading_system_button.draw(screen)
        if not self.shop.close:
            font = pg.font.Font("assets/fonts/Minecraft.ttf", 32)
            text_c=font.render(f"{self.game_manager.bag._items_data[3]["count"]}", True, (255,255,255))
            text_b=font.render(f"you have {self.game_manager.bag._items_data[4]["count"]}  ! !", True, (255,255,255))
            text_p=font.render(f"you have ({self.game_manager.bag._items_data[0]["count"]}, {self.game_manager.bag._items_data[1]["count"]}, {self.game_manager.bag._items_data[2]["count"]} ) ! !", True, (255,255,255))
            font2=pg.font.Font("assets/fonts/Minecraft.ttf", 20)
            text_potion_price=font.render(f"$25", True, (255,255,255))
            text_ball_price=font.render(f"$5", True, (255,255,255))
            text_y=font2.render(f"you can only get 80% of price if you sell the item, BE CAREFULL ! !", True, (255,255,255))
            self.board_button.draw(screen)
            self.potion_button.draw(screen)
            self.ball_button.draw(screen)
            self.coin_button.draw(screen)
            self.sell_ball_button.draw(screen)
            self.sell_potion_button.draw(screen)
            self.buy_ball_button.draw(screen)
            self.buy_potion_button.draw(screen)
            _=screen.blit(text_ball_price,(230,250))
            _=screen.blit(text_potion_price,(230,150))
            _=screen.blit(text_c, (850, 450))
            _=screen.blit(text_p, (350, 150))
            _=screen.blit(text_b, (350, 250))
            _=screen.blit(text_y,(250,400))
        if self.online_manager and self.game_manager.player:
            
            list_online = self.online_manager.get_list_players()
            print(list_online)

            for player in list_online:
                if player["map"] == self.game_manager.current_map.path_name:
                    cam = camera
                    pos = cam.transform_position_as_position(Position(player["x"], player["y"]))
                    
                    self.sprite_online.position=pos
                    self.sprite_online.animation.moving=player["moving"]
                    
                    self.sprite_online.animation.update_pos(pos)
                    print(self.sprite_online.animation.moving)
                    self.sprite_online.draw(screen,None)
        # try:
            #     self._draw_chat_bubbles(...)
            # except Exception:
            #     pass
        if self.navigating:
            if len(self.navigation_path)==0:
                self.navigating=False
            for tile in self.navigation_path:
                px = tile[0]*GameSettings.TILE_SIZE+GameSettings.TILE_SIZE/2
                py = tile[1]*GameSettings.TILE_SIZE+GameSettings.TILE_SIZE/2
                if abs(px - self.game_manager.player.position.x) < GameSettings.TILE_SIZE and abs(py - self.game_manager.player.position.y) < GameSettings.TILE_SIZE:
                        self.navigation_path.remove(tile)
                        break
            for tile in self.navigation_path:
                px = tile[0]*GameSettings.TILE_SIZE+GameSettings.TILE_SIZE/2
                py = tile[1]*GameSettings.TILE_SIZE+GameSettings.TILE_SIZE/2
                walk=(0,0)
                if self.navigation_path.index(tile)+1<len(self.navigation_path):
                    walk=(self.navigation_path[self.navigation_path.index(tile)+1][0]-tile[0],self.navigation_path[self.navigation_path.index(tile)+1][1]-tile[1])
                if walk[0]>0:
                    d="right"
                elif walk[1]>0:
                    d="down"
                elif walk[0]<0:
                    d="left"
                else:
                    d="up"
                points=self.draw_triangle_prepare(px-camera.x, py-camera.y,d)
                pg.draw.polygon(screen,(255,0,0),points)
    def _draw_chat_bubbles(self, screen: pg.Surface, camera: PositionCamera) -> None:
        
        # if not self.online_manager:
        #     return
        # REMOVE EXPIRED BUBBLES
        # now = time.monotonic()
        # expired = [pid for pid, (_, ts) in self._chat_bubbles.items() if ts <= now]
        # for pid in expired:
        #     self._chat_bubbles.____(..., ...)
        # if not self._chat_bubbles:
        #     return

        # DRAW LOCAL PLAYER'S BUBBLE
        # local_pid = self.____
        # if self.game_manager.player and local_pid in self._chat_bubbles:
        #     text, _ = self._chat_bubbles[...]
        #     self._draw_bubble_for_pos(..., ..., ..., ..., ...)

        # DRAW OTHER PLAYERS' BUBBLES
        # for pid, (text, _) in self._chat_bubbles.items():
        #     if pid == local_pid:
        #         continue
        #     pos_xy = self._online_last_pos.____(..., ...)
        #     if not pos_xy:
        #         continue
        #     px, py = pos_xy
        #     self._draw_bubble_for_pos(..., ..., ..., ..., ...)

        pass
        """
        DRAWING CHAT BUBBLES:
        - When a player sends a chat message, the message should briefly appear above
        that player's character in the world, similar to speech bubbles in RPGs.
        - Each bubble should last only a few seconds before fading or disappearing.
        - Only players currently visible on the map should show bubbles.

        What you need to think about:
            ------------------------------
            1. **Which players currently have messages?**
            You will have a small structure mapping player IDs to the text they sent
            and the time the bubble should disappear.

            2. **How do you know where to place the bubble?**
            The bubble belongs above the player's *current position in the world*.
            The game already tracks each player’s world-space location.
            Convert that into screen-space and draw the bubble there.

            3. **How should bubbles look?**
            You decide. The visual style is up to you:
            - A rounded rectangle, or a simple box.
            - Optional border.
            - A small triangle pointing toward the character's head.
            - Enough padding around the text so it looks readable.

            4. **How do bubbles disappear?**
            Compare the current time to the stored expiration timestamp.
            Remove any bubbles that have expired.

            5. **In what order should bubbles be drawn?**
            Draw them *after* world objects but *before* UI overlays.

        Reminder:
        - For the local player, you can use the self.game_manager.player.position to get the player's position
        - For other players, maybe you can find some way to store other player's last position?
        - For each player with a message, maybe you can call a helper to actually draw a single bubble?
        """

    def _draw_chat_bubble_for_pos(self, screen: pg.Surface, camera: PositionCamera, world_pos: Position, text: str, font: pg.font.Font):
        pass
    """
    Steps:
        ------------------
        1. Convert a player’s world position into a location on the screen.
        (Use the camera system provided by the game engine.)

        2. Decide where "above the player" is.
        Typically a little above the sprite’s head.

        3. Measure the rendered text to determine bubble size.
        Add padding around the text.
    """
                