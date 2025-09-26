from typing import ClassVar, Mapping, Any

import settings
from BaseClasses import Item, Location, ItemClassification, Region
from worlds.AutoWorld import World
from . import client, options, locations


client.register_client()


class VoltorbFlipWorld(World):
    game = "Voltorb Flip"
    options_dataclass = options.VoltorbFlipOptions
    options: options.VoltorbFlipOptions
    topology_present = True
    item_name_to_id = {"Luck": 50000}
    location_name_to_id = locations.locations

    def create_item(self, name: str) -> "Item":
        return VoltorbFlipItem(name, ItemClassification.progression_deprioritized_skip_balancing,
                               self.item_name_to_id[name], self.player)

    def get_filler_item_name(self) -> str:
        return "Luck"

    def create_regions(self) -> None:
        print("Regions")
        reg = Region("Menu", self.player, self.multiworld)
        print(f"Levels maximum {self.options.level_locations_adjustments['Maximum']}")
        reg.locations.extend([
            locations.VoltorbFlipLocation(self.player, f"Win level {i}", i, reg)
            for i in range(1, self.options.level_locations_adjustments["Maximum"] + 1)
        ])
        coin_steps = self.options.coin_locations_adjustments["Steps"]
        print(f"Coins maximum {self.options.coin_locations_adjustments['Maximum']}")
        print(f"Coin steps {coin_steps}")
        reg.locations.extend([
            locations.VoltorbFlipLocation(self.player, f"Collect {i} coins", i, reg)
            for i in range(coin_steps, self.options.coin_locations_adjustments["Maximum"] + 1, coin_steps)
        ])
        goal = locations.VoltorbFlipLocation(self.player, "Goal", None, reg)
        goal.place_locked_item(self.create_item("Luck"))
        reg.locations.append(goal)
        self.multiworld.completion_condition[self.player] = lambda state: state.can_reach_location("Goal", self.player)
        self.multiworld.regions.append(reg)

    def create_items(self) -> None:
        print("Items")
        levels = self.options.level_locations_adjustments["Maximum"]
        coins = self.options.coin_locations_adjustments["Maximum"] // self.options.coin_locations_adjustments["Steps"]
        for _ in range(levels + coins):
            self.multiworld.itempool.append(self.create_item("Luck"))

    def set_rules(self) -> None:
        print("Rules")
        items = []
        while len(items) < 6:
            item = self.random.choice(self.multiworld.itempool)
            if item.classification | ItemClassification.progression:
                items.append(item)

        levels = self.options.level_locations_adjustments["Maximum"]
        coins = self.options.coin_locations_adjustments["Maximum"]
        coin_steps = self.options.coin_locations_adjustments["Steps"]
        if levels > 5:
            self.get_location("Win level 5").access_rule = lambda state: state.has(items[0].name, items[0].player)
        if levels > 7:
            self.get_location("Win level 7").access_rule = lambda state: state.has(items[1].name, items[1].player)
        if levels > 1:
            self.get_location(f"Win level {levels}").access_rule = lambda state: state.has(items[2].name, items[2].player)
        if coins > 1000:
            if coin_steps <= 1000:
                self.get_location(f"Collect {1000 - (1000 % coin_steps)} coins").access_rule = lambda state: state.has(items[3].name, items[3].player)
            else:
                self.get_location(f"Collect {coin_steps} coins").access_rule = lambda state: state.has(items[3].name, items[3].player)
        if coin_steps <= coins//2:
            self.get_location(f"Collect {(coins//2) - ((coins//2) % coin_steps)} coins").access_rule = lambda state: state.has(items[4].name, items[4].player)
        self.get_location(f"Collect {coins - (coins % coin_steps)} coins").access_rule = lambda state: state.has(items[5].name, items[5].player)

        if self.options.goal == "levels":
            self.get_location("Goal").access_rule = lambda state: state.can_reach_location(f"Win level {levels}", self.player)
        else:
            self.get_location("Goal").access_rule = lambda state: state.can_reach_location(f"Collect {coins - (coins % coin_steps)} coins", self.player)

    def fill_slot_data(self) -> Mapping[str, Any]:
        return {
            "goal": self.options.goal.current_key,
            "level_locations_adjustments": self.options.level_locations_adjustments.value,
            "coin_locations_adjustments": self.options.coin_locations_adjustments.value,
        }


class VoltorbFlipItem(Item):
    game = "Voltorb Flip"
