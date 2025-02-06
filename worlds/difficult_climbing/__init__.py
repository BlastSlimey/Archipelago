from typing import Dict

from BaseClasses import Item, ItemClassification, Region, Tutorial
from worlds.AutoWorld import WebWorld, World
from .items import items_list, ADGACItem
from .locations import location_table, Reg, ADGACLocation
from .options import ADGACOptions


class ADGACWeb(WebWorld):
    rich_text_options_doc = True
    theme = "ocean"
    game_info_languages = ['en']
    setup_en = Tutorial(
        "Multiworld Setup Guide",
        "A guide to playing A Difficult Game About Climbing with Archipelago:",
        "English",
        "setup_en.md",
        "setup/en",
        ["BlastSlimey"]
    )
    tutorials = [setup_en]


class ADGACWorld(World):
    """A Difficult Game About Climbing is a rage platformer inspired by Getting Over It."""
    game = "A Difficult Game About Climbing"
    options_dataclass = ADGACOptions
    options: ADGACOptions
    topology_present = True
    web = ADGACWeb()

    item_name_to_id = {name: id for id, name in enumerate(items_list.keys(), 25250204)}
    location_name_to_id = {loc.name: 25250204 + loc.value for loc in location_table}

    def create_item(self, name: str) -> Item:
        return ADGACItem(name, items_list[name](self.options), self.item_name_to_id[name], self.player)

    def get_filler_item_name(self) -> str:
        return "Grip Strength"

    def create_regions(self) -> None:

        # Define regions
        regions: Dict[Reg, Region] = {
            Reg.MENU: Region("Menu", self.player, self.multiworld),
            Reg.EARLY: Region("Early game", self.player, self.multiworld),
            Reg.FOSSIL: Region("Fossils", self.player, self.multiworld),
            Reg.FIRST_CHECKPOINT: Region("First checkpoint", self.player, self.multiworld),
            Reg.CLOTHESLINE: Region("Clothesline", self.player, self.multiworld),
            Reg.LATE: Region("Late game", self.player, self.multiworld),
        }

        # Connect regions
        regions[Reg.MENU].connect(
            regions[Reg.EARLY], "After first gap",
            lambda state: state.has("Grip Strength", self.player, 1 if self.options.difficulty == "challenge" else 3)
        )
        regions[Reg.EARLY].connect(
            regions[Reg.FOSSIL], "After gas pump",
            lambda state: state.has("Grip Strength", self.player, 2 if self.options.difficulty == "challenge" else 3)
        )
        regions[Reg.FOSSIL].connect(
            regions[Reg.FIRST_CHECKPOINT], "After first difficult jump",
            lambda state: state.has("Grip Strength", self.player, 3)
        )
        regions[Reg.FIRST_CHECKPOINT].connect(
            regions[Reg.CLOTHESLINE], "After cogs",
            lambda state: (self.options.difficulty == "vanilla" and state.has("Rotating Cog Repair", self.player)) or
                          (self.options.difficulty == "extra_buff" and state.has_all(["Rotating Cog Halting",
                                                                                      "Side Cog Halting"], self.player))
        )
        regions[Reg.CLOTHESLINE].connect(
            regions[Reg.LATE], "After metal beam",
            lambda state: state.has("Swinging Metal Beam", self.player) and
                          state.has("Metal Beam Angle Increase", self.player,
                                    2 if self.options.difficulty == "challenge" else 4) and
                          ((not self.options.difficulty == "extra_buff") or state.has("Grip Strength", self.player, 5))
        )

        # Add locations to regions
        for loc in location_table:
            regions[location_table[loc]].locations.append(
                ADGACLocation(self.player, loc.name, self.location_name_to_id[loc.name], regions[location_table[loc]])
            )

        # Goal event
        goal_location = ADGACLocation(self.player, "Goal", None, regions[Reg.LATE])
        goal_location.place_locked_item(ADGACItem("Goal", ItemClassification.progression_skip_balancing,
                                                  None, self.player))
        regions[Reg.LATE].locations.append(goal_location)
        self.multiworld.completion_condition[self.player] = lambda state: state.has("Goal", self.player)

        # Adding finalized regions to multiworld
        self.multiworld.regions.extend(regions.values())

    def create_items(self) -> None:
        self.multiworld.itempool.extend([
            self.create_item("Rotating Cog Repair"),
            self.create_item("Rotating Cog Halting"),
            self.create_item("Side Cog Halting"),
            self.create_item("Deafness Trap"),
            self.create_item("Swinging Metal Beam"),
        ] + [
            self.create_item("Metal Beam Angle Increase") for _ in range(4)
        ] + [
            self.create_item("Grip Strength") for _ in range(7)
        ])
