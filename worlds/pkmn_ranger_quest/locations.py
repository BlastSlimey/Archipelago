from BaseClasses import Location


class RangerQuestLocation(Location):
    game = "Pokemon Ranger (Quest)"


def lookup_table() -> dict[str, int]:
    from .data.locations import table
    return table
