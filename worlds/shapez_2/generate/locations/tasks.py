from typing import TYPE_CHECKING

from BaseClasses import Region

if TYPE_CHECKING:
    from ... import Shapez2World
    from ...data import AccessRule


def create_locations(world: "Shapez2World",
                     regions: dict[str, Region],
                     processor_rules_dict: dict[list[str], "AccessRule"]) -> None:
    ...  # TODO
