from typing import TYPE_CHECKING, Iterator

if TYPE_CHECKING:
    from ... import Shapez2World


def generate_default(world: "Shapez2World") -> Iterator[str]:

    if world.options.lock_locations.is_operator_lines:
        for i in range(world.options.operator_levels_adjustments["Operator lines"]):
            yield f"Operator line #{i + 1}"
