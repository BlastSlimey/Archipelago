import math
from typing import Optional, TYPE_CHECKING

from BaseClasses import Location, Region, LocationProgressType, ItemClassification
from Options import OptionError
from .data.locations import milestones, tasks, operator_levels
from .generate import reseed

if TYPE_CHECKING:
    from . import Shapez2World
    from .data import ExtendedRule, AccessRule


class Shapez2Location(Location):
    game = "shapez 2"

    def __init__(self, player: int, name: str, address: Optional[int], region: Region,
                 progress_type: LocationProgressType, rule: "AccessRule"):
        super(Shapez2Location, self).__init__(player, name, address, region)
        self.progress_type = progress_type
        self.access_rule = rule


def lookup_table() -> dict[str, int]:
    return {
        name: data.location_id
        for table in (milestones.locations, tasks.locations, operator_levels.locations)
        for name, data in table.items()
    }


def get_regions(world: "Shapez2World") -> dict[str, Region]:

    operator_adj = world.options.operator_levels_adjustments

    return {
        "Menu": Region("Menu", world.player, world.multiworld),
        "Events": Region("Events", world.player, world.multiworld),
    } | {
        f"Milestone {x}": Region(f"Milestone {x}", world.player, world.multiworld)
        for x in range(1, world.options.milestone_adjustments["Milestones"] + 1)
    } | {
        f"Job line {x}": Region(f"Job line {x}", world.player, world.multiworld)
        for x in range(1, world.options.jobs_adjustments["Job lines"] + 1)
    } | {
        f"Operator levels (section {x})": Region(f"Operator levels (section {x})", world.player, world.multiworld)
        for x in range(
            1,
            operator_adj["Operator lines"] + 1
            if operator_adj["Operator level checks"] // operator_adj["Operator lines"] >= 5
            else int(math.ceil(operator_adj["Operator level checks"] / 5)) + 1
        )
    }


def connect_regions(world: "Shapez2World", regions: dict[str, Region]) -> None:
    from .data import region_connections

    def get_rule(ext_rule: Optional["ExtendedRule"]) -> "AccessRule":
        if ext_rule is None:
            return lambda state: True
        else:
            return lambda state: ext_rule(state, world)

    for name, data in region_connections.connections.items():
        if data.entering_region in regions and data.exiting_region in regions:
            regions[data.exiting_region].connect(
                regions[data.entering_region],
                name,
                get_rule(data.rule)
            )


@reseed
def pre_generate_logic(world: "Shapez2World") -> None:
    from .generate.shapes import milestones, task_lines, operator_lines, blueprint_points

    world.milestone_processors = milestones.get_processors_list(world)
    world.task_processors = task_lines.get_processors_list(world)
    world.operator_processors = operator_lines.get_processors_list(world)

    world.milestone_shapes = milestones.get_shapes_list(world)
    world.task_shapes = task_lines.get_shapes_list(world, world.task_processors)
    world.operator_shapes = operator_lines.get_shapes_list(world, world.operator_processors)
    world.blueprint_shapes = blueprint_points.get_shapes_list(world)

    world.blueprint_points = blueprint_points.get_points(world, world.blueprint_shapes)


@reseed
def calculate_locations_count(world: "Shapez2World"):
    operator_lvl_adj = world.options.operator_levels_adjustments
    lock_locs = world.options.lock_locations
    miles_adj = world.options.milestone_adjustments
    jobs_adj = world.options.jobs_adjustments
    if world.options.goal == "operator_levels" and not operator_lvl_adj["Operator level checks"]:
        raise OptionError(f"{world.player_name}: Goal operator_levels requires at least 1 operator level check.")
    required_locations = (
        60 +
        jobs_adj["Job lines"] * lock_locs.is_job_lines +
        operator_lvl_adj["Operator lines"] * lock_locs.is_operator_lines +
        lock_locs.is_operator_levels_tab
    )
    max_possible_locations = (
        miles_adj["Milestones"] * miles_adj["Maximum checks per milestone"] +
        jobs_adj["Job lines"] * jobs_adj["Maximum checks per job line"] +
        operator_lvl_adj["Operator level checks"]
    )
    if required_locations > max_possible_locations:
        raise OptionError(f"{world.player_name}: Not enough possible locations ({max_possible_locations}) "
                          f"for required items ({required_locations}).")
    required_locations -= operator_lvl_adj["Operator level checks"]
    world.milestone_checks_counts[:] = (miles_adj["Minimum checks per milestone"],) * miles_adj["Milestones"]
    world.task_counts[:] = (jobs_adj["Minimum checks per job line"],) * jobs_adj["Job lines"]
    required_locations -= sum(world.milestone_checks_counts) + sum(world.task_counts)
    while required_locations > 0:
        for i in range(min(required_locations, miles_adj["Milestones"])):
            world.milestone_checks_counts[i] += 1
        required_locations -= miles_adj["Milestones"]
        for i in range(min(required_locations, jobs_adj["Job lines"])):
            world.task_counts[i] += 1
        required_locations -= jobs_adj["Job lines"]
    for i in range(miles_adj["Milestones"]):
        if world.milestone_checks_counts[i] < miles_adj["Maximum checks per milestone"]:
            world.milestone_checks_counts[i] = world.random.randint(world.milestone_checks_counts[i],
                                                                    miles_adj["Maximum checks per milestone"])
    for i in range(jobs_adj["Job lines"]):
        if world.task_counts[i] < jobs_adj["Maximum checks per job line"]:
            world.task_counts[i] = world.random.randint(world.task_counts[i], jobs_adj["Maximum checks per job line"])


def create_events(world: "Shapez2World",
                  regions: dict[str, Region],
                  processor_rules_dict: dict[tuple[str, ...], "AccessRule"]) -> None:
    from .generate.events import milestones, operator_lines, processors, task_lines
    from .items import Shapez2Item

    processors.get_events(world, regions)  # ALWAYS run this first!!!
    milestones.get_events(world, regions, processor_rules_dict)
    task_lines.get_events(world, regions)
    operator_lines.get_events(world, regions, processor_rules_dict)

    if world.options.goal == "milestones":
        world.multiworld.completion_condition[world.player] = lambda state: (
            state.has(f"[ACCESS] Milestone {world.options.milestone_adjustments['Milestones']}", world.player)
        )
    else:
        item = Shapez2Item("Goal", ItemClassification.progression, None, world.player)
        region = regions["Events"]
        location = Shapez2Location(
            world.player, "[EVENT] Last operator level", None, region, LocationProgressType.DEFAULT,
            lambda state: state.can_reach_location(
                f"Operator level {world.options.operator_levels_adjustments['Operator level checks']}", world.player
            )
        )
        region.locations.append(location)
        location.place_locked_item(item)
        world.multiworld.completion_condition[world.player] = lambda state: state.has("Goal", world.player)


def create_and_place_locations(world: "Shapez2World",
                               regions: dict[str, Region],
                               processor_rules_dict: dict[tuple[str, ...], "AccessRule"]) -> None:
    from .generate.locations import milestones, tasks, operator_levels

    milestones.create_locations(world, regions)
    tasks.create_locations(world, regions, processor_rules_dict)
    operator_levels.create_locations(world, regions)
