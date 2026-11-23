from typing import TYPE_CHECKING, Iterator

if TYPE_CHECKING:
    from ... import Shapez2World


def generate_default(world: "Shapez2World") -> Iterator[str]:
    from ...data.items.buildings import always, simple_processors

    yield from always.keys()

    for name in simple_processors:
        if name != world.starting_processor:
            yield name

    if world.options.item_pool_modifiers.is_unlock_pipes_with_pumps:
        yield "Mini Pump + Pipe"
    else:
        yield "Mini Pump"
        yield "Pipe"

    # if world.options.item_pool_modifiers.is_add_sandbox_buildings:
    #     yield from sandbox.keys()


def generate_starting(world: "Shapez2World") -> Iterator[str]:
    from ...data.items.buildings import starting

    yield from starting.keys()

    if world.starting_processor is not None:
        yield world.starting_processor
