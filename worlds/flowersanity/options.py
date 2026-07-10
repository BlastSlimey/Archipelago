from dataclasses import dataclass

from Options import Choice, PerGameCommonOptions, StartInventoryPool, Range, OptionSet
from .data import colornames_trunc


class Goal(Choice):
    """
    Select your goal.

    - **Colors count** - Get a certain number of flower colors.
    - **Specific colors** - Get all flower colors from a certain list.
    """
    display_name = "Goal"
    option_colors_count = 0
    option_specific_colors = 1
    default = 0


class GoalColors(OptionSet):
    """
    The list of colors you need to get for the **Specific colors** goal.
    """
    display_name = "Goal Colors"
    valid_keys = colornames_trunc.colors.keys()


class GoalAmount(Range):
    """
    The amount of colors you need to get for the **Colors count** goal.
    """
    display_name = "Goal Amount"
    range_start = 10
    range_end = 7800
    default = 100


class PoolSize(Range):
    """
    The amount of colors, i.e. locations and items without the calculations and free checks, in your world.
    """
    display_name = "Pool Size"
    range_start = 10
    range_end = 7800
    default = 100


@dataclass
class FlowersanityOptions(PerGameCommonOptions):
    goal: Goal
    goal_colors: GoalColors
    goal_amount: GoalAmount
    pool_size: PoolSize
    start_inventory_from_pool: StartInventoryPool
