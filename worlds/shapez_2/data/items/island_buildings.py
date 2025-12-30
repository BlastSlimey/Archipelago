from .. import ItemData
from ..classification import *

always: dict[str, ItemData] = {
    "1x1 Foundation": ItemData(1000, always_progression_skip_balancing, "Remote1x1Foundation", ("FoundationGroup_1x1", )),
    "1x2 Foundation": ItemData(1001, always_progression_skip_balancing, "Remote1x2Foundation", ("FoundationGroup_1x2", )),
    "Shape Miner Extension": ItemData(1002, always_useful, "RemoteShapeMinerExtension", ("ShapeMinerChainsGroup", )),
    "Space Pipe": ItemData(1003, always_progression, "RemoteSpacePipe", ("SpacePipesGroup", )),
    "Fluid Miner": ItemData(1004, always_progression, "RemoteFluidMiner", ("FluidMinerExtractorsGroup", )),
    "Fluid Miner Extension": ItemData(1005, always_useful, "RemoteFluidMinerExtension", ("FluidMinerChainsGroup", )),
    "Rails": ItemData(1006, always_progression, "RemoteRails", (
        "TrainLaunchersGroup", "TrainCatchersGroup","RailLiftUp1X1X2Group", "RailLiftDown1X1X2Group",
        "RailLiftUp1X1X3Group", "RailLiftDown1X1X3Group"
    )),
    "Shape (Un)loader": ItemData(1007, always_progression, "RemoteShapeUnLoader", (
        "TrainShapeLoadersGroup", "TrainShapeUnloadersGroup",
    )),
    "Shape Wagon": ItemData(1008, always_progression, "RemoteShapeWagon", ("ShapeCargoFactoriesGroup", )),
    "Red Trains": ItemData(1009, always_progression_skip_balancing, "RemoteRedTrains", ("RedTrainProducerGroup", "RedRailGroup", )),
    "1x3 Foundation": ItemData(1010, always_progression_skip_balancing, "Remote1x3Foundation", ("FoundationGroup_1x3", )),
    "1x4 Foundation": ItemData(1011, always_progression_skip_balancing, "Remote1x4Foundation", ("FoundationGroup_1x4", )),
    "3-Blocks L Foundation": ItemData(1012, always_progression_skip_balancing, "Remote3BlocksLFoundation", ("FoundationGroup_L3", )),
    "4-Blocks L Foundation": ItemData(1013, always_progression_skip_balancing, "Remote4BlocksLFoundation", ("FoundationGroup_L4", )),
    "T Foundation": ItemData(1014, always_progression_skip_balancing, "RemoteTFoundation", ("FoundationGroup_T4", )),
    "S Foundation": ItemData(1015, always_progression_skip_balancing, "RemoteSFoundation", ("FoundationGroup_S4", )),
    "Cross Foundation": ItemData(1016, always_progression_skip_balancing, "RemoteCrossFoundation", ("FoundationGroup_C5", )),
    "2x2 Foundation": ItemData(1017, always_progression_skip_balancing, "Remote2x2Foundation", ("FoundationGroup_2x2", )),
    "2x3 Foundation": ItemData(1018, always_progression_skip_balancing, "Remote2x3Foundation", ("FoundationGroup_2x3", )),
    "2x4 Foundation": ItemData(1019, always_progression_skip_balancing, "Remote2x4Foundation", ("FoundationGroup_2x4", )),
    "3x3 Foundation": ItemData(1020, always_progression_skip_balancing, "Remote3x3Foundation", ("FoundationGroup_3x3", )),
    "Green Trains": ItemData(1021, always_progression_skip_balancing, "RemoteGreenTrains", ("GreenRailGroup", "GreenTrainProducerGroup", )),
    "Blue Trains": ItemData(1022, always_progression_skip_balancing, "RemoteBlueTrains", ("BlueRailGroup", "BlueTrainProducerGroup", )),
    "Cyan Trains": ItemData(1023, always_progression_skip_balancing, "RemoteCyanTrains", ("CyanRailGroup", "CyanTrainProducerGroup", )),
    "Magenta Trains": ItemData(1024, always_progression_skip_balancing, "RemoteMagentaTrains", (
        "MagentaTrainProducerGroup", "MagentaRailGroup",
    )),
    "Yellow Trains": ItemData(1025, always_progression_skip_balancing, "RemoteYellowTrains", ("YellowTrainProducerGroup", "YellowRailGroup", )),
    "White Trains": ItemData(1026, always_progression_skip_balancing, "RemoteWhiteTrains", ("WhiteTrainProducerGroup", "WhiteRailGroup", )),
    "Fluid (Un)loader": ItemData(1027, always_progression, "RemoteFluidUnLoader", (
        "TrainFluidLoadersGroup", "TrainFluidUnloadersGroup",
    )),
    "Fluid Wagon": ItemData(1028, always_progression, "RemoteFluidWagon", ("FluidCargoFactoriesGroup", )),
    "Shape Wagon Transfer": ItemData(1029, always_useful, "RemoteShapeWagonTransfer", ("TrainShapeTransferGroup", )),
    "Fluid Wagon Transfer": ItemData(1030, always_useful, "RemoteFluidWagonTransfer", ("TrainFluidTransferGroup", )),
    "Train Quick Stop": ItemData(1031, always_progression, "RemoteTrainQuickStop", ("TrainQuickStationsGroup", )),
    "Train Wait Stop": ItemData(1032, always_progression, "RemoteTrainWaitStop", ("TrainWaitStationsGroup", )),
    "Filler Wagon": ItemData(1033, always_filler, "RemoteFillerWagon", ("FillerCargoFactoriesGroup", )),
    # Might make using roller coasters possible even without the supporter edition
    # "Roller Coaster": ItemData(000, always_filler, "RemoteRollerCoaster", (
    #     "TrainTwistersGroup", "TrainLoopsGroup", "RailLiftUp2X1X2Group", "RailLiftDown2X1X2Group",
    # )),
}

starting: dict[str, ItemData] = {
    "Space Belt": ItemData(1100, always_progression, "RemoteSpaceBelt", ("SpaceBeltsGroup", )),
    "Shape Miner": ItemData(1101, always_progression, "RemoteShapeMiner", ("ShapeMinerExtractorsGroup", )),
}
