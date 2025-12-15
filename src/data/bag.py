import pygame as pg
import json
from src.utils import GameSettings 
from src.utils.definition import Monster, Item
# from saves import something


class Bag:
    _monsters_data: list[Monster]
    _items_data: list[Item]

    def __init__(self, monsters_data: list[Monster] | None = None, items_data: list[Item] | None = None):
        self._monsters_data = monsters_data if monsters_data else []
        self._items_data = items_data if items_data else []

    def update(self, dt: float):
        pass

    def draw(self, screen: pg.Surface):
        px, py = GameSettings.SCREEN_WIDTH // 2, GameSettings.SCREEN_HEIGHT * 3 // 4
        x=px-400
        y=py-400
        font = pg.font.Font("assets/fonts/Minecraft.ttf", 24)
        for mons in self._monsters_data:
            text = font.render(f"{mons['name']} hp:{mons['hp']} max_hp:{mons['max_hp']} level:{mons["level"]}", True, (255,255,255))
            _=screen.blit(text, (x, y))
            y+=30
        for it in self._items_data:
            text=font.render(f"{it["name"]}:{it['count']} ", True, (255,255,255))
            screen.blit(text, (x, y))
            y+=30
    def to_dict(self) -> dict[str, object]:
        return {
            "monsters": list(self._monsters_data),
            "items": list(self._items_data)
        }

    @classmethod
    def from_dict(cls, data: dict[str, object]) -> "Bag":
        monsters = data.get("monsters") or []
        items = data.get("items") or []
        bag = cls(monsters, items)
        return bag