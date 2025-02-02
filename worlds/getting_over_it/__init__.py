from typing import Dict, Mapping, Any, List

from BaseClasses import Item, ItemClassification, Region, Tutorial, MultiWorld
from worlds.AutoWorld import WebWorld, World
from .items import items_list, GOIItem
from .locations import locations_list, GOILocation, instant_spots, early_spots, midgame_spots, late_spots, \
    float_only_spots, spots_list
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

    def __init__(self, multiworld: MultiWorld, player: int):
        super().__init__(multiworld, player)

        # Universal Tracker support
        self.ut_active: bool = False
        self.passthrough: Dict[str, any] = {}
        self.ut_spots: List[str] = []

    def generate_early(self) -> None:
        # Load values from UT if this is a regenerated world
        if hasattr(self.multiworld, "re_gen_passthrough"):
            if "Getting Over It" in self.multiworld.re_gen_passthrough:
                self.ut_active = True
                self.passthrough = self.multiworld.re_gen_passthrough["Getting Over It"]
                self.ut_spots = self.passthrough["spots"]

    def create_item(self, name: str) -> Item:
        return GOIItem(name, items_list[name], self.item_name_to_id[name], self.player)

    def get_filler_item_name(self) -> str:
        return "Frustration"

    def create_regions(self) -> None:

        # Define regions
        region_menu = Region("Menu", self.player, self.multiworld)
        region_early = Region("Early spots", self.player, self.multiworld)
        region_mid = Region("Midgame spots", self.player, self.multiworld)
        region_late = Region("Late spots", self.player, self.multiworld)
        region_float = Region("Float-only spots", self.player, self.multiworld)

        # Connect regions
        region_menu.connect(
            region_early, "Past tree and paddle",
            lambda state: state.has("Gravity Reduction", self.player, self.options.difficulty.value))
        region_early.connect(
            region_mid, "Getting on to the slide",
            lambda state: state.has("Gravity Reduction", self.player, self.options.difficulty.value + 1))
        region_mid.connect(
            region_late, "Jumping from the anvil",
            lambda state: state.has("Gravity Reduction", self.player, self.options.difficulty.value + 2) or
                          state.has("Goal Height Reduction", self.player, 4))
        region_menu.connect(
            region_float, "Jumping to very high places",
            lambda state: state.has("Gravity Reduction", self.player, 4))

        # Add tree and paddle (guaranteed locations) and "Got Over It #X" locations
        for loc in instant_spots:
            region_menu.locations.append(GOILocation(self.player, loc, self.location_name_to_id[loc], region_menu))
        for count in range(1, self.options.required_completions.value):
            loc_name = f"Got Over It #{count}"
            region_late.locations.append(
                GOILocation(self.player, loc_name, self.location_name_to_id[loc_name], region_late))

        # Choose 5-14 random additional locations from the remaining spots
        def add(name: str):
            if name in early_spots:
                region_early.locations.append(
                    GOILocation(self.player, name, self.location_name_to_id[name], region_early))
            elif name in midgame_spots:
                region_mid.locations.append(
                    GOILocation(self.player, name, self.location_name_to_id[name], region_mid))
            elif name in late_spots:
                region_late.locations.append(
                    GOILocation(self.player, name, self.location_name_to_id[name], region_late))
            elif name in float_only_spots:
                region_float.locations.append(
                    GOILocation(self.player, name, self.location_name_to_id[name], region_float))
            else:
                raise ValueError(f"Tried to add spot {name} without having a region defined")

        if self.ut_active:
            for spot in self.ut_spots:
                add(spot)
        else:
            remaining_spots = early_spots + midgame_spots + late_spots + float_only_spots
            for _ in range(15 - self.options.required_completions.value):
                add(remaining_spots.pop(self.random.randint(0, len(remaining_spots)-1)))

        # Goal event
        goal_location = GOILocation(self.player, "Goal", None, region_late)
        goal_location.place_locked_item(GOIItem("Goal", ItemClassification.progression_skip_balancing,
                                                None, self.player))
        region_late.locations.append(goal_location)
        self.multiworld.completion_condition[self.player] = lambda state: state.has("Goal", self.player)

        # Adding finalized regions to multiworld
        self.multiworld.regions.extend([region_menu, region_early, region_mid, region_late, region_float])

    def create_items(self) -> None:
        self.multiworld.itempool.extend([self.create_item("Gravity Reduction") for _ in range(4)] +
                                        [self.create_item("Wind Trap") for _ in range(6)] +
                                        [self.create_item("Goal Height Reduction") for _ in range(6)])

    def fill_slot_data(self) -> Mapping[str, Any]:
        spots: List[str] = []
        for location in self.get_locations():
            if location.name in spots_list:
                spots.append(location.name)
        return {"spots": spots}
