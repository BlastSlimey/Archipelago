import typing
from dataclasses import dataclass

from BaseClasses import PlandoOptions
from Options import Choice, PerGameCommonOptions, OptionError, StartInventoryPool, Visibility, Range

from .data.common_options import ToggleSet, ExtendedOptionCounter

if typing.TYPE_CHECKING:
    from worlds.AutoWorld import World
    from . import Shapez2World


class Deprecated:
    visibility = Visibility.none


class Goal(Choice):
    """
    Select your goal.

    - **Milestones** - Complete all milestones.
    - **Operator levels** - Reach the operator level that
        contains your last operator level check. Requires
        an operator level checks number higher than 0.
    """
    display_name = "Goal"
    option_milestones = 0
    option_operator_levels = 1
    default = 0


class LockLocations(ToggleSet):
    """
    Locks certain lines of locations behind keys.
    You can add as many of the following modifiers as you want.

    - **Job lines** - Makes job lines require an item to be
        unlocked. Job lines #1-3 are always unlocked.
    - **Operator lines** - Makes operator lines require an item
        to be unlocked.
    - **Operator levels tab** - Makes the operator levels tab
        require an item to be unlocked.
    """
    display_name = "Lock Locations"
    is_job_lines = False
    is_operator_lines = True
    is_operator_levels_tab = False


class LocationModifiers(Deprecated, ToggleSet):
    """
    Deprecated, use **Lock Locations** instead.
    """
    display_name = "Location Modifiers"
    is_lock_task_lines = False
    is_lock_operator_lines = False
    is_lock_operator_levels_tab = False
    is_deprecated = True


class MilestoneAdjustments(ExtendedOptionCounter):
    """
    Adjust various parameters of milestones.
    Any minimum parameter cannot be higher than its corresponding maximum
    parameter. Weighting for each parameter individually, "random", and
    "random-range-x-y" are supported.

    Do note that you have to add enough (minimum) locations in total to fit all
    non-filler items (filler items are research/blueprint credits and platform
    capacity). Excluding job/operator line keys, there are ~60 items.

    Allowed values (in range) are...
    - **Milestones** - 3-20
    - **Minimum checks per milestone** - 2-12
    - **Maximum checks per milestone** - 5-12
    """
    display_name = "Milestone Adjustments"
    valid_keys = [
        "Milestones",
        "Minimum checks per milestone",
        "Maximum checks per milestone",
    ]
    default = {
        "Milestones": 8,
        "Minimum checks per milestone": 8,
        "Maximum checks per milestone": 12,
    }
    individual_min_max = {
        "Milestones": (3, 20),
        "Minimum checks per milestone": (2, 12),
        "Maximum checks per milestone": (5, 12),
    }
    min_max_pairs = [
        ("Minimum checks per milestone", "Maximum checks per milestone"),
    ]


class JobsAdjustments(ExtendedOptionCounter):
    """
    Adjust various parameters of job lines.
    Any minimum parameter cannot be higher than its corresponding maximum
    parameter. Weighting for each parameter individually, "random", and
    "random-range-x-y" are supported.

    Do note that you have to add enough (minimum) locations in total to fit all
    non-filler items (filler items are research/blueprint credits and platform
    capacity). Excluding job/operator line keys, there are ~60 items.

    Allowed values (in range) are...
    - **Job lines** - 3-200
    - **Minimum checks per job line** - 1-5
    - **Maximum checks per job line** - 1-5
    """
    display_name = "Jobs Adjustments"
    valid_keys = [
        "Job lines",
        "Minimum checks per job line",
        "Maximum checks per job line",
    ]
    default = {
        "Job lines": 20,
        "Minimum checks per job line": 3,
        "Maximum checks per job line": 5,
    }
    individual_min_max = {
        "Job lines": (3, 200),
        "Minimum checks per job line": (1, 5),
        "Maximum checks per job line": (1, 5),
    }
    min_max_pairs = [
        ("Minimum checks per job line", "Maximum checks per job line"),
    ]


