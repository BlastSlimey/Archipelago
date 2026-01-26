import zipfile
from typing import TYPE_CHECKING, Any
from orjson import orjson

from worlds.Files import APPlayerContainer

if TYPE_CHECKING:
    from . import Shapez2World


class Shapez2ScenarioContainer(APPlayerContainer):
    game = "shapez 2"
    patch_file_ending = ".zip"

    def __init__(self, world: "Shapez2World", path: str | None = None):
        self.world = world
        super().__init__(path, world.player, world.player_name, "")

    def write_contents(self, opened_zipfile: zipfile.ZipFile) -> None:
        from .generate.files import (example_shapes, blueprint, milestones, tasks, upgrades, operator_lines,
                                     mechanics, starting_location)
        super().write_contents(opened_zipfile)

        scenario_id = self.world.multiworld.get_out_file_name_base(self.player)
        scenario: dict[str, Any] = {
            "FormatVersion": 2,
            "GameVersion": 1058,
            "UniqueId": scenario_id,
            "SupportedGameModes": ["RegularGameMode"],
            "NextScenarios": [],
            "ExampleShapes": example_shapes.get_example_shapes(self),
            "Title": f"Archipelago ({self.player_name})",
            "Description": f"Scenario for player {self.player_name} from the multiworld "
                           f"with seed {self.world.multiworld.seed_name}.",
            "PreviewImageId": "Scenario_Regular",
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
                "IntroductionWikiEntryId": "WKWelcome",
                "InitiallyUnlockedUpgrades": ["RNInitial"],
                "TutorialConfig": "TCNoTutorial"
            },
            "Progression": {
                "Levels": {"Levels": milestones.get_milestones(self)},
                "SideQuestGroups": {"SideQuestGroups": tasks.get_task_lines(self)},
                "SideUpgrades": {
                    "UpgradeCategories": ["ProcessingSpeeds","Buildings","Platforms","Trains","Wires",
                                          "Decorations","Other"],
                    "SideUpgrades": upgrades.get_remote_upgrades(self)
                },
                "LinearUpgrades": {
                    "HubInputSizeUpgradeId": "LRUHubInputSize",
                    "ShapeQuantityUpgradeId": "LRUShapeQuantity",
                    "SpeedsToLinearUpgradeMappings": {
                        "BeltSpeed": "LRUBeltSpeed",
                        "CutterSpeed": "LRUCuttingSpeed",
                        "StackerSpeed": "LRUStackingSpeed",
                        "PainterSpeed": "LRUPaintingSpeed",
                        "TrainSpeed": "LRUTrainSpeed",
                        "TrainCapacity": "LRUTrainCapacity"
                    },
                    "LinearUpgrades": upgrades.linear_upgrades
                }
            },
            "StartingLocation":{
                "InitialViewport":{
                    "PositionY":-11.56,
                    "Zoom":480.0,
                    "Angle":70.0,
                    "ShowAllBuildingLayers":True,
                    "ShowAllIslandLayers":True
                },
                "InitialIslands":{"InitialIslands":[{"Position_GC":{"x":-1},"LayoutId":"Layout_HUB"}]},
                "FixedPatches":{"FixedPatches": starting_location.get_fixed_patches(self)},
                "StartingChunks":{"StartingChunks":[]}
            },
            "PlayerLevelConfig":{
                "IconicLevelShapes":{"LevelShapes": example_shapes.get_iconic_shapes(self)},
                "IconicLevelShapeInterval":1,
                "GoalLines": operator_lines.get_operator_lines(self),
                "Rewards": operator_lines.get_operator_rewards(self)
            },
            "Mechanics":{
                "Mechanics": mechanics.get_mechanic_definitions(self),
                "BuildingLayerMechanicIds":["RULayer2","RULayer3"],
                "IslandLayerMechanicIds":["RUIslandLayer2","RUIslandLayer3"],
                "IslandLayersUnlockOrder":[-1,1],
                "BlueprintsMechanicId":"RUBlueprints",
                "RailsMechanicId":"RUTrains",
                "IslandManagementMechanicId":"RUIslandPlacement",
                "PlayerLevelMechanicId":"RUPlayerLevel",
                "TrainHubDeliveryMechanicId":"RUTrainHubDelivery"
            },
            "ConvertersConfig":{"Configs":{}},
            "ResearchStationConfig":{"Recipes":{}},
            "RailColorsConfig":{
                "RailColors":[
                    {"Id":{"RailColorId":"Blue"},"Tint":"197FE5"},
                    {"Id":{"RailColorId":"Green"},"Tint":"19E566"},
                    {"Id":{"RailColorId":"Red"},"Tint":"F43F3F"},
                    {"Id":{"RailColorId":"White"},"Tint":"EAEAEA"},
                    {"Id":{"RailColorId":"Cyan"},"Tint":"19E5EA"},
                    {"Id":{"RailColorId":"Magenta"},"Tint":"EA19EA"},
                    {"Id":{"RailColorId":"Yellow"},"Tint":"EAEA19"}
                ]
            },
            "ToolbarConfig": "#include_raw:Scenarios/Shared/Toolbar/ToolbarConfig"
        }
        scenario_preset: dict[str, Any] = {
          "Version": "1",
          "UniqueId": scenario_id + "_preset",
          "Title": "@scenario-preset.default.title",
          "Description": "@scenario-preset.default.description",
          "Parameters": {
            "ScenarioId": scenario_id,
            "MapGenerationParameters": {
              "FluidsSpawnPrimaryColors": True,
              "FluidsSpawnSecondaryColors": False,
              "FluidsSpawnTertiaryColors": False,
              "FluidPatchLikelinessPercent": 40,
              "FluidPatchBaseSize": 2,
              "FluidPatchSizeGrowPercentPerChunk": 70,
              "FluidPatchMaxSize": 4,
              "ShapePatchLikelinessPercent": 100,
              "ShapePatchBaseSize": 2,
              "ShapePatchSizeGrowPercentPerChunk": 70,
              "ShapePatchMaxSize": 7,
              "ShapePatchShapeColorfulnessPercent": 50,
              "ShapePatchRareShapeLikelinessPercent": 30,
              "ShapePatchVeryRareShapeLikelinessPercent": 10,
              "ShapePatchGenerationLikeliness": [
                {"GenerationType": "TertiaryColorFullShapePure","MinimumDistanceToOrigin": 40,"Weight": 1},
                {"GenerationType": "TertiaryColorFullShape","MinimumDistanceToOrigin": 32,"Weight": 1},
                {"GenerationType": "TertiaryColorAlmostFullShape","MinimumDistanceToOrigin": 28,"Weight": 1},
                {"GenerationType": "TertiaryColorHalfShape","MinimumDistanceToOrigin": 24,"Weight": 1},
                {"GenerationType": "SecondaryColorFullShapePure","MinimumDistanceToOrigin": 20,"Weight": 1},
                {"GenerationType": "SecondaryColorFullShape","MinimumDistanceToOrigin": 16,"Weight": 2},
                {"GenerationType": "SecondaryColorAlmostFullShape","MinimumDistanceToOrigin": 12,"Weight": 2},
                {"GenerationType": "SecondaryColorHalfShape","MinimumDistanceToOrigin": 10,"Weight": 3},
                {"GenerationType": "PrimaryColorFullShapePure","MinimumDistanceToOrigin": 8,"Weight": 3},
                {"GenerationType": "PrimaryColorFullShape","MinimumDistanceToOrigin": 6,"Weight": 4},
                {"GenerationType": "PrimaryColorAlmostFullShape","MinimumDistanceToOrigin": 4,"Weight": 4},
                {"GenerationType": "PrimaryColorHalfShape","MinimumDistanceToOrigin": 3,"Weight": 5},
                {"GenerationType": "UncoloredFullShapePure","MinimumDistanceToOrigin": 2,"Weight": 10},
                {"GenerationType": "UncoloredFullShape","MinimumDistanceToOrigin": 1,"Weight": 30},
                {"GenerationType": "UncoloredAlmostFullShape","MinimumDistanceToOrigin": 1,"Weight": 50},
                {"GenerationType": "UncoloredHalfShape","MinimumDistanceToOrigin": 0,"Weight": 100}
              ]
            },
            "GameRuleParameters": {"RuleIds": []}
          }
        }
        scenario_json: bytes = orjson.dumps(scenario)
        position = scenario_json.find(b"\"FormatVersion\":2,")
        if position != -1:
            scenario_json = scenario_json[:position] + b"\"FormatVersion\": 2," + scenario_json[position+18:]
        opened_zipfile.writestr("scenario_" + scenario_id + ".json", scenario_json)
        opened_zipfile.writestr("preset_" + scenario_id + ".json", orjson.dumps(scenario_preset))
