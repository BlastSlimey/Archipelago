from typing import TYPE_CHECKING

from . import Processor

if TYPE_CHECKING:
    from ... import Shapez2World


def get_processors_list(world: "Shapez2World") -> list[list[Processor]]:
    milestone_processors: list[list[Processor]] = []
    milestone_order: list[Processor] = []
    milestone_count = world.options.location_adjustments["Milestones"]
    for _ in range(min(milestone_count, 8)):
        Processor.add_random_next(world.random, milestone_order, None)
    for i in range(milestone_count):
        order_index = (i * 8) // milestone_count if milestone_count > 8 else i
        proc = [milestone_order[order_index]]
        if order_index > 0:
            if not Processor.add_restricted_previous(world.random, proc, milestone_order[:order_index]):
                Processor.add_random_next(world.random, proc, milestone_order[:order_index])
        if order_index > 1:
            if not Processor.add_restricted_previous(world.random, proc, milestone_order[:order_index]):
                Processor.add_random_next(world.random, proc, milestone_order[:order_index])
        milestone_processors.append(proc)
    return milestone_processors


def get_shapes_list(
    world: "Shapez2World",
    milestone_processors: list[list[Processor]]
) -> list[tuple[list[str], list[str]]]:
    from .generator import generate_shape
    from .downgrader import downgrade_shape

    milestone_shapes: list[tuple[list[str], list[str]]] = []

    i = 0
    for milestone in milestone_processors:
        i += 3
        # Assumes all milestones have at least 1 processor
        if len(milestone) == 1:
            builder1 = generate_shape(world, milestone, i)
            builder2 = generate_shape(world, milestone, i)
            shapes1 = [builder1.build()]
            shapes2 = [builder2.build()]
            shapes1.insert(0, downgrade_shape(world, builder1, [], milestone[0], i).build())
            shapes2.insert(0, downgrade_shape(world, builder2, [], milestone[0], i).build())
            milestone_shapes.append((shapes1, shapes2))
        else:
            builder1 = generate_shape(world, milestone, i)
            builder2 = generate_shape(world, milestone, i)
            shapes1 = [builder1.build()]
            shapes2 = [builder2.build()]
            builder1 = downgrade_shape(world, builder1, milestone[:-1], milestone[-1], i)
            builder2 = downgrade_shape(world, builder2, milestone[:-1], milestone[-1], i)
            shapes1.insert(0, builder1.build())
            shapes2.insert(0, builder2.build())
            shapes1.insert(0, downgrade_shape(world, builder1, milestone[:-2], milestone[-2], i).build())
            shapes2.insert(0, downgrade_shape(world, builder2, milestone[:-2], milestone[-2], i).build())
            milestone_shapes.append((shapes1, shapes2))

    return milestone_shapes
