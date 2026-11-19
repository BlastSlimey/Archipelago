from typing import Any

from .rewards import get_bundle
from ...output import Shapez2ScenarioContainer
from ...data.required_amounts import task_lines as shape_amounts


def get_task_lines(container: "Shapez2ScenarioContainer", mechanics: list[dict[str, str]],
                   other_players_items: set[str]) -> list[dict[str, Any]]:
    from .mechanics import add_other_item

    multiplier = container.world.options.required_shapes_multiplier.value
    locked = container.world.options.lock_locations.is_job_lines

    out = []
    for task_line in range(container.world.options.jobs_adjustments["Job lines"]):
        shapes = container.world.task_shapes[task_line]
        amounts = shape_amounts[task_line]
        tasks = []
        for task_num in range(len(shapes)):
            loc_item = container.world.get_location(f"Job #{task_line+1}-{task_num+1}").item
            if loc_item.player != container.world.player:
                rewards = []
                add_other_item(mechanics, rewards, loc_item, other_players_items, container.world)
            else:
                rewards = [*get_bundle(loc_item.name)]
            tasks.append({
                "Id": f"LocJob_{task_line}_{task_num}",
                "Rewards": rewards,
                "Costs": [{
                    "Shape": shapes[task_num],
                    "Amount": max(1, amounts[
                        -1 if task_num == len(shapes) - 1
                        else (0 if task_num == 0 else (task_num - 1) * (len(amounts) - 2) // (len(shapes) - 2) + 1)
                    ] * multiplier // 100)
                }]
            })
        out.append({
            "Title": f"Job Line #{task_line + 1}",
            "RequiredUpgradeIds": [],
            "RequiredMechanicIds": [f"JobLine{task_line + 1}"] if locked else [],
            "SideQuests": tasks,
        })

    return out
