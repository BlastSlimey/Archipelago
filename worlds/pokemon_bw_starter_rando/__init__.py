# Do not change anything about the imports unless you know what you do
from typing import TYPE_CHECKING, Any
from types import ModuleType

import orjson

from .data import version

if TYPE_CHECKING:
    try:
        from worlds.pokemon_bw.ndspy.rom import NintendoDSRom
        from worlds.pokemon_bw.rom import PokemonBWPatch
    except:
        pass


class Plugin:
    name = version.name

    @staticmethod
    def patch(rom: "NintendoDSRom", bw_patch_instance: "PokemonBWPatch", files_dump: dict[str, bytes | bytearray],
              plugins: list[tuple[str, ModuleType]]):
        from worlds.pokemon_bw.ndspy.narc import NARC
        from worlds.pokemon_bw.data.pokemon.species import by_name
        import random
        from . import lz11

        slot_data = orjson.loads(bw_patch_instance.files.get("slot_data.json", b'{}'))
        options: dict[str, Any] = slot_data.get("options", {})
        plugin_options: dict[str, Any] = options.get("plugin_options", {})
        seed = random.Random(slot_data.get("seed", random.randint(10000, 999999999)))
        stat_tolerance = options.get("pokemon_randomization_adjustments", {}).get("Stats leniency", 10)
        if "starter_rando" not in plugin_options:
            rando_wild = options.get("randomize_wild_pokemon", [])
            similar_stats = "similar base stats" in rando_wild
            same_types = "type themed areas" in rando_wild
            base_only = False
        else:
            this_options = plugin_options.get("starter_rando", {})
            is_dict = isinstance(this_options, dict)
            similar_stats = is_dict and this_options.get("similar_stats", False)
            same_types = is_dict and this_options.get("same_types", False)
            base_only = is_dict and this_options.get("base_only", False)
        stats_total = lambda data: (
            data.base_hp + data.base_attack + data.base_defense +
            data.base_sp_attack + data.base_sp_defense + data.base_speed
        )
        snivy = by_name["Snivy"]
        tepig = by_name["Tepig"]
        oshawott = by_name["Oshawott"]

        possible_grass, possible_fire, possible_water = [], [], []
        for dat in by_name.values():
            if similar_stats and abs(stats_total(snivy)-stats_total(dat)) > stat_tolerance:
                continue
            if same_types and "Grass" not in (dat.type_1, dat.type_2):
                continue
            if base_only and dat.evolution_stage != 1:
                continue
            possible_grass.append(dat)
        for dat in by_name.values():
            if similar_stats and abs(stats_total(tepig)-stats_total(dat)) > stat_tolerance:
                continue
            if same_types and "Fire" not in (dat.type_1, dat.type_2):
                continue
            if base_only and dat.evolution_stage != 1:
                continue
            possible_fire.append(dat)
        for dat in by_name.values():
            if similar_stats and abs(stats_total(oshawott)-stats_total(dat)) > stat_tolerance:
                continue
            if same_types and "Water" not in (dat.type_1, dat.type_2):
                continue
            if base_only and dat.evolution_stage != 1:
                continue
            possible_water.append(dat)
        snivy = seed.choice(possible_grass)
        tepig = seed.choice(possible_fire)
        oshawott = seed.choice(possible_water)

        narc = NARC(rom.getFileByName("a/0/5/7"))
        script = bytearray(narc.files[782])
        script = script.replace(b'\x28\x00\x21\x80\xEF\x01',
                                b'\x28\x00\x21\x80' + snivy.dex_number.to_bytes(2, "little"))
        script = script.replace(b'\x57\x00\x01\xEF\x01', b'\x57\x00\x01' + snivy.dex_number.to_bytes(2, "little"))
        script = script.replace(b'\x28\x00\x21\x80\xEF\x01',
                                b'\x28\x00\x21\x80' + tepig.dex_number.to_bytes(2, "little"))
        script = script.replace(b'\x57\x00\x01\xEF\x01', b'\x57\x00\x01' + tepig.dex_number.to_bytes(2, "little"))
        script = script.replace(b'\x28\x00\x21\x80\xEF\x01',
                                b'\x28\x00\x21\x80' + oshawott.dex_number.to_bytes(2, "little"))
        script = script.replace(b'\x57\x00\x01\xEF\x01', b'\x57\x00\x01' + oshawott.dex_number.to_bytes(2, "little"))
        narc.files[782] = bytes(script)
        files_dump[f"a057/782"] = narc.files[782]
        rom.setFileByName("a/0/5/7", narc.save())

        starter_narc = NARC(rom.getFileByName("a/2/0/5"))
        sprites_narc = NARC(rom.getFileByName("a/0/0/4"))
        starter_narc.files[0] = sprites_narc.files[snivy.dex_number * 20 + 18]
        starter_narc.files[2] = sprites_narc.files[tepig.dex_number * 20 + 18]
        starter_narc.files[4] = sprites_narc.files[oshawott.dex_number * 20 + 18]
        starter_narc.files[12] = lz11.decomp(sprites_narc.files[snivy.dex_number * 20], 0)
        starter_narc.files[13] = lz11.decomp(sprites_narc.files[tepig.dex_number * 20], 0)
        starter_narc.files[14] = lz11.decomp(sprites_narc.files[oshawott.dex_number * 20], 0)
        files_dump[f"a205/0"] = starter_narc.files[0]
        files_dump[f"a205/2"] = starter_narc.files[2]
        files_dump[f"a205/4"] = starter_narc.files[4]
        files_dump[f"a205/12"] = starter_narc.files[12]
        files_dump[f"a205/13"] = starter_narc.files[13]
        files_dump[f"a205/14"] = starter_narc.files[14]
        rom.setFileByName("a/2/0/5", starter_narc.save())

        # UPR also changes the IDs used in the Dreamyard script, the text file of the player room, and the cry overlay
