from typing import TYPE_CHECKING, Iterator

if TYPE_CHECKING:
    from ... import Shapez2World


def generate_default(world: "Shapez2World") -> Iterator[str]:
    from ...data.items.island_buildings import always

    pool_mods = world.options.item_pool_modifiers

    yield from always.keys()

    if pool_mods.is_unlock_booster_with_miners and pool_mods.is_unlock_pipes_with_pumps:
        yield "Asteroid Pump + Booster + Pipe"
    elif pool_mods.is_unlock_booster_with_miners:
        yield "Asteroid Pump + Booster"
        yield "Space Pipe"
    elif pool_mods.is_unlock_pipes_with_pumps:
        yield "Asteroid Pump + Pipe"
        yield "Asteroid Pump Booster"
        yield "Asteroid Miner Booster"
    else:
        yield "Asteroid Pump"
        yield "Asteroid Pump Booster"
        yield "Space Pipe Pipe"
        yield "Asteroid Miner Booster"


def generate_starting(world: "Shapez2World") -> Iterator[str]:
    from ...data.items.island_buildings import starting

    yield from starting

    if world.options.item_pool_modifiers.is_unlock_booster_with_miners:
        yield "Asteroid Miner + Booster"
    else:
        yield "Asteroid Miner"
