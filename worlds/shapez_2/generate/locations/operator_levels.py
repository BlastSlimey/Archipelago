from typing import TYPE_CHECKING

from BaseClasses import Region

if TYPE_CHECKING:
    from ... import Shapez2World


def create_locations(world: "Shapez2World", regions: dict[str, Region]) -> None:
    ...  # TODO
