from typing import List, Tuple, Dict, Optional

from BaseClasses import Location, LocationProgressType, Region
from .options import SonicRushOptions

location_description = {}

act_locations: List[str] = [f"Zone {zone} Act {act} {rank}({char})"
                            for zone in [1, 2, 3, 4, 5, 6, 7]
                            for act in [1, 2]
                            for char in ["Sonic", "Blaze"]
                            for rank in ["", "S Rank "]]
boss_locations: List[str] = ([f"Zone {zone} Boss {rank}({char})"
                              for zone in [1, 2, 3, 4, 5, 6, 7]
                              for char in ["Sonic", "Blaze"]
                              for rank in ["", "S Rank "]]
                             + ["F-Zone (Sonic)", "F-Zone (Blaze)", "Extra Zone"])
special_stage_locations: List[str] = [f"Special Stage Zone {zone}" for zone in [1, 2, 3, 4, 5, 6, 7]]

all_locations: List[str] = act_locations + boss_locations + special_stage_locations

base_id = 20010707
location_lookup_by_name: Dict[str, int] = {
    name: next_id for next_id, name in enumerate(all_locations, base_id)
}


def add_base_acts(options: SonicRushOptions) -> Dict[str, Tuple[str, LocationProgressType]]:

    return {
        f"Zone {zone} Act {act} {rank}({char})": (f"Zone {zone} ({char})", LocationProgressType.DEFAULT)
        for zone in [1, 2, 3, 4, 5, 6, 7]
        for act in [1, 2]
        for char in ["Sonic", "Blaze"]
        for rank in (["", "S Rank "] if options.include_s_rank_checks in ["only_acts", "all"] else [""])
    }


def add_bosses(options: SonicRushOptions) -> Dict[str, Tuple[str, LocationProgressType]]:

    return {
        **{
            f"Zone {zone} Boss {rank}({char})": (f"Zone {zone} ({char})", LocationProgressType.PRIORITY)
            for zone in [1, 2, 3, 4, 5, 6, 7]
            for char in ["Sonic", "Blaze"]
            for rank in (["", "S Rank "] if options.include_s_rank_checks in ["only_bosses", "all"] else [""])
        },
        **{
            "F-Zone (Sonic)": (
                "F-Zone (Sonic)",
                LocationProgressType.EXCLUDED if options.screw_f_zone else LocationProgressType.PRIORITY),
            "F-Zone (Blaze)": (
                "F-Zone (Blaze)",
                LocationProgressType.EXCLUDED if options.screw_f_zone else LocationProgressType.PRIORITY),
        },
        **({
            "Extra Zone": ("Extra Zone", LocationProgressType.PRIORITY)
        } if not options.goal == "extra_zone" else {}),
    }


def add_special_stages(options: SonicRushOptions) -> Dict[str, Tuple[str, LocationProgressType]]:

    return {
        f"Special Stage Zone {zone}": (f"Zone {zone} (Sonic)", LocationProgressType.PRIORITY)
        for zone in [1, 2, 3, 4, 5, 6, 7]
    }


class SonicRushLocation(Location):
    game = "Sonic Rush"

    def __init__(self, player: int, name: str, address: Optional[int], region: Region,
                 progress_type: LocationProgressType):
        super(SonicRushLocation, self).__init__(player, name, address, region)
        self.progress_type = progress_type
