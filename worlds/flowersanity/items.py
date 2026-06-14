from random import Random
from typing import TYPE_CHECKING, Any

from BaseClasses import Item, ItemClassification
from .data import colornames_trunc, calculations

if TYPE_CHECKING:
    from . import FlowersanityWorld


class FlowersanityItem(Item):
    game = "Flowersanity"


def lookup_table() -> dict[str, int]:
    calcs = tuple(calculations.item_names.values())
    return {
        dat[0]: (num or 0x1000000)
        for num, dat in colornames_trunc.colors.items()
    } | {
        calcs[i]: 0x1000001 + i for i in range(len(calcs))
    }


def generate_item(name: str, world: "FlowersanityWorld") -> FlowersanityItem:
    # Item id from lookup table is used instead of id from data for safety purposes
    return FlowersanityItem(name, ItemClassification.progression_deprioritized_skip_balancing,
                            world.item_name_to_id[name], world.player)


def get_main_item_pool(world: "FlowersanityWorld") -> list[FlowersanityItem]:
    return [generate_item(name, world) for name in calculations.item_names.values()] + [
        generate_item(colornames_trunc.colors[color][0], world) for color in world.colors
    ]


def generate_filler(world: "FlowersanityWorld") -> str:
    return "Black"


def random_choice_nested(random: Random, nested: list[Any | list | dict]) -> Any:
    """Helper function for getting a random element from a nested list."""
    current: Any | list | dict = nested
    while isinstance(current, list | dict):
        if isinstance(current, list):
            current = random.choice(current)
        else:
            current = random.choice(tuple(current.keys()))
    return current
