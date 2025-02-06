from dataclasses import dataclass

from Options import PerGameCommonOptions, Choice


class Difficulty(Choice):
    """Choose your difficulty."""
    display_name = "Difficulty"
    option_vanilla = 0
    option_extra_buff = 1
    option_challenge = 2
    default = 0


@dataclass
class ADGACOptions(PerGameCommonOptions):
    difficulty: Difficulty