class OperatorLevelsAdjustments(ExtendedOptionCounter):
    """
    Adjust various parameters of operator levels.
    Any minimum parameter cannot be higher than its corresponding maximum
    parameter. Weighting for each parameter individually, "random", and
    "random-range-x-y" are supported.

    - **Operator lines** (1-100) - The amount of operator lines that can
        contribute to your operator level.
    - **Random operator lines** (0-3) - The amount of operator lines (out of the
        value in **Operator lines**) that contain a random shape each level.
    - **Operator level checks** (0-200) - The amount of operator levels that
        can contain checks. Every level after this will grant extra
        research/blueprint credits and platform capacity.

    Do note that you have to add enough (minimum) locations in total to fit all
    non-filler items (filler items are research/blueprint credits and platform
    capacity). Excluding job/operator line keys, there are ~60 items.
    """
    display_name = "Operator Level Adjustments"
    valid_keys = [
        "Operator lines",
        "Random operator lines",
        "Operator level checks",
    ]
    default = {
        "Operator lines": 8,
        "Random operator lines": 2,
        "Operator level checks": 0,
    }
    individual_min_max = {
        "Operator lines": (1, 100),
        "Random operator lines": (0, 3),
        "Operator level checks": (0, 200),
    }
    min_max_pairs = [
        ("Random operator lines", "Operator lines"),
    ]


class StartingPoints(ExtendedOptionCounter):
    """
    Adjust the amount of research/blueprint credits and platform
    capacity given at the start of the game.
    Any minimum parameter cannot be higher than its corresponding
    maximum parameter. Weighting for each parameter individually,
    "random", and "random-range-x-y" are supported.

    Allowed values (in range) are...
    - **Platform capacity** - 250-2000
    - **Research credits** - 0-5000
    - **Blueprint credits** - 0-10000

    Note that research credits only exist as 100 credits bundles.
    """
    display_name = "Starting Points"
    valid_keys = [
        "Platform capacity",
        "Research credits",
        "Blueprint credits",
    ]
    default = {
        "Platform capacity": 250,
        "Research credits": 0,
        "Blueprint credits": 0,
    }
    individual_min_max = {
        "Platform capacity": (250, 2000),
        "Research credits": (0, 5000),
        "Blueprint credits": (0, 10000),
    }


class RequiredShapesMultiplier(Range):
    """
    Multiplies the amount of required shapes for milestones,
    jobs, and operator levels. The value is in percent, i.e.
    100 is the default amount of shapes. The default amounts
    are based on the (vanilla) regular scenario.
    """
    display_name = "Required Shapes Multiplier"
    rich_text_doc = True
    range_start = 1
    range_end = 1000
    default = 100


class LocationAdjustments(Deprecated, ExtendedOptionCounter):
    """
    Deprecated, use individual location adjustment options instead.
    """
    display_name = "Location Adjustments"
    valid_keys = [
        "Milestones",
        "Minimum checks per milestone",
        "Maximum checks per milestone",
        "Starting platform points",
        "Starting research points",
        "Starting blueprint points",
        "Task lines",
        "Minimum checks per task line",
        "Maximum checks per task line",
        "Operator lines",
        "Random operator lines",
        "Operator level checks",
        "Required shapes multiplier",
        "Deprecated",
    ]
    default = "deprecated"
    individual_min_max = {
        "Milestones": (3, 20),
        "Minimum checks per milestone": (2, 12),
        "Maximum checks per milestone": (5, 12),
        "Starting platform points": (250, 2000),
        "Starting research points": (0, 50),
        "Starting blueprint points": (0, 10000),
        "Task lines": (3, 200),
        "Minimum checks per task line": (1, 5),
        "Maximum checks per task line": (1, 5),
        "Operator lines": (1, 100),
        "Random operator lines": (0, 3),
        "Operator level checks": (0, 200),
        "Required shapes multiplier": (1, 1000),
        "Deprecated": (0, 0),
    }
    min_max_pairs = [
        ("Minimum checks per milestone", "Maximum checks per milestone"),
        ("Minimum checks per task line", "Maximum checks per task line"),
        ("Random operator lines", "Operator lines"),
    ]


