import struct
from typing import TYPE_CHECKING

from BaseClasses import Location
from settings import get_settings
from worlds.Files import APProcedurePatch, APTokenMixin, APTokenTypes
from .data import data

if TYPE_CHECKING:
    from . import PokemonRSOA


ARM9_ROM_OFFSET = 0x4000


class PokemonRangerSOAProcedurePatch(APProcedurePatch, APTokenMixin):
    game = "PokemonRangerSOA"
    hash = "f957f5784abf9557be086fdb6fdc74cc"
    patch_file_ending = ".apprsoa"
    result_file_ending = ".nds"

    procedure = [
        ("apply_tokens", ["token_data.bin"]),
    ]

    @classmethod
    def get_source_data(cls) -> bytes:
        with open(get_settings().pokemon_ranger_soa_settings.rom_file, "rb") as infile:
            base_rom_bytes = bytes(infile.read())

        return base_rom_bytes


def write_tokens(
    world: "PokemonRSOA",
    patch: PokemonRangerSOAProcedurePatch,
    starting_se: int = None,
) -> None:

    _nop_instructions(world, patch)

    _remove_field_moves(world, patch)

    patch.write_file("token_data.bin", patch.get_token_binary())


def _nop_instructions(
    world: "PokemonRSOA", patch: PokemonRangerSOAProcedurePatch
) -> None:

    addresses = []

    addresses += data.rom_addresses["INSTRUCTION_STYLER_UPGRADE_SET"].addresses

    if world.options.level_up_type > 0:
        addresses += data.rom_addresses[
            "INSTRUCTION_LEVEL_UP_STYLER_LEVEL_UP"
        ].addresses
        # addresses += data.rom_addresses["INSTRUCTION_LEVEL_UP_MAX_HEALTH_UP"].addresses
        # This sets the game to 0 hp on new save. Causes issues.
    if world.options.rank_up_type > 0:
        addresses += data.rom_addresses["INSTRUCTION_RANGER_RANK_SET"].addresses

    if world.options.styler_model_item > 0:
        addresses += data.rom_addresses["INSTRUCTION_STYLER_MODEL_SET"].addresses

    for address in addresses:
        patch.write_token(
            APTokenTypes.WRITE,
            address,
            struct.pack("<I", 0xE3A00000),
        )


def _remove_field_moves(
    world: "PokemonRSOA", patch: PokemonRangerSOAProcedurePatch
) -> None:
    if world.options.field_move_item == world.options.field_move_item.option_vanilla:
        return

    for pok in data.species.values():

        for val in pok.poke_id_indexes:
            print("removing shit")
            address = data.rom_addresses["POKE_ID_TABLE_ADDRESS"].first + val * 24 + 5
            patch.write_token(
                APTokenTypes.WRITE,
                address,
                struct.pack("<B", 0),
            )
