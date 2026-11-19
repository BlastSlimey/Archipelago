from typing import TYPE_CHECKING
from BaseClasses import Region, LocationProgressType, ItemClassification

if TYPE_CHECKING:
    from ... import Shapez2World


def get_events(world: "Shapez2World", regions: dict[str, Region]) -> None:
    from ...locations import Shapez2Location
    from ...items import Shapez2Item
    from ..rules import extended_has_any, extended_has, extended_has_all

    reg = regions["Events"]

    if any(it in world.starting_items for it in ("Cutter", "Half Destroyer")):
        world.starting_items.append("[PROCESSOR] Cutter")
    else:
        loc = Shapez2Location(
            world.player, "[PROCESSOR] Cutter", None, reg, LocationProgressType.PRIORITY,
            lambda state: extended_has_any(world, state, "Cutter", "Half Destroyer")
        )
        loc.place_locked_item(Shapez2Item(
            "[PROCESSOR] Cutter", ItemClassification.progression, None, world.player
        ))
        reg.locations.append(loc)

    if any(it in world.starting_items for it in ("Rotator (CW)", "Rotator (CCW)")):
        world.starting_items.append("[PROCESSOR] Rotator")
    else:
        loc = Shapez2Location(
            world.player, "[PROCESSOR] Rotator", None, reg, LocationProgressType.PRIORITY,
            lambda state: extended_has_any(world, state, "Rotator (CW)", "Rotator (CCW)")
        )
        loc.place_locked_item(Shapez2Item(
            "[PROCESSOR] Rotator", ItemClassification.progression, None, world.player
        ))
        reg.locations.append(loc)

    if "2nd Machine Level" in world.starting_items and any(it in world.starting_items for it in ("Stacker", "Stacker (Bent)")):
        world.starting_items.append("[PROCESSOR] Stacker")
    else:
        loc = Shapez2Location(
            world.player, "[PROCESSOR] Stacker", None, reg, LocationProgressType.PRIORITY,
            lambda state: extended_has_any(world, state, "Stacker", "Stacker (Bent)")
                          and extended_has(world, state, "2nd Machine Level")
        )
        loc.place_locked_item(Shapez2Item(
            "[PROCESSOR] Stacker", ItemClassification.progression, None, world.player
        ))
        reg.locations.append(loc)

    # Shared requirements of fluid-related processors
    if world.options.item_pool_modifiers.is_unlock_pipes_with_pumps:
        fluids_rule = lambda state: (
            extended_has_any(world, state, "Asteroid Pump + Booster + Pipe", "Asteroid Pump + Pipe")
            and extended_has(world, state, "Mini Pump + Pipe")
        )
        fluids_condition = "Mini Pump + Pipe" in world.starting_items and any(
            it in world.starting_items for it in ("Asteroid Pump + Booster + Pipe", "Asteroid Pump + Pipe")
        )
    else:
        fluids_rule = lambda state: (
            extended_has_all(world, state, "Space Pipe", "Pipe", "Mini Pump")
            and extended_has_any(world, state, "Asteroid Pump + Booster", "Asteroid Pump")
        )
        fluids_condition = any(
            it in world.starting_items for it in ("Asteroid Pump + Booster", "Asteroid Pump")
        ) and all(
            it in world.starting_items for it in ("Space Pipe", "Pipe", "Mini Pump")
        )

    if fluids_condition and "Painter" in world.starting_items:
        world.starting_items.append("[PROCESSOR] Painter")
    else:
        loc = Shapez2Location(
            world.player, "[PROCESSOR] Painter", None, reg, LocationProgressType.PRIORITY,
            lambda state: extended_has(world, state, "Painter") and fluids_rule(state)
        )
        loc.place_locked_item(Shapez2Item(
            "[PROCESSOR] Painter", ItemClassification.progression, None, world.player
        ))
        reg.locations.append(loc)

    if fluids_condition and "Color Mixer" in world.starting_items:
        world.starting_items.append("[PROCESSOR] Mixer")
    else:
        loc = Shapez2Location(
            world.player, "[PROCESSOR] Mixer", None, reg, LocationProgressType.PRIORITY,
            lambda state: extended_has(world, state, "Color Mixer") and fluids_rule(state)
        )
        loc.place_locked_item(Shapez2Item(
            "[PROCESSOR] Mixer", ItemClassification.progression, None, world.player
        ))
        reg.locations.append(loc)

    if "Pin Pusher" in world.starting_items:
        world.starting_items.append("[PROCESSOR] Pin Pusher")
    else:
        loc = Shapez2Location(
            world.player, "[PROCESSOR] Pin Pusher", None, reg, LocationProgressType.PRIORITY,
            lambda state: extended_has(world, state, "Pin Pusher")
        )
        loc.place_locked_item(Shapez2Item(
            "[PROCESSOR] Pin Pusher", ItemClassification.progression, None, world.player
        ))
        reg.locations.append(loc)

    if fluids_condition and all(it in world.starting_items for it in ("Crystal Generator", "2nd Machine Level")):
        world.starting_items.append("[PROCESSOR] Crystallizer")
    else:
        loc = Shapez2Location(
            world.player, "[PROCESSOR] Crystallizer", None, reg, LocationProgressType.PRIORITY,
            lambda state: extended_has_all(world, state, "Crystal Generator", "2nd Machine Level") and fluids_rule(state)
        )
        loc.place_locked_item(Shapez2Item(
            "[PROCESSOR] Crystallizer", ItemClassification.progression, None, world.player
        ))
        reg.locations.append(loc)

    if "Swapper" in world.starting_items:
        world.starting_items.append("[PROCESSOR] Swapper")
    else:
        loc = Shapez2Location(
            world.player, "[PROCESSOR] Swapper", None, reg, LocationProgressType.PRIORITY,
            lambda state: extended_has(world, state, "Swapper")
        )
        loc.place_locked_item(Shapez2Item(
            "[PROCESSOR] Swapper", ItemClassification.progression, None, world.player
        ))
        reg.locations.append(loc)
