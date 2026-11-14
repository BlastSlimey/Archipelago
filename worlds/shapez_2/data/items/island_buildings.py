from .. import ItemData
from ..classification import *

always: dict[str, ItemData] = {
    "Shape Trains": ItemData(1006, always_useful, "RemoteShapeTrains", (),
                             ("TrainLaunchersGroup", "TrainCatchersGroup",
                              "RailLiftUp1X1X2Group", "RailLiftDown1X1X2Group", "RailLiftUp1X1X3Group", "RailLiftDown1X1X3Group",
                              "RedTrainProducerGroup", "RedRailGroup",
                              "TrainQuickStationsGroup", "TrainWaitStationsGroup", "TrainStationStraightSpacerShapeGroup",
                              "ShapeCargoFactoriesGroup",
                              "TrainShapeLoadersGroup", "TrainShapeUnloadersGroup", ),
                             ("RUTrains", )),
    "Fluid Trains": ItemData(1007, always_useful, "RemoteFluidTrains", (),
                             ("TrainLaunchersGroup", "TrainCatchersGroup",
                              "RailLiftUp1X1X2Group", "RailLiftDown1X1X2Group", "RailLiftUp1X1X3Group", "RailLiftDown1X1X3Group",
                              "RedTrainProducerGroup", "RedRailGroup",
                              "TrainQuickStationsGroup", "TrainWaitStationsGroup", "TrainStationStraightSpacerShapeGroup",
                              "FluidCargoFactoriesGroup",
                              "TrainFluidLoadersGroup", "TrainFluidUnloadersGroup", ),
                             ("RUTrains", )),
    "1x3 Platform": ItemData(1010, always_progression_skip_balancing, "Remote1x3Platform", (), ("FoundationGroup_1x3", ), ()),
    "1x4 Platform": ItemData(1011, always_progression_skip_balancing, "Remote1x4Platform", (), ("FoundationGroup_1x4", ), ()),
    "3-Blocks L Platform": ItemData(1012, always_progression_skip_balancing, "Remote3BlocksLPlatform", (), ("FoundationGroup_L3", ), ()),
    "4-Blocks L Platform": ItemData(1013, always_progression_skip_balancing, "Remote4BlocksLPlatform", (), ("FoundationGroup_L4", ), ()),
    "T Platform": ItemData(1014, always_progression_skip_balancing, "RemoteTPlatform", (), ("FoundationGroup_T4", ), ()),
    "S Platform": ItemData(1015, always_progression_skip_balancing, "RemoteSPlatform", (), ("FoundationGroup_S4", ), ()),
    "Cross Platform": ItemData(1016, always_progression_skip_balancing, "RemoteCrossPlatform", (), ("FoundationGroup_C5", ), ()),
    "2x2 Platform": ItemData(1017, always_progression_skip_balancing, "Remote2x2Platform", (), ("FoundationGroup_2x2", ), ()),
    "2x3 Platform": ItemData(1018, always_progression_skip_balancing, "Remote2x3Platform", (), ("FoundationGroup_2x3", ), ()),
    "2x4 Platform": ItemData(1019, always_progression_skip_balancing, "Remote2x4Platform", (), ("FoundationGroup_2x4", ), ()),
    "3x3 Platform": ItemData(1020, always_progression_skip_balancing, "Remote3x3Platform", (), ("FoundationGroup_3x3", ), ()),
    "Train Color: Green": ItemData(1021, always_useful, "RemoteGreenTrains", (), ("GreenRailGroup", "GreenTrainProducerGroup", ), ()),
    "Train Color: Blue": ItemData(1022, always_useful, "RemoteBlueTrains", (), ("BlueRailGroup", "BlueTrainProducerGroup", ), ()),
    "Train Color: Cyan": ItemData(1023, always_useful, "RemoteCyanTrains", (), ("CyanRailGroup", "CyanTrainProducerGroup", ), ()),
    "Train Color: Magenta": ItemData(1024, always_useful, "RemoteMagentaTrains", (), ("MagentaTrainProducerGroup", "MagentaRailGroup"), ()),
    "Train Color: Yellow": ItemData(1025, always_useful, "RemoteYellowTrains", (), ("YellowTrainProducerGroup", "YellowRailGroup", ), ()),
    "Train Color: White": ItemData(1026, always_useful, "RemoteWhiteTrains", (), ("WhiteTrainProducerGroup", "WhiteRailGroup", ), ()),
    "Wagon Transfer": ItemData(1029, always_useful, "RemoteWagonTransfer", (), ("TrainShapeTransferGroup", "TrainFluidTransferGroup", ), ()),
    "Spacer Wagon": ItemData(1033, always_filler, "RemoteSpacerWagon", (), ("FillerCargoFactoriesGroup", ), ()),
    # Might make using roller coasters possible even without the supporter edition
    # "Roller Coaster": ItemData(000, always_filler, "RemoteRollerCoaster", (), (
    #     "TrainTwistersGroup", "TrainLoopsGroup", "RailLiftUp2X1X2Group", "RailLiftDown2X1X2Group",
    # ), ()),
}

starting: dict[str, ItemData] = {
    "Space Belt": ItemData(1100, always_progression, "RemoteSpaceBelt", (), ("SpaceBeltsGroup", ), ()),
    "1x1 Platform": ItemData(1105, always_progression_skip_balancing, "Remote1x1Platform", (), ("FoundationGroup_1x1", ), ()),
    "1x2 Platform": ItemData(1106, always_progression_skip_balancing, "Remote1x2Platform", (), ("FoundationGroup_1x2", ), ()),
}

miners: dict[str, ItemData] = {
    "Asteroid Miner": ItemData(1200, always_progression, "RemoteAsteroidMiner", (), ("ShapeMinerExtractorsGroup", ), ()),
    "Asteroid Pump": ItemData(1201, always_progression, "RemoteAsteroidPump", (), ("FluidMinerExtractorsGroup", ), ()),
    "Asteroid Miner Booster": ItemData(1202, always_useful, "RemoteAsteroidMinerBooster", (), ("ShapeMinerChainsGroup", ), ()),
    "Asteroid Pump Booster": ItemData(1203, always_useful, "RemoteAsteroidPumpBooster", (), ("FluidMinerChainsGroup", ), ()),
    "Asteroid Miner + Booster": ItemData(1204, always_progression, "RemoteAsteroidMinerPlusBooster", (), ("ShapeMinerExtractorsGroup", "ShapeMinerChainsGroup"), ()),
    "Asteroid Pump + Booster": ItemData(1205, always_progression, "RemoteAsteroidPumpPlusBooster", (), ("FluidMinerExtractorsGroup", "FluidMinerChainsGroup"), ()),
    "Space Pipe": ItemData(1206, always_progression, "RemoteSpacePipe", (), ("SpacePipesGroup", ), ()),
    "Asteroid Pump + Pipe": ItemData(1207, always_progression, "RemoteAsteroidPumpPlusPipe", (), ("FluidMinerExtractorsGroup", "SpacePipesGroup", ), ()),
    "Asteroid Pump + Booster + Pipe": ItemData(1208, always_progression, "RemoteAsteroidPumpPlusBoosterPipe", (),
                                               ("FluidMinerExtractorsGroup", "FluidMinerChainsGroup""SpacePipesGroup", ), ()),
}
