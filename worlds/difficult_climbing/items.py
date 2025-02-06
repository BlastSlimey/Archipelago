from typing import Dict, Callable

from BaseClasses import ItemClassification as IClass, Item
from .options import ADGACOptions


def always_progression(options: ADGACOptions) -> IClass:
    return IClass.progression


def always_trap(options: ADGACOptions) -> IClass:
    return IClass.trap


def prog_not_challenge(options: ADGACOptions) -> IClass:
    return IClass.progression if not options.difficulty == "challenge" else IClass.useful


def prog_extra_buff(options: ADGACOptions) -> IClass:
    return IClass.progression if options.difficulty == "extra_buff" else IClass.useful


items_list: Dict[str, Callable[[ADGACOptions], IClass]] = {
    "Grip Strength": always_progression,
    "Swinging Metal Beam": always_progression,
    "Metal Beam Angle Increase": always_progression,
    "Deafness Trap": always_trap,
    "Rotating Cog Repair": prog_not_challenge,
    "Rotating Cog Halting": prog_extra_buff,
    "Side Cog Halting": prog_extra_buff,
}


class ADGACItem(Item):
    game = "A Difficult Game About Climbing"
