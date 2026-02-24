from __future__ import annotations

from typing import TYPE_CHECKING, Dict, Set

from BaseClasses import ItemClassification, Location, Region

from .data import data, LocationData, LocationCategory

from . import items

if TYPE_CHECKING:
    from .world import PokemonRSOA


class PokemonRSOALocation(Location):
    game = "PokemonRangerSOA"


def location_to_ap_id(location: data.LocationData) -> int:
    return location.id


def ap_id_to_location(id) -> data.LocationData:
    return next(location for location in data.locations.values() if location.id == id)


def create_location_label_to_id_map() -> Dict[str, int]:
    """
    Creates a map from location labels to their AP location id (address)
    """
    label_to_id_map: Dict[str, int] = {}

    for name, location_data in data.locations.items():
        label_to_id_map[location_data.label] = location_to_ap_id(location_data)

    return label_to_id_map


def get_location_names_with_ids(location_labels: list[str]) -> dict[str, int | None]:
    location_label_to_id_map = create_location_label_to_id_map()
    return {label: location_label_to_id_map[label] for label in location_labels}


def create_all_locations(world: PokemonRSOA) -> None:
    region = world.get_region("Overworld")

    for name, location_data in data.locations.items():
        if location_data.category not in [
            LocationCategory.MISSION,
            LocationCategory.QUEST,
        ]:
            continue

        print(name, location_data)
        print(world.location_name_to_id)

        new_location = PokemonRSOALocation(
            world.player,
            name,
            world.location_name_to_id[location_data.label],
            region,
        )

        region.locations.append(new_location)

    create_pokemon_locations(world)


# def create_locations_by_category(
#     world: "PokemonRSOA",
#     regions: Dict[str, Region],
#     categories: Set[LocationCategory],
# ) -> None:
#     """
#     Iterates through region data and adds locations to the multiworld if
#     those locations include any of the provided tags.
#     """
#     for region_name, region_data in data.regions.items():
#         region = regions[region_name]
#         filtered_locations = [
#             loc
#             for loc in region_data.locations
#             if data.locations[loc].category in categories
#         ]
#
#         for location_name in filtered_locations:
#             location_data = data.locations[location_name]
#
#             location_id = location_to_ap_id(location_data)
#             if location_data.flag == 0:  # Dexsanity location
#                 national_dex_id = int(
#                     location_name[-3:]
#                 )  # Location names are formatted POKEDEX_REWARD_###
#
#                 # Don't create this pokedex location if player can't find it in the wild
#                 if (
#                     NATIONAL_ID_TO_SPECIES_ID[national_dex_id]
#                     in world.blacklisted_wilds
#                 ):
#                     continue
#
#                 location_id += POKEDEX_OFFSET + national_dex_id
#
#             location = PokemonEmeraldLocation(
#                 world.player,
#                 location_data.label,
#                 location_id,
#                 region,
#                 location_name,
#                 location_data.addresses,
#                 location_data.default_item,
#             )
#             region.locations.append(location)


def create_quest_locations(world: PokemonRSOA) -> None:
    return


def create_pokemon_locations(world: PokemonRSOA) -> None:
    # for region_name, region_data in data.regions.items():
    #
    #     region = world.get_region(region_name)

    region = world.get_region("Overworld")

    for browser_id, pokemon in data.species.items():

        if pokemon.browser_id in world.blacklisted_captures:
            continue

        location_name = f"Capture {pokemon.name}"
        new_location = PokemonRSOALocation(
            world.player,
            location_name,
            world.location_name_to_id[location_name],
            region,
        )

        region.locations.append(new_location)
