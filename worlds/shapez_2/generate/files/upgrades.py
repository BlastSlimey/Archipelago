from typing import Any

from ...output import Shapez2ScenarioContainer
from ...data.items import all_remote_items
from .rewards import get_rewards


def get_remote_upgrades(container: "Shapez2ScenarioContainer") -> list[dict[str, Any]]:

    surprise = container.world.random.choice(container.world.main_item_names)
    out = [{
        "Id": "CBWires_Core",
        "PreviewImageId": "CBWires_Core",
        "VideoId": "PlaceholderVideoVD",
        "Title": "Wires (Category)",
        "IconId": "SignalTransportGroup",
        "Description": "@research.CBWires_Core.description",
        "Hidden": True,
        "Category": "Wires",
        "RequiredUpgradeIds": [],
        "RequiredMechanicIds": [],
        "Rewards": [{"$type": "MechanicReward", "MechanicId": "RUWires"}],
        "Costs": [{"$type": "ResearchPointsCost", "Amount": 1}]
    }]

    surprise_count = container.world.options.surprise_out_of_logic_item["Amount"]
    surprise_cost = container.world.options.surprise_out_of_logic_item["Cost per item"]
    for i in range(surprise_count):
        out.append({
            "Id": f"RNSurprise{i+1}",
            "PreviewImageId": "CBBelts_Core",
            "VideoId": "PlaceholderVideoVD",
            "Title": "Surprise out-of-logic item" + ("" if surprise_count == 1 else f" #{i+1}"),
            "IconId": "building.SandboxItemProducerDefaultVariant",
            "Description": "Rewards you with a random building, space platform, or mechanic "
                           "without being taken into account by logic.",
            "Category": "Other",
            "RequiredUpgradeIds": [],
            "RequiredMechanicIds": [],
            "Rewards": list(get_rewards(surprise)),
            "Costs": [{"$type": "ResearchPointsCost", "Amount": surprise_cost // 100}]
        })

    for name, data in all_remote_items.items():
        out.append({
            "Id": data.remote_id,
            "PreviewImageId": "",
            "VideoId": "PlaceholderVideoVD",
            "Title": name,
            "IconId": data.icon,
            "Description": "",
            "Hidden": True,
            "Category": "Other",
            "RequiredUpgradeIds": [],
            "RequiredMechanicIds": [],
            "Rewards": list(get_rewards(name)),
            "Costs": []
        })

    return out


linear_upgrades: list[dict[str, Any]] = [
    {
        "Id": "LRUDummy_Zero",
        "Title": "@research.LRUDummy.title",
        "DisplayType":3,
        "Levels":[
            {}
        ],
        "Attribute": "@research.LRUDummy.attribute",
        "Description": "@research.LRUDummy.description",
        "RequiredUpgradeIds":[],
        "RequiredMechanicIds":[],
        "Category": "Hidden"
    },
    {
        "Id": "LRUGlobalSpeed",
        "Title": "@research.LRUGlobalSpeed.title",
        "DisplayType":2,
        "Levels":[
            {"Value":100},
            {"Value":125, "Cost":{"$type": "ResearchPointsCost", "Amount":50}},
            {"Value":150, "Cost":{"$type": "ResearchPointsCost", "Amount":100}}
        ],
        "Attribute": "@research.LRUGlobalSpeed.attribute",
        "Description": "@research.LRUGlobalSpeed.description",
        "RequiredUpgradeIds":[],
        "RequiredMechanicIds":[],
        "Category": "Upgrades"
    },
    {
        "Id": "LRUHubInputSize",
        "Title": "@research.LRUHubInputSize.title",
        "DisplayType":3,
        "Levels":[
            {"Value":4},
            {"Value":6,"Cost":{"$type": "ResearchPointsCost","Amount":7}},
            {"Value":8,"Cost":{"$type": "ResearchPointsCost","Amount":10}},
            {"Value":10,"Cost":{"$type": "ResearchPointsCost","Amount":15}},
            {"Value":12,"Cost":{"$type": "ResearchPointsCost","Amount":40}}
        ],
        "Attribute": "@research.LRUHubInputSize.attribute",
        "Description": "@research.LRUHubInputSize.description",
        "RequiredUpgradeIds":[],
        "RequiredMechanicIds":[],
        "Category": "Upgrades"
    },
    {
        "Id": "LRUChunkLimitAdd",
        "Title": "@research.LRUChunkLimitAdd.title",
        "DisplayType":5,
        "Levels":[
            {},
            {"Value":2000,"Cost":{"$type": "ResearchPointsCost","Amount":1}},
            {"Value":3000,"Cost":{"$type": "ResearchPointsCost","Amount":4}},
            {"Value":5000,"Cost":{"$type": "ResearchPointsCost","Amount":8}},
            {"Value":8000,"Cost":{"$type": "ResearchPointsCost","Amount":20}},
            {"Value":16000,"Cost":{"$type": "ResearchPointsCost","Amount":50}},
            {"Value":32000,"Cost":{"$type": "ResearchPointsCost","Amount":100}},
            {"Value":100000,"Cost":{"$type": "ResearchPointsCost","Amount":500}},
            {"Value":200000,"Cost":{"$type": "ResearchPointsCost","Amount":1200}},
            {"Value":500000,"Cost":{"$type": "ResearchPointsCost","Amount":2500}}
        ],
        "Attribute": "@research.LRUChunkLimitAdd.attribute",
        "Description": "@research.LRUChunkLimitAdd.description",
        "RequiredUpgradeIds":[],
        "RequiredMechanicIds":[],
        "Category": "Upgrades"
    },
    {
        "Id": "LRUTrainSpeed",
        "Title": "@research.LRUTrainSpeed.title",
        "DisplayType":2,
        "Levels":[
            {"Value":100},
            {"Value":140,"Cost":{"$type": "ResearchPointsCost","Amount":8}},
            {"Value":180,"Cost":{"$type": "ResearchPointsCost","Amount":12}},
            {"Value":200,"Cost":{"$type": "ResearchPointsCost","Amount":30}}
        ],
        "Attribute": "@research.LRUTrainSpeed.attribute",
        "Description": "@research.LRUTrainSpeed.description",
        "RequiredUpgradeIds":[],
        "RequiredMechanicIds":[],
        "Category": "Upgrades"
    },
    {
        "Id": "LRUTrainCapacity",
        "Title": "@research.LRUTrainCapacity.title",
        "DisplayType":4,
        "Levels":[
            {"Value":100},
            {"Value":200,"Cost":{"$type": "ResearchPointsCost","Amount":8}},
            {"Value":300,"Cost":{"$type": "ResearchPointsCost","Amount":12}},
            {"Value":400,"Cost":{"$type": "ResearchPointsCost","Amount":18}},
            {"Value":500,"Cost":{"$type": "ResearchPointsCost","Amount":30}},
            {"Value":600,"Cost":{"$type": "ResearchPointsCost","Amount":50}}
        ],
        "Attribute": "@research.LRUTrainCapacity.attribute",
        "Description": "@research.LRUTrainCapacity.description",
        "RequiredUpgradeIds":[],
        "RequiredMechanicIds":[],
        "Category": "Upgrades"
    },
    {
        "Id": "LRUShapeQuantity",
        "Title": "@research.LRUShapeQuantity.title",
        "DisplayType":3,
        "Levels":[
            {"Value":1},
            {"Value":2,"Cost":{"$type": "ResearchPointsCost","Amount":350}},
            {"Value":3,"Cost":{"$type": "ResearchPointsCost","Amount":750}},
            {"Value":4,"Cost":{"$type": "ResearchPointsCost","Amount":1250}},
            {"Value":5,"Cost":{"$type": "ResearchPointsCost","Amount":1750}},
            {"Value":6,"Cost":{"$type": "ResearchPointsCost","Amount":3500}},
            {"Value":7,"Cost":{"$type": "ResearchPointsCost","Amount":4000}},
            {"Value":8,"Cost":{"$type": "ResearchPointsCost","Amount":4500}},
            {"Value":9,"Cost":{"$type": "ResearchPointsCost","Amount":5000}},
            {"Value":10,"Cost":{"$type": "ResearchPointsCost","Amount":5500}},
            {"Value":11,"Cost":{"$type": "ResearchPointsCost","Amount":6000}},
            {"Value":12,"Cost":{"$type": "ResearchPointsCost","Amount":9999}}
        ],
        "Attribute": "@research.LRUShapeQuantity.attribute",
        "Description": "@research.LRUShapeQuantity.description",
        "RequiredUpgradeIds":[],
        "RequiredMechanicIds":[],
        "Category": "Upgrades"
    }
]
