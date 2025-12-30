import enum
from random import Random
from typing import Self


class Processor(enum.IntEnum):
    CUTTER = 0
    ROTATOR = 1
    STACKER = 2
    PAINTER = 3
    MIXER = 4
    PIN_PUSHER = 5
    CRYSTALLIZER = 6
    SWAPPER = 7

    @classmethod
    def restrictions(cls) -> dict[Self, tuple[Self, Self]]:
        return {
            cls.ROTATOR: (cls.CUTTER, cls.SWAPPER),
            cls.CRYSTALLIZER: (cls.CUTTER, cls.PIN_PUSHER),
            cls.MIXER: (cls.PAINTER, cls.CRYSTALLIZER),
        }

    @classmethod
    def add_random_next(cls, random: Random, active: list[Self], possible: list[Self] | None) -> None:
        # Assumes active is a sublist of possible
        poss = possible.copy() if possible is not None else [
            cls.CUTTER, cls.ROTATOR, cls.STACKER, cls.PAINTER, cls.MIXER, cls.PIN_PUSHER, cls.CRYSTALLIZER, cls.SWAPPER
        ]
        for a in active:
            poss.remove(a)
        for rest, reqs in cls.restrictions().items():
            if rest in poss and reqs[0] not in active and reqs[1] not in active:
                poss.remove(rest)
        active.append(random.choice(poss))

    @classmethod
    def add_restricted_previous(cls, random: Random, active: list[Self], possible: list[Self] | None) -> bool:
        # Only intended for adding something before rotator/mixer/crystallizer
        # Assumes that there is at least one required processor possible
        active: list[Processor]
        for rest, reqs in cls.restrictions().items():
            if active[0] == rest:
                if reqs[1] not in possible:
                    active.insert(0, reqs[0])
                elif reqs[0] not in possible:
                    active.insert(0, reqs[1])
                else:
                    active.insert(0, random.choice(reqs))
                return True
        return False


event_by_processor: dict[Processor, str] = {
    Processor.CUTTER: "[PROCESSOR] Cutter",
    Processor.ROTATOR: "[PROCESSOR] Rotator",
    Processor.STACKER: "[PROCESSOR] Stacker",
    Processor.PAINTER: "[PROCESSOR] Painter",
    Processor.MIXER: "[PROCESSOR] Mixer",
    Processor.PIN_PUSHER: "[PROCESSOR] Pin Pusher",
    Processor.CRYSTALLIZER: "[PROCESSOR] Crystallizer",
    Processor.SWAPPER: "[PROCESSOR] Swapper",
}
