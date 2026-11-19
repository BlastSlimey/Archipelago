from .. import ItemData, PointsItemData
from ..classification import *

task_lines: dict[str, ItemData] = {
    f"Job line #{i}": ItemData(3000+i, always_progression_deprioritized, f"RemoteJobLine{i}", (), (), (f"JobLine{i}", ))
    for i in range(1, 201)
}

operator_lines: dict[str, ItemData] = {
    f"Operator line #{i}": ItemData(4000+i, always_progression_deprioritized, f"RemoteOperatorLine{i}", (), (),
                                    (f"OperatorLine{i}", ))
    for i in range(1, 101)
}

research_points: dict[str, PointsItemData] = {
    f"{i*100} Research Credits": PointsItemData(5000+i, always_filler, i, 0, 0)
    for i in range(1, 101)
}

platforms: dict[str, PointsItemData] = {
    f"{i} Platform Capacity": PointsItemData(6000+i, always_filler, 0, i*2, 0)
    for i in range(1, 501)
}

blueprint_points: dict[str, PointsItemData] = {
    f"{i*100} Blueprint Credits": PointsItemData(7000+i, always_filler, 0, 0, i*100)
    for i in range(1, 101)
}
