from typing import Any

from ...output import Shapez2ScenarioContainer


def get_mechanic_definitions(container: "Shapez2ScenarioContainer") -> list[dict[str, str]]:
    return [
        *({
            "Id": f"RUTaskLine{x+1}",
            "Title": f"Task line #{x+1}",
            "Description": "Unlocks a certain task line.",
            "IconId": "PlayerLevel"
        } for x in range(len(container.world.task_shapes))),
        *({
            "Id": f"RUOperatorLine{x+1}",
            "Title": f"Operator line #{x+1}",
            "Description": "Unlocks a certain operator line.",
            "IconId": "PlayerLevel"
        } for x in range(len(container.world.operator_shapes))),
        {
            "Id":"RUAPItem",
            "Title":"AP Item",
            "Description":"An item that belongs to another player.",
            "IconId":"PlayerLevel"
        },
        {
            "Id":"RUSideUpgrades",
            "Title":"@research.RUSideUpgrades.title",
            "Description":"@research.RUSideUpgrades.description",
            "IconId":"SideUpgrades"
        },
        {
            "Id":"RULayer2",
            "Title":"@research.RULayer2.title",
            "Description":"@research.RULayer2.description",
            "IconId":"GenericLayerUnlock"
        },
        {
            "Id":"RULayer3",
            "Title":"@research.RULayer3.title",
            "Description":"@research.RULayer3.description",
            "IconId":"GenericLayerUnlock"
        },
        {
            "Id":"RUBlueprints",
            "Title":"@research.RUBlueprints.title",
            "Description":"@research.RUBlueprints.description",
            "IconId":"Blueprints"
        },
        {
            "Id":"RUIslandPlacement",
            "Title":"@research.RUIslandPlacement.title",
            "Description":"@research.RUIslandPlacement.description",
            "IconId":"IslandPlacement"
        },
        {
            "Id":"RUTrains",
            "Title":"@research.RUTrains.title",
            "Description":"@research.RUTrains.description",
            "IconId":"Trains"
        },
        {
            "Id":"RUFluids",
            "Title":"@research.RUFluids.title",
            "Description":"@research.RUFluids.description",
            "IconId":"Fluids"
        },
        {
            "Id":"RUWires",
            "Title":"@research.RUWires.title",
            "Description":"@research.RUWires.description",
            "IconId":"Wires"
        },
        {
            "Id":"RUPlayerLevel",
            "Title":"@research.RUPlayerLevel.title",
            "Description":"@research.RUPlayerLevel.description",
            "IconId":"PlayerLevel"
        },
        {
            "Id":"RUTrainHubDelivery",
            "Title":"@research.RUTrainHubDelivery.title",
            "Description":"@research.RUTrainHubDelivery.description",
            "IconId":"Trains"
        },
        {
            "Id":"RUInfiniteGoals",
            "Title":"@research.RUInfiniteGoals.title",
            "Description":"@research.RUInfiniteGoals.description",
            "IconId":"Infinite"
        },
        {
            "Id":"RUIslandLayer2",
            "Title":"@research.RUIslandLayer2.title",
            "Description":"@research.RUIslandLayer2.description",
            "IconId":"GenericLayerUnlock"
        },
        {
            "Id":"RUIslandLayer3",
            "Title":"@research.RUIslandLayer3.title",
            "Description":"@research.RUIslandLayer3.description",
            "IconId":"GenericLayerUnlock"
        }
    ]
