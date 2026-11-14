from typing import TYPE_CHECKING

from . import Processor
from .. import reseed

if TYPE_CHECKING:
    from ... import Shapez2World


@reseed
def get_processors_list(world: "Shapez2World") -> list[list[Processor]]:
    operator_processors: list[list[Processor]] = []
    line_count = world.options.operator_levels_adjustments["Operator lines"]
    random_lines_count = world.options.operator_levels_adjustments["Random operator lines"]
    max_tasks_per_line = world.options.jobs_adjustments["Maximum checks per job line"]
    use_milestones = world.options.operator_lines_shapes.is_milestones
    use_jobs = world.options.operator_lines_shapes.is_jobs
    full_jobs = ()
    if use_jobs:
        full_jobs = tuple(i for i in range(len(world.task_counts)) if world.task_counts[i] == max_tasks_per_line)
    jobs_start = 0 if not use_milestones else len(world.milestone_processors) - 2
    for line_index in range(line_count-random_lines_count):
        if use_milestones and line_index + 2 < len(world.milestone_processors):
            operator_processors.append(world.milestone_processors[line_index + 2].copy())
        elif use_jobs and line_index >= jobs_start and line_index - jobs_start < len(full_jobs):
            operator_processors.append(world.task_processors[full_jobs[line_index - jobs_start]].copy())
        else:
            proc_count = world.random.randint(3, 8)
            proc = []
            for _ in range(proc_count):
                Processor.add_random_next(world.random, proc, None)
            operator_processors.append(proc)
    for line_index in range(random_lines_count):
        if line_index != 0 and line_index == random_lines_count - 1:
            operator_processors.append([
                Processor.CUTTER, Processor.ROTATOR, Processor.STACKER, Processor.PAINTER,
                Processor.MIXER, Processor.PIN_PUSHER, Processor.CRYSTALLIZER, Processor.SWAPPER,
            ])
        else:
            operator_processors.append([
                Processor.CUTTER, Processor.ROTATOR, Processor.STACKER, Processor.PAINTER,
                Processor.MIXER, Processor.PIN_PUSHER, Processor.SWAPPER,
            ])
    return operator_processors


@reseed
def get_shapes_list(
    world: "Shapez2World",
    operator_processors: list[list[Processor]]
) -> list[str | None | int]:
    from .generator import generate_shape

    # str is shape, None is random, positive int is milestone, 0 and negative int is job line
    operator_shapes: list[str | None | int] = []
    line_count = world.options.operator_levels_adjustments["Operator lines"]
    random_lines_count = world.options.operator_levels_adjustments["Random operator lines"]
    milestone_count = world.options.milestone_adjustments["Milestones"]
    max_tasks_per_line = world.options.jobs_adjustments["Maximum checks per job line"]
    use_milestones = world.options.operator_lines_shapes.is_milestones
    use_jobs = world.options.operator_lines_shapes.is_jobs
    full_jobs = ()
    if use_jobs:
        full_jobs = tuple(i for i in range(len(world.task_counts)) if world.task_counts[i] == max_tasks_per_line)
    jobs_start = 0 if not use_milestones else milestone_count - 2

    for line_index in range(line_count-random_lines_count):
        if use_milestones and line_index + 2 < milestone_count:
            operator_shapes.append(line_index + 2)
        elif use_jobs and line_index >= jobs_start and line_index - jobs_start < len(full_jobs):
            operator_shapes.append(-full_jobs[line_index - jobs_start])
        else:
            operator_shapes.append(generate_shape(world, operator_processors[line_index],
                                                  world.random.randint(15, 30)).build())
    operator_shapes.extend([None] * random_lines_count)

    return operator_shapes
