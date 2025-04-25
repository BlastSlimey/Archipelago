from typing import Dict, Tuple, List

from BaseClasses import Region, MultiWorld, LocationProgressType, ItemClassification, CollectionState
from worlds.generic.Rules import set_rule
from .items import SonicRushItem, emeralds
from .locations import SonicRushLocation
from .options import SonicRushOptions


def can_play_zone(state: CollectionState, player: int, zone: int, char: str) -> bool:
    if state.has(f"Unlock Zone {zone} ({char})", player):
        # Zone is unlocked, no further checking needed
        return True
    progressive_level_selects = state.count(f"Progressive Level Select ({char})", player)
    if not progressive_level_selects >= zone:
        # Not enough progressive level selects, zone is unreachable
        return False
    for any_zone in range(1, progressive_level_selects+1):
        # Zone is reachable through level select, but level select must be accessible through another zone
        if state.has(f"Unlock Zone {any_zone} ({char})", player):
            return True
    # Neither unlocked nor through level select accessible
    return False


def can_play_f_zone(state: CollectionState, player: int, char: str) -> bool:
    return state.has(f"Unlock F-Zone ({char})", player)


def can_play_extra_zone(state: CollectionState, player: int) -> bool:
    return state.has_all(emeralds, player)


def can_play_all_main_zones(state: CollectionState, player: int, char: str, options: SonicRushOptions) -> bool:
    for zone in range(1, 8):
        if not can_play_zone(state, player, zone, char):
            return False
    return options.screw_f_zone or can_play_f_zone(state, player, char)


def create_regions(player: int, multiworld: MultiWorld, options: SonicRushOptions, location_name_to_id: Dict[str, int],
                   included_locations: Dict[str, Tuple[str, LocationProgressType]]) -> List[Region]:
    """Creates and returns a list of all regions with entrances and all locations placed correctly."""

    regions: Dict[str, Region] = {}

    for char1 in ["Sonic", "Blaze"]:
        regions[f"F-Zone ({char1})"] = Region(f"F-Zone ({char1})", player, multiworld)
        for zone in [1, 2, 3, 4, 5, 6, 7]:
            regions[f"Zone {zone} ({char1})"] = Region(f"Zone {zone} ({char1})", player, multiworld)

    regions["Extra Zone"] = Region("Extra Zone", player, multiworld)
    regions["Goal"] = Region("Goal", player, multiworld)
    regions["Menu"] = Region("Menu", player, multiworld)

    for name, data in included_locations.items():
        regions[data[0]].locations.append(
            SonicRushLocation(player, name, location_name_to_id[name], regions[data[0]], data[1])
        )

    # Create goal event
    goal_location = SonicRushLocation(player, "Goal", None, regions["Goal"], LocationProgressType.DEFAULT)
    goal_location.place_locked_item(SonicRushItem("Goal", ItemClassification.progression_skip_balancing, None, player))
    if options.goal == "bosses_once":
        set_rule(
            goal_location,
            lambda state: (can_play_zone(state, player, 1, "Sonic") or can_play_zone(state, player, 2, "Blaze")) and
                          (can_play_zone(state, player, 2, "Sonic") or can_play_zone(state, player, 4, "Blaze")) and
                          (can_play_zone(state, player, 3, "Sonic") or can_play_zone(state, player, 3, "Blaze")) and
                          (can_play_zone(state, player, 4, "Sonic") or can_play_zone(state, player, 1, "Blaze")) and
                          (can_play_zone(state, player, 5, "Sonic") or can_play_zone(state, player, 6, "Blaze")) and
                          (can_play_zone(state, player, 6, "Sonic") or can_play_zone(state, player, 5, "Blaze")) and
                          (can_play_zone(state, player, 7, "Sonic") and can_play_zone(state, player, 7, "Blaze")) and
                          (options.screw_f_zone or
                           can_play_f_zone(state, player, "Sonic") or can_play_f_zone(state, player, "Blaze"))
        )
    elif options.goal == "bosses_both":
        set_rule(
            goal_location,
            lambda state: can_play_all_main_zones(state, player, "Sonic", options) and
                          can_play_all_main_zones(state, player, "Blaze", options)
        )
    elif options.goal == "extra_zone":
        set_rule(
            goal_location,
            lambda state: can_play_extra_zone(state, player)
        )
    elif options.goal == "100_percent":
        set_rule(
            goal_location,
            lambda state: can_play_all_main_zones(state, player, "Sonic", options) and
                          can_play_all_main_zones(state, player, "Blaze", options) and
                          can_play_extra_zone(state, player)
        )
    else:
        set_rule(goal_location, lambda state: False)  # In case I add another goal and forget to add a rule for it
    regions["Goal"].locations.append(goal_location)
    multiworld.completion_condition[player] = lambda state: state.has("Goal", player)

    # Connect Menu to rest of regions
    regions["Menu"].connect(regions["Goal"], "Goal")
    regions["Menu"].connect(
        regions["Extra Zone"], "Access Extra Zone",
        lambda state: can_play_extra_zone(state, player)
    )
    for char in ["Sonic", "Blaze"]:
        regions["Menu"].connect(
            regions[f"F-Zone ({char})"], f"Access F-Zone ({char})",
            lambda state: can_play_f_zone(state, player, char)
        )
        for zone in range(1, 8):
            regions["Menu"].connect(
                regions[f"Zone {zone} ({char})"], f"Access Zone {zone} ({char})",
                lambda state: can_play_zone(state, player, zone, char)
            )

    return list(regions.values())
