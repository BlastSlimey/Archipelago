from typing import List, Mapping, Any

from BaseClasses import Item, Region, LocationProgressType, ItemClassification, Tutorial
from worlds.AutoWorld import World, WebWorld
from .items import SonicRushItem, item_table, progressive_act_items, final_boss_items, emerald_items, traps
from .locations import location_table, SonicRushLocation, has_progressive, can_play_special_stages
from .options import SonicRushOptions
from worlds.generic.Rules import set_rule


class SonicRushWeb(WebWorld):
    rich_text_options_doc = True
    game_info_languages = ['en']
    setup_en = Tutorial(
        "Multiworld Setup Guide",
        "A guide to playing Sonic Rush with Archipelago.",
        "English",
        "setup_en.md",
        "setup/en",
        ["Unknown"]
    )
    tutorials = [setup_en]


class SonicRushWorld(World):
    """
    Sonic Rush is a 2.5D platformer for the Nintendo DS from 2005. It's the game that introduced Blaze the Cat and the
    boost ability.
    """
    game = "Sonic Rush"
    options_dataclass = SonicRushOptions
    options: SonicRushOptions
    topology_present = True
    origin_region_name = "Overworld"
    web = SonicRushWeb()

    base_id = 20071224
    location_count: int = 0  # Placeholder value

    item_name_to_id = {name: id for id, name in enumerate(item_table.keys(), base_id)}
    location_name_to_id = {name: id for id, name in enumerate(location_table.keys(), base_id)}

    def create_item(self, name: str) -> Item:
        return SonicRushItem(name, item_table[name], self.item_name_to_id[name], self.player)

    def get_filler_item_name(self) -> str:
        return "Extra Life"

    def create_regions(self) -> None:
        overworld_region: Region = Region("Overworld", self.player, self.multiworld)
        self.multiworld.regions.append(overworld_region)

        self.location_count = 0
        for name in location_table.keys():
            overworld_region.locations.append(SonicRushLocation(self.player, name, self.location_name_to_id[name],
                                                                overworld_region, location_table[name]))
            self.location_count += 1

        goal_location = SonicRushLocation(self.player, "Goal", None, overworld_region, LocationProgressType.DEFAULT)
        overworld_region.locations.append(goal_location)
        goal_location.place_locked_item(SonicRushItem("Goal", ItemClassification.progression_skip_balancing,
                                                      None, self.player))

    def create_items(self) -> None:
        included_progressive_acts: List[Item] = [self.create_item(name)
                                                 for name in progressive_act_items.keys() for _ in range(3)]
        for _ in range(self.options.starting_acts.value):
            self.multiworld.push_precollected(
                included_progressive_acts.pop(self.random.randint(0, len(included_progressive_acts)-1))
            )

        included_items: List[Item] = (included_progressive_acts +
                                      [self.create_item(name) for name in final_boss_items.keys()] +
                                      [self.create_item(name) for name in emerald_items.keys()])

        remaining = self.location_count-len(included_items)  # -1 because of prefilled starting act and goal
        traps_amount = remaining * self.options.traps_percentage.value // 100
        for _ in range(traps_amount):
            included_items.append(self.create_item(list(traps.keys())[self.random.randint(0, len(traps)-1)]))
        for _ in range(remaining-traps_amount):
            included_items.append(self.create_filler())

        self.multiworld.itempool.extend(included_items)

    def set_rules(self) -> None:
        # goal event
        goal_location = self.get_location("Goal")
        self.multiworld.completion_condition[self.player] = lambda state: state.has("Goal", self.player)
        if self.options.goal == "8_bosses_once":
            set_rule(goal_location, lambda state: has_progressive(state, "Leaf Storm", 3, self.player) and
                                                  has_progressive(state, "Water Palace", 3, self.player) and
                                                  has_progressive(state, "Mirage Road", 3, self.player) and
                                                  has_progressive(state, "Night Carnival", 3, self.player) and
                                                  has_progressive(state, "Huge Crisis", 3, self.player) and
                                                  has_progressive(state, "Altitude Limit", 3, self.player) and
                                                  has_progressive(state, "Dead Line", 3, self.player) and
                                                  state.has_any(final_boss_items.keys(), self.player))
        elif self.options.goal == "8_bosses_both":
            set_rule(goal_location,
                     lambda state: state.has_all_counts({key: 3 for key in progressive_act_items.keys()}, self.player)
                                   and state.has_all(final_boss_items.keys(), self.player))
        elif self.options.goal == "7_bosses_extra":
            set_rule(goal_location,
                     lambda state: state.has_all_counts({key: 3 for key in progressive_act_items.keys()}, self.player))
        elif self.options.goal == "emeralds":
            set_rule(goal_location, lambda state: state.has_all(emerald_items.keys(), self.player))
        elif self.options.goal == "emeralds_extra":
            set_rule(goal_location, lambda state: state.has_all(emerald_items.keys(), self.player))
        else:  # == "100_percent"
            set_rule(goal_location,
                     lambda state: state.has_all_counts({key: 3 for key in progressive_act_items.keys()}, self.player)
                                   and state.has_all(final_boss_items.keys(), self.player)
                                   and state.has_all(emerald_items.keys(), self.player))

        set_rule(self.get_location("Unknown Boss (Sonic)"),
                 lambda state: state.has("Unknown (Sonic)", self.player))
        set_rule(self.get_location("Unknown Boss (Blaze)"),
                 lambda state: state.has("Unknown (Blaze)", self.player))
        for name in ["Leaf Storm", "Water Palace", "Mirage Road", "Night Carnival",
                     "Huge Crisis", "Altitude Limit", "Dead Line"]:
            set_rule(self.get_location(f"{name} Special Stage"),
                     lambda state: state.has(f"Progressive {name} (Sonic)", self.player, 1))
            for character in ["Sonic", "Blaze"]:
                set_rule(self.get_location(f"{name} Act 1 ({character})"),
                         lambda state: state.has(f"Progressive {name} ({character})", self.player, 1))
                set_rule(self.get_location(f"{name} Act 2 ({character})"),
                         lambda state: state.has(f"Progressive {name} ({character})", self.player, 2))
                set_rule(self.get_location(f"{name} Boss ({character})"),
                         lambda state: state.has(f"Progressive {name} ({character})", self.player, 3))
        # TODO look up how many unlocks are actually needed, and special stages
        set_rule(self.get_location(f"Battle Flapper"),
                 lambda state: has_progressive(state, "Night Carnival", 1, self.player) or
                               can_play_special_stages(state, self.player, ["Night Carnival", "Huge Crisis",
                                                                            "Altitude Limit", "Dead Line", ]))
        set_rule(self.get_location(f"Bomb Hawk"),
                 lambda state: has_progressive(state, "Huge Crisis", 1, self.player))
        set_rule(self.get_location(f"Cannon Flapper"),
                 lambda state: has_progressive(state, "Altitude Limit", 1, self.player))
        set_rule(self.get_location(f"Egg Bishop"),
                 lambda state: has_progressive(state, "Mirage Road", 1, self.player))
        set_rule(self.get_location(f"Egg Hammer"),
                 lambda state: has_progressive(state, "Mirage Road", 1, self.player) or
                               has_progressive(state, "Dead Line", 2, self.player))
        set_rule(self.get_location(f"Egg Pawn"),
                 lambda state: has_progressive(state, "Leaf Storm", 1, self.player) or
                               has_progressive(state, "Mirage Road", 1, self.player))
        set_rule(self.get_location(f"Egg Pawn Bunny"),
                 lambda state: has_progressive(state, "Night Carnival", 1, self.player))
        set_rule(self.get_location(f"Egg Pawn Manager (gun)"),
                 lambda state: has_progressive(state, "Leaf Storm", 1, self.player))
        set_rule(self.get_location(f"Egg Pawn Manager (SF gun)"),
                 lambda state: has_progressive(state, "Dead Line", 1, self.player))
        set_rule(self.get_location(f"Falco"),
                 lambda state: has_progressive(state, "Altitude Limit", 1, self.player))
        set_rule(self.get_location(f"Flapper"),
                 lambda state: has_progressive(state, "Water Palace", 2, self.player) or
                               has_progressive(state, "Leaf Storm", 1, self.player) or
                               can_play_special_stages(state, self.player, ["Water Palace", "Mirage Road",
                                                                            "Night Carnival", "Huge Crisis",
                                                                            "Altitude Limit", "Dead Line", ]))
        set_rule(self.get_location(f"Gun Hunter"),
                 lambda state: has_progressive(state, "Huge Crisis", 1, self.player))
        set_rule(self.get_location(f"Klagen"),
                 lambda state: has_progressive(state, "Water Palace", 1, self.player))
        set_rule(self.get_location(f"Knight Pawn"),
                 lambda state: has_progressive(state, "Water Palace", 1, self.player))
        set_rule(self.get_location(f"Laser Flapper"),
                 lambda state: has_progressive(state, "Dead Line", 1, self.player))
        set_rule(self.get_location(f"Rhino Cannon"),
                 lambda state: has_progressive(state, "Huge Crisis", 1, self.player))
        set_rule(self.get_location(f"Sea Pawn"),
                 lambda state: has_progressive(state, "Water Palace", 1, self.player))
        set_rule(self.get_location(f"Solid Pawn"),
                 lambda state: has_progressive(state, "Dead Line", 1, self.player))

    def fill_slot_data(self) -> Mapping[str, Any]:
        return {
            "goal": self.options.goal.current_key,
            "traps_percentage": self.options.traps_percentage.value,
            "sonic_vs_blaze_multiplier": self.options.sonic_vs_blaze_multiplier.value,
            "death_link": bool(self.options.death_link.value)
        }
