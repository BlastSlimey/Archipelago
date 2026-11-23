import os
import zipfile
from typing import TYPE_CHECKING, Any
import orjson

from settings import get_settings
from worlds.Files import APAutoPatchInterface

if TYPE_CHECKING:
    from . import Shapez2World


class Shapez2ScenarioContainer(APAutoPatchInterface):
    game = "shapez 2"
    patch_file_ending = ".spz2scenario"
    result_file_ending = ".json"
    files: dict[str, Any]

    def __init__(self, path: str, player=None, player_name="", world: "Shapez2World" = None):
        self.world = world
        self.files = {}
        super().__init__(path=path, player=player, player_name=player_name, server="")

    def write_contents(self, opened_zipfile: zipfile.ZipFile) -> None:
        from .generate.files import (example_shapes, blueprint, milestones, tasks, upgrades, operator_lines,
                                     mechanics, starting_location, debug, wiki)
        super().write_contents(opened_zipfile)

        scenario_id = self.world.multiworld.get_out_file_name_base(self.player)
        mechanic_definitions = mechanics.get_mechanic_definitions(self)
        other_players_items: set[str] = set()  # ONLY FOR LOOKUP!!!
        scenario: dict[str, Any] = {
            "FormatVersion": 3,
            "GameVersion": 1058,
            "UniqueId": scenario_id,
            "SupportedGameModes": ["RegularGameMode"],
            "NextScenarios": [],
            "ExampleShapes": example_shapes.get_example_shapes(self),
            "Title": f"Archipelago ({self.player_name})",
            "Description": f"Scenario for player {self.player_name} from the multiworld "
                           f"with seed {self.world.multiworld.seed_name}.",
            "PreviewImageId": "ScenarioBackground_Classic_Regular",
            "PlayerBadge": {
                "Title": f"AP: {self.player_name} ({self.world.multiworld.seed_name})",
                "ImageId": "OperatorBadgeClassicRegular"
            },
            "ResearchConfig": {
                "BaseChunkLimitMultiplier": 200,
                "BaseBlueprintRewardMultiplier": 500,
                "MaxShapeLayers": self.world.options.shape_generation_adjustments["Maximum layers"],
                "ShapesConfigurationId": ("DefaultShapesQuadConfiguration"
                                          if self.world.options.shape_configuration == "tetragonal"
                                          else "DefaultShapesHexagonalConfiguration"),
                "ColorSchemeConfigurationId": "DefaultColorSchemeRGBFlex",
                "ResearchLevelsAreProgressive": True,
                "BlueprintCurrencyShapes": blueprint.get_blueprint_shapes(self),
                "IntroductionWikiEntryId": "WKClassicRegularWelcome",
                "InitiallyUnlockedUpgrades": ["Milestone_Initial"],
                "TutorialConfig": "TCNoTutorial"
            },
            "Progression": {
                "Levels": {"Levels": milestones.get_milestones(self, mechanic_definitions, other_players_items)},
                "SideQuestGroups": {"SideQuestGroups": tasks.get_task_lines(self, mechanic_definitions,
                                                                            other_players_items)},
                "ScenarioContent": {
                    "UpgradeCategories": ["Upgrades","Buildings","Platforms","Trains","Wires",
                                          "Decorations","Other"],
                    "ContentBundles": [{"ContentBundle": upgrades.get_remote_upgrades(self)}]
                },
                "LinearUpgrades": {
                    "HubInputSizeUpgradeId": "LRUHubInputSize",
                    "ShapeQuantityUpgradeId": "LRUShapeQuantity",
                    "ChunkLimitAddUpgradeId": "LRUChunkLimitAdd",
                    "SpeedsToLinearUpgradeMappings": {
                        "BeltSpeed": "LRUGlobalSpeed",
                        "CutterSpeed": "LRUGlobalSpeed",
                        "StackerSpeed": "LRUGlobalSpeed",
                        "PainterSpeed": "LRUGlobalSpeed",
                        "TrainSpeed": "LRUTrainSpeed",
                        "TrainCapacity": "LRUTrainCapacity"
                    },
                    "LinearUpgrades": upgrades.linear_upgrades
                },
                "WikiConfiguration": {
                    "Categories": wiki.categories,
                    "WikiEntries": wiki.wiki_entries,
                }
            },
            "StartingLocation": {
                "InitialViewport": {
                    "PositionY": -11.56,
                    "Zoom": 480.0,
                    "Angle": 70.0,
                    "ShowAllBuildingLayers": True,
                    "ShowAllIslandLayers": True
                },
                "CentralElementCoordinate": {
                    "x": -1
                },
                "InitialIslands": {"InitialIslands": [{"Position_GC": {"x": -1}, "LayoutId": "Layout_HUB"}]},
                "FixedPatches": {"FixedPatches": starting_location.get_fixed_patches(self)},
                "StartingChunks": {"StartingChunks": [{
                    "GuaranteedShapePatches": [],
                    "GuaranteedColorPatches": ["r", "b", "g"]
                }]}
            },
            "PlayerLevelConfig": {
                "IconicLevelShapes": {"LevelShapes": example_shapes.get_iconic_shapes(self)},
                "IconicLevelShapeInterval": 1,
                "RankDifficultyMultiplier": 1.0,
                "GoalLines": operator_lines.get_operator_lines(self),
                "Rewards": operator_lines.get_operator_rewards(self, mechanic_definitions, other_players_items)
            },
            "Mechanics": {
                "Mechanics": mechanic_definitions,
                "BuildingLayerMechanicIds": ["RULayer2", "RULayer3"],
                "IslandLayerMechanicIds": ["RUIslandLayer2", "RUIslandLayer3"],
                "IslandLayersUnlockOrder": [1, 2],
                "BlueprintsMechanicId": "RUBlueprints",
                "RailsMechanicId": "RUTrains",
                "IslandManagementMechanicId": "RUIslandPlacement",
                "PlayerLevelMechanicId": "RUPlayerLevel",
                "TrainHubDeliveryMechanicId": "RUTrainHubDelivery",
                "SideUpgradeMechanicId": "RUSideUpgrades",
                "TradeStationsMechanicId": "RUTradeStations"
            },
            "ConvertersConfig": {"RocketGroups": [], "Configs": {}},
            "ResearchStationConfig": {"Recipes": {}},
            "RailColorsConfig": {
                "RailColors": [
                    {"Id": {"RailColorId": "Blue"}, "Tint": "197FE5"},
                    {"Id": {"RailColorId": "Green"}, "Tint": "19E566"},
                    {"Id": {"RailColorId": "Red"}, "Tint": "F43F3F"},
                    {"Id": {"RailColorId": "White"}, "Tint": "EAEAEA"},
                    {"Id": {"RailColorId": "Cyan"}, "Tint": "19E5EA"},
                    {"Id": {"RailColorId": "Magenta"}, "Tint": "EA19EA"},
                    {"Id": {"RailColorId": "Yellow"}, "Tint": "EAEA19"}
                ]
            },
            "ToolbarConfig": "#include_raw:Scenarios/Classic/DefaultData/Toolbar/ToolbarConfig"
        }
        scenario_preset: dict[str, Any] = {
          "Version": "1",
          "UniqueId": scenario_id + "_preset",
          "Title": "@scenario-preset.default.title",
          "Description": "@scenario-preset.default.description",
          "Parameters": {
            "ScenarioId": scenario_id,
            "MapGenerationParameters": "#include:Scenarios/SharedData/BaseMapGenerationParameters",
            "GameRuleParameters": {"RuleIds": []}
          }
        }
        opened_zipfile.writestr("scenario.json", orjson.dumps(scenario, option=orjson.OPT_INDENT_2))
        opened_zipfile.writestr("preset.json", orjson.dumps(scenario_preset, option=orjson.OPT_INDENT_2))
        opened_zipfile.writestr("shapes_debug.txt", debug.write_shapes_debug(self))

    def patch(self, target: str) -> None:
        from Utils import messagebox

        self.read()
        mod = os.path.join(get_settings()["shapez_2_settings"]["save_data_folder"], "mods", "APScenario")
        scenarios = os.path.join(mod, "scenarios")
        presets = os.path.join(mod, "scenario-presets")
        os.makedirs(scenarios, exist_ok=True)
        os.makedirs(presets, exist_ok=True)
        append = "" if get_settings()["shapez_2_settings"]["overwrite_scenario"] else "_" + os.path.split(target)[1]
        with (open(os.path.join(scenarios, f"scenario{append}.json"), "wb") as sc_out,
              open(os.path.join(presets, f"preset{append}.json"), "wb") as pr_out,
              open(os.path.join(mod, "manifest.json"), "wb") as ma_out):
            sc_out.write(self.files["scenario.json"])
            pr_out.write(self.files["preset.json"])
            ma_out.write(orjson.dumps({
                "Version": "1.0.0",
                "Description": "Code-less mod for the scenario and preset files generated by Archipelago",
                "Author": "Archipelago",
                "AffectsSaveGames": False,
                "DisablesAchievements": True,
                "SaveGameCompabilityRange": "*",
                "GameVersionSupportRange": ">=1.2.0",
                "Assemblies": [],
                "Dependencies": [],
                "Conflicts": []
            }, option=orjson.OPT_INDENT_2))
        messagebox("Success",
                   "Successfully installed the scenario and preset files into <save_data_folder>/mods/APScenario")

    def read_contents(self, opened_zipfile: zipfile.ZipFile) -> dict[str, Any]:
        manifest = super().read_contents(opened_zipfile)
        self.files |= {file: opened_zipfile.read(file) for file in opened_zipfile.namelist()}
        return manifest
