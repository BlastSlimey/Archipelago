from typing import ClassVar

import settings
from BaseClasses import Item, Location, ItemClassification, Region
from worlds.AutoWorld import World
from . import client, options


client.register_client()


class VoltorbFlipSettings(settings.Group):

    class PokemonHGSSRomFile(settings.UserFilePath):
        """File name of your Pokémon Heartgold or Soulsilver ROM"""
        description = "Pokemon HGSS ROM"
        copy_to = "PokemonHGSS_VF.nds"

    rom: PokemonHGSSRomFile = PokemonHGSSRomFile(PokemonHGSSRomFile.copy_to)


class VoltorbFlipWorld(World):
    game = "Voltorb Flip"
    options_dataclass = options.VoltorbFlipOptions
    options: options.VoltorbFlipOptions
    topology_present = True
    item_name_to_id = {"Luck": 50000}
    location_name_to_id = {f"Level {i}": i for i in range(2, 8)}
    settings_key = "voltorb_flip_settings"
    settings = ClassVar[VoltorbFlipSettings]

    def create_item(self, name: str) -> "Item":
        return VoltorbFlipItem(name, ItemClassification.progression_deprioritized_skip_balancing,
                               self.item_name_to_id[name], self.player)

    def get_filler_item_name(self) -> str:
        return "Luck"

    def create_regions(self) -> None:
        reg = Region("Menu", self.player, self.multiworld)
        for i in range(2, 8):
            reg.locations.append(VoltorbFlipLocation(self.player, f"Level {i}", i, reg))
        goal = VoltorbFlipLocation(self.player, "Goal", None, reg)
        goal.place_locked_item(self.create_item("Luck"))
        reg.locations.append(goal)
        self.multiworld.completion_condition[self.player] = lambda state: state.can_reach_location("Goal", self.player)
        self.multiworld.regions.append(reg)

    def create_items(self) -> None:
        for i in range(2, 8):
            self.multiworld.itempool.append(self.create_item("Luck"))

    def set_rules(self) -> None:
        items = []
        while len(items) < 3:
            item = self.random.choice(self.multiworld.itempool)
            if item.classification | ItemClassification.progression:
                items.append(item)
        self.get_location("Level 5").access_rule = lambda state: state.has(items[0].name, items[0].player)
        self.get_location("Level 6").access_rule = lambda state: state.has(items[1].name, items[1].player)
        self.get_location("Level 7").access_rule = lambda state: state.has(items[2].name, items[2].player)
        self.get_location("Goal").access_rule = lambda state: (state.can_reach_location("Level 5", self.player) and
                                                               state.can_reach_location("Level 6", self.player) and
                                                               state.can_reach_location("Level 7", self.player))


class VoltorbFlipItem(Item):
    game = "Voltorb Flip"


class VoltorbFlipLocation(Location):
    game = "Voltorb Flip"
