from typing import TYPE_CHECKING, Iterator
from ...items import Shapez2Item

if TYPE_CHECKING:
    from ... import Shapez2World


def generate_default(world: "Shapez2World") -> Iterator[Shapez2Item]:
    from ...data.items.buildings import always, simple_processors, pump_pipe

    for name, data in always.items():
        yield Shapez2Item(name, data.classification(world), data.item_id, world.player)

    for name, data in simple_processors.items():
        if name != world.starting_processor:
            yield Shapez2Item(name, data.classification(world), data.item_id, world.player)

    if world.options.item_pool_modifiers.is_unlock_pipes_with_pumps:
        data = pump_pipe["Mini Pump + Pipe"]
        yield Shapez2Item("Mini Pump + Pipe", data.classification(world), data.item_id, world.player)
    else:
        data = pump_pipe["Mini Pump"]
        yield Shapez2Item("Mini Pump", data.classification(world), data.item_id, world.player)
        data = pump_pipe["Pipe"]
        yield Shapez2Item("Pipe", data.classification(world), data.item_id, world.player)

    # if world.options.item_pool_modifiers.is_add_sandbox_buildings:
    #     for name, data in sandbox.items():
    #         yield Shapez2Item(name, data.classification(world), data.item_id, world.player)


def generate_starting(world: "Shapez2World") -> Iterator[str]:
    from ...data.items.buildings import starting

    yield from starting.keys()

    if world.starting_processor is not None:
        yield world.starting_processor
