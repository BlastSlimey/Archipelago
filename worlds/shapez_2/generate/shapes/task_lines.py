from typing import TYPE_CHECKING

from . import Processor

if TYPE_CHECKING:
    from ... import Shapez2World


def get_processors_list(world: "Shapez2World") -> list[list[Processor]]:
    task_processors: list[list[Processor]] = []
    line_count = world.options.location_adjustments["Task lines"]
    min_per_line = world.options.location_adjustments["Minimum checks per task line"]
    max_per_line = world.options.location_adjustments["Maximum checks per task line"]
    for i in range(line_count):
        task_count = world.random.randint(min_per_line, max_per_line)
        if i < 3 and task_count == 5:  # Ensures that the first three lines **can** always have a sphere 1 shape
            task_count = 4
        task: list[Processor] = []
        for __ in range(task_count):
            Processor.add_random_next(world.random, task, None)
        task_processors.append(task)
    return task_processors


def get_shapes_list(
    world: "Shapez2World",
    task_processors: list[list[Processor]]
) -> list[list[str]]:
    from .generator import generate_shape, downgrade_shape

    task_shapes: list[list[str]] = []
    i = -1
    for task in task_processors:
        i += 1
        shapes = [generate_shape(world, task, world.random.randint(len(task) + 2 + (i // 3), len(task) + 3 + i))]
        for j in range(len(task)):
            shapes.insert(0, downgrade_shape(world, shapes[0], task[-j]))
        if i < 3 or (len(task) < 5 and world.random.choice((True, False, False))):
            # Assumes the first three lines always have less than 5 processors
            shapes.insert(0, downgrade_shape(world, shapes[0], task[0]))
        task_shapes.append(shapes)

    return task_shapes
