from typing import TYPE_CHECKING, Iterator
from ...items import Shapez2Item

if TYPE_CHECKING:
    from ... import Shapez2World


def generate_default(world: "Shapez2World") -> Iterator[Shapez2Item]:
    from ...data.items.mechanics import always

    operator_levels_locked = "Lock operator levels tab" in world.options.location_modifiers

    for name, data in always.items():
        if operator_levels_locked or name != "Operator Levels":
            yield Shapez2Item(name, data.classification(world), world.item_name_to_id[name], world.player)


def generate_starting(world: "Shapez2World") -> Iterator[str]:
    from ...data.items.mechanics import starting

    if "Lock operator levels tab" not in world.options.location_modifiers:
        yield "Operator Levels"

    yield from starting
