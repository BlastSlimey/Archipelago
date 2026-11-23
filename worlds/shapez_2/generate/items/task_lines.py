from typing import TYPE_CHECKING, Iterator

if TYPE_CHECKING:
    from ... import Shapez2World


def generate_default(world: "Shapez2World") -> Iterator[str]:

    if world.options.lock_locations.is_job_lines:
        for i in range(3, world.options.jobs_adjustments["Job lines"]):
            yield f"Job line #{i+1}"


def generate_starting(world: "Shapez2World") -> Iterator[str]:
    if world.options.lock_locations.is_job_lines:
        yield from ("Job line #1", "Job line #2", "Job line #3")
