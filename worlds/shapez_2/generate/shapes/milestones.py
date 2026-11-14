from typing import TYPE_CHECKING

from . import Processor
from .. import reseed

if TYPE_CHECKING:
    from ... import Shapez2World


@reseed
def get_processors_list(world: "Shapez2World") -> list[list[Processor]]:
    milestone_processors: list[list[Processor]] = []
    milestone_order: list[Processor] = []
    milestone_count = world.options.milestone_adjustments["Milestones"]
    max_processors = world.options.shape_generation_adjustments["Maximum processors per milestone"]
    for _ in range(min(milestone_count, 8)):
        Processor.add_random_next(world.random, milestone_order, None)
    for i in range(milestone_count):
        order_index = (i * 8) // milestone_count if milestone_count > 8 else i
        proc = [milestone_order[order_index]]
        for _ in range(min(max_processors - 1, order_index)):
            if not Processor.add_restricted_previous(world.random, proc, milestone_order[:order_index]):
                Processor.add_random_next(world.random, proc, milestone_order[:order_index])
        milestone_processors.append(proc)
    return milestone_processors


@reseed
def get_shapes_list(world: "Shapez2World") -> list[tuple[list[str], list[str]]]:
    from .generator import generate_shape
    from .downgrader import distinct_downgrades

    milestone_shapes: list[tuple[list[str], list[str]]] = []

    i = 0
    for milestone in world.milestone_processors:
        i += 3
        # Assumes all milestones have at least 1 processor
        builder1 = generate_shape(world, milestone, i)
        line_1 = distinct_downgrades(world, builder1, milestone.copy(), min(2, len(milestone)), i, builder1.build(), [])[0]
        builder2 = generate_shape(world, milestone, i, line_1)
        line_2 = distinct_downgrades(world, builder2, milestone.copy(), min(2, len(milestone)), i, builder2.build(), line_1)[0]
        milestone_shapes.append((line_1, line_2))

    return milestone_shapes
