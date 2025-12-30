from .. import ItemData
from ..classification import *

always: dict[str, ItemData] = {
    "2nd Floor": ItemData(2000, always_progression, "Remote2ndFloor", ("RULayer2", )),
    # Only used for wiki entry
    # "Upgrades": ItemData(000, always_, "RemoteUpgrades", ("RUSideUpgrades", )),
    "Blueprints": ItemData(2001, always_useful, "RemoteBlueprints", ("RUBlueprints", )),
    # Only used for wiki entry and task/upgrade unlocks
    # "Fluids": ItemData(000, always_progression, "RemoteFluids", ("RUFluids", )),
    "Operator Levels": ItemData(2002, always_progression, "RemoteOperatorLevels", ("RUPlayerLevel", )),
    # Only used for wiki entry and task/upgrade unlocks
    # "Trains": ItemData(000, always_progression, "RemoteTrains", ("RUTrains", )),
    "3rd Platform Floor": ItemData(2003, always_useful, "Remote3rdPlatformFloor", ("RUIslandLayer3", )),
    # Entirely for display purposes
    # "Infinite Goals": ItemData(000, always_progression, "RemoteInfiniteGoals", ("RUInfiniteGoals", )),
    "3rd Floor": ItemData(2004, always_useful, "Remote3rdFloor", ("RULayer3", )),
    # Only used for wiki entry
    # "Wires (Category)": ItemData(000, always_progression, "RemoteWiresCategory", ("RUWires", )),
    "Train Delivery": ItemData(2005, always_progression, "RemoteTrainDelivery", ("RUTrainHubDelivery", )),
}

starting: dict[str, ItemData] = {
    "Space Platforms": ItemData(2100, always_progression, "RemoteSpacePlatforms", ("RUIslandPlacement", )),
    "2nd Platform Floor": ItemData(2101, always_useful, "Remote2ndPlatformFloor", ("RUIslandLayer2", )),
}
