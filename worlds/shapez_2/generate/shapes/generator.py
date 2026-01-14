import math
from random import Random
from typing import TYPE_CHECKING

from . import Processor, generate_hexagonal, generate_tetragonal, ShapeBuilder

if TYPE_CHECKING:
    from ... import Shapez2World


def generate_shape(world: "Shapez2World",
                   processors: list[Processor],
                   complexity: int,
                   exclude: list[str] | None = None) -> ShapeBuilder:
    return generate_new(world.random, processors, complexity, world.options.shape_configuration == "hexagonal",
                        world.options.shape_generation_adjustments["Maximum layers"], exclude)


def generate_new(rand: Random, processors: list[Processor], complexity: int, is_hexagonal: bool, max_layer_count: int,
                 exclude: list[str] | None = None, regen_pools: tuple[list[str], ...] | None = None) -> ShapeBuilder:

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





        # TODO rework pin layers to being decided here instead of inside generate_layer
        # TODO generally rework this in a way that different layers get different tasked lists (such that the important bool isn't needed anymore)

        required_proc = [False] * 8
        for proc in processors:
            required_proc[proc] = True
        builder = ShapeBuilder(processors, required_proc)

        # Make less layers more likely
        layer_weights_multiple = {
            x: max_layer_count - x + 1 for x in range(2, max_layer_count + 1)
        }
        # Make single layer much more likely
        layer_weights = layer_weights_multiple | {1: len(layer_weights_multiple) // 3}
        if required_proc[Processor.PIN_PUSHER]:  # Pin pusher always needs at least 2 layers
            layer_count = rand.choices(tuple(layer_weights_multiple), tuple(layer_weights_multiple.values()))[0]
        elif not required_proc[Processor.STACKER]:  # No stacker and no pin pusher means no multiple layers
            layer_count = 1
        else:  # No pin pusher, but stacker, so every layer count possible
            layer_count = rand.choices(tuple(layer_weights), tuple(layer_weights.values()))[0]
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
        # Max out layers in cases where fewer layers would definitely lead to complexity waste
        if (
            (Processor.STACKER in processors or Processor.PIN_PUSHER in processors) and
            len(processors) <= 2 and complexity >= 15
        ):
            layer_count = current_max_layers
        layer_count = min(max(layer_count, current_min_layers), current_max_layers, max_layer_count)

        # Remove complexity needed for stacking/pin pushing every layer after the first one
        complexity -= layer_count - 1

        generate_layer = (generate_hexagonal.generate_layer if is_hexagonal else generate_tetragonal.generate_layer)
        for layer_index in range(1, layer_count):
            # Get random complexity part for each layer, BUT leave enough to make last layer have enough
            # in order to complete all required processors that weren't completed before the last layer
            part_range_end = builder.calc_required_complexity()
            max_complexity_part = complexity - part_range_end
            complexity_part = math.floor(rand.triangular(0, max_complexity_part, max_complexity_part / 3))
            complexity -= complexity_part
            if (
                layer_index == layer_count - 1 and
                (required_proc[Processor.STACKER] or required_proc[Processor.PIN_PUSHER]) and
                Processor.PIN_PUSHER in processors
            ):
                required_proc[Processor.PIN_PUSHER] = False
                complexity_part += complexity - 1
                complexity = 1
                generate_layer(rand, complexity_part, builder, True, regen_pools=regen_pools)
                required_proc[Processor.PIN_PUSHER] = True
            else:
                generate_layer(rand, complexity_part, builder, False, regen_pools=regen_pools)
        generate_layer(rand, complexity, builder, True, regen_pools=regen_pools)

    if any(not isinstance(layer, str) for layer in builder.shape):
        raise Exception(f"Non-string layer found:\n"
                        f"complexity = {complexity}, builder = {builder.debug_string()}")

    return builder
