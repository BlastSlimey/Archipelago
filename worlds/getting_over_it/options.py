from dataclasses import dataclass

from Options import PerGameCommonOptions, Range, Choice


class RequiredCompletions(Range):
    """Specifies how many times the player is required to reach the top to complete this world."""
    display_name = "Required completions"
    range_start = 1
    range_end = 10
    default = 1


class Difficulty(Choice):
    """Choose your difficulty. The hard difficulty corresponds to what an experienced player with 50+ hours of playtime,
    100+ completions, and an all-time best of less than 6 minutes is able to do."""
    display_name = "Difficulty"
    option_hard = 0
    option_medium = 1
    option_easy = 2
    default = 2


@dataclass
class GOIOptions(PerGameCommonOptions):
    required_completions: RequiredCompletions
    difficulty: Difficulty
