from .. import ItemData
from ..classification import *

always: dict[str, ItemData] = {
    "Painter": ItemData(1, always_progression, "building.PainterDefaultVariant", "RemotePainter", ("PainterDefaultVariant", ), (), ()),
    "Color Mixer": ItemData(4, always_progression, "building.MixerDefaultVariant", "RemoteColorMixer", ("MixerDefaultVariant", ), (), ()),
    "Crystal Generator": ItemData(5, always_progression, "building.CrystalGeneratorDefaultVariant",
                                  "RemoteCrystalGenerator", ("CrystalGeneratorDefaultVariant", ), (), ()),
    "Trash": ItemData(6, always_useful, "building.TrashDefaultVariant", "RemoteTrash", ("TrashDefaultVariant", ), (), ()),
    "Label": ItemData(7, always_filler, "building.LabelDefaultVariant", "RemoteLabel", ("LabelDefaultVariant", ), (), ()),
    "Overflow Splitter": ItemData(8, always_useful, "building.SplitterOverflowVariant", "RemoteOverflowSplitter", ("SplitterOverflowVariant", ), (), ()),
    "Wires": ItemData(
        9, always_useful, "SignalTransportGroup", "RemoteWires",
        ("WireDefaultVariant", "WireBridgeVariant","WireTransmitterSenderVariant", "WireTransmitterReceiverVariant"), (), ()
    ),
    "Signal Producer": ItemData(10, always_useful, "SignalTransportGroup", "RemoteSignalProducer", ("ConstantSignalDefaultVariant", ), (), ()),
    "Belt Filter": ItemData(11, always_useful, "SignalTransportGroup", "RemoteBeltFilter", ("BeltFilterDefaultVariant", ), (), ()),
    "Belt Reader": ItemData(12, always_useful, "SignalTransportGroup", "RemoteBeltReader", ("BeltReaderDefaultVariant", ), (), ()),
    "Pipe Gate": ItemData(13, always_useful, "SignalTransportGroup", "RemotePipeGate", ("PipeGateDefaultVariant", ), (), ()),
    "Display": ItemData(14, always_filler, "SignalTransportGroup", "RemoteDisplay",
                        ("DisplayDefaultVariant", "Display2x2Variant", "Display3x3Variant", ), (), ()),
    "Button": ItemData(15, always_useful, "SignalTransportGroup", "RemoteButton", ("ButtonDefaultVariant", ), (), ()),
    "Logic Gates": ItemData(16, always_useful, "LogicGatesGroup", "RemoteLogicGates",
                            ("LogicGateAndVariant", "LogicGateOrVariant", "LogicGateIfVariant",
                             "LogicGateXOrVariant", "LogicGateNotVariant", "LogicGateCompareVariant"), (), ()),
    "Simulated Machines": ItemData(17, always_useful, "building.VirtualAnalyzerDefaultVariant", "RemoteSimulatedMachines",
                                   ("VirtualRotatorDefaultVariant", "VirtualAnalyzerDefaultVariant",
                                    "VirtualUnstackerDefaultVariant","VirtualStackerDefaultVariant",
                                    "VirtualHalfCutterDefaultVariant", "VirtualPainterDefaultVariant",
                                    "VirtualPinPusherDefaultVariant", "VirtualCrystalGeneratorDefaultVariant",
                                    "VirtualHalvesSwapperDefaultVariant", "VirtualRotatorCCWVariant"), (), ()),
    "Global Signal Transmitter": ItemData(18, always_useful, "building.WireGlobalTransmitterReceiverVariant", "RemoteGlobalSignalTransmission",
                                          ("ControlledSignalReceiverVariant", "ControlledSignalTransmitterVariant"), (), ()),
    "Operator Signal Receiver": ItemData(19, always_useful, "building.WireGlobalTransmitterReceiverVariant",
                                         "RemoteOperatorSignalReceiver", ("WireGlobalTransmitterReceiverVariant", ), (), ()),
    "Fluid Tank": ItemData(20, always_useful, "building.FluidStorageDefaultVariant", "RemoteFluidTank", ("FluidStorageDefaultVariant", ), (), ()),
    "Stacker": ItemData(21, always_progression, "building.StackerStraightVariant", "RemoteStacker", ("StackerStraightVariant", ), (), ()),
    "Stacker (Bent)": ItemData(22, always_progression, "building.StackerDefaultVariant", "RemoteStackerBent", ("StackerDefaultVariant", ), (), ()),
    "Rotator (CW)": ItemData(23, always_progression, "building.RotatorOneQuadVariant", "RemoteRotatorCW", ("RotatorOneQuadVariant", ), (), ()),
    "Rotator (CCW)": ItemData(24, always_progression, "building.RotatorOneQuadCCWVariant", "RemoteRotatorCCW", ("RotatorOneQuadCCWVariant", ), (), ()),
    "Rotator (180)": ItemData(25, always_progression, "building.RotatorHalfVariant", "RemoteRotator180", ("RotatorHalfVariant", ), (), ()),
}

