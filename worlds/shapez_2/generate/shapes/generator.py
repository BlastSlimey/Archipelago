import math
from enum import Enum, IntEnum
from random import Random
from typing import TYPE_CHECKING, Iterable

from . import Processor, generate_hexagonal, generate_tetragonal, ShapeBuilder

if TYPE_CHECKING:
    from ... import Shapez2World


def generate_shape(world: "Shapez2World",
                   processors: list[Processor],
                   complexity: int,
                   exclude: list[str] | None = None) -> ShapeBuilder:

    if exclude is None:
        exclude = []

    # Make sure that there is enough complexity to use every processor at least once
    if len(processors) > complexity or (
        len(processors) + 1 > complexity and Processor.ROTATOR in processors and (
            Processor.CUTTER not in processors or Processor.SWAPPER not in processors
        )
    ):
        raise Exception(f"Too low complexity ({complexity}) "
                        f"for processors {', '.join(proc.name for proc in processors)}")

    builder: ShapeBuilder | None = None

    # Use "exclude" as a blacklist
    while builder is None or builder.shape in exclude:

        required_proc = [False] * 8
        for proc in processors:
            required_proc[proc] = True
        builder = ShapeBuilder(processors, required_proc)

        # Hard limit of layer count from player options
        max_layer_count = world.options.shape_generation_adjustments["Maximum layers"]
        # Make less layers more likely
        layer_weights_multiple = {
            x: max_layer_count - x + 1 for x in range(2, max_layer_count + 1)
        }
        # Make single layer much more likely
        layer_weights = layer_weights_multiple | {1: len(layer_weights_multiple) // 3}
        if required_proc[Processor.PIN_PUSHER]:  # Pin pusher always needs at least 2 layers
            layer_count = world.random.choices(tuple(layer_weights_multiple), tuple(layer_weights_multiple.values()))[0]
        elif not required_proc[Processor.STACKER]:  # No stacker and no pin pusher means no multiple layers
            layer_count = 1
        else:  # No pin pusher, but stacker, so every layer count possible
            layer_count = world.random.choices(tuple(layer_weights), tuple(layer_weights.values()))[0]
        # Too low complexity makes too many layers impossible
        current_max_layers = complexity + 1 - sum(
            1 for proc in processors if proc not in (Processor.STACKER, Processor.PIN_PUSHER)
        )
        # Having stacker makes at least 2 layers needed, except with certain cutter-rotator-complexity combination
        if Processor.STACKER in processors:
            if Processor.ROTATOR in processors and Processor.CUTTER in processors and complexity >= len(processors) + 2:
                current_min_layers = 1
            else:
                current_min_layers = 2
        else:
            current_min_layers = 1
        # Pin pusher always adds another layer
        if Processor.PIN_PUSHER in processors:
            current_min_layers += 1
        layer_count = min(max(layer_count, current_min_layers), current_max_layers, max_layer_count)

        # Remove complexity needed for stacking/pin pushing every layer after the first one
        complexity -= layer_count - 1

        generate_layer = (
            generate_hexagonal.generate_layer
            if world.options.shape_configuration == "hexagonal"
            else generate_tetragonal.generate_layer
        )
        for layer_index in range(1, layer_count):
            # Get random complexity part for each layer, BUT leave enough to make last layer have enough
            # in order to complete all required processors that weren't completed before the last layer
            part_range_end = sum(required_proc)
            # Every processor that requires something else to work also needs an extra complexity
            # for that other processor
            for rest in Processor.restrictions().items():
                if required_proc[rest[0]] and not required_proc[rest[1][0]] and not required_proc[rest[1][1]]:
                    part_range_end += 1
            max_complexity_part = complexity - part_range_end
            complexity_part = math.floor(world.random.triangular(0, max_complexity_part, max_complexity_part / 3))
            complexity -= complexity_part
            if layer_index == layer_count - 1 and required_proc[Processor.STACKER] and Processor.PIN_PUSHER in processors:
                if layer_index == 1:
                    temp_req_proc = required_proc.copy()
                    temp_req_proc[Processor.PIN_PUSHER] = False
                    builder.tasked = temp_req_proc
                    generate_layer(world, complexity_part, builder, True)
                    builder.tasked = required_proc
                    for i in range(8):
                        if required_proc[i] and not temp_req_proc[i]:
                            required_proc[i] = False
                else:
                    temp_processors = processors.copy()
                    temp_processors.remove(Processor.PIN_PUSHER)
                    generate_layer(world, complexity_part, builder, False)
            else:
                generate_layer(world, complexity_part, builder, False)
        generate_layer(world, complexity, builder, True)

    return builder
