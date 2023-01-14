from __future__ import annotations

from dataclasses import dataclass
from dataclasses_json import dataclass_json
from game_message import Position, EnemyType, TowerType

@dataclass_json
@dataclass
class SellAction:
    position: Position
    action: str = "SELL"


@dataclass_json
@dataclass
class SendReinforcementsAction:
    enemyType: EnemyType
    team: str
    action: str = "SEND_REINFORCEMENTS"


@dataclass_json
@dataclass
class BuildAction:
    towerType: TowerType
    position: Position
    action: str = "BUILD"
