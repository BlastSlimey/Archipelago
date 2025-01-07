from typing import Mapping, Any, Dict

from BaseClasses import Item, Location, ItemClassification, Region
from worlds.AutoWorld import WebWorld, World
from .options import GOIOptions


class GOIWeb(WebWorld):
    rich_text_options_doc = True
    theme = "stone"


class GOIWorld(World):
    """
    Getting Over It is a game.
    """
    game = "Getting Over It"
    options_dataclass = GOIOptions
    options: GOIOptions
    topology_present = True
    web = GOIWeb()

    base_id = 22220107
    items_list: Dict[str, ItemClassification] = {
        "Gravity Reduction": ItemClassification.progression,
        "Wind Trap": ItemClassification.trap,
        "Goal Height Reduction": ItemClassification.progression,
        "Frustration": ItemClassification.filler,
    }
    instant_spot = ["Tree", "Paddle"]
    early_spots = ["Concrete Pipe", "Cup", "Trash", "Second Lamp", "Bathtub", "Grill", "Kids Slide"]
    midgame_spots = ["Child", "Staircase", "Security Cam", "Toilet", "Orange Table", "Gargoyle", "Church Top", "Hedge",
                     "Hat"]
    late_spots = ["Snake Ride", "Bucket", "Landing Stage", "Ice Mountain", "Temple", "Antenna Top"]
    spots_list = instant_spot + early_spots + midgame_spots + late_spots
    completions_list = [f"Got Over It #{count}" for count in range(1, 10)]
    locations_list = spots_list + completions_list

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
        region_completions = Region("Completions", self.player, self.multiworld)

        region_menu.connect(region_early, "Past tree",
                            lambda state: state.has("Gravity Reduction", self.player, self.options.difficulty.value))
        region_early.connect(region_mid, "Got on the slide",
                             lambda state: state.has("Gravity Reduction", self.player,
                                                     self.options.difficulty.value + 1))
        region_mid.connect(region_late, "From the anvil",
                           lambda state: state.has("Gravity Reduction", self.player, self.options.difficulty.value + 2))
        region_mid.connect(region_completions, "Reaching the top",
                           lambda state: state.has("Gravity Reduction", self.player, self.options.difficulty.value + 2)
                                         or state.has("Goal Height Reduction", self.player, 4))

        region_menu.locations.append(GOILocation(self.player, "Tree", self.location_name_to_id["Tree"], region_menu))
        region_menu.locations.append(GOILocation(self.player, "Paddle", self.location_name_to_id["Paddle"],
                                                 region_menu))
        for count in range(1, self.options.required_completions.value):
            loc_name = f"Got Over It #{count}"
            region_completions.locations.append(GOILocation(self.player, loc_name, self.location_name_to_id[loc_name],
                                                            region_late))
        remaining_spots = self.early_spots + self.midgame_spots + self.late_spots
        for _ in range(13 - self.options.required_completions.value):
            loc_name = remaining_spots.pop(self.random.randint(0, len(remaining_spots)-1))
            if loc_name in self.early_spots:
                region_early.locations.append(GOILocation(self.player, loc_name, self.location_name_to_id[loc_name],
                                                          region_early))
            elif loc_name in self.midgame_spots:
                region_mid.locations.append(GOILocation(self.player, loc_name, self.location_name_to_id[loc_name],
                                                        region_mid))
            if loc_name in self.late_spots:
                region_late.locations.append(GOILocation(self.player, loc_name, self.location_name_to_id[loc_name],
                                                         region_late))

        goal_location = GOILocation(self.player, "Goal", None, region_completions)
        goal_location.place_locked_item(GOIItem("Goal", ItemClassification.progression_skip_balancing,
                                                None, self.player))
        region_completions.locations.append(goal_location)
        self.multiworld.completion_condition[self.player] = lambda state: state.has("Goal", self.player)

        self.multiworld.regions.extend([region_menu, region_early, region_mid, region_late, region_completions])

    def create_items(self) -> None:
        self.multiworld.itempool.extend([self.create_item("Gravity Reduction") for _ in range(4)] +
                                        [self.create_item("Wind Trap") for _ in range(6)] +
                                        [self.create_item("Goal Height Reduction") for _ in range(4)])


class GOIItem(Item):
    game = "Getting Over It"


class GOILocation(Location):
    game = "Getting Over It"
