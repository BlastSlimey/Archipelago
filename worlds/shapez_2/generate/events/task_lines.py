from typing import TYPE_CHECKING
from BaseClasses import Region, LocationProgressType, ItemClassification


if TYPE_CHECKING:
    from ... import Shapez2World
    from ...data import AccessRule


def get_events(world: "Shapez2World", regions: dict[str, Region]) -> None:
    from ...items import Shapez2Item
    from ...locations import Shapez2Location
    from ..rules import extended_has

    def get_rule(_i: int) -> "AccessRule":
        return lambda state: extended_has(world, state, f"Job line #{_i}")

    reg = regions["Events"]
    lines_count = world.options.jobs_adjustments["Job lines"]
    all_unlocked = not world.options.lock_locations.is_job_lines

    for x in range(lines_count):
        if all_unlocked or f"Job line #{x+1}" in world.starting_items:
            world.starting_items.append(f"[ACCESS] Job line {x+1}")
        else:
            loc = Shapez2Location(
                world.player, f"[ACCESS] Job line {x+1}", None, reg, LocationProgressType.PRIORITY,
                get_rule(x+1)
            )
            loc.place_locked_item(Shapez2Item(
                f"[ACCESS] Job line {x+1}", ItemClassification.progression, None, world.player
            ))
            reg.locations.append(loc)
