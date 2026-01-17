from typing import TYPE_CHECKING

from . import Processor, ShapeBuilder, downgrade_hexagonal, downgrade_tetragonal

if TYPE_CHECKING:
    from ... import Shapez2World


def downgrade_shape(world: "Shapez2World", builder: ShapeBuilder, remaining_processors: list[Processor],
                    missing_processor: Processor, original_complexity: int) -> ShapeBuilder:
    # IMPORTANT: Modifies the builder itself
    if world.options.shape_configuration == "hexagonal":
        return downgrade_hexagonal.downgrade_6(world.random, builder, remaining_processors, missing_processor,
                                               original_complexity)
    else:
        return downgrade_tetragonal.downgrade_4(world.random, builder, remaining_processors, missing_processor,
                                                original_complexity)
