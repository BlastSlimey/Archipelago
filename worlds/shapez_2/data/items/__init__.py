from typing import ChainMap, TYPE_CHECKING
from .. import ItemData, PointsItemData
from . import buildings, island_buildings, mechanics, misc

# ID domains:
# buildings < 1000
# island buildings 1xxx
# mechanics 2xxx
# task lines 3xxx
# operator lines 4xxx
# research points 5xxx
# platforms 6xxx


all_items = ChainMap[str, ItemData | PointsItemData](
    buildings.always,
    buildings.starting,
    buildings.simple_processors,
    buildings.sandbox,
    island_buildings.always,
    island_buildings.starting,
    mechanics.always,
    mechanics.starting,
    misc.task_lines,
    misc.operator_lines,
    misc.research_points,
    misc.platforms,
    misc.blueprint_points,
)
