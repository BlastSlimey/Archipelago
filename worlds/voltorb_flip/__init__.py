import logging
from typing import ClassVar, Mapping, Any

import settings
from BaseClasses import Item, ItemClassification, Region, MultiWorld
from worlds.AutoWorld import World
from . import client, options, locations


client.register_client()


class VoltorbFlipSettings(settings.Group):

    class AllowExperimentalLogic(settings.Bool):
        """Allows the **experimental** choice in the **Artificial Logic** option."""

    allow_experimental_logic: AllowExperimentalLogic | bool = False


class VoltorbFlipWorld(World):
    game = "Voltorb Flip"
    options_dataclass = options.VoltorbFlipOptions
    options: options.VoltorbFlipOptions
    settings_key = "voltorb_flip_settings"
    settings: ClassVar[VoltorbFlipSettings]
    topology_present = True
    item_name_to_id = {"Luck": 50000}
    location_name_to_id = locations.locations
    progression_list: ClassVar[list[tuple[str, int]]] = []  # Only used in set_rules, so reusable for other slots

    def __init__(self, multiworld: MultiWorld, player: int):
        super().__init__(multiworld, player)
        self.regions: dict[str, Region] = {}
        self.max_level = 0
        self.last_coin = 0

    def create_item(self, name: str) -> "Item":
        return VoltorbFlipItem(name, ItemClassification.progression_deprioritized_skip_balancing,
                               self.item_name_to_id[name], self.player)

    def get_filler_item_name(self) -> str:
        return "Luck"

    def create_regions(self) -> None:
        self.regions = {
            "Menu": Region("Menu", self.player, self.multiworld),
            "Earlier levels": Region("Earlier levels", self.player, self.multiworld),  # Always sphere 1
            "Later levels": Region("Later levels", self.player, self.multiworld),
            "Last level": Region("Last level", self.player, self.multiworld),
            "Early coins": Region("Early coins", self.player, self.multiworld),  # Always sphere 1
            "Mid coins": Region("Mid coins", self.player, self.multiworld),
            "Late coins": Region("Late coins", self.player, self.multiworld),
            "Last coins": Region("Last coins", self.player, self.multiworld),
        }
        max_level = self.options.level_locations_adjustments["Maximum"]
        self.max_level = max_level
        for i in range(1, max_level+1):
            if i == 1 or i/max_level <= 0.4:
                self.regions["Earlier levels"].locations.append(locations.VoltorbFlipLocation(
                    self.player, f"Win level {i}", i, self.regions["Earlier levels"]
                ))
            elif i == max_level:
                self.regions["Last level"].locations.append(locations.VoltorbFlipLocation(
                    self.player, f"Win level {i}", i, self.regions["Last level"]
                ))
            else:
                self.regions["Later levels"].locations.append(locations.VoltorbFlipLocation(
                    self.player, f"Win level {i}", i, self.regions["Later levels"]
                ))
        max_coins = self.options.coin_locations_adjustments["Maximum"]
        coin_steps = self.options.coin_locations_adjustments["Steps"]
        last_coin = max_coins - (max_coins % coin_steps)
        self.last_coin = last_coin
        for i in range(coin_steps, last_coin+1, coin_steps):
            if i == coin_steps:
                self.regions["Early coins"].locations.append(locations.VoltorbFlipLocation(
                    self.player, f"Collect {i} coins", i, self.regions["Early coins"]
                ))
            elif i == last_coin:
                self.regions["Last coins"].locations.append(locations.VoltorbFlipLocation(
                    self.player, f"Collect {i} coins", i, self.regions["Last coins"]
                ))
            elif i <= 1000:
                self.regions["Early coins"].locations.append(locations.VoltorbFlipLocation(
                    self.player, f"Collect {i} coins", i, self.regions["Early coins"]
                ))
            elif i <= last_coin//2:
                self.regions["Mid coins"].locations.append(locations.VoltorbFlipLocation(
                    self.player, f"Collect {i} coins", i, self.regions["Mid coins"]
                ))
            else:
                self.regions["Late coins"].locations.append(locations.VoltorbFlipLocation(
                    self.player, f"Collect {i} coins", i, self.regions["Late coins"]
                ))
        self.multiworld.regions.extend(self.regions.values())

    def create_items(self) -> None:
        for _ in range(sum(len(reg.locations) for reg in self.regions.values())):
            self.multiworld.itempool.append(self.create_item("Luck"))

    def set_rules(self) -> None:
        self.regions["Menu"].connect(self.regions["Earlier levels"], "Earlier levels")
        self.regions["Menu"].connect(self.regions["Early coins"], "Early coins")
        if self.options.artificial_logic == "experimental" and not settings.get_settings()["voltorb_flip_settings"]["allow_experimental_logic"]:
            import logging
            logging.warning("Experimental logic was disabled in host settings, so it will be reverted to non-experimental for player "+self.player_name+".")
            self.options.artificial_logic.value = 1
        if self.options.artificial_logic == "experimental":
            self.options.progression_balancing.value = 0  # Reduces rate of generation failures
            if not VoltorbFlipWorld.progression_list:
                VoltorbFlipWorld.progression_list.extend([
                    (item.name, item.player)
                    for item in self.multiworld.itempool
                    if ItemClassification.progression in item.classification
                ])
            items = [self.random.choice(VoltorbFlipWorld.progression_list) for _ in range(5)]
            print(items)
            self.regions["Earlier levels"].connect(self.regions["Later levels"], "Later levels", lambda state: state.has(items[0][0], items[0][1]))
            self.regions["Later levels"].connect(self.regions["Last level"], "Last level", lambda state: state.has(items[1][0], items[1][1]))
            self.regions["Early coins"].connect(self.regions["Mid coins"], "Mid coins", lambda state: state.has(items[2][0], items[2][1]))
            self.regions["Mid coins"].connect(self.regions["Late coins"], "Late coins", lambda state: state.has(items[3][0], items[3][1]))
            self.regions["Late coins"].connect(self.regions["Last coins"], "Last coins", lambda state: state.has(items[4][0], items[4][1]))
        elif self.options.artificial_logic == "on":
            count = sum(len(reg.locations) for reg in self.regions.values())
            self.regions["Earlier levels"].connect(self.regions["Later levels"], "Later levels", lambda state: state.has("Luck", self.player, 1))
            self.regions["Later levels"].connect(self.regions["Last level"], "Last level", lambda state: state.has("Luck", self.player, count//2))
            self.regions["Early coins"].connect(self.regions["Mid coins"], "Mid coins", lambda state: state.has("Luck", self.player, 1))
            self.regions["Mid coins"].connect(self.regions["Late coins"], "Late coins", lambda state: state.has("Luck", self.player, max(1, count//5)))
            self.regions["Late coins"].connect(self.regions["Last coins"], "Last coins", lambda state: state.has("Luck", self.player, count//2))
        else:
            self.regions["Earlier levels"].connect(self.regions["Later levels"], "Later levels")
            self.regions["Later levels"].connect(self.regions["Last level"], "Last level")
            self.regions["Early coins"].connect(self.regions["Mid coins"], "Mid coins")
            self.regions["Mid coins"].connect(self.regions["Late coins"], "Late coins")
            self.regions["Late coins"].connect(self.regions["Last coins"], "Last coins")
        if self.options.goal == "levels":
            self.multiworld.completion_condition[self.player] = lambda state: state.can_reach_location(f"Win level {self.max_level}", self.player)
        else:
            self.multiworld.completion_condition[self.player] = lambda state: state.can_reach_location(f"Collect {self.last_coin} coins", self.player)
        self.regions.clear()

    def fill_slot_data(self) -> Mapping[str, Any]:
        return {
            "goal": self.options.goal.current_key,
            "level_locations_adjustments": self.options.level_locations_adjustments.value,
            "coin_locations_adjustments": self.options.coin_locations_adjustments.value,
        }


class VoltorbFlipItem(Item):
    game = "Voltorb Flip"
