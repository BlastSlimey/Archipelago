from typing import ChainMap, TYPE_CHECKING
from .. import ItemData, PointsItemData

# ID domains:
# buildings < 1000
# island buildings 1xxx
# mechanics 2xxx
# task lines 3xxx
# operator lines 4xxx
# research points 5xxx
# platforms 6xxx


all_locations = ChainMap[str, ItemData | PointsItemData](
    
)
