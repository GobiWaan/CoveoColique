from __future__ import annotations

from dataclasses import dataclass
from typing import List, Dict
from enum import Enum, unique
from cattrs.gen import make_dict_structure_fn, override
import cattrs


@dataclass
class GameMessage:
    type: str
    tick: int
    map: Map
    round: int
    ticksUntilPayout: int
    teamId: str
    teams: List[str]
    teamInfos: Dict[str, TeamInfo]
    playAreas: Dict[str, PlayArea]
    shop: Shop
    lastTickErrors: List[str]
    constants: Constants


@dataclass
class TeamInfo:
    id: str
    name: str
    money: int
    hp: int
    isAlive: bool
    payoutBonus: int
    sentReinforcements: List[EnemyReinforcements]


@dataclass
class Map:
    name: str
    width: int
    height: int
    paths: List[Path]
    obstacles: List[Position]


@dataclass
class Path:
    tiles: List[Position]
    id: str


@dataclass
class PlayArea:
    teamId: str
    enemies: List[Enemy]
    enemyReinforcementsQueue: List[EnemyReinforcements]
    towers: List[Tower]
    grid: Dict[int, Dict[int, Tile]]

    def get_tile_at(self, position: Position):
        try:
            return self.grid[position.x][position.y]
        except KeyError:
            return None

    def is_empty(self, position: Position):
        tile = self.get_tile_at(position)
        if tile is None:
            return True
        return len(tile.towers) == 0 and len(tile.enemies) == 0


@unique
class EnemyType(str, Enum):
    LVL1 = "LVL1"
    LVL2 = "LVL2"
    LVL3 = "LVL3"
    LVL4 = "LVL4"
    LVL5 = "LVL5"
    LVL6 = "LVL6"
    LVL7 = "LVL7"
    LVL8 = "LVL8"
    LVL9 = "LVL9"
    LVL10 = "LVL10"
    LVL11 = "LVL11"
    LVL12 = "LVL12"


@dataclass
class Enemy:
    id: str
    type: EnemyType
    position: Position
    precisePosition: PositionPrecise
    isKilled: bool
    hasEndedPath: bool
    path: str


@dataclass
class EnemyReinforcements:
    enemyType: EnemyType
    count: int
    fromTeam: str
    toTeam: str

cattrs.register_structure_hook(EnemyReinforcements, make_dict_structure_fn(EnemyReinforcements, cattrs.global_converter, fromTeam=override(rename="from"), toTeam=override(rename="to")))


@dataclass
class Tower:
    id: str
    type: TowerType
    position: Position
    width: int
    height: int
    isShooting: bool


@dataclass
class Tile:
    towers: List[Tower]
    enemies: List[Enemy]
    paths: List[str]
    hasObstacle: bool


@dataclass
class Shop:
    towers: Dict[TowerType, TowerShopEntry]
    reinforcements: Dict[EnemyType, ReinforcementsShopEntry]


@dataclass
class TowerShopEntry:
    price: int


@dataclass
class ReinforcementsShopEntry:
    price: float
    payoutBonus: float
    count: int
    delayPerSpawnInTicks: float


@dataclass(eq=True, frozen=True)
class Position:
    x: int
    y: int


@dataclass
class PositionPrecise:
    x: float
    y: float


@dataclass
class Constants:
    payoutIntervalInTick: int
    maxReinforcementsSentPerTeam: int


@unique
class TowerType(str, Enum):
    SPIKE_SHOOTER = "SPIKE_SHOOTER"
    BOMB_SHOOTER = "BOMB_SHOOTER"
    SPEAR_SHOOTER = "SPEAR_SHOOTER"
