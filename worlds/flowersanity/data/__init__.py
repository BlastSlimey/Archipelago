from typing import NamedTuple, TYPE_CHECKING, Any, Callable

from BaseClasses import ItemClassification, CollectionState, LocationProgressType

if not TYPE_CHECKING:
    AccessRule: type = Any
    ExtendedRule: type = Any
    ClassificationMethod: type = Any
    ProgressTypeMethod: type = Any
else:
    from .. import FlowersanityWorld
    AccessRule: type = Callable[[CollectionState], bool]
    ExtendedRule: type = Callable[[CollectionState, FlowersanityWorld], bool]
    ClassificationMethod: type = Callable[[FlowersanityWorld], ItemClassification]
    ProgressTypeMethod: type = Callable[[FlowersanityWorld], LocationProgressType]


class ItemData(NamedTuple):
    item_id: int
    classification: ClassificationMethod


class LocationData(NamedTuple):
    location_id: int
    progress_type: ProgressTypeMethod
