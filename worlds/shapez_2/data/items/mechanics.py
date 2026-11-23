from .. import ItemData
from ..classification import *

always: dict[str, ItemData] = {
    "2nd Machine Level": ItemData(2000, always_progression, "GenericLayerUnlock", "Remote2ndMachineLevel", (), (), ("RULayer2", )),
    "Blueprints": ItemData(2001, always_useful, "Blueprints", "RemoteBlueprints", (), (), ("RUBlueprints", )),
    "3rd Space Level": ItemData(2003, always_useful, "Platforms", "Remote3rdSpaceLevel", (), (), ("RUIslandLayer3", )),
    # Entirely for display purposes
    # "Infinite Goals": ItemData(000, always_progression, "", "RemoteInfiniteGoals", (), (), ("RUInfiniteGoals", )),
    "3rd Machine Level": ItemData(2004, always_useful, "GenericLayerUnlock", "Remote3rdMachineLevel", (), (), ("RULayer3", )),
    "Train Vortex Delivery": ItemData(2005, always_useful, "ConverterVortex", "RemoteTrainVortexDelivery", (), (), ("RUTrainHubDelivery", )),
}

starting: dict[str, ItemData] = {
    "Space Platforms": ItemData(2100, always_progression, "Platforms", "RemoteSpacePlatforms", (), (), ("RUIslandPlacement", )),
    "2nd Space Level": ItemData(2101, always_progression, "Platforms", "Remote2ndSpaceLevel", (), (), ("RUIslandLayer2", )),
    # That item just keeps messing up the UI
    # "Wires (Category)": ItemData(2102, always_useful, "SignalTransportGroup", "RemoteWiresCategory", (), (), ("RUWires", )),
    "Fluids": ItemData(2104, always_progression, "FluidsCategory", "RemoteFluids", (), (), ("RUFluids", )),
    "Shop": ItemData(2105, always_progression, "SideUpgrades", "RemoteShop", (), (), ("RUSideUpgrades", )),
}

special: dict[str, ItemData] = {
    "Operator Levels": ItemData(2200, always_progression, "VirtualProcessorsGroup", "RemoteOperatorLevels", (), (), ("RUPlayerLevel", )),
}
