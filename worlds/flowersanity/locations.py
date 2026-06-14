from typing import Optional, TYPE_CHECKING, Callable

from BaseClasses import Location, Region, LocationProgressType, ItemClassification
from .data import colornames_trunc, calculations

if TYPE_CHECKING:
    from . import FlowersanityWorld
    from .data import AccessRule


class FlowersanityLocation(Location):
    game = "Flowersanity"

    def __init__(self, player: int, name: str, address: Optional[int], region: Region,
                 progress_type: LocationProgressType, rule: "AccessRule"):
        super().__init__(player, name, address, region)
        self.progress_type = progress_type
        self.access_rule = rule


def lookup_table() -> dict[str, int]:
    return {
        dat[0]: (num or 0x1000000)
        for num, dat in colornames_trunc.colors.items()
    } | {
        f"Free {i}": 0x1000000 + i for i in range(1, 101)
    }


def get_regions(world: "FlowersanityWorld") -> dict[str, Region]:
    return {
        "Menu": Region("Menu", world.player, world.multiworld),
    }


def pre_generate_logic(world: "FlowersanityWorld") -> None:

    calcs = list(calculations.item_names)

    colors: list[int] = []
    while len(colors) < world.options.pool_size.value:
        if len(colors) < 2 or world.random.random() < 0.1:
            color_id = world.random.randrange(0x1000000)
            while color_id not in colornames_trunc.colors or color_id in colors:
                color_id = (color_id + 1) & 0xffffff
            colors.append(color_id)
        else:
            c1, c2 = world.random.choices(colors, k=2)
            world.random.shuffle(calcs)
            for cal in calcs:
                new_c = cal(c1, c2)
                if new_c in colornames_trunc.colors and new_c not in colors:
                    colors.append(new_c)
                    break

    world.colors = colors


def create_events(world: "FlowersanityWorld", regions: dict[str, Region]) -> None:
    from .items import FlowersanityItem

    def check_calc(c: Callable[[int, int], int], c1: int, c2: int):
        if c1 == c2 and c == calculations.subtraction and c1 % 32:
            return
        new_c = c(c1, c2)
        if new_c == 0xffffff and c == calculations.addition and c1 % 32:
            return
        if c1 != new_c != c2 and new_c in world.colors and new_c in colornames_trunc.colors:
            new_c_name = colornames_trunc.colors[new_c][0]
            c1_name = colornames_trunc.colors[c1][0]
            c2_name = colornames_trunc.colors[c2][0]
            calc_name = calculations.item_names[c]
            loc = FlowersanityLocation(
                world.player, f"{calc_name} [{c1_name}] [{c2_name}]", None, regions["Menu"],
                LocationProgressType.DEFAULT, lambda state: state.has_all((c1_name, c2_name, calc_name), world.player)
            )
            regions["Menu"].locations.append(loc)
            item = FlowersanityItem(new_c_name, ItemClassification.progression, None, world.player)
            loc.place_locked_item(item)

    for calc in calculations.item_names:
        checks = 0
        for i in range(len(world.colors)):
            if len(world.colors) <= 150:
                ran = range(i, len(world.colors))
            else:
                p = world.random.randrange(i, len(world.colors) - 100)
                ran = range(p, p + 100)
            for j in ran:
                check_calc(calc, world.colors[i], world.colors[j])
                checks += 1
                if checks >= 2000:
                    break
            else:
                continue
            break

    all_colors = tuple(colornames_trunc.colors[col][0] for col in world.colors)
    if world.options.goal == "colors_count":
        world.multiworld.completion_condition[world.player] = \
            lambda state: state.has_from_list_unique(all_colors, world.player, world.options.goal_amount)
    else:
        world.multiworld.completion_condition[world.player] = \
            lambda state: state.has_all(world.options.goal_colors, world.player)


def create_and_place_locations(world: "FlowersanityWorld", regions: dict[str, Region]) -> None:

    def get_rule(col: int) -> Callable:
        return lambda state: state.has(colornames_trunc.colors[col][0], world.player)

    for color in world.colors:
        regions["Menu"].locations.append(FlowersanityLocation(
            world.player, colornames_trunc.colors[color][0], color, regions["Menu"], LocationProgressType.DEFAULT,
            get_rule(color)
        ))
    free_rule = lambda state: True
    for i in range(1, 7):
        regions["Menu"].locations.append(FlowersanityLocation(
            world.player, f"Free {i}", 0x1000000 + i, regions["Menu"], LocationProgressType.DEFAULT, free_rule
        ))
