from enum import Enum, auto
from typing import Dict

from BaseClasses import Location


class Loc(Enum):
    Rock = auto()
    Wood = auto()
    Foliage = auto()
    Plank = auto()
    Wet = auto()
    MetalStiff = auto()
    Metal = auto()
    Bone = auto()
    Concrete = auto()
    RunningWater = auto()
    Rubber = auto()
    Cloth = auto()
    Ice = auto()
    Snow = auto()
    Mushroom = auto()
    Cloud = auto()


class Reg(Enum):
    MENU = auto()
    EARLY = auto()
    FOSSIL = auto()
    FIRST_CHECKPOINT = auto()
    CLOTHESLINE = auto()
    LATE = auto()


location_table: Dict[Loc, Reg] = {
    Loc.Rock: Reg.MENU,
    Loc.Wood: Reg.MENU,
    Loc.Foliage: Reg.MENU,
    Loc.Plank: Reg.EARLY,
    Loc.Wet: Reg.EARLY,
    Loc.MetalStiff: Reg.EARLY,
    Loc.Metal: Reg.EARLY,
    Loc.Bone: Reg.FOSSIL,
    Loc.Concrete: Reg.FOSSIL,
    Loc.RunningWater: Reg.FIRST_CHECKPOINT,
    Loc.Rubber: Reg.CLOTHESLINE,
    Loc.Cloth: Reg.CLOTHESLINE,
    Loc.Ice: Reg.LATE,
    Loc.Snow: Reg.LATE,
    Loc.Mushroom: Reg.LATE,
    Loc.Cloud: Reg.LATE,
}


class ADGACLocation(Location):
    game = "A Difficult Game About Climbing"