starting: dict[str, ItemData] = {
    "Conveyor Belt": ItemData(100, always_progression, "building.BeltDefaultVariant", "RemoteConveyorBelt",
                              ("BeltDefaultVariant", "BeltPortSenderVariant", "BeltPortReceiverVariant",
                               "Merger2To1Variant", "Merger3To1Variant", "MergerTShapeVariant", "Splitter1To2Variant",
                               "Splitter1To3Variant", "SplitterTShapeVariant", "Lift1LayerVariant",
                               "Lift2LayerVariant"), (), ()),
    "Mini-Miner": ItemData(101, always_progression, "ShapeCategory", "RemoteMiniMiner", ("ExtractorDefaultVariant", ), (), ()),
}

simple_processors: dict[str, ItemData] = {
    "Half Destroyer": ItemData(200, always_progression, "building.CutterHalfVariant", "RemoteHalfDestroyer", ("CutterHalfVariant", ), (), ()),
    "Pin Pusher": ItemData(203, always_progression, "building.PinPusherDefaultVariant", "RemotePinPusher", ("PinPusherDefaultVariant", ), (), ()),
    "Cutter": ItemData(204, always_progression, "building.CutterDefaultVariant", "RemoteCutter", ("CutterDefaultVariant", ), (), ()),
    "Swapper": ItemData(205, always_progression, "building.HalvesSwapperDefaultVariant", "RemoteSwapper", ("HalvesSwapperDefaultVariant", ), (), ()),
}

sandbox: dict[str, ItemData] = {
    "Sandbox Item Producer": ItemData(300, always_progression, "building.SandboxItemProducerDefaultVariant",
                                      "RemoteSandboxItemProducer", ("SandboxItemProducerDefaultVariant", ), (), ()),
    "Sandbox Fluid Producer": ItemData(301, always_progression, "building.SandboxItemProducerDefaultVariant",
                                       "RemoteSandboxFluidProducer", ("SandboxFluidProducerDefaultVariant", ), (), ()),
}

pump_pipe: dict[str, ItemData] = {
    "Mini Pump": ItemData(400, always_progression, "FluidsCategory", "RemoteMiniPump", ("PumpDefaultVariant", ), (), ()),
    "Pipe": ItemData(
        401, always_progression, "FluidsCategory", "RemotePipe",
        ("PipeDefaultVariant", "Pipe1LayerVariant", "Pipe2LayerVariant",
         "FluidPortSenderVariant", "FluidPortReceiverVariant"), (), ()
    ),
    "Mini Pump + Pipe": ItemData(
        402, always_progression, "FluidsCategory", "RemoteMiniPumpPipe",
        ("PipeDefaultVariant", "Pipe1LayerVariant", "Pipe2LayerVariant",
         "FluidPortSenderVariant", "FluidPortReceiverVariant", "PumpDefaultVariant", ), (), ()
    ),
}
