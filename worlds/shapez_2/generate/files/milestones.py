from typing import Any, Iterator

from .rewards import get_rewards
from ...data.items import all_items
from ...output import Shapez2ScenarioContainer
from ...data.required_amounts import milestones as shape_amounts


wiki_entry_rewards = ["WKVortexLTD_Handbook", "WKFluids_Intro", "WKTrains_Intro", "WKProcessing_PinPusher",
                      "WKFluids_Mixing", "WKIslands_Floors", "WKFluids_CrystalGenerator", "WKTrains_VortexDelivery",
                      "WKWires_MaM"]

milestone_graphics = [("MilestoneClassicInitialVD", "building.BeltDefaultVariant"),
                      ("MilestoneClassicPainterVD", "building.PainterDefaultVariant"),
                      ("MilestoneClassicTrainsVD", "Trains"),
                      ("MilestoneClassicPinPusherVD", "building.PinPusherDefaultVariant"),
                      ("MilestoneClassicMixerVD", "building.MixerDefaultVariant"),
                      ("MilestoneClassicSpaceLayer3VD", "GenericLayerUnlock"),
                      ("MilestoneClassicCrystalsVD", "building.CrystalGeneratorDefaultVariant"),
                      ("MilestoneClassicVortexDeliveryVD", "Trains"),
                      ("MilestoneClassicFinalVD", "ConverterVortex")]


def rotate(shape: str) -> Iterator[str]:
    yield shape
    parts = shape.split(":")
    for i in range(2, len(parts[0]), 2):
        yield ":".join(layer[i:] + layer[:i] for layer in parts)


def get_milestones(container: "Shapez2ScenarioContainer", mechanics: list[dict[str, str]],
                   other_players_items: set[str]) -> list[dict[str, Any]]:
    from .mechanics import add_other_item

    multiplier = container.world.options.required_shapes_multiplier.value
    research_points = container.world.options.starting_points["Research credits"] // 100
    blueprint_points = container.world.options.starting_points["Blueprint credits"]

    video, icon = container.world.random.choice(milestone_graphics)
    rewards = [
        {"$type": "ChunkLimitReward", "Amount": container.world.options.starting_points["Platform capacity"] * 2},
        {"$type": 'ContentBundleReward', 'ContentBundleId': "CBWires_Core"},
        *(reward for item in container.world.starting_items if item in all_items for reward in get_rewards(item)),
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

    for milestone_num in range(container.world.options.milestone_adjustments["Milestones"]):
        video, icon = container.world.random.choice(milestone_graphics)
        checks_count = container.world.milestone_checks_counts[milestone_num]
        raw_shapes_1, raw_shapes_2 = container.world.milestone_shapes[milestone_num]
        amounts = shape_amounts[milestone_num]

        shapes_1, shapes_2 = [], []
        unique = set()  # Only lookup!
        for s in raw_shapes_1:
            if s not in unique:
                shapes_1.append(s)
                for rot in rotate(s):
                    unique.add(rot)
        for s in raw_shapes_2:
            if s not in unique:
                shapes_2.append(s)
                unique.add(s)
                for rot in rotate(s):
                    unique.add(rot)

        rewards = []
        for check_num in range(checks_count):
            loc_item = container.world.get_location(f"Milestone {milestone_num + 1} reward #{check_num + 1}").item
            if loc_item.player != container.world.player:
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
