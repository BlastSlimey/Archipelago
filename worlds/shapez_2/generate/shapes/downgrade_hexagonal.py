import math
from enum import Enum, IntEnum
from random import Random
from typing import TYPE_CHECKING, Iterable

from . import Processor, generate_hexagonal, generate_tetragonal, ShapeBuilder

if TYPE_CHECKING:
    from ... import Shapez2World


def downgrade_6(rand: Random, builder: ShapeBuilder, remaining_processors: list[Processor],
                missing_processor: Processor, original_complexity: int) -> ShapeBuilder:
    from .generate_hexagonal import Variant


def _unpaint(remaining_processors: list[Processor], *,
             parts: Iterable[str] = None, long: str = None) -> Iterable[str] | str:
    ...


def _unmix(remaining_processors: list[Processor], replacements: dict[str, str], *,
           parts: Iterable[str] = None, long: str = None) -> Iterable[str] | str:
    ...


def _decrystallize(remaining_processors: list[Processor], replacements: dict[str, str], *,
                   parts: Iterable[str] = None, long: str = None) -> Iterable[str] | str:
    ...
