from dataclasses import dataclass
from typing import Iterable

from Options import PerGameCommonOptions, Range, Toggle, OptionSet, OptionError, ItemDict
from .data.pokemon import by_name


class CasefoldOptionSet(OptionSet):
    valid_keys_casefold = True

    def __init__(self, value: Iterable[str]):
        super().__init__(value)
        self.value: set[str] = set(val.casefold() for val in value)

    def __contains__(self, item: str):
        return item.casefold() in self.value

    def verify_keys(self) -> None:
        if self.valid_keys:
            dataset = set(word.casefold() for word in self.value)
            extra = dataset - set(key.casefold() for key in self._valid_keys)
            if extra:
                raise OptionError(
                    f"Found unexpected key {', '.join(extra)} in {getattr(self, 'display_name', self)}. "
                    f"Allowed keys: {self._valid_keys}."
                )


class QuestCount(Range):
    """
    Sets the number of quests that are shuffled as items into the item pool.

    Allowed values are actually in range 1 to 1000.
    However, special values like "random" will only roll values up to 200 and software like the Option Creator
        will only allow you to choose values up to 200.
    If you want any value above 200, you will have to edit your yaml in a text editor.
    """
    display_name = "Quest Count"
    range_start = 1
    range_end = 200
    actual_range_end = 1000
    default = 20

    def __init__(self, value: int):
        try:
            super().__init__(value)
        except Exception as e:
            if value > self.actual_range_end:
                raise Exception(f"{value} is higher than maximum {self.actual_range_end} "
                                f"for option {self.__class__.__name__}")
            elif self.range_end < value <= 1000:
                self.value = value
            else:
                raise e


class GoalAmount(Range):
    """
    Sets the number quests needed to goal (including the "Inspect a pokemon" check).
    It cannot be higher than **Quest Count**.
    It also actually accepts values up to 1000.
    """
    display_name = "Goal Amount"
    range_start = 1
    range_end = 200
    actual_range_end = 1000
    default = 20

    def __init__(self, value: int):
        try:
            super().__init__(value)
        except Exception as e:
            if value > self.actual_range_end:
                raise Exception(f"{value} is higher than maximum {self.actual_range_end} "
                                f"for option {self.__class__.__name__}")
            elif self.range_end < value <= 1000:
                self.value = value
            else:
                raise e


class ModifyQuestPool(CasefoldOptionSet):
    """
    Modifies what type of quests are allowed as items to be shuffled into the multiworld's item pool.

    The following is an example for how this option can look like:
    ```
    modify_quest_pool:
        ["Captures (off-mission)", "Poké Assists"]
    ```
    Here is an alternative way to format it:
    ```
    modify_quest_pool:
        - Captures (off-mission)
        - Poké Assists
    ```

    You can add as many of the following modifiers as you want.
    However, at least one modifier is always required.
    - **Captures (off-mission)** - Quests for capturing a specific (non-legendary) pokemon species,
        that can be caught at any time on a completed save file.
    - **Captures (missions-only)** - Quests for capturing a specific pokemon species, that can only be caught
        during story missions. Requires starting a new save file or continuing an incomplete save file.
    - **Legendary captures (off-mission)** - Quests for capturing a specific legendary(!) pokemon species,
        that can be caught at any time on a completed save file.
    - **Captures (special missions)** - Quests for capturing either Deoxys, Celebi, or Mew
        (which can only be caught during special missions outside of your save file).
    - **Poké Assists** - Quests for using a specific type of Poke Assist while capturing another pokemon.
    """
    display_name = "Modify Quest Pool"
    valid_keys = [
        "Captures (off-mission)",
        "Captures (missions-only)",
        "Legendary captures (off-mission)",
        "Captures (special missions)",
        "Poké Assists",
        # "Field moves (any level)",
        # "Field moves (specific level)",
    ]
    default = ["Captures (off-mission)", "Poké Assists"]


class DuplicateQuests(Toggle):
    """
    Allows quests to appear more than once in the item pool. Otherwise, every item will be unique.

    However, if you set **Quest Count** higher than the actual available amount of quests,
        duplicate quests will inevitably be added regardless of this option.
    """
    display_name = "Duplicate Quests"
    default = False


class CapturesBlacklist(OptionSet):  # Not casefold because entries have to be looked up in data table (case-sensitive)
    """
    Prevents these pokemon from having a capture quests shuffled into the item pool.
    """
    display_name = "Captures Blacklist"
    valid_keys = list(by_name)


class QuestPlando(ItemDict):
    """
    Ensures that these quests will be put into the item pool at least as many times as specified.
    Ignores **Modify Quest Pool** and **Captures Blacklist**.

    The following is an example for how this option can look like:
    ```
    quest_plando:
        {"Capture a Zigzagoon": 1, "Use a Fire type Poké Assist": 5}
    ```
    Here is an alternative way to format it:
    ```
    quest_plando:
        Capture a Zigzagoon: 1
        Use a Fire type Poké Assist: 5
    ```

    However, if you add more quests to this option than what you set in **Quest Count**,
        only a random slice of this option is put into the item pool.
    """
    display_name = "Quest Plando"
    verify_item_name = True


class ForceOneCheckAtATime(Toggle):
    """
    Forces every action in-game to check only one quest at a time.
    Otherwise, having duplicate quests active at the same time will check all of them at the same time when completed.
    """
    display_name = "Force One Check at a Time"
    default = False


@dataclass
class RangerQuestOptions(PerGameCommonOptions):
    quest_count: QuestCount
    goal_amount: GoalAmount
    modify_quest_pool: ModifyQuestPool
    duplicate_quests: DuplicateQuests
    captures_blacklist: CapturesBlacklist
    quest_plando: QuestPlando
    force_one_check_at_a_time: ForceOneCheckAtATime
