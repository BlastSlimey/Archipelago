from typing import Any, TYPE_CHECKING

from BaseClasses import Item, ItemClassification as ItCl
from ...output import Shapez2ScenarioContainer

if TYPE_CHECKING:
    from ... import Shapez2World


classification_names = {
    ItCl.progression: "Progression",
    ItCl.useful: "Useful",
    ItCl.filler: "Filler",
    ItCl.trap: "Trap",
}


def add_other_item(mechanic_defs: list[dict[str, str]], rewards: list[dict[str, Any]], item: Item,
                   other_players_items: set[str], world: "Shapez2World") -> None:
    web = world.multiworld.worlds[item.player].web
    option = world.options.show_other_players_items.current_key
    if option == "no":
        rewards.append({"$type": "MechanicReward", "MechanicId": "RUAPItem"})
    else:
        name = item.name
        mech_id = f"RU{item.player}_{name}"
        if mech_id not in other_players_items:
            display_name = name
            if "player" in option:
                display_name = world.multiworld.player_name[item.player] + "'s " + display_name
            if web is not None and web.item_descriptions is not None and name in web.item_descriptions:
                description = web.item_descriptions[name]
            else:
                description = "An item that belongs to another player."
            if "classification" in option:
                class_name = classification_names[item.classification & (ItCl.progression | ItCl.useful |
                                                                         ItCl.filler | ItCl.trap)]
                description = f"({class_name}) " + description
            mechanic_defs.append({
                "Id": mech_id,
                "Title": display_name,
                "Description": description,
                "IconId": "PlayerLevel"
            })
            other_players_items.add(mech_id)
        rewards.append({"$type": "MechanicReward", "MechanicId": mech_id})


