from random import Random
from typing import Callable, Any, ClassVar, TYPE_CHECKING

try:
    from BaseClasses import CollectionState, ItemClassification
    if TYPE_CHECKING:
        from worlds.pokemon_bw.ndspy.rom import NintendoDSRom
        from worlds.pokemon_bw.ndspy.narc import NARC
        from worlds.pokemon_bw.ndspy.code import Overlay
        from worlds.pokemon_bw.rom import PokemonBWPatch
        from worlds.pokemon_bw import PokemonBWWorld
        from worlds.pokemon_bw.data import ExtendedRule
except ImportError:
    pass


def override(function: Callable):
    function.override = True
    return function


class PluginProtocol:
    slot_data: ClassVar[dict[str, Any]]
    general_options: ClassVar[dict[str, Any]]
    all_plugin_options: ClassVar[dict[str, Any]]
    all_plugin_settings: ClassVar[dict[str, Any]]
    patch_instance: "PokemonBWPatch"
    world: "PokemonBWWorld"
    all_plugins: list
    random: Random

    _initialized: bool
    _ov_table: dict[int, "Overlay"]
    _ov_arrays: dict[int, bytearray]
    _narcs: dict[str, "NARC"]
    _rom: "NintendoDSRom"
    _files_dump: dict[str, bytes | bytearray]
    _options: dict[str, Any]
    _settings: dict[str, Any]
    _arm9: bytearray | None
    _arm7: bytearray | None

    @staticmethod
    def otpp_patch_array(array: bytearray, otp: bytes | bytearray): ...

    def get_option(self, name: str, default=None, typ: type = object, support_weighting=True) -> Any: ...

    def get_setting(self, name: str, default=None, typ: type = object, support_weighting=True) -> Any: ...

    def get_from_narc(self, path: str, file_num: int) -> bytearray: ...

    def get_overlay(self, ov_num: int) -> bytearray: ...

    def get_arm9(self) -> bytearray: ...

    def get_arm7(self) -> bytearray: ...

    @staticmethod
    def modify_rule(old: "ExtendedRule", new: Callable[["ExtendedRule", "CollectionState", "PokemonBWWorld"], bool]): ...

    def new_item(self, name: str, classification: "ItemClassification" = None): ...
