from typing import Any

from ...output import Shapez2ScenarioContainer
from ...generate.shapes import Processor
from .rewards import get_rewards


line_data_by_processors = {
    0: (50000, 30),
    1: (15000, 22),
    2: (15000, 18),
    3: (15000, 18),
    4: (12000, 17),
    5: (10000, 16),
    6: (8000, 16),
    7: (8000, 15),
    8: (8000, 15),
}


def get_operator_lines(container: "Shapez2ScenarioContainer") -> list[dict[str, Any]]:

    multiplier = container.world.options.required_shapes_multiplier.value
    locked = container.world.options.lock_locations.is_operator_lines

    out = []
    for line in range(container.world.options.operator_levels_adjustments["Operator lines"]):
        processors = container.world.operator_processors[line]
        shape = container.world.operator_shapes[line]
        line_obj = {
            "Id": f"Random{line + 1}",
            "RandomizedExtraShapesPer10Level": [],
            "RequiredUpgradeIds": [],
            "RequiredMechanicIds": [f"OperatorLine{line + 1}"] if locked else [],
        }
        if shape is None:
            has_crystals = Processor.CRYSTALLIZER in processors
            line_obj.update({
                "Randomized": True,
                "RandomizedUseCrystals": has_crystals,
                "StartingAmount": 1000,
                "ExponentialGrowthPercentPerLevel": 4 if has_crystals else 5,
            })
        elif isinstance(shape, int):
            if shape > 0:
                line_obj.update({
                    "Shape": container.world.milestone_shapes[shape][0][-1],
                    "StartingAmount": max(1, line_data_by_processors[len(processors)][0] * multiplier // 100),
                    "ExponentialGrowthPercentPerLevel": line_data_by_processors[len(processors)][1],
                })
            else:
                line_obj.update({
                    "Shape": container.world.task_shapes[-shape][-1],
                    "StartingAmount": max(1, line_data_by_processors[len(processors)][0] * multiplier // 100),
                    "ExponentialGrowthPercentPerLevel": line_data_by_processors[len(processors)][1],
                })
        else:
            line_obj.update({
                "Shape": shape,
                "StartingAmount": max(1, line_data_by_processors[len(processors)][0] * multiplier // 100),
                "ExponentialGrowthPercentPerLevel": line_data_by_processors[len(processors)][1],
            })
        out.append(line_obj)
    return out


def get_operator_rewards(container: "Shapez2ScenarioContainer", mechanics: list[dict[str, str]],
                         other_players_items: set[str]) -> list[dict[str, Any]]:
    from .mechanics import add_other_item

    checks_count = container.world.options.operator_levels_adjustments["Operator level checks"]
    out = [{
        "MinimumLevel": max(25, checks_count + 1),
        "Rewards": [
            {"$type": "ChunkLimitReward", "Amount": 100},
            {"$type": "BlueprintCurrencyReward", "Amount": 20000},
            {"$type": "ResearchPointsReward", "Amount": 10}
        ]
    }]
    if checks_count < 24:
        out.append({
            "MinimumLevel": max(10, checks_count + 1),
            "Rewards": [
                {"$type": "ChunkLimitReward", "Amount": 50},
                {"$type": "BlueprintCurrencyReward", "Amount": 10000},
                {"$type": "ResearchPointsReward", "Amount": 4}
            ]
        })
    if checks_count < 9:
        out.append({
            "MinimumLevel": checks_count + 1,
            "Rewards": [
                {"$type": "ChunkLimitReward", "Amount": 25},
                {"$type": "BlueprintCurrencyReward", "Amount": 5000},
                {"$type": "ResearchPointsReward", "Amount": 2}
            ]
        })
    for check in range(checks_count):
        loc_item = container.world.get_location(f"Operator level {checks_count - check}").item
        if loc_item.player != container.world.player:
            rewards = []
            add_other_item(mechanics, rewards, loc_item, other_players_items, container.world)
        else:
            rewards = [*get_rewards(loc_item.name)]
        out.append({
            "MinimumLevel": checks_count - check,
            "Rewards": rewards
        })
    return out
