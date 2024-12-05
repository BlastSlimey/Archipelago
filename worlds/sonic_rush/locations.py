from typing import Dict, Optional, List

from BaseClasses import Location, Region, LocationProgressType, CollectionState

act_locations: Dict[str, LocationProgressType] = {
    f"{name} Act {act} ({character})": LocationProgressType.DEFAULT
    for name in ["Leaf Storm", "Water Palace", "Mirage Road", "Night Carnival",
                 "Huge Crisis", "Altitude Limit", "Dead Line"]
    for act in [1, 2]
    for character in ["Sonic", "Blaze"]
}

boss_locations: Dict[str, LocationProgressType] = {
    f"{name} Boss ({character})": LocationProgressType.PRIORITY
    for name in ["Leaf Storm", "Water Palace", "Mirage Road", "Night Carnival",
                 "Huge Crisis", "Altitude Limit", "Dead Line", "Unknown"]
    for character in ["Sonic", "Blaze"]
}

special_stage_locations: Dict[str, LocationProgressType] = {
    f"{name} Special Stage": LocationProgressType.DEFAULT
    for name in ["Leaf Storm", "Water Palace", "Mirage Road", "Night Carnival",
                 "Huge Crisis", "Altitude Limit", "Dead Line"]
}

enemysanity_locations: Dict[str, LocationProgressType] = {
    "Battle Flapper": LocationProgressType.DEFAULT,
    "Bomb Hawk": LocationProgressType.DEFAULT,
    "Cannon Flapper": LocationProgressType.DEFAULT,
    "Egg Bishop": LocationProgressType.DEFAULT,
    "Egg Hammer": LocationProgressType.DEFAULT,
    "Egg Pawn": LocationProgressType.DEFAULT,
    "Egg Pawn Bunny": LocationProgressType.DEFAULT,
    "Egg Pawn Manager (gun)": LocationProgressType.DEFAULT,
    "Egg Pawn Manager (SF gun)": LocationProgressType.DEFAULT,
    "Falco": LocationProgressType.DEFAULT,
    "Flapper": LocationProgressType.DEFAULT,
    "Gun Hunter": LocationProgressType.DEFAULT,
    "Klagen": LocationProgressType.DEFAULT,
    "Knight Pawn": LocationProgressType.DEFAULT,
    "Laser Flapper": LocationProgressType.DEFAULT,
    "Rhino Cannon": LocationProgressType.DEFAULT,
    "Sea Pawn": LocationProgressType.DEFAULT,
    "Solid Pawn": LocationProgressType.DEFAULT
}

location_table: Dict[str, LocationProgressType] = {
    **act_locations,
    **boss_locations,
    **special_stage_locations,
    **enemysanity_locations
}


def has_progressive(state: CollectionState, name: str, amount: int, player: int) -> bool:
    return state.has_any_count({f"Progressive {name} ({character})": amount
                                for character in ["Sonic", "Blaze"]}, player)


def can_play_special_stages(state: CollectionState, player: int, names: List[str]) -> bool:
    return state.has_any([f"Progressive {name} (Sonic)" for name in names], player)


class SonicRushLocation(Location):
    game = "Sonic Rush"

    def __init__(self, player: int, name: str, address: Optional[int], region: Region,
                 progress_type: LocationProgressType):
        super(SonicRushLocation, self).__init__(player, name, address, region)
        self.progress_type = progress_type

