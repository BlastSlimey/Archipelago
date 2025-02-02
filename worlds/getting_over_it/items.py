from typing import Dict

from BaseClasses import ItemClassification, Item

items_list: Dict[str, ItemClassification] = {
    "Gravity Reduction": ItemClassification.progression,
    "Wind Trap": ItemClassification.trap,
    "Goal Height Reduction": ItemClassification.progression,
    "Frustration": ItemClassification.filler,
}


class GOIItem(Item):
    game = "Getting Over It"
