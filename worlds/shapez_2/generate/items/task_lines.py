from typing import TYPE_CHECKING, Iterator
from ...items import Shapez2Item

if TYPE_CHECKING:
    from ... import Shapez2World


def generate_default(world: "Shapez2World") -> Iterator[Shapez2Item]:
    from ...data.items.misc import task_lines

    if world.options.lock_locations.is_job_lines:
        for i in range(3, world.options.jobs_adjustments["Job lines"]):
            name = f"Job line #{i+1}"
            data = task_lines[name]
            yield Shapez2Item(name, data.classification(world), world.item_name_to_id[name], world.player)


def generate_starting(world: "Shapez2World") -> Iterator[str]:
    if world.options.lock_locations.is_job_lines:
        yield from ("Job line #1", "Job line #2", "Job line #3")
