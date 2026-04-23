from typing import Any, Iterator

from ...output import Shapez2ScenarioContainer
from ...data.items import RewardType, all_items
from ...data import PointsItemData
from ...data.required_amounts import milestones as shape_amounts


wiki_entry_rewards = ["WKVortexLTD_Handbook", "WKFluids_Intro", "WKTrains_Intro", "WKProcessing_PinPusher",
                      "WKFluids_Mixing", "WKIslands_Floors", "WKFluids_CrystalGenerator", "WKTrains_VortexDelivery",
                      "WKWires_MaM"]

reward_types = {
    RewardType.building: ("BuildingReward", "BuildingDefinitionGroupId"),
    RewardType.island_building: ("IslandGroupReward", "GroupId"),
    RewardType.mechanic: ("MechanicReward", "MechanicId"),
    RewardType.platforms: ("ChunkLimitReward", "Amount"),
    RewardType.blueprint_points: ("BlueprintCurrencyReward", "Amount"),
    RewardType.research_points: ("ResearchPointsReward", "Amount"),
}

milestone_graphics = [("MilestoneClassicInitialVD", "building.BeltDefaultVariant"),
                      ("MilestoneClassicPainterVD", "building.PainterDefaultVariant"),
                      ("MilestoneClassicTrainsVD", "Trains"),
                      ("MilestoneClassicPinPusherVD", "building.PinPusherDefaultVariant"),
                      ("MilestoneClassicMixerVD", "building.MixerDefaultVariant"),
                      ("MilestoneClassicSpaceLayer3VD", "GenericLayerUnlock"),
                      ("MilestoneClassicCrystalsVD", "building.CrystalGeneratorDefaultVariant"),
                      ("MilestoneClassicVortexDeliveryVD", "Trains"),
                      ("MilestoneClassicFinalVD", "ConverterVortex")]


def get_milestones(container: "Shapez2ScenarioContainer", mechanics: list[dict[str, str]],
                   other_players_items: set[str]) -> list[dict[str, Any]]:
    from .mechanics import add_other_item

    multiplier = container.world.options.location_adjustments["Required shapes multiplier"]
    research_points = container.world.options.location_adjustments["Starting research points"]
    blueprint_points = container.world.options.location_adjustments["Starting blueprint points"]
    show_other = container.world.options.show_other_players_items.current_key

    def get_rewards(_item: str) -> Iterator[dict[str, str | int]]:
        if _item[0] != "[":  # event item
            _data = all_items[_item]
            _type, _key = reward_types[_data.reward_type]
            if isinstance(_data, PointsItemData):
                yield {"$type": _type, "Amount": _data.amount}
            else:
                for _rew in _data.reward_ids:
                    yield {"$type": _type, _key: _rew}

    video, icon = container.world.random.choice(milestone_graphics)
    rewards = [
        {"$type": "ChunkLimitReward",
         "Amount": container.world.options.location_adjustments["Starting platform points"]},
        *(reward for item in container.world.starting_items for reward in get_rewards(item)),
    ]
    if research_points:
        rewards.append({"$type": "ResearchPointsReward", "Amount": research_points})
    if blueprint_points:
        rewards.append({"$type": "BlueprintCurrencyReward", "Amount": blueprint_points})
    out = [{
        "Definition": {
            "Id": "Milestone_Initial",
            "VideoId": video,
            "PreviewImageId": "Placeholder",
            "Title": "Starting inventory",
            "Description": "Everything that's unlocked right from the beginning, including the player-defined "
                           "starting inventory.",
            "WikiEntryId": "WKVortexLTD_Handbook",
            "IconId": icon,
        },
        "Lines": {"Lines": []},
        "Rewards": {"Rewards": rewards}
    }]

    for milestone_num in range(container.world.options.location_adjustments["Milestones"]):
        video, icon = container.world.random.choice(milestone_graphics)
        checks_count = container.world.milestone_checks_counts[milestone_num]
        shapes_1, shapes_2 = container.world.milestone_shapes[milestone_num]
        amounts = shape_amounts[milestone_num]

        rewards = []
        for check_num in range(checks_count):
            loc_item = container.world.get_location(f"Milestone {milestone_num + 1} reward #{check_num + 1}").item
            if loc_item.player != container.world.player:
                if show_other == "no_names":
                    rewards.append({"$type": "MechanicReward", "MechanicId": "RUAPItem"})
                else:
                    add_other_item(mechanics, rewards, loc_item, other_players_items, container.world)
            else:
                rewards.extend(get_rewards(loc_item.name))

        out.append({
            "Definition": {
                "Id": f"LocMilestone_{milestone_num + 1}",
                "VideoId": video,
                "PreviewImageId": "Placeholder",
                "Title": f"Milestone #{milestone_num + 1}",
                "Description": f"Another Milestone containing {checks_count} items",
                "WikiEntryId": container.world.random.choice(wiki_entry_rewards),
                "IconId": icon,
            },
            "Lines": {"Lines": [
                {"ReusedForPlayerLevel": milestone_num in container.world.operator_shapes,
                 "Shapes": [{"Shape": shapes_1[i], "Amount": max(1, amounts[i] * multiplier // 100)}
                            for i in range(len(shapes_1))]},
                {"Shapes": [{"Shape": shapes_2[i], "Amount": max(1, amounts[i] * multiplier // 100)}
                            for i in range(len(shapes_2))]},
            ]},
            "Rewards": {"Rewards": rewards}
        })

    return out
