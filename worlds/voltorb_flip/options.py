import dataclasses

from BaseClasses import PlandoOptions
from Options import PerGameCommonOptions, Choice, Range, OptionCounter, OptionError
from worlds.AutoWorld import World


class Goal(Choice):
    """
    Select your goal.

    - **Levels** - Win all levels you have checks for.
    - **Coins** - Collect enough coins in one session to check all coin locations.
    """
    display_name = "Goal"
    option_levels = 0
    option_coins = 1
    default = 0


class LevelLocationsAdjustments(OptionCounter):
    """
    Adjust various things about the **Win level x** locations.

    - **Maximum** - The maximum level that has a location. Allowed values are in range 1 to 8.
    """
    display_name = "Level Locations Adjustments"
    valid_keys = [
        "Maximum",
    ]
    default = {
        "Maximum": 7,
    }

    def verify(self, world: type[World], player_name: str, plando_options: PlandoOptions) -> None:
        super().verify(world, player_name, plando_options)

        errors = []

        if not 1 <= self.value["Maximum"] <= 8:
            errors.append(f"Maximum: {self.value['Maximum']} not in range 10 to 50000")

        if len(errors) != 0:
            errors = [f"For option {getattr(self, 'display_name', self)} of player {player_name}:"] + errors
            raise OptionError("\n".join(errors))


class CoinLocationsAdjustments(OptionCounter):
    """
    Adjust various things about the **Collect x coins** locations.

    - **Maximum** - The maximum amount of coins that locations have. Allowed values are in range 10 to 50000.
    - **Steps** - The amount of coins needed for each next location. Allowed values are in range 10 to 50000. Cannot be higher than **Maximum**.
    """
    display_name = "Coin Locations Adjustments"
    valid_keys = [
        "Maximum",
        "Steps",
    ]
    default = {
        "Maximum": 10000,
        "Steps": 1000,
    }

    def verify(self, world: type[World], player_name: str, plando_options: PlandoOptions) -> None:
        super().verify(world, player_name, plando_options)

        errors = []

        if not 10 <= self.value["Maximum"] <= 50000:
            errors.append(f"Maximum: {self.value['Maximum']} not in range 10 to 50000")
        if not 10 <= self.value["Steps"] <= 50000:
            errors.append(f"Steps: {self.value['Steps']} not in range 10 to 50000")
        if self.value["Steps"] > self.value["Maximum"]:
            errors.append(f"Steps: {self.value['Steps']} is higher than Maximum: {self.value['Maximum']}")

        if len(errors) != 0:
            errors = [f"For option {getattr(self, 'display_name', self)} of player {player_name}:"] + errors
            raise OptionError("\n".join(errors))


@dataclasses.dataclass
class VoltorbFlipOptions(PerGameCommonOptions):
    goal: Goal
    level_locations_adjustments: LevelLocationsAdjustments
    coin_locations_adjustments: CoinLocationsAdjustments
