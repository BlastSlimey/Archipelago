from .. import ItemData
from ..classification import *

always: dict[str, ItemData] = {
    "2nd Floor": ItemData(2000, always_progression, "Remote2ndFloor", ("RULayer2", ), 2),
    # Only used for wiki entry
    # "Upgrades": ItemData(000, always_, "RemoteUpgrades", ("RUSideUpgrades", ), 2),
    "Blueprints": ItemData(2001, always_useful, "RemoteBlueprints", ("RUBlueprints", ), 2),
    # Only used for wiki entry and task/upgrade unlocks
    # "Fluids": ItemData(000, always_progression, "RemoteFluids", ("RUFluids", ), 2),
    "Operator Levels": ItemData(2002, always_progression, "RemoteOperatorLevels", ("RUPlayerLevel", ), 2),
    # Only used for wiki entry and task/upgrade unlocks
    # "Trains": ItemData(000, always_progression, "RemoteTrains", ("RUTrains", ), 2),
    "3rd Platform Floor": ItemData(2003, always_useful, "Remote3rdPlatformFloor", ("RUIslandLayer3", ), 2),
    # Entirely for display purposes
    # "Infinite Goals": ItemData(000, always_progression, "RemoteInfiniteGoals", ("RUInfiniteGoals", ), 2),
    "3rd Floor": ItemData(2004, always_useful, "Remote3rdFloor", ("RULayer3", ), 2),
    # Only used for wiki entry
    # "Wires (Category)": ItemData(000, always_progression, "RemoteWiresCategory", ("RUWires", ), 2),
    "Train Delivery": ItemData(2005, always_progression, "RemoteTrainDelivery", ("RUTrainHubDelivery", ), 2),
}

starting: dict[str, ItemData] = {
    "Space Platforms": ItemData(2100, always_progression, "RemoteSpacePlatforms", ("RUIslandPlacement", ), 2),
    "2nd Platform Floor": ItemData(2101, always_useful, "Remote2ndPlatformFloor", ("RUIslandLayer2", ), 2),
}
