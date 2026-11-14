from .. import ItemData, BPItemData, PCItemData, RPItemData
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

research_points: dict[str, RPItemData] = {
    f"{i*100} Research Credits": RPItemData(5000+i, always_filler, i)
    for i in range(1, 101)
}

platforms: dict[str, PCItemData] = {
    f"{i} Platform Capacity": PCItemData(6000+i, always_filler, i*2)
    for i in range(1, 501)
}

blueprint_points: dict[str, BPItemData] = {
    f"{i*100} Blueprint Credits": BPItemData(7000+i, always_filler, i*100)
    for i in range(1, 101)
}
