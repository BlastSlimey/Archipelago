from copy import deepcopy
from typing import Mapping, Any, TYPE_CHECKING

from BaseClasses import MultiWorld, Tutorial, Region, ItemClassification
from Options import OptionError
from worlds.AutoWorld import WebWorld, World
from . import items, locations, options, client
from .data import descriptions

if TYPE_CHECKING:
    pass

client.register_client()


class RangerQuestWeb(WebWorld):
    rich_text_options_doc = True
    theme = "grass"
    game_info_languages = ['en']
    setup_en = Tutorial(
        "Multiworld Setup Guide",
        "A guide to playing Pokémon Ranger (Quest) with Archipelago:",
        "English",
        "setup_en.md",
        "setup/en",
        ["BlastSlimey"]
    )
    tutorials = [setup_en]
    item_descriptions = descriptions.items


class RangerQuestWorld(World):
    """

    """
    game = "Pokemon Ranger (Quest)"
    options_dataclass = options.RangerQuestOptions
    options: options.RangerQuestOptions
    topology_present = True
    web = RangerQuestWeb()
    item_name_to_id = items.lookup_table()
    location_name_to_id = locations.lookup_table()

    def __init__(self, multiworld: MultiWorld, player: int):
        super().__init__(multiworld, player)

        from .data.version import ap_minimum
        from Utils import version_tuple
        if version_tuple < ap_minimum():
            raise Exception(f"Archipelago version too old for Pokemon Ranger (Quest) "
                            f"(requires minimum {ap_minimum()}, found {version_tuple}")

        self.nested_quest_pool: list[list[str]] = []  # Might get modified depending on options
        self.nested_quest_pool_copy: list[list[str]] = []  # Doesn't get modified

    def generate_early(self) -> None:

        self.nested_quest_pool = items.get_quest_pool(self)
        self.nested_quest_pool_copy = deepcopy(self.nested_quest_pool)

        if not self.options.modify_quest_pool.value:
            raise OptionError(f"Player {self.player_name}: You need to add at least one type of quests to "
                              f"\"Modify Quest Pool\".")
        if self.options.goal_amount > self.options.quest_count:
            raise OptionError(f"Player {self.player_name}: Goal amount is higher than quest count "
                              f"({self.options.goal_amount} > {self.options.quest_count}).")
        if not self.nested_quest_pool:
            raise OptionError(f"Player {self.player_name}: Empty quest pool, most likely due to a too restrictive "
                              f"capture blacklist.")

    def create_item(self, name: str) -> items.RangerQuestItem:
        return items.RangerQuestItem(name, ItemClassification.progression_skip_balancing,
                                     self.item_name_to_id[name], self.player)

    def get_filler_item_name(self) -> str:
        while True:
            if not self.nested_quest_pool:
                if not self.nested_quest_pool_copy:
                    self.nested_quest_pool = [["Capture a Zigzagoon"] * 100]
                else:
                    self.nested_quest_pool = deepcopy(self.nested_quest_pool_copy)
            subpool = self.random.choice(self.nested_quest_pool)
            if not subpool:
                self.nested_quest_pool.remove(subpool)
                continue
            ret = self.random.choice(subpool)
            if not self.options.duplicate_quests:
                subpool.remove(ret)
            return ret

    def create_regions(self) -> None:

        def get_rule(count: int):
            return lambda state: state.count_from_list(self.item_name_to_id, self.player) >= count

        region = Region("Menu", self.player, self.multiworld)
        for i in range(1, self.options.quest_count.value):  # not +1 because of inspect a pokémon location
            name = f"Complete quest #{i}"
            loc = locations.RangerQuestLocation(self.player, name, self.location_name_to_id[name], region)
            loc.access_rule = get_rule(i)
            region.locations.append(loc)
        touch_loc = "Inspect a pokémon"
        region.locations.append(locations.RangerQuestLocation(self.player, touch_loc,
                                                              self.location_name_to_id[touch_loc], region))
        self.multiworld.regions.append(region)
        self.multiworld.completion_condition[self.player] = get_rule(self.options.goal_amount.value)

    def create_items(self) -> None:
        plando = [self.create_item(name)
                  for name, count in self.options.quest_plando.value.items() for _ in range(count)]
        item_pool = plando[:self.options.quest_count.value]
        self.random.shuffle(item_pool)  # In case the player plando'd more quests than the provided quest count
        item_pool += [self.create_item(self.get_filler_item_name())
                      for _ in range(len(item_pool), self.options.quest_count.value)]
        self.multiworld.itempool += item_pool

    def fill_slot_data(self) -> Mapping[str, Any]:
        return {
            "goal_amount": self.options.goal_amount.value,
            "force_one_check_at_a_time": self.options.force_one_check_at_a_time.value,
        }
