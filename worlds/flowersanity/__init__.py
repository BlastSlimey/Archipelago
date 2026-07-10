from typing import Mapping, Any

from BaseClasses import MultiWorld, Tutorial
from Options import Option, OptionError
from worlds.AutoWorld import WebWorld, World
from . import options, locations, items


class FlowersanityWeb(WebWorld):
    rich_text_options_doc = True
    theme = "partyTime"
    game_info_languages = ['en']
    setup_en = Tutorial(
        "Multiworld Setup Guide",
        "A guide to playing Flowersanity with Archipelago:",
        "English",
        "setup_en.md",
        "setup/en",
        ["BlastSlimey"]
    )
    tutorials = [setup_en]


class FlowersanityWorld(World):
    """
    Flowersanity is a game about merging flowers and mixing their colors.
    It was made for the Archipelago Game Jam 2026.
    By spawning in the flower colors you received and merging them using different
    calculation modes, you create and thereby check new colors.
    """
    game = "Flowersanity"
    options_dataclass = options.FlowersanityOptions
    options: options.FlowersanityOptions
    topology_present = True
    web = FlowersanityWeb()
    item_name_to_id = items.lookup_table()
    location_name_to_id = locations.lookup_table()
    ut_can_gen_without_yaml = True

    def __init__(self, multiworld: MultiWorld, player: int):
        super().__init__(multiworld, player)

        from .data.version import ap_minimum
        from Utils import version_tuple
        if version_tuple < ap_minimum():
            raise Exception(f"Archipelago version too old for Flowersanity "
                            f"(requires minimum {ap_minimum()}, found {version_tuple}")

        self.seed: int = 0
        self.to_be_filled_locations: int = 0
        self.colors: list[int] | None = None

        self.ut_active: bool = False
        self.location_id_to_alias: dict[int, str] = {}

    def generate_early(self) -> None:

        # Load values from UT if this is a regenerated world
        if hasattr(self.multiworld, "re_gen_passthrough"):
            if self.game in self.multiworld.re_gen_passthrough:
                from .data import version

                self.ut_active = True
                re_gen_slot_data: dict[str, Any] = self.multiworld.re_gen_passthrough[self.game]
                re_gen_options: dict[str, Any] = re_gen_slot_data["options"]
                # Populate options from UT
                for key, value in re_gen_options.items():
                    opt: Option | None = getattr(self.options, key, None)
                    if opt is not None:
                        setattr(self.options, key, opt.from_any(value))
                self.seed = re_gen_slot_data["seed"]

        if not self.ut_active:
            self.seed = self.random.getrandbits(64)

        self.random.seed(self.seed)

        if self.options.goal_amount > self.options.pool_size:
            raise OptionError(f"{self.player_name}: Goal Amount cannot be higher than Pool size")

        locations.pre_generate_logic(self)

    def create_item(self, name: str) -> items.FlowersanityItem:
        return items.generate_item(name, self)

    def get_filler_item_name(self) -> str:
        return items.generate_filler(self)

    def create_regions(self) -> None:
        regions = locations.get_regions(self)
        locations.create_events(self, regions)
        locations.create_and_place_locations(self, regions)
        self.to_be_filled_locations = sum(
            (0 if loc.item else 1)
            for reg in regions.values()
            for loc in reg.locations
        )
        self.multiworld.regions.extend(regions.values())

    def create_items(self) -> None:
        item_pool = items.get_main_item_pool(self)
        if len(item_pool) > self.to_be_filled_locations:
            raise Exception(f"Player {self.player_name} has more guaranteed items ({len(item_pool)}) "
                            f"than to-be-filled locations ({self.to_be_filled_locations})."
                            f"Please report this to the apworld dev and provide the yaml used for generating.")
        for _ in range(self.to_be_filled_locations-len(item_pool)):
            item_pool.append(self.create_item(self.get_filler_item_name()))
        self.multiworld.itempool.extend(item_pool)

    def fill_slot_data(self) -> Mapping[str, Any]:
        from .data import version

        # Some options and data are included for UT
        return {
            "options": {
                "goal": self.options.goal.current_key,
                "goal_amount": self.options.goal_amount.value,
                "goal_colors": self.options.goal_colors.value,
                "pool_size": self.options.pool_size.value,
            },
            # Needed for UT
            "seed": self.seed,
        }

    @staticmethod
    def interpret_slot_data(slot_data: dict[str, Any]) -> dict[str, Any]:
        """Helper function for Universal Tracker"""
        return slot_data
