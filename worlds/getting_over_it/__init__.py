from typing import Dict

from BaseClasses import Item, Location, ItemClassification, Region, Tutorial
from worlds.AutoWorld import WebWorld, World
from .items import items_list, GOIItem
from .locations import locations_list, GOILocation
from .options import GOIOptions


class GOIWeb(WebWorld):
    rich_text_options_doc = True
    theme = "stone"
    game_info_languages = ['en']
    setup_en = Tutorial(
        "Multiworld Setup Guide",
        "A guide to playing Getting Over It with Archipelago:",
        "English",
        "setup_en.md",
        "setup/en",
        ["BlastSlimey"]
    )
    tutorials = [setup_en]


class GOIWorld(World):
    """
    Getting Over It is a frustrating psychological horror game about climbing a mountain.
    """
    game = "Getting Over It"
    options_dataclass = GOIOptions
    options: GOIOptions
    topology_present = True
    web = GOIWeb()

    base_id = 22220107

    item_name_to_id = {name: id for id, name in enumerate(items_list.keys(), base_id)}
    location_name_to_id = {name: id for id, name in enumerate(locations_list, base_id)}

    def create_item(self, name: str) -> Item:
        return GOIItem(name, self.items_list[name], self.item_name_to_id[name], self.player)

    def get_filler_item_name(self) -> str:
        return "Frustration"

    def create_regions(self) -> None:

        region_menu = Region("Menu", self.player, self.multiworld)
        region_early = Region("Early spots", self.player, self.multiworld)
        region_mid = Region("Midgame spots", self.player, self.multiworld)
        region_late = Region("Late spots", self.player, self.multiworld)
        region_float = Region("Float-only spots", self.player, self.multiworld)

        region_menu.connect(region_early, "Past tree and paddle",
                            lambda state: state.has("Gravity Reduction", self.player, self.options.difficulty.value))
        region_early.connect(region_mid, "Getting on to the slide",
                             lambda state: state.has("Gravity Reduction", self.player,
                                                     self.options.difficulty.value + 1))
        region_mid.connect(region_late, "Jumping from the anvil",
                           lambda state: state.has("Gravity Reduction", self.player, self.options.difficulty.value + 2)
                                         or state.has("Goal Height Reduction", self.player, 4))
        region_late.connect(region_float, "Jumping to very high places",
                            lambda state: state.has("Gravity Reduction", self.player, 4))

        for loc in self.instant_spots:  # always 2 locations
            region_menu.locations.append(GOILocation(self.player, loc, self.location_name_to_id[loc], region_menu))
        for count in range(1, self.options.required_completions.value):  # 0-9 locations
            loc_name = f"Got Over It #{count}"
            region_late.locations.append(GOILocation(self.player, loc_name,
                                                     self.location_name_to_id[loc_name], region_late))
        remaining_spots = self.early_spots + self.midgame_spots + self.late_spots + self.float_only_spots
        for _ in range(15 - self.options.required_completions.value):  # => 14-5 extra locations
            loc_name = remaining_spots.pop(self.random.randint(0, len(remaining_spots)-1))
            if loc_name in self.early_spots:
                region_early.locations.append(GOILocation(self.player, loc_name, self.location_name_to_id[loc_name],
                                                          region_early))
            elif loc_name in self.midgame_spots:
                region_mid.locations.append(GOILocation(self.player, loc_name, self.location_name_to_id[loc_name],
                                                        region_mid))
            elif loc_name in self.late_spots:
                region_late.locations.append(GOILocation(self.player, loc_name, self.location_name_to_id[loc_name],
                                                         region_late))
            elif loc_name in self.float_only_spots:
                region_float.locations.append(GOILocation(self.player, loc_name, self.location_name_to_id[loc_name],
                                                          region_float))

        # Goal event
        goal_location = GOILocation(self.player, "Goal", None, region_late)
        goal_location.place_locked_item(GOIItem("Goal", ItemClassification.progression_skip_balancing,
                                                None, self.player))
        region_late.locations.append(goal_location)
        self.multiworld.completion_condition[self.player] = lambda state: state.has("Goal", self.player)

        self.multiworld.regions.extend([region_menu, region_early, region_mid, region_late, region_float])

    def create_items(self) -> None:
        self.multiworld.itempool.extend([self.create_item("Gravity Reduction") for _ in range(4)] +
                                        [self.create_item("Wind Trap") for _ in range(6)] +
                                        [self.create_item("Goal Height Reduction") for _ in range(6)])