class ShapeConfiguration(Choice):
    """
    Choose how many corners all shapes have.

    - **Tetragonal** - 4 corners (standard).
    - **Hexagonal** - 6 corners.
    """
    display_name = "Shape Configuration"
    option_tetragonal = 4
    option_hexagonal = 6
    default = 4


class OperatorLinesShapes(ToggleSet):
    """
    Modifies what shapes are generated for operator lines.
    You can add as many of the following modifiers as you want.

    - **Milestones** - Uses the final shape(s) of (some) milestones.
    - **Jobs** - Uses the final shape of (some) job lines.
    """
    display_name = "Operator Lines Shapes"
    is_milestones = True
    is_jobs = True


class ShapeGenerationModifiers(Deprecated, ToggleSet):
    """
    Deprecated, use **Operator Lines Shapes** instead.
    """
    display_name = "Shape Generation Modifiers"
    is_milestone_operator_lines = False
    is_deprecated = True


class ShapeGenerationAdjustments(ExtendedOptionCounter):
    """
    Adjust various parameters about how shape requirements for
    milestones, jobs, and operator lines are generated.
    Weighting for each parameter individually, "random", and
    "random-range-x-y" are supported.

    - **Maximum layers** (2-10) - The maximum number of layers any
        shape can have.
    - **Maximum processors per milestone** (3-8) - The maximum number
        of certain buildings that are required to produce the final
        shapes of milestones.
    """
    display_name = "Shape Generation Adjustments"
    valid_keys = [
        "Maximum layers",
        "Maximum processors per milestone",
    ]
    default = {
        "Maximum layers": 4,
        "Maximum processors per milestone": 4,
    }
    individual_min_max = {
        "Maximum layers": (2, 10),
        "Maximum processors per milestone": (3, 8),
    }


class BlueprintShapes(Choice):
    """
    Choose which set of shapes rewards the player with blueprint points.

    If tetragonal shapes are chosen, **Regular**, **Hard**, and **Insane**
    use the corresponding scenario's set.
    If hexagonal shapes are chosen, all of those three options use the
    hexagonal scenario's only set.
    **Randomized** generates a random set of 3 to 5 different blueprint
    shapes.

    You can also put in a list of custom blueprint shapes.
    See this game's option guides for more information.
    """
    display_name = "Blueprint Shapes"
    option_regular = 0
    option_hard = 1
    option_insane = 2
    option_randomized = 3
    default = 0

    def __init__(self, value: int, plando: list[str] | None = None):
        if "plando" not in self.options:
            self.options["plando"] = 99
        if "plando" not in self.name_lookup:
            self.name_lookup[99] = "plando"
        super().__init__(value)
        self.plando = plando

    def is_plando(self) -> bool:
        return self.plando is not None

    @classmethod
    def from_any(cls, data: typing.Any) -> typing.Self:
        if isinstance(data, list):
            return cls(99, data)
        return super().from_any(data)

    def verify(self, world: typing.Type["World"], player_name: str, plando_options: PlandoOptions) -> None:
        super().verify(world, player_name, plando_options)
        if self.is_plando():
            reasons: list[str] = []
            for val in self.plando:
                if not isinstance(val, str):
                    reasons.append(f"Shapes list must only contain strings, but found {type(val)}")
            if not (0 < len(self.plando) <= 5):
                reasons.append(f"Number of blueprint shapes must be in range 1-5, but found {len(self.plando)}")
            if reasons:
                raise OptionError(f"Player {player_name}: Bad plando formatting for blueprint_shapes option:\n" + ", ".join(reasons))

    def verify_plando(self, world: "Shapez2World"):
        if self.is_plando():
            from .generate.shapes.verify import is_valid_shape
            parts = 4 if world.options.shape_configuration == "tetragonal" else 6
            layers = world.options.shape_generation_adjustments["Maximum layers"]
            if any(not is_valid_shape(shape, parts, layers) for shape in self.plando):
                raise OptionError(f"Player {world.player_name}: Invalid plando shapes in option blueprint_shapes.\n"
                                  f"See this option's plando guide for more information.")

    def to_slot_data(self) -> str | list[str]:
        if self.is_plando():
            return self.plando
        else:
            return self.current_key


