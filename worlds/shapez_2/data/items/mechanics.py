from .. import ItemData
from ..classification import *

always: dict[str, ItemData] = {
    "2nd Machine Level": ItemData(2000, always_progression, "Remote2ndMachineLevel", (), (), ("RULayer2", )),
    "Blueprints": ItemData(2001, always_useful, "RemoteBlueprints", (), (), ("RUBlueprints", )),
    "3rd Space Level": ItemData(2003, always_useful, "Remote3rdSpaceLevel", (), (), ("RUIslandLayer3", )),
    # Entirely for display purposes
    # "Infinite Goals": ItemData(000, always_progression, "RemoteInfiniteGoals", (), (), ("RUInfiniteGoals", )),
    "3rd Machine Level": ItemData(2004, always_useful, "Remote3rdMachineLevel", (), (), ("RULayer3", )),
    "Train Vortex Delivery": ItemData(2005, always_useful, "RemoteTrainVortexDelivery", (), (), ("RUTrainHubDelivery", )),
}

starting: dict[str, ItemData] = {
    "Space Platforms": ItemData(2100, always_progression, "RemoteSpacePlatforms", (), (), ("RUIslandPlacement", )),
    "2nd Space Level": ItemData(2101, always_progression, "Remote2ndSpaceLevel", (), (), ("RUIslandLayer2", )),
    "Wires (Category)": ItemData(2102, always_useful, "RemoteWiresCategory", (), (), ("RUWires", )),
    "Fluids": ItemData(2104, always_progression, "RemoteFluids", (), (), ("RUFluids", )),
    "Shop": ItemData(2105, always_progression, "RemoteUpgrades", (), (), ("RUSideUpgrades", )),
}

special: dict[str, ItemData] = {
    "Operator Levels": ItemData(2200, always_progression, "RemoteOperatorLevels", (), (), ("RUPlayerLevel", )),
}
