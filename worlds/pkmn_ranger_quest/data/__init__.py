from typing import NamedTuple


class PokemonData(NamedTuple):
    number: int
    poke_assist: str
    field_move: tuple[str, int] | None
    missions_only: bool
    legendary: bool
    special_missions: bool
    catchable: bool


class CaptureItemData(NamedTuple):
    item_id: int
    number: int
    internal_ids: tuple[int, ...]


class AssistItemData(NamedTuple):
    item_id: int
    type_id: int


class FieldItemData(NamedTuple):
    item_id: int
    move_id: int
    level: int
