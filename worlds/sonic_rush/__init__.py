import os
import pkgutil
from typing import Mapping, Any, ClassVar

import settings
from BaseClasses import Tutorial, MultiWorld, Item
from worlds.AutoWorld import WebWorld, World
from .items import SonicRushItem, item_table
from .options import SonicRushOptions


class SonicRushSettings(settings.Group):
    class RomFile(settings.UserFilePath):
        """File name of the Sonic Rush (USA) rom"""
        copy_to = "Sonic_Rush_USA.nds"
        description = "Sonic Rush (USA) ROM File"
        md5s = ["bd4dcf6ad27de0e3212b8c67864df0ec"]

    rom_file: RomFile = RomFile(RomFile.copy_to)
    rom_start: bool = True


class SonicRushWeb(WebWorld):
    rich_text_options_doc = True
    theme = "grass"
    game_info_languages = ['en']
    setup_en = Tutorial(
        "Multiworld Setup Guide",
        "A guide to playing Sonic Rush with Archipelago:",
        "English",
        "setup_en.md",
        "setup/en",
        ["BlastSlimey"]
    )
    tutorials = [setup_en]


class SonicRushWorld(World):
    """
    Sonic Rush is 2.5D platformer from 2005 for the Nintendo DS, that introduced Blaze the Cat and the boost ability.
    """
    game = "Sonic Rush"
    options_dataclass = SonicRushOptions
    options: SonicRushOptions
    topology_present = True
    web = SonicRushWeb()
    settings: ClassVar[SonicRushSettings]
    item_name_to_id = {}
    location_name_to_id = {}

    def __init__(self, multiworld: MultiWorld, player: int):
        super().__init__(multiworld, player)

    def generate_early(self) -> None:
        pass

    def create_item(self, name: str) -> Item:
        return SonicRushItem(name, item_table[name], self.item_name_to_id[name], self.player)

    def get_filler_item_name(self) -> str:
        return "Filler"

    def create_regions(self) -> None:
        pass

    def create_items(self) -> None:
        pass

    def set_rules(self) -> None:
        pass

    def fill_slot_data(self) -> Mapping[str, Any]:
        pass

    def generate_output(self, output_directory: str) -> None:
        patch = SonicRushProcedurePatch(player=self.player, player_name=self.multiworld.player_name[self.player])
        patch.write_file("base_patch.bsdiff4", pkgutil.get_data(__name__, "data/archipelago-base.bsdiff"))
        rom_path = os.path.join(
            output_directory, f"{self.multiworld.get_out_file_name_base(self.player)}" f"{patch.patch_file_ending}"
        )
        patch.write(rom_path)