class ItemPoolModifiers(ToggleSet):
    """
    Modifies what items your world puts into the item pool.
    You can add as many of the following modifiers as you want.

    - **Random starting processor** - Adds a random processor building that
        doesn't require other buildings to the starting milestone.
    - **Include blueprint credits** - Allows blueprint credits to be added as
        filler items. If blueprint costs are disabled ingame, blueprint credits
        and rewards granting them will be invisible ingame.
    - **Arbitrary research credits** - Allows research credits items to give any
        amount in range of 100-10000 instead of snapping them to nice numbers.
    - **Arbitrary platform capacity** - Allows platform capacity items to give
        any amount in range of 1-500 instead of snapping them to nice numbers.
    - **Arbitrary blueprint credits** - Allows blueprint credits to give
        amounts in range of 1000-10000 snapped to 100-step numbers instead of
        only 1000-step numbers.
    - **Unlock boosters with miners** - Makes the asteroid miner and pumps also
        unlock their respective booster with them.
    - **Unlock pipes with pumps** - Makes mini/asteroid pumps also unlock their
        respective pipe with them.
    """
    # - **Add sandbox buildings** - Adds the sandbox item and fluid producers to the itempool.
    display_name = "Item Pool Modifiers"
    is_random_starting_processor = True
    is_include_blueprint_credits = False
    is_arbitrary_research_credits = False
    is_arbitrary_blueprint_credits = False
    is_arbitrary_platform_capacity = False
    is_unlock_booster_with_miners = True
    is_unlock_pipes_with_pumps = True
    aliases_convert = [
        ("Include blueprint points", "Include blueprint credits"),
        ("Arbitrary research points", "Arbitrary research credits"),
        ("Arbitrary blueprint points", "Arbitrary blueprint credits"),
        ("Arbitrary platform items", "Arbitrary platform capacity"),
        ("Unlock extensions with miners", "Unlock boosters with miners"),
    ]


class SurpriseOutOfLogicItems(ExtendedOptionCounter):
    """
    Adds mysterious items to the shop that can contain a copy of any building,
    space platform, or mechanic in your item pool, without being accounted for
    in logic.
    You can adjust various parameters of these shop items. Weighting for each
    parameter individually, "random", and "random-range-x-y" are supported.

    - **Amount** (0-6) - The amount of surprise out-of-logic items in the shop.
    - **Cost per item** (1000-50000) - The amount of research credits required
        to purchase each item. The actual cost ingame is always rounded down to
        the nearest 100-step.
    """
    display_name = "Surprise Out-Of-Logic Item"
    valid_keys = [
        "Amount",
        "Cost per item",
    ]
    default = {
        "Amount": 1,
        "Cost per item": 10000,
    }
    individual_min_max = {
        "Amount": (0, 6),
        "Cost per item": (1000, 50000),
    }


class ShowItemNames(ToggleSet):
    """
    Adds some information to items belonging to other players in your game.
    You can add as many of the following modifiers as you want.

    - **Item** - Shows the item's name, otherwise it will be called "AP Item".
    - **Player** - Appends the player's name to the item's name.
    - **Classification** - Appends the item's classification (progression,
        filler, ...) to its name.
    """
    display_name = "Show Item Names"
    is_item = True
    is_player = False
    is_classification = False


