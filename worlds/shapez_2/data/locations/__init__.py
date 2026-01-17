from typing import ChainMap, TYPE_CHECKING
from .. import ItemData, PointsItemData, LocationData
from . import milestones, tasks, operator_levels

# ID domains:
# milestones < 10000
# tasks 1xxxx
# operator levels 2xxxx

all_locations = ChainMap[str, LocationData](
    milestones.locations,
    tasks.locations,
    operator_levels.locations,
)
