import random
from typing import TYPE_CHECKING
if __name__ == '__main__':
    from data.api import PluginProtocol
else:
    from .data.api import PluginProtocol
try:
    if TYPE_CHECKING:
        from worlds.pokemon_bw.ndspy.rom import NintendoDSRom
        from worlds.pokemon_bw.rom import PokemonBWPatch
        from worlds.pokemon_bw.items import PokemonBWItem
        from worlds.pokemon_bw.data import SpeciesData, ExtendedRule
        from worlds.pokemon_bw import PokemonBWWorld
    from worlds.pokemon_bw.plugins._dev import DEV
except ImportError:
    DEV = False


class Plugin(PluginProtocol):
    name = "Pokemon BW Starters Rando Plugin"
    domain = "starter_rando"
    version = "1.1.0"
    author = "BlastSlimey"

    def patch(self):
        from worlds.pokemon_bw.data.pokemon.species import by_name
        from worlds.pokemon_bw.patch import lz11
        if DEV: return

        stat_tolerance = self.general_options["pokemon_randomization_adjustments"]["Stats leniency"]
        rando_wild = self.general_options["randomize_wild_pokemon"]
        similar_stats = self.get_option("similar_stats", "similar base stats" in rando_wild, int)
        same_types = self.get_option("same_types", "type themed areas" in rando_wild, int)
        base_only = self.get_option("base_only", False, int)
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
        snivy = self.random.choice(possible_grass)
        tepig = self.random.choice(possible_fire)
        oshawott = self.random.choice(possible_water)

        script = self.get_from_narc("a/0/5/7", 782)

        index = script.find(b'\x28\x00\x21\x80\xEF\x01')
        while index != -1:
            script[index:index+6] = b'\x28\x00\x21\x80' + snivy.dex_number.to_bytes(2, "little")
            index = script.find(b'\x28\x00\x21\x80\xEF\x01', index+1)
        index = script.find(b'\x57\x00\x01\xEF\x01')
        while index != -1:
            script[index:index+5] = b'\x57\x00\x01' + snivy.dex_number.to_bytes(2, "little")
            index = script.find(b'\x57\x00\x01\xEF\x01', index+1)

        index = script.find(b'\x28\x00\x21\x80\xf2\x01')
        while index != -1:
            script[index:index+6] = b'\x28\x00\x21\x80' + tepig.dex_number.to_bytes(2, "little")
            index = script.find(b'\x28\x00\x21\x80\xf2\x01', index+1)
        index = script.find(b'\x57\x00\x01\xf2\x01')
        while index != -1:
            script[index:index+5] = b'\x57\x00\x01' + tepig.dex_number.to_bytes(2, "little")
            index = script.find(b'\x57\x00\x01\xf2\x01', index+1)

        index = script.find(b'\x28\x00\x21\x80\xf5\x01')
        while index != -1:
            script[index:index+6] = b'\x28\x00\x21\x80' + oshawott.dex_number.to_bytes(2, "little")
            index = script.find(b'\x28\x00\x21\x80\xf5\x01', index+1)
        index = script.find(b'\x57\x00\x01\xf5\x01')
        while index != -1:
            script[index:index+5] = b'\x57\x00\x01' + oshawott.dex_number.to_bytes(2, "little")
            index = script.find(b'\x57\x00\x01\xf5\x01', index+1)

        self.get_from_narc("a/2/0/5", 0)[:] = self.get_from_narc("a/0/0/4", snivy.dex_number * 20 + 18)
        self.get_from_narc("a/2/0/5", 2)[:] = self.get_from_narc("a/0/0/4", tepig.dex_number * 20 + 18)
        self.get_from_narc("a/2/0/5", 4)[:] = self.get_from_narc("a/0/0/4", oshawott.dex_number * 20 + 18)
        self.get_from_narc("a/2/0/5", 12)[:] = lz11.decomp(self.get_from_narc("a/0/0/4", snivy.dex_number * 20), 0)
        self.get_from_narc("a/2/0/5", 13)[:] = lz11.decomp(self.get_from_narc("a/0/0/4", tepig.dex_number * 20), 0)
        self.get_from_narc("a/2/0/5", 14)[:] = lz11.decomp(self.get_from_narc("a/0/0/4", oshawott.dex_number * 20), 0)

        # UPR also changes the IDs used in the Dreamyard script, the text file of the player room, and the cry overlay


if __name__ == '__main__':
    from data.build import build

    build(Plugin.name, Plugin.version, Plugin.author)
