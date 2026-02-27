from typing import TYPE_CHECKING

from BaseClasses import Item
from .data.items import capture, assist
from .data.pokemon import data_by_number, by_name

if TYPE_CHECKING:
    from . import RangerQuestWorld


class RangerQuestItem(Item):
    game = "Pokemon Ranger (Quest)"


def lookup_table() -> dict[str, int]:
    return {
        name: data.item_id
        for table in (capture, assist)  # TODO add field_any/level when implemented
        for name, data in table.items()
    }


def get_quest_pool(world: "RangerQuestWorld") -> list[list[str]]:
    pool = []
    _capture = []
    _capture_special = []
    _assist = []
    allow_off_mission = "Captures (off-mission)" in world.options.modify_quest_pool
    allow_missions_only = "Captures (missions-only)" in world.options.modify_quest_pool
    allow_legendary_off_mission = "Legendary captures (off-mission)" in world.options.modify_quest_pool
    allow_special_missions = "Captures (special missions)" in world.options.modify_quest_pool
    blacklist = set(by_name[name].number for name in world.options.captures_blacklist.value)  # only lookup, no iterate
    for name, item_data in capture.items():
        poke_data = data_by_number[item_data.number]
        if not poke_data.catchable or poke_data.number in blacklist:
            continue
        if poke_data.missions_only:
            if allow_missions_only:
                _capture_special.append(name)
            else:
                continue
        elif poke_data.special_missions:
            if allow_special_missions:
                _capture_special.append(name)
            else:
                continue
        elif poke_data.legendary:  # and not poke_data.missions_only
            if allow_legendary_off_mission:
                _capture_special.append(name)
            else:
                continue
        elif allow_off_mission:
            _capture.append(name)
    if "Poké Assists" in world.options.modify_quest_pool:
        _assist = list(assist)
    if _assist:
        pool.append(_assist)
    if _capture_special:
        pool.append(_capture_special)
    if _capture:
        if pool:
            pool += [_capture] * (3 * len(pool))
        else:
            pool = [_capture]
    return pool
