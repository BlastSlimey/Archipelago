from typing import Dict

from BaseClasses import Item, ItemClassification

progressive_act_items: Dict[str, ItemClassification] = {
    f"Progressive {name} ({character})": ItemClassification.progression
    for name in ["Leaf Storm", "Water Palace", "Mirage Road", "Night Carnival",
                 "Huge Crisis", "Altitude Limit", "Dead Line"]
    for character in ["Sonic", "Blaze"]
}

final_boss_items: Dict[str, ItemClassification] = {
    "Unknown (Sonic)": ItemClassification.progression,
    "Unknown (Blaze)": ItemClassification.progression
}

emerald_items: Dict[str, ItemClassification] = {
    f"{color} {character} Emerald": ItemClassification.progression
    for color in ["Red", "Blue", "Yellow", "Green", "Silver", "Cyan", "Purple"]
    for character in ["Chaos", "Sol"]
}

filler: Dict[str, ItemClassification] = {
    "Extra Life": ItemClassification.filler
}

traps: Dict[str, ItemClassification] = {
    "Confusion Trap": ItemClassification.trap,
    "Slowness Trap": ItemClassification.trap
}

item_table: Dict[str, ItemClassification] = {
    **progressive_act_items,
    **final_boss_items,
    **emerald_items,
    **filler,
    **traps
}


class SonicRushItem(Item):
    game = "Sonic Rush"
