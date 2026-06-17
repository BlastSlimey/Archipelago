# Do not change anything about these imports unless you know what you do
import pkgutil
from typing import TYPE_CHECKING
from zipfile import ZipFile
if __name__ == '__main__':
    from data.api import PluginProtocol
else:
    from .data.api import PluginProtocol
try:
    from BaseClasses import ItemClassification, CollectionState
    if TYPE_CHECKING:
        from worlds.pokemon_bw.ndspy.rom import NintendoDSRom
        from worlds.pokemon_bw.rom import PokemonBWPatch
        from worlds.pokemon_bw.items import PokemonBWItem
        from worlds.pokemon_bw.data import SpeciesData, ExtendedRule
        from worlds.pokemon_bw import PokemonBWWorld
    from worlds.pokemon_bw.plugins._dev import DEV
except ImportError:
    DEV = False


# This has to exactly be named "Plugin" and should inherit from "PluginProtocol"
class Plugin(PluginProtocol):

    # The following fields need to always be set by the plugin creator.
    # "domain" is the key that is used for plugin options and settings, i.e. the player needs to put
    # >  plugin_options:
    # >    <domain>:
    # >      option_1: 123
    # into their player yaml and
    # >  plugin_settings:
    # >    <domain>:
    # >      setting_1: 123
    # into their host.yaml.
    # The version needs to always have the semantic format, i.e. "<major>.<minor>.<patch>".
    name = "Pokemon BW Plugin Template"
    domain = "template"
    version = "2.0.0"
    author = "BlastSlimey"

    # All of the following methods can be safely deleted if you don't need them.

    # This is called during the patching process, after the main apworld did all its standard modifications to the rom.
    def patch(self):
        if DEV: return  # This line is only relevant to the main apworld dev and can be removed if you want.

        # The following are examples of how to load different files from within the rom.
        # Those objects can be edited directly and automatically get saved once the whole patching process is done.
        # See https://docs.google.com/spreadsheets/d/1zsTqs4hhdXg2AZsTWGuY2mhDImnAh_qUTrGy2qCm0s8/edit?gid=1423566666#gid=1423566666
        # for a list of all the narcs' contents.
        script_859 = self.get_from_narc("a/0/5/7", 859)
        str_city_encounters = self.get_from_narc("a/1/2/6", 0)
        ov_93 = self.get_overlay(93)
        arm9 = self.get_arm9()
        arm7 = self.get_arm7()

        # In this example, the encounter table of Striaton City gets directly modified, such that the first
        # surfing slot always gives you level 100 pokémon and the second slot can give you pokémon as weak as level 1.
        # This is done by directly writing bytes to static addresses.
        str_city_encounters[154:156] = b'\x64\x64'
        str_city_encounters[158] = 1

        # In this example, an otpp patch file gets loaded from within the apworld and applied to the
        # move deleter/reminder script file in order to revert the "free move reminder" change.
        # The "self.otpp_patch_array()" method only works with files loaded using any of the "self.get_..." methods.
        loaded_file = pkgutil.get_data(__name__, "files/a057_859.otpp")
        self.otpp_patch_array(script_859, loaded_file)  #

        # In this example, the second and third surfing slots' max levels are set to whatever the player defined
        # in their yaml. The second "self.get_option()" also has a default value (50), that is used if the player
        # didn't put that into their yaml and a type check (int), that checks whether the player put that type of
        # value into their yaml and falls back to the default value if the type doesn't match. If not defined, the
        # default value is "None" and type checking disabled.
        str_city_encounters[159] = self.get_option("slot_1_max_lvl")
        str_city_encounters[163] = self.get_option("slot_2_max_lvl", 50, int)

        # In this example, the third surfing slot's min level is set to whatever the player defined in their host.yaml
        # settings. It works pretty much the same as the "self.get_option()" method, but for host.yaml settings.
        str_city_encounters[162] = self.get_setting("slot_2_min_lvl", 10, int)

        # In this example, a file will be loaded from within the patch file. What you do with it is up to you.
        # In case you didn't know, AP patch files are actually just zip files with a fancy file ending.
        hello_txt = self.patch_instance.files.get("hello.txt", b'')  # If it doesn't exist in the patch file, "b''" will be used instead
        print(str(hello_txt))  # Let's just print its content to the console

    # This is called pretty much at the beginning of generating the world.
    def generate_early(self):
        from worlds.pokemon_bw.data.locations.rules import can_use_surf, can_use_waterfall, can_use_dive
        if DEV: return

        # In this example, the rules that check for being able to use Surf are extended to also check for having the
        # Quake Badge in your inventory. Yes, you can define functions while inside another function.
        def surf_with_quake_badge(old_rule: "ExtendedRule", state: CollectionState, world: "PokemonBWWorld") -> bool:
            # Since this function takes the to-be-modified rule as a parameter, you can reuse it for multiple rules.
            return old_rule(state, world) and state.has("Quake Badge", world.player)
        self.modify_rule(can_use_surf, surf_with_quake_badge)
        self.modify_rule(can_use_waterfall, surf_with_quake_badge)
        self.modify_rule(can_use_dive, surf_with_quake_badge)

    # This is called after generating all wild encounters, static encounters, and trainer teams.
    def generate_encounter(self):
        from worlds.pokemon_bw.generate import EncounterEntry, StaticEncounterEntry, TrainerPokemonEntry

        if DEV: return

        # In this example, the first grass slot is set to always be a Blastoise.
        old_encounter = self.world.wild_encounter["r1 - G 0"]
        self.world.wild_encounter["r1 - G 0"] = EncounterEntry(
            (9, 0),  # Species ID = 9 (Blastoise), form ID = 0 (always 0 if the pokémon has no forms)
            old_encounter.encounter_region,  # Always copy from old entry
            old_encounter.file_index,  # Always copy from old entry
            True  # Always set to true, else it won't be written to the ROM
        )

        # In this example, N's pokémon in his second fight are set to always be Arceus, Mew, and Celebi.
        # This is a bit more complex due to how the generator structures trainer teams data.
        for i in range(len(self.world.trainer_teams)):
            old = self.world.trainer_teams[i]
            if old.trainer_id == 65 and old.team_number == 0:
                self.world.trainer_teams[i] = TrainerPokemonEntry(65, 0, "Arceus")
            if old.trainer_id == 65 and old.team_number == 1:
                self.world.trainer_teams[i] = TrainerPokemonEntry(65, 1, "Mew")
            if old.trainer_id == 65 and old.team_number == 2:
                self.world.trainer_teams[i] = TrainerPokemonEntry(65, 2, "Celebi")

        # In this example, the Zoroark encounter in Lostlorn Forest is set to be Maractus instead.
        # Additionally, the requirement to have the legendary beasts in your party is removed from logic and the
        # encounter is forced to always be in logic regardless of whether wild pokémon have been randomized.
        # However, you'd need to change the script file of Lostlorn Forest yourself (and patch that in the "patch()"
        # method), as the main apworld lacks the function to do so itself atm.
        old_encounter = self.world.static_encounter["Lostlorn Forest Static Encounter"]
        self.world.static_encounter["Lostlorn Forest Static Encounter"] = StaticEncounterEntry(
            (556, 0),  # Same as in wild encounters
            old_encounter.encounter_region,  # Always copy from old entry
            lambda world: True,  # Forces the encounter to always be included in logic
            lambda state, world: True  # Removes any logic requirement apart from having access to Lostlorn Forest
        )

    # This is called after generating all regions, regions connections, locations, and events
    def create_regions(self, catchable_species_data: dict[str, "SpeciesData"]):
        if DEV: return

        # In this example, a new (one-way) connection from P2 Lab to Liberty Garden is created in logic.
        # The actual ingame connection needs to be added in the "patch()" method.
        self.world.regions["P2 Laboratory"].connect(
            self.world.regions["Liberty Garden"],
            "P2 to Liberty Garden ship",  # A name for the connection, that will be shown in the spoiler log (must be unique)
            lambda state: state.has("Liberty Pass", self.world.player)  # A rule that checks for having the liberty pass
        )

        # In this example, another connection from Liberty Garden back to P2 Lab is created, but only if you can
        # catch a Budew somewhere (because why not).
        if "Budew" in catchable_species_data:
            self.world.regions["Liberty Garden"].connect(
                self.world.regions["P2 Laboratory"],
                "Liberty Garden to P2 ship",
                lambda state: True  # Always accessible, as there#s no other way to get to Liberty Garden without the Liberty Pass (unless...)
            )

    # This is called after generating the item pool of a world and placing all locked items (e.g. gym badges in gym rewards)
    def create_items(self, item_pool: list["PokemonBWItem"]):
        if DEV: return

        # In this example, the Bicycle from the item pool gets locked to the first mom location.
        # In this case, the item needs to be removed from the item pool afterwards.
        for i in range(len(item_pool)):
            item = item_pool[i]
            if item.name == "Bicycle":
                self.world.get_location("Nuvema Town - Item from Mom after first fight").place_locked_item(item)
                item_pool.pop(i)  # Removes the item from the pool
                break  # Break the current for-loop, else all items of that name get placed into the same location

        # In this example, all simple Potions in the item pool are replaced by Super Potions.
        for i in range(len(item_pool)):
            item = item_pool[i]
            if item.name == "Potion":
                item_pool[i] = self.new_item("Super Potion")
                # No break this time, as we want to replace ALL Potions

        # In this example, a random filler item gets replaced by another Master Ball
        for i in range(len(item_pool)):
            item = item_pool[i]
            if item.classification == ItemClassification.filler:
                item_pool[i] = self.new_item("Master Ball")
                break  # Once again, only one item should be replaced

        # In this example, all TM94 Rock Smash get their classification changed to progression
        for i in range(len(item_pool)):
            item = item_pool[i]
            if item.name == "TM94 Rock Smash":
                item.classification = ItemClassification.progression
                # No break this time, as we want to modify ALL TM94 Rock Smash

        # In this example, another Exp. Share gets put into starting inventory. Also, as you can see here,
        # you can optionally add a custom classification instead of the default one if you want.
        self.world.push_precollected(self.new_item("Exp. Share", ItemClassification.progression))

        # In this example, the Dowsing Machine that already exists in the item pool gets taken out of it and put
        # into starting inventory. In this case, the item needs to be removed from the pool afterwards.
        for i in range(len(item_pool)):
            item = item_pool[i]
            if item.name == "Dowsing Machine":
                self.world.push_precollected(item)
                item_pool.pop(i)
                break  # No need to go through the rest of the pool

    # This is called after writing all the necessary data to the patch file
    def write_patch(self, opened_zipfile: ZipFile):
        if DEV: return

        # In this example, a custom file is written to inside the patch file.
        opened_zipfile.writestr(
            "hello.txt",  # Name of the file
            "Hello world!"  # Content of the file
        )


# Just run this python script and it will pack this plugin into an apworld file for you.
# Note that any file or folder that contains "_temp" in its name will be ignored and the archipelago.json that's
# bundled will be overwritten.
if __name__ == '__main__':
    from data.build import build

    build(Plugin.name, Plugin.version, Plugin.author)
