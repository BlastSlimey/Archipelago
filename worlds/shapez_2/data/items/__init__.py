
from typing import ChainMap
from . import buildings, island_buildings, mechanics, misc
from .. import ItemData, PointsItemData

# ID domains:
# buildings < 1000
# island buildings 1xxx
# mechanics 2xxx
# task lines 3xxx
# operator lines 4xxx
# research points 5xxx
# platforms 6xxx


all_points_items = ChainMap[str, PointsItemData](
    misc.research_points,
    misc.platforms,
    misc.blueprint_points,
)

all_line_items = ChainMap[str, ItemData](
    misc.task_lines,
    misc.operator_lines,
)

all_standard_items = ChainMap[str, ItemData](
    buildings.always,
    buildings.starting,
    buildings.simple_processors,
    buildings.sandbox,
    buildings.pump_pipe,
    island_buildings.always,
    island_buildings.starting,
    island_buildings.miners,
    mechanics.always,
    mechanics.starting,
    mechanics.special,
)

all_remote_items = ChainMap[str, ItemData](
    all_standard_items,
    all_line_items,
)

all_items = ChainMap[str, ItemData | PointsItemData](
    all_remote_items,
    all_points_items,
)
