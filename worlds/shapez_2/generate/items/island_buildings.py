from typing import TYPE_CHECKING, Iterator
from ...items import Shapez2Item

if TYPE_CHECKING:
    from ... import Shapez2World


def generate_default(world: "Shapez2World") -> Iterator[Shapez2Item]:
    from ...data.items.island_buildings import always, miners

    pool_mods = world.options.item_pool_modifiers

    for name, data in always.items():
        yield Shapez2Item(name, data.classification(world), world.item_name_to_id[name], world.player)

    if pool_mods.is_unlock_booster_with_miners and pool_mods.is_unlock_pipes_with_pumps:
        to_add = ("Asteroid Pump + Booster + Pipe", )
    elif pool_mods.is_unlock_booster_with_miners:
        to_add = ("Asteroid Pump + Booster", "Space Pipe")
    elif pool_mods.is_unlock_pipes_with_pumps:
        to_add = ("Asteroid Pump + Pipe", "Asteroid Pump Booster", "Asteroid Miner Booster")
    else:
        to_add = ("Asteroid Pump", "Asteroid Pump Booster", "Space Pipe", "Asteroid Miner Booster")

    for name in to_add:
        data = miners[name]
        yield Shapez2Item(name, data.classification(world), world.item_name_to_id[name], world.player)


def generate_starting(world: "Shapez2World") -> Iterator[str]:
    from ...data.items.island_buildings import starting

    yield from starting

    if world.options.item_pool_modifiers.is_unlock_booster_with_miners:
        yield "Asteroid Miner + Booster"
    else:
        yield "Asteroid Miner"
