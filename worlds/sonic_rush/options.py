from dataclasses import dataclass

from Options import PerGameCommonOptions, Choice, Range, DeathLink


class Goal(Choice):
    """Choose the required goal to finish your game.
    **8 bosses once:** Defeat all 8 main bosses at least once.
    **8 bosses both:** Defeat all 8 main bosses with both Sonic and Blaze.
    **7 bosses extra:** Defeat all bosses including extra zone, except Unknown, with both Sonic and Blaze.
    **Emeralds:** Collect all Chaos and Sol emeralds.
    **Emeralds extra:** Collect all Chaos and Sol emeralds and beat extra zone."""
    display_name = "Goal"
    rich_text_doc = True
    option_8_bosses_once = 0
    option_8_bosses_both = 1
    option_7_bosses_extra = 2
    option_emeralds = 3
    option_emeralds_extra = 4
    option_100_percent = 5
    default = 1


class StartingActs(Range):
    """Define how many progressive acts you start with."""
    display_name = "Starting Acts"
    rich_text_doc = True
    range_start = 3
    range_end = 10
    default = 3


class SonicVsBlazeMultiplier(Range):
    """A multiplier for making the second phase of Sonic Vs. Blaze longer."""
    display_name = "Sonic Vs. Blaze Multiplier"
    rich_text_doc = True
    range_start = 1
    range_end = 100
    default = 2


class TrapsPercentage(Range):
    """Amount of traps replacing filler items (in percent)."""
    display_name = "Traps Percentage"
    rich_text_doc = True
    range_start = 0
    range_end = 100
    default = 0


@dataclass
class SonicRushOptions(PerGameCommonOptions):
    goal: Goal
    starting_acts: StartingActs
    sonic_vs_blaze_multiplier: SonicVsBlazeMultiplier
    traps_percentage: TrapsPercentage
    death_link: DeathLink