class ShowOtherPlayersItems(Deprecated, Choice):
    """
    Deprecated, use *+Show Item Names** instead.
    """
    display_name = "Show other players' items"
    option_no = 0
    option_item = 1
    option_player = 2
    option_classification = 3
    option_player_classification = 4
    option_deprecated = 99
    default = 99


def fix_deprecated(world: "Shapez2World"):
    options = world.options
    if options.show_other_players_items != "deprecated":
        opt = options.show_other_players_items.current_key
        if opt in ("item", "player", "classification"):
            options.show_item_names.set_afterwards(opt, True)
        elif opt == "player_classification":
            options.show_item_names.set_afterwards("player", True)
            options.show_item_names.set_afterwards("classification", True)
    if not options.location_modifiers.is_deprecated:
        options.lock_locations.set_afterwards("job lines", options.location_modifiers.is_lock_task_lines)
        options.lock_locations.set_afterwards("operator lines", options.location_modifiers.is_lock_operator_lines)
        options.lock_locations.set_afterwards("operator levels tab", options.location_modifiers.is_lock_operator_levels_tab)
    if not options.location_adjustments.reported_deprecated:
        options.milestone_adjustments["Milestones"] = options.location_adjustments["Milestones"]
        options.milestone_adjustments["Minimum checks per milestone"] = options.location_adjustments["Minimum checks per milestone"]
        options.milestone_adjustments["Maximum checks per milestone"] = options.location_adjustments["Maximum checks per milestone"]
        options.starting_points["Platform capacity"] = options.location_adjustments["Starting platform points"]
        options.starting_points["Research credits"] = options.location_adjustments["Starting research points"]
        options.starting_points["Blueprint credits"] = options.location_adjustments["Starting blueprint points"]
        options.jobs_adjustments["Job lines"] = options.location_adjustments["Task lines"]
        options.jobs_adjustments["Minimum checks per job line"] = options.location_adjustments["Minimum checks per task line"]
        options.jobs_adjustments["Maximum checks per job line"] = options.location_adjustments["Maximum checks per task line"]
        options.operator_levels_adjustments["Operator lines"] = options.location_adjustments["Operator lines"]
        options.operator_levels_adjustments["Random operator lines"] = options.location_adjustments["Random operator lines"]
        options.operator_levels_adjustments["Operator level checks"] = options.location_adjustments["Operator level checks"]
        options.required_shapes_multiplier.value = options.location_adjustments["Required shapes multiplier"]
    if not options.shape_generation_modifiers.is_deprecated:
        options.operator_lines_shapes.set_afterwards("milestones", options.shape_generation_modifiers.is_milestone_operator_lines)


@dataclass
class Shapez2Options(PerGameCommonOptions):
    goal: Goal
    lock_locations: LockLocations
    location_modifiers: LocationModifiers  # Deprecated
    milestone_adjustments: MilestoneAdjustments
    jobs_adjustments: JobsAdjustments
    operator_levels_adjustments: OperatorLevelsAdjustments
    starting_points: StartingPoints
    required_shapes_multiplier: RequiredShapesMultiplier
    location_adjustments: LocationAdjustments  # Deprecated
    shape_configuration: ShapeConfiguration
    operator_lines_shapes: OperatorLinesShapes
    shape_generation_modifiers: ShapeGenerationModifiers  # Deprecated
    shape_generation_adjustments: ShapeGenerationAdjustments
    blueprint_shapes: BlueprintShapes
    item_pool_modifiers: ItemPoolModifiers
    surprise_out_of_logic_item: SurpriseOutOfLogicItems
    show_item_names: ShowItemNames
    show_other_players_items: ShowOtherPlayersItems  # Deprecated
    start_inventory_from_pool: StartInventoryPool