def get_mechanic_definitions(container: "Shapez2ScenarioContainer") -> list[dict[str, str]]:
    return [
        *({
            "Id": f"TaskLine{x+1}",
            "Title": f"Task line #{x+1}",
            "Description": "Unlocks a certain task line.",
            "IconId": "PlayerLevel"
        } for x in range(len(container.world.task_shapes))),
        *({
            "Id": f"OperatorLine{x+1}",
            "Title": f"Operator line #{x+1}",
            "Description": "Unlocks a certain operator line.",
            "IconId": "PlayerLevel"
        } for x in range(len(container.world.operator_shapes))),
        {
            "Id": "RUAPItem",
            "Title": "AP Item",
            "Description": "An item that belongs to another player.",
            "IconId": "PlayerLevel"
        },
        {
            "Id": "RUSandbox",
            "Title": "@research.RUSandbox.title",
            "Description": "@research.RUSandbox.description",
            "IconId": "SandboxCategory"
        },
        {
            "Id": "RUSideUpgrades",
            "Title": "@research.RUSideUpgrades.title",
            "Description": "@research.RUSideUpgrades.description",
            "IconId": "SideUpgrades"
        },
        {
            "Id": "RULayer2",
            "Title": "@research.RULayer2.title",
            "Description": "@research.RULayer2.description",
            "IconId": "GenericLayerUnlock"
        },
        {
            "Id": "RULayer3",
            "Title": "@research.RULayer3.title",
            "Description": "@research.RULayer3.description",
            "IconId": "GenericLayerUnlock"
        },
        {
            "Id": "RUBlueprints",
            "Title": "@research.RUBlueprints.title",
            "Description": "@research.RUBlueprints.description",
            "IconId": "Blueprints"
        },
        {
            "Id": "RUIslandPlacement",
            "Title": "@research.RUIslandPlacement.title",
            "Description": "@research.RUIslandPlacement.description",
            "IconId": "IslandPlacement"
        },
        {
            "Id": "RUTrains",
            "Title": "@research.RUTrains.title",
            "Description": "@research.RUTrains.description",
            "IconId": "TrainsCategory"
        },
        {
            "Id": "RUFluids",
            "Title": "@research.RUFluids.title",
            "Description": "@research.RUFluids.description",
            "IconId": "Fluids"
        },
        # {
        #     "Id": "RUWires",
        #     "Title": "@research.RUWires.title",
        #     "Description": "@research.RUWires.description",
        #     "IconId": "Wires"
        # },
        {
            "Id": "RUPlayerLevel",
            "Title": "@research.RUPlayerLevel.title",
            "Description": "@research.RUPlayerLevel.description",
            "IconId": "PlayerLevel"
        },
        {
            "Id": "RUTrainHubDelivery",
            "Title": "@research.RUTrainHubDelivery.title",
            "Description": "@research.RUTrainHubDelivery.description",
            "IconId": "Trains"
        },
        {
            "Id": "RUInfiniteGoals",
            "Title": "@research.RUInfiniteGoals.title",
            "Description": "@research.RUInfiniteGoals.description",
            "IconId":"InfiniteGoals"
        },
        {
            "Id": "RUIslandLayer2",
            "Title": "@research.RUIslandLayer2.title",
            "Description": "@research.RUIslandLayer2.description",
            "IconId": "GenericLayerUnlock"
        },
        {
            "Id": "RUIslandLayer3",
            "Title": "@research.RUIslandLayer3.title",
            "Description": "@research.RUIslandLayer3.description",
            "IconId": "GenericLayerUnlock"
        },
        {
            "Id": "RUOperatorBadge",
            "Title": "@research.RUOperatorBadge.title",
            "Description": "@research.RUOperatorBadge.description",
            "IconId": "PlayerLevel"
        },
        {
            "Id": "RUTradeStations",
            "Title": "@research.RUTradeStations.title",
            "Description": "@research.RUTradeStations.description",
            "IconId": "ConverterStation"
        },
        {
            "Id": "RUClassicTier1CMY",
            "Title": "@research.RUClassicTier1CMY.title",
            "Description": "@research.RUClassicTier1CMY.description",
            "IconId": "ConverterShape_CMY"
        },
        {
            "Id": "RUClassicTier2WK",
            "Title": "@research.RUClassicTier2WK.title",
            "Description": "@research.RUClassicTier2WK.description",
            "IconId": "ConverterShape_WK"
        },
        {
            "Id": "RUClassicTier3VGA",
            "Title": "@research.RUClassicTier3VGA.title",
            "Description": "@research.RUClassicTier3VGA.description",
            "IconId": "ConverterVortex",
            "HideReward": True
        },
        {
            "Id": "RUPinPushing",
            "Title": "@research.RUPinPushing.title",
            "Description": "@research.RUPinPushing.description",
            "IconId": "building.PinPusherDefaultVariant"
        },
        {
            "Id": "RUColorMixing",
            "Title": "@research.RUColorMixing.title",
            "Description": "@research.RUColorMixing.description",
            "IconId": "building.MixerDefaultVariant"
        },
        {
            "Id": "RUCrystals",
            "Title": "@research.RUCrystals.title",
            "Description": "@research.RUCrystals.description",
            "IconId": "building.CrystalGeneratorDefaultVariant"
        },
        {
            "Id": "RUTier1Ruby",
            "Title": "@research.RUTier1Ruby.title",
            "Description": "@research.RUTier1Ruby.description",
            "IconId": "ConverterShape_tier1"
        },
        {
            "Id": "RUTier2Sapphire",
            "Title": "@research.RUTier2Sapphire.title",
            "Description": "@research.RUTier2Sapphire.description",
            "IconId": "ConverterShape_tier2"
        },
        {
            "Id": "RUTier3Emerald",
            "Title": "@research.RUTier3Emerald.title",
            "Description": "@research.RUTier3Emerald.description",
            "IconId": "ConverterShape_tier3"
        },
        {
            "Id": "RUTier4Gold",
            "Title": "@research.RUTier4Gold.title",
            "Description": "@research.RUTier4Gold.description",
            "IconId": "ConverterShape_tier4"
        },
        {
            "Id": "RUTier5Aquamarine",
            "Title": "@research.RUTier5Aquamarine.title",
            "Description": "@research.RUTier5Aquamarine.description",
            "IconId": "ConverterShape_tier5"
        },
        {
            "Id": "RUTier6Amethyst",
            "Title": "@research.RUTier6Amethyst.title",
            "Description": "@research.RUTier6Amethyst.description",
            "IconId": "ConverterShape_tier6"
        },
        {
            "Id": "RUTier7Diamonds",
            "Title": "@research.RUTier7Diamonds.title",
            "Description": "@research.RUTier7Diamonds.description",
            "IconId": "ConverterShape_tier7"
        },
        {
            "Id": "RUTier8Painite",
            "Title": "@research.RUTier8Painite.title",
            "Description": "@research.RUTier8Painite.description",
            "IconId": "ConverterShape_tier8"
        },
        {
            "Id": "RUTier9VortexTrader",
            "Title": "@research.RUTier9VortexTrader.title",
            "Description": "@research.RUTier9VortexTrader.description",
            "IconId": "ConverterShape_tier9"
        }
    ]
