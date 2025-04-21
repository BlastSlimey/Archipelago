from typing import Dict, Callable, Any, List

from BaseClasses import Item, ItemClassification as IClass
from .options import SonicRushOptions


def always_progression(options: SonicRushOptions) -> IClass:
    return IClass.progression


def always_useful(options: SonicRushOptions) -> IClass:
    return IClass.useful


def always_filler(options: SonicRushOptions) -> IClass:
    return IClass.filler


def always_trap(options: SonicRushOptions) -> IClass:
    return IClass.trap


zone_unlocks: Dict[str, Callable[[SonicRushOptions], IClass]] = {
    "Unlock Zone 1 (Sonic)": always_progression,
    "Unlock Zone 2 (Sonic)": always_progression,
    "Unlock Zone 3 (Sonic)": always_progression,
    "Unlock Zone 4 (Sonic)": always_progression,
    "Unlock Zone 5 (Sonic)": always_progression,
    "Unlock Zone 6 (Sonic)": always_progression,
    "Unlock Zone 7 (Sonic)": always_progression,
    "Unlock F-Zone (Sonic)": always_progression,
    "Unlock Zone 1 (Blaze)": always_progression,
    "Unlock Zone 2 (Blaze)": always_progression,
    "Unlock Zone 3 (Blaze)": always_progression,
    "Unlock Zone 4 (Blaze)": always_progression,
    "Unlock Zone 5 (Blaze)": always_progression,
    "Unlock Zone 6 (Blaze)": always_progression,
    "Unlock Zone 7 (Blaze)": always_progression,
    "Unlock F-Zone (Blaze)": always_progression,
}

progressive_level_selects: Dict[str, Callable[[SonicRushOptions], IClass]] = {
    "Progressive Level Select (Sonic)": always_progression,
    "Progressive Level Select (Blaze)": always_progression,
}

emeralds: Dict[str, Callable[[SonicRushOptions], IClass]] = {
    "Red Chaos Emerald": always_progression,
    "Blue Chaos Emerald": always_progression,
    "Yellow Chaos Emerald": always_progression,
    "Green Chaos Emerald": always_progression,
    "White Chaos Emerald": always_progression,
    "Turquoise Chaos Emerald": always_progression,
    "Purple Chaos Emerald": always_progression,
    "Red Sol Emerald": always_progression,
    "Blue Sol Emerald": always_progression,
    "Yellow Sol Emerald": always_progression,
    "Green Sol Emerald": always_progression,
    "White Sol Emerald": always_progression,
    "Turquoise Sol Emerald": always_progression,
    "Purple Sol Emerald": always_progression,
}

sidekicks: Dict[str, Callable[[SonicRushOptions], IClass]] = {
    "Tails": always_filler,
    "Cream": always_filler,
    "Kidnapping Tails": always_trap,
    "Kidnapping Cream": always_trap,
}

fillers: Dict[str, Callable[[SonicRushOptions], IClass]] = {
    "Extra Life (Sonic)": always_filler,
    "Extra Life (Blaze)": always_filler,
}

traps: Dict[str, Callable[[SonicRushOptions], IClass]] = {
    "Halving Extra Lives (Sonic)": always_trap,
    "Halving Extra Lives (Blaze)": always_trap,
}

item_table: Dict[str, Callable[[SonicRushOptions], IClass]] = {
    **zone_unlocks,
    **progressive_level_selects,
    **emeralds,
    **sidekicks,
    **fillers,
    **traps,
}

item_list: List[str] = [
    *zone_unlocks,
    *progressive_level_selects,
    *emeralds,
    *sidekicks,
    *fillers,
    *traps,
]

base_id = 20010707
item_lookup_by_name: Dict[str, int] = {name: next_id for next_id, name in enumerate(item_list, base_id)}
item_lookup_by_id: Dict[int, str] = {next_id: name for next_id, name in enumerate(item_list, base_id)}


def filler(random: float) -> str:
    """Returns a random filler item."""
    pool = [
        *fillers
    ]
    return random_choice_nested(random, pool)


def trap(random: float) -> str:
    """Returns a random trap item."""
    pool = [
        *traps
    ]
    return random_choice_nested(random, pool)


def random_choice_nested(random: float, nested: List[Any]) -> Any:
    """Helper function for getting a random element from a nested list."""
    current: Any = nested
    while isinstance(current, List):
        index_float = random*len(current)
        current = current[int(index_float)]
        random = index_float-int(index_float)
    return current


item_descriptions = {}


class SonicRushItem(Item):
    game = "Sonic Rush"
