from typing import TYPE_CHECKING, Iterator
from ...items import Shapez2Item

if TYPE_CHECKING:
    from ... import Shapez2World


def generate_default(world: "Shapez2World") -> Iterator[Shapez2Item]:
    from ...data.items.island_buildings import always

    for name, data in always.items():
        yield Shapez2Item(name, data.classification(world), world.item_name_to_id[name], world.player)


def generate_starting() -> Iterator[str]:
    from ...data.items.island_buildings import starting

    yield from starting
