from typing import Any

from ...output import Shapez2ScenarioContainer
from ...data import ItemData
from ...data.items import buildings, island_buildings, mechanics, misc, all_standard_items
from .rewards import get_rewards

milestone_ids: tuple[str, ...] = ("Milestone_FluidPainting", "Milestone_ShapeTrains",
                                  "Milestone_PinPusher", "Milestone_ColorMixing", "Milestone_SpaceFloor3",
                                  "Milestone_Crystals", "Milestone_VortexDelivery", "Milestone_FinalConverters",
                                  "Milestone_PostFinal_Tier0", "Milestone_PostFinal_Tier1", "Milestone_PostFinal_Tier2",
                                  "Milestone_PostFinal_Tier3")


def get_remote_upgrades(container: "Shapez2ScenarioContainer") -> list[dict[str, Any]]:

    allowed_surprises = [
        buildings.always, buildings.simple_processors, buildings.pump_pipe,
        island_buildings.always, island_buildings.miners,
    ]
    if container.world.options.lock_locations.is_job_lines:
        allowed_surprises.append({f"Job line #{i}": None for i in
                                  range(3, container.world.options.jobs_adjustments["Job lines"] + 1)})
    if container.world.options.lock_locations.is_operator_lines:
        allowed_surprises.append({f"Operator line #{i}": None for i in
                                  range(1, container.world.options.operator_levels_adjustments["Operator lines"] + 1)})
    if container.world.options.lock_locations.is_operator_levels_tab:
        allowed_surprises.append(mechanics.always | mechanics.special)
    else:
        allowed_surprises.append(mechanics.always)
    table = container.world.random.choice(allowed_surprises)
    surprise = container.world.random.choice(list(table.keys()))
    out = [{
        "Id": "RNSurprise",
        "PreviewImageId": "CBBelts_Core",
        "VideoId": "PlaceholderVideoVD",
        "Title": "Surprise out-of-logic item",
        "IconId": "building.SandboxItemProducerDefaultVariant",
        "Description": "Rewards you with a random building, island platform, or mechanic "
                       "without being taken into account by logic.",
        "Category": "Other",
        "RequiredUpgradeIds": [],
        "RequiredMechanicIds": [],
        "Rewards": list(get_rewards(surprise)),
        "Costs": [{"$type": "ResearchPointsCost", "Amount": 100}]
    }, {
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

    # for vanilla in milestone_ids:
    #     out.append({
    #         "Id": vanilla,
    #         "PreviewImageId": "",
    #         "VideoId": "PlaceholderVideoVD",
    #         "Title": vanilla,
    #         "IconId": "building.SandboxItemProducerDefaultVariant",
    #         "Description": "",
    #         "Hidden": True,
    #         "Category": "Other",
    #         "RequiredUpgradeIds": [],
    #         "RequiredMechanicIds": [],
    #         "Rewards": [],
    #         "Costs": []
    #     })

    for name, data in all_standard_items.items():
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
        "Id":"LRUDummy_Zero",
        "Title":"@research.LRUDummy.title",
        "DisplayType":3,
        "Levels":[
            {}
        ],
        "Attribute":"@research.LRUDummy.attribute",
        "Description":"@research.LRUDummy.description",
        "RequiredUpgradeIds":[],
        "RequiredMechanicIds":[],
        "Category":"Hidden"
    },
    {
        "Id":"LRUGlobalSpeed",
        "Title":"@research.LRUGlobalSpeed.title",
        "DisplayType":2,
        "Levels":[
            {"Value":100},
            {"Value":125, "Cost":{"$type":"ResearchPointsCost", "Amount":50}},
            {"Value":150, "Cost":{"$type":"ResearchPointsCost", "Amount":100}}
        ],
        "Attribute":"@research.LRUGlobalSpeed.attribute",
        "Description":"@research.LRUGlobalSpeed.description",
        "RequiredUpgradeIds":[],
        "RequiredMechanicIds":[],
        "Category":"Upgrades"
    },
    {
        "Id":"LRUHubInputSize",
        "Title":"@research.LRUHubInputSize.title",
        "DisplayType":3,
        "Levels":[
            {"Value":4},
            {"Value":6,"Cost":{"$type":"ResearchPointsCost","Amount":7}},
            {"Value":8,"Cost":{"$type":"ResearchPointsCost","Amount":10}},
            {"Value":10,"Cost":{"$type":"ResearchPointsCost","Amount":15}},
            {"Value":12,"Cost":{"$type":"ResearchPointsCost","Amount":40}}
        ],
        "Attribute":"@research.LRUHubInputSize.attribute",
        "Description":"@research.LRUHubInputSize.description",
        "RequiredUpgradeIds":[],
        "RequiredMechanicIds":[],
        "Category":"Upgrades"
    },
    {
        "Id":"LRUChunkLimitAdd",
        "Title":"@research.LRUChunkLimitAdd.title",
        "DisplayType":5,
        "Levels":[
            {},
            {"Value":2000,"Cost":{"$type":"ResearchPointsCost","Amount":1}},
            {"Value":3000,"Cost":{"$type":"ResearchPointsCost","Amount":4}},
            {"Value":5000,"Cost":{"$type":"ResearchPointsCost","Amount":8}},
            {"Value":8000,"Cost":{"$type":"ResearchPointsCost","Amount":20}},
            {"Value":16000,"Cost":{"$type":"ResearchPointsCost","Amount":50}},
            {"Value":32000,"Cost":{"$type":"ResearchPointsCost","Amount":100}},
            {"Value":100000,"Cost":{"$type":"ResearchPointsCost","Amount":500}},
            {"Value":200000,"Cost":{"$type":"ResearchPointsCost","Amount":1200}},
            {"Value":500000,"Cost":{"$type":"ResearchPointsCost","Amount":2500}}
        ],
        "Attribute":"@research.LRUChunkLimitAdd.attribute",
        "Description":"@research.LRUChunkLimitAdd.description",
        "RequiredUpgradeIds":[],
        "RequiredMechanicIds":[],
        "Category":"Upgrades"
    },
    {
        "Id":"LRUTrainSpeed",
        "Title":"@research.LRUTrainSpeed.title",
        "DisplayType":2,
        "Levels":[
            {"Value":100},
            {"Value":140,"Cost":{"$type":"ResearchPointsCost","Amount":8}},
            {"Value":180,"Cost":{"$type":"ResearchPointsCost","Amount":12}},
            {"Value":200,"Cost":{"$type":"ResearchPointsCost","Amount":30}}
        ],
        "Attribute":"@research.LRUTrainSpeed.attribute",
        "Description":"@research.LRUTrainSpeed.description",
        "RequiredUpgradeIds":[],
        "RequiredMechanicIds":[],
        "Category":"Upgrades"
    },
    {
        "Id":"LRUTrainCapacity",
        "Title":"@research.LRUTrainCapacity.title",
        "DisplayType":4,
        "Levels":[
            {"Value":100},
            {"Value":200,"Cost":{"$type":"ResearchPointsCost","Amount":8}},
            {"Value":300,"Cost":{"$type":"ResearchPointsCost","Amount":12}},
            {"Value":400,"Cost":{"$type":"ResearchPointsCost","Amount":18}},
            {"Value":500,"Cost":{"$type":"ResearchPointsCost","Amount":30}},
            {"Value":600,"Cost":{"$type":"ResearchPointsCost","Amount":50}}
        ],
        "Attribute":"@research.LRUTrainCapacity.attribute",
        "Description":"@research.LRUTrainCapacity.description",
        "RequiredUpgradeIds":[],
        "RequiredMechanicIds":[],
        "Category":"Upgrades"
    },
    {
        "Id":"LRUShapeQuantity",
        "Title":"@research.LRUShapeQuantity.title",
        "DisplayType":3,
        "Levels":[
            {"Value":1},
            {"Value":2,"Cost":{"$type":"ResearchPointsCost","Amount":350}},
            {"Value":3,"Cost":{"$type":"ResearchPointsCost","Amount":750}},
            {"Value":4,"Cost":{"$type":"ResearchPointsCost","Amount":1250}},
            {"Value":5,"Cost":{"$type":"ResearchPointsCost","Amount":1750}},
            {"Value":6,"Cost":{"$type":"ResearchPointsCost","Amount":3500}},
            {"Value":7,"Cost":{"$type":"ResearchPointsCost","Amount":4000}},
            {"Value":8,"Cost":{"$type":"ResearchPointsCost","Amount":4500}},
            {"Value":9,"Cost":{"$type":"ResearchPointsCost","Amount":5000}},
            {"Value":10,"Cost":{"$type":"ResearchPointsCost","Amount":5500}},
            {"Value":11,"Cost":{"$type":"ResearchPointsCost","Amount":6000}},
            {"Value":12,"Cost":{"$type":"ResearchPointsCost","Amount":9999}}
        ],
        "Attribute":"@research.LRUShapeQuantity.attribute",
        "Description":"@research.LRUShapeQuantity.description",
        "RequiredUpgradeIds":[],
        "RequiredMechanicIds":[],
        "Category":"Upgrades"
    }
]
