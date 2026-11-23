from typing import TYPE_CHECKING, Iterator

if TYPE_CHECKING:
    from ... import Shapez2World


def generate_default(world: "Shapez2World") -> Iterator[str]:
    from ...data.items.mechanics import always

    yield from always.keys()

    if world.options.lock_locations.is_operator_levels_tab:
        yield "Operator Levels"


def generate_starting(world: "Shapez2World") -> Iterator[str]:
    from ...data.items.mechanics import starting

    if not world.options.lock_locations.is_operator_levels_tab:
        yield "Operator Levels"

    yield from starting
