import math
from enum import Enum, IntEnum
from random import Random
from typing import TYPE_CHECKING, Iterable

from . import Processor, generate_hexagonal, generate_tetragonal, ShapeBuilder

if TYPE_CHECKING:
    from ... import Shapez2World


def downgrade_shape(world: "Shapez2World", builder: ShapeBuilder, remaining_processors: list[Processor],
                    missing_processor: Processor, original_complexity: int) -> str:
    # IMPORTANT: Modifies the builder itself
    if world.options.shape_configuration == "hexagonal":
        return _downgrade_6(world, builder, remaining_processors, missing_processor, original_complexity).build()
    else:
        return _downgrade_4(world, builder, remaining_processors, missing_processor, original_complexity).build()


def _downgrade_4(world: "Shapez2World", builder: ShapeBuilder, remaining_processors: list[Processor],
                 missing_processor: Processor, original_complexity: int) -> ShapeBuilder:
    from .generate_tetragonal import Variant, stack, generate_shape

    builder.shape = []
    builder.has_crystals = False
    mixer_replacements = None if missing_processor != Processor.MIXER else {
        "y": world.random.choice("rg"),
        "c": world.random.choice("bg"),
        "m": world.random.choice("rb"),
        "w": world.random.choice("rgb"),
    }
    crystal_replacement = None if missing_processor != Processor.CRYSTALLIZER else {
        "r": generate_shape(world),
        "g": generate_shape(world),
        "b": generate_shape(world),
        "p": generate_shape(world),
        "c": generate_shape(world),
        "m": generate_shape(world),
        "w": generate_shape(world),
    }

    if missing_processor == Processor.STACKER and len(builder.blueprint) > (
        2 if Processor.PIN_PUSHER in remaining_processors else 1
    ):
        from .generator import generate_shape
        return generate_shape(world, remaining_processors, original_complexity)

    for layer_index in range(len(builder.blueprint)):
        variant, stack_top, data = builder.blueprint[layer_index]
        has_vertical_split = any(layer[0:2] != layer[6:8] or layer[2:4] != layer[4:6] for layer in builder.shape)
        has_horizontal_split = any(layer[0:2] != layer[2:4] or layer[6:8] != layer[4:6] for layer in builder.shape)
        match variant:
            case Variant.full:
                if missing_processor == Processor.PAINTER:
                    data["part"] = _unpaint(remaining_processors, long=data["part"])
                elif missing_processor == Processor.MIXER:
                    data["part"] = _unmix(remaining_processors, mixer_replacements, long=data["part"])
                stack(world, builder, data["part"] * 4, True, 0, blueprint=stack_top)
            case Variant.half:
                builder.blueprint.append((Variant.half, stack_top, {"layer": layer, "part": part}))
                leave_as_is = False
                if missing_processor == Processor.PAINTER:
                    # unpaint
                elif missing_processor == Processor.MIXER:
                    # unmix
                elif missing_processor == Processor.CUTTER:
                    # if rotator and vertical split then horizontal half half, elif swapper then vertical half half, else full
                elif missing_processor == Processor.ROTATOR:
                    # right half
                else:
                    leave_as_is = True
                if leave_as_is:
                    ...
            case Variant.half_half:
                builder.blueprint.append((Variant.half_half, stack_top,
                                          {"parts": (part_1, part_2), "layer" : layer}))  # part 1 is top right
                leave_as_is = False
                if missing_processor == Processor.PAINTER:
                    # unpaint
                elif missing_processor == Processor.MIXER:
                    # unmix
                elif missing_processor == Processor.CUTTER:
                    #  leave as is
                elif missing_processor == Processor.ROTATOR:
                    # if swapper then vertical half half, else right half
                elif missing_processor == Processor.STACKER:
                    # if swapper then leave as is, else left/horizontal half
                elif missing_processor == Processor.SWAPPER:
                    # if not cutter then full, elif not rotator then right half, elif not stacker then left/horizontal half, else leave as is
                else:
                    leave_as_is = True
                if leave_as_is:
                    ...
            case Variant.cut_out:
                builder.blueprint.append((Variant.cut_out, {"ordered": ordered_parts}))
                leave_as_is = False
                if missing_processor == Processor.PAINTER:
                    ordered = data["ordered"] = _unpaint(remaining_processors, parts=data["ordered"])
                    stack(world, builder, "".join(ordered), True, 0, blueprint=stack_top)
                elif missing_processor == Processor.MIXER:
                    ordered = data["ordered"] = _unmix(remaining_processors, mixer_replacements, parts=data["ordered"])
                    stack(world, builder, "".join(ordered), True, 0, blueprint=stack_top)
                elif missing_processor == Processor.CUTTER:
                    # 3-1
                elif missing_processor == Processor.ROTATOR:
                    # left half
                elif missing_processor == Processor.STACKER:
                    # if swapper then leave as is, else (rotated) half
                elif missing_processor == Processor.SWAPPER:
                    # if stacker then leave as is, else (rotated) half
                else:
                    leave_as_is = True
                if leave_as_is:
                    # same
            case Variant._3_1:
                builder.blueprint.append((Variant._3_1, {"ordered": ordered_parts}))
                leave_as_is = False
                if missing_processor == Processor.PAINTER:
                    # unpaint
                elif missing_processor == Processor.MIXER:
                    # unmix
                elif missing_processor == Processor.ROTATOR:
                    # if swapper then vertical half half, else left half
                elif missing_processor == Processor.STACKER:
                    # if not cutter then leave as is, elif swapper then 2 singles, else single
                elif missing_processor == Processor.SWAPPER:
                    # if stacker then leave as is, else single
                else:
                    leave_as_is = True
                if leave_as_is:
                    # same
            case Variant.cornered:
                builder.blueprint.append((Variant.cornered, {"half": ("--", part)}))
                leave_as_is = False
                if missing_processor == Processor.PAINTER:
                    # unpaint
                elif missing_processor == Processor.MIXER:
                    # unmix
                elif missing_processor == Processor.CUTTER:
                    # checkered
                elif missing_processor == Processor.ROTATOR:
                    # left half
                elif missing_processor == Processor.STACKER:
                    # if swapper then leave as is, else single
                elif missing_processor == Processor.SWAPPER:
                    # if stacker then leave as is, else single
                else:
                    leave_as_is = True
                if leave_as_is:
                    # same
            case Variant.random_shapes_1_color:
                builder.blueprint.append((Variant.random_shapes_1_color, {"ordered": ordered_parts, "color": color}))
                leave_as_is = False
                if missing_processor == Processor.PAINTER:
                    # unpaint
                elif missing_processor == Processor.MIXER:
                    # unmix
                elif missing_processor == Processor.CUTTER:
                    # if stacker then leave as is, else half half
                elif missing_processor == Processor.ROTATOR:
                    # if swapper then vertical half half, else left half
                elif missing_processor == Processor.STACKER:
                    # if swapper then leave as is, else single
                elif missing_processor == Processor.SWAPPER:
                    # if stacker then leave as is, else single
                else:
                    leave_as_is = True
                if leave_as_is:
                    # same
            case Variant.checkered:
                builder.blueprint.append((Variant.checkered,
                                          {"parts": (part_1, part_2)}))  # parts are up right and down right
                leave_as_is = False
                if missing_processor == Processor.PAINTER:
                    # unpaint
                elif missing_processor == Processor.MIXER:
                    # unmix
                elif missing_processor == Processor.ROTATOR:
                    # if swapper then vertical half half, else left half
                elif missing_processor == Processor.STACKER:
                    # if swapper then leave as is, else single
                elif missing_processor == Processor.SWAPPER:
                    # if stacker then leave as is, else single
                else:
                    leave_as_is = True
                if leave_as_is:
                    # same
            case Variant.random_colors_1_shape:
                builder.blueprint.append((Variant.random_colors_1_shape, {"ordered": ordered_colors, "shape": shape_part}))
                leave_as_is = False
                if missing_processor == Processor.PAINTER:
                    # unpaint, make full
                elif missing_processor == Processor.MIXER:
                    # unmix
                elif missing_processor == Processor.ROTATOR:
                    # if swapper then vertical half half, else left half
                elif missing_processor == Processor.STACKER:
                    # if swapper then leave as is, else single
                elif missing_processor == Processor.SWAPPER:
                    # if stacker then leave as is, else single
                else:
                    leave_as_is = True
                if leave_as_is:
                    # same
            case Variant.pins:
                builder.blueprint.append((Variant.pins, {}))
                if missing_processor != Processor.PIN_PUSHER:  # make pin layer
                else:  # remove layer
            case Variant.full_crystal:
                builder.blueprint.append((Variant.full_crystal, {"part": part}))
                if missing_processor == Processor.CRYSTALLIZER:
                    # if pins then pin layer, else single
                elif missing_processor == Processor.MIXER:
                    # unmix
                elif missing_processor == Processor.PIN_PUSHER:
                    # if rotator then leave as is, else right half crystal half shape
                elif missing_processor == Processor.ROTATOR:
                    # if pins then leave as is, else right half crystal half shape
            case Variant.half_crystal:
                builder.blueprint.append((Variant.half_crystal, stack_top, {"layer": layer, "part": part}))
                if missing_processor == Processor.CRYSTALLIZER:
                    # (rotated) half
                elif missing_processor == Processor.MIXER:
                    # unmix
                elif missing_processor == Processor.CUTTER:
                    # full crystal
                elif missing_processor == Processor.ROTATOR:
                    # left half crystal half shape
            case Variant.half_half_crystal:
                builder.blueprint.append((Variant.half_half_crystal, stack_top,
                                          {"parts": (part_1, part_2), "layer": layer}))  # part 1 is top right
                if missing_processor == Processor.CRYSTALLIZER:
                    # if stacker then half half, elif any split then left/horizontal half, else single
                elif missing_processor == Processor.MIXER:
                    # unmix
                elif missing_processor == Processor.CUTTER:
                    # half half
                elif missing_processor == Processor.ROTATOR:
                    # left half crystal half shape
            case Variant.half_crystal_half_shape:
                builder.blueprint.append((Variant.half_crystal_half_shape, stack_top,
                                          {"parts": (part_1, part_2), "layer": layer}))  # parts are shape to crystal
                if missing_processor == Processor.CRYSTALLIZER:
                    # if not rotator then right half, elif stacker then half half, elif any split then corresponding half, else single
                elif missing_processor == Processor.PAINTER:
                    # unpaint
                elif missing_processor == Processor.MIXER:
                    # unmix
                elif missing_processor == Processor.CUTTER:
                    # full crystal
                elif missing_processor == Processor.ROTATOR:
                    # left half crystal half shape
            case Variant.cut_out_crystal:
                builder.blueprint.append((Variant.cut_out_crystal, {"ordered": ordered_parts}))
                if missing_processor == Processor.CRYSTALLIZER:
                    # cutter rotator stacker swapper pins =
                    # cutter rotator stacker swapper  =
                    # cutter rotator  swapper pins =
                    # cutter rotator  swapper  =
                elif missing_processor == Processor.MIXER:
                    # unmix
                elif missing_processor == Processor.CUTTER:
                    # rotator stacker swapper pins =
                    # rotator stacker swapper  =
                    # rotator  swapper pins =
                    # rotator  swapper  =
                elif missing_processor == Processor.ROTATOR:
                    # cutter stacker swapper pins =
                    # cutter stacker swapper  =
                    # cutter  swapper pins =
                    # cutter  swapper  =
                elif missing_processor == Processor.SWAPPER:
                    # cutter rotator stacker pins =
                    # cutter rotator stacker  =
                    # cutter rotator  pins =
                    # cutter rotator  =
            case Variant._3_1_crystals:
                builder.blueprint.append((Variant._3_1_crystals, {"ordered": ordered_parts}))
                if missing_processor == Processor.CRYSTALLIZER:
                    # cutter rotator stacker swapper pins =
                    # cutter rotator stacker swapper  =
                    # cutter rotator stacker pins  =
                    # cutter rotator  swapper pins =
                    # cutter rotator stacker   =
                    # cutter rotator  swapper  =
                    # cutter rotator pins  =
                    # cutter rotator   =
                elif missing_processor == Processor.MIXER:
                    # unmix
                elif missing_processor == Processor.CUTTER:
                    # rotator stacker swapper pins =
                    # rotator stacker swapper  =
                    # rotator stacker  pins =
                    # rotator  swapper pins =
                    # rotator stacker  =
                    # rotator  swapper  =
                    # rotator  pins =
                    # rotator  =
                elif missing_processor == Processor.ROTATOR:
                    # cutter stacker swapper pins =
                    # cutter stacker swapper  =
                    # cutter stacker  pins =
                    # cutter  swapper pins =
                    # cutter stacker  =
                    # cutter  swapper  =
                    # cutter  pins =
                    # cutter  =
            case Variant._3_crystals_1_shape:
                builder.blueprint.append((Variant._3_crystals_1_shape, {"ordered": ordered_parts}))
                if missing_processor == Processor.CRYSTALLIZER:
                    # cutter rotator stacker swapper pins =
                    # cutter rotator stacker swapper  =
                    # cutter rotator stacker pins  =
                    # cutter rotator  swapper pins =
                    # cutter rotator stacker   =
                    # cutter rotator  swapper  =
                    # cutter rotator pins  =
                    # cutter rotator   =
                elif missing_processor == Processor.PAINTER:
                    # unpaint
                elif missing_processor == Processor.MIXER:
                    # unmix
                elif missing_processor == Processor.CUTTER:
                    # rotator stacker swapper pins =
                    # rotator stacker swapper  =
                    # rotator stacker  pins =
                    # rotator  swapper pins =
                    # rotator stacker  =
                    # rotator  swapper  =
                    # rotator  pins =
                    # rotator  =
                elif missing_processor == Processor.ROTATOR:
                    # cutter stacker swapper pins =
                    # cutter stacker swapper  =
                    # cutter stacker  pins =
                    # cutter  swapper pins =
                    # cutter stacker  =
                    # cutter  swapper  =
                    # cutter  pins =
                    # cutter  =
            case Variant._3_shapes_1_crystal:
                builder.blueprint.append((Variant._3_shapes_1_crystal, {"ordered": ordered_parts}))
                if missing_processor == Processor.CRYSTALLIZER:
                    # cutter rotator stacker swapper pins =
                    # cutter rotator stacker swapper  =
                    # cutter rotator stacker pins  =
                    # cutter rotator  swapper pins =
                    # cutter rotator stacker   =
                    # cutter rotator  swapper  =
                    # cutter rotator pins  =
                    # cutter rotator   =
                elif missing_processor == Processor.PAINTER:
                    # unpaint
                elif missing_processor == Processor.MIXER:
                    # unmix
                elif missing_processor == Processor.CUTTER:
                    # rotator stacker swapper pins =
                    # rotator stacker swapper  =
                    # rotator stacker  pins =
                    # rotator  swapper pins =
                    # rotator stacker  =
                    # rotator  swapper  =
                    # rotator  pins =
                    # rotator  =
                elif missing_processor == Processor.ROTATOR:
                    # cutter stacker swapper pins =
                    # cutter stacker swapper  =
                    # cutter stacker  pins =
                    # cutter  swapper pins =
                    # cutter stacker  =
                    # cutter  swapper  =
                    # cutter  pins =
                    # cutter  =
                elif missing_processor == Processor.STACKER:
                    # cutter rotator swapper pins =
                    # cutter rotator swapper  =
                    # cutter rotator  pins =
                    # cutter rotator  =
                elif missing_processor == Processor.SWAPPER:
                    # cutter rotator stacker pins =
                    # cutter rotator stacker  =
                    # cutter rotator  pins =
                    # cutter rotator  =
            case Variant.cornered_crystal:
                builder.blueprint.append((Variant.cornered_crystal, {"half": ("--" + part)}))
                if missing_processor == Processor.CRYSTALLIZER:
                    # cutter rotator stacker swapper pins =
                    # cutter rotator stacker swapper  =
                    # cutter rotator  swapper pins =
                    # cutter rotator  swapper  =
                elif missing_processor == Processor.MIXER:
                    # unmix
                elif missing_processor == Processor.CUTTER:
                    # rotator stacker swapper pins =
                    # rotator stacker swapper  =
                    # rotator  swapper pins =
                    # rotator  swapper  =
                elif missing_processor == Processor.ROTATOR:
                    # cutter stacker swapper pins =
                    # cutter stacker swapper  =
                    # cutter  swapper pins =
                    # cutter  swapper  =
                elif missing_processor == Processor.SWAPPER:
                    # cutter rotator stacker pins =
                    # cutter rotator stacker  =
                    # cutter rotator  pins =
                    # cutter rotator  =
            case Variant.checkered_crystal:
                builder.blueprint.append((Variant.checkered_crystal,
                                          {"parts": (part_1, part_2)}))  # parts are up right and down right
                if missing_processor == Processor.CRYSTALLIZER:
                    # cutter rotator stacker swapper pins =
                    # cutter rotator stacker swapper  =
                    # cutter rotator  swapper pins =
                    # cutter rotator  swapper  =
                elif missing_processor == Processor.MIXER:
                    # unmix
                elif missing_processor == Processor.CUTTER:
                    # rotator stacker swapper pins =
                    # rotator stacker swapper  =
                    # rotator  swapper pins =
                    # rotator  swapper  =
                elif missing_processor == Processor.ROTATOR:
                    # cutter stacker swapper pins =
                    # cutter stacker swapper  =
                    # cutter  swapper pins =
                    # cutter  swapper  =
                elif missing_processor == Processor.SWAPPER:
                    # cutter rotator stacker pins =
                    # cutter rotator stacker  =
                    # cutter rotator  pins =
                    # cutter rotator  =
            case Variant.single:
                builder.blueprint.append((Variant.single, {"ordered": ordered_parts}))
                if missing_processor == Processor.CRYSTALLIZER:
                    # cutter rotator stacker swapper pins =
                    # cutter rotator stacker swapper  =
                    # cutter rotator stacker pins  =
                    # cutter rotator  swapper pins =
                    # cutter rotator stacker   =
                    # cutter rotator  swapper  =
                    # cutter rotator pins  =
                    # cutter rotator   =
                elif missing_processor == Processor.PAINTER:
                    # unpaint
                elif missing_processor == Processor.MIXER:
                    # unmix
                elif missing_processor == Processor.CUTTER:
                    # rotator stacker swapper pins =
                    # rotator stacker swapper  =
                    # rotator stacker  pins =
                    # rotator  swapper pins =
                    # rotator stacker  =
                    # rotator  swapper  =
                    # rotator  pins =
                    # rotator  =
                    # crystal rotator stacker swapper pins =
                    # crystal rotator stacker swapper  =
                    # crystal rotator stacker  pins =
                    # crystal rotator  swapper pins =
                    # crystal rotator stacker  =
                    # crystal rotator  swapper  =
                    # crystal rotator  pins =
                    # crystal rotator  =
                elif missing_processor == Processor.ROTATOR:
                    # crystal cutter stacker swapper pins =
                    # crystal cutter stacker swapper  =
                    # crystal cutter stacker  pins =
                    # crystal cutter  swapper pins =
                    # crystal cutter stacker  =
                    # crystal cutter  swapper  =
                    # crystal cutter  pins =
                    # crystal cutter  =
                    # cutter stacker swapper pins =
                    # cutter stacker swapper  =
                    # cutter stacker  pins =
                    # cutter  swapper pins =
                    # cutter stacker  =
                    # cutter  swapper  =
                    # cutter  pins =
                    # cutter  =
            case 128:  # 2/3/4 singles
                if missing_processor == Processor.CRYSTALLIZER:
                    # cutter rotator stacker swapper pins =
                    # cutter rotator stacker swapper  =
                    # cutter rotator stacker pins  =
                    # cutter rotator  swapper pins =
                    # cutter rotator stacker   =
                    # cutter rotator  swapper  =
                    # cutter rotator pins  =
                    # cutter rotator   =
                elif missing_processor == Processor.PAINTER:
                    # unpaint
                elif missing_processor == Processor.MIXER:
                    # unmix
                elif missing_processor == Processor.CUTTER:
                    # rotator stacker swapper pins =
                    # rotator stacker swapper  =
                    # rotator stacker  pins =
                    # rotator  swapper pins =
                    # rotator stacker  =
                    # rotator  swapper  =
                    # rotator  pins =
                    # rotator  =
                    # crystal rotator stacker swapper pins =
                    # crystal rotator stacker swapper  =
                    # crystal rotator stacker  pins =
                    # crystal rotator  swapper pins =
                    # crystal rotator stacker  =
                    # crystal rotator  swapper  =
                    # crystal rotator  pins =
                    # crystal rotator  =
                elif missing_processor == Processor.ROTATOR:
                    # crystal cutter stacker swapper pins =
                    # crystal cutter stacker swapper  =
                    # crystal cutter stacker  pins =
                    # crystal cutter  swapper pins =
                    # crystal cutter stacker  =
                    # crystal cutter  swapper  =
                    # crystal cutter  pins =
                    # crystal cutter  =
                    # cutter stacker swapper pins =
                    # cutter stacker swapper  =
                    # cutter stacker  pins =
                    # cutter  swapper pins =
                    # cutter stacker  =
                    # cutter  swapper  =
                    # cutter  pins =
                    # cutter  =
                elif missing_processor == Processor.STACKER:
                    # crystal cutter rotator swapper pins =
                    # crystal cutter rotator swapper  =
                    # crystal cutter rotator  pins =
                    # crystal cutter rotator  =
                    # cutter rotator swapper pins =
                    # cutter rotator swapper  =
                    # cutter rotator  pins =
                    # cutter rotator  =
                elif missing_processor == Processor.SWAPPER:
                    # crystal cutter rotator stacker pins =
                    # crystal cutter rotator stacker  =
                    # crystal cutter rotator  pins =
                    # crystal cutter rotator  =
                    # cutter rotator stacker pins =
                    # cutter rotator stacker  =
                    # cutter rotator  pins =
                    # cutter rotator  =
            case e:
                raise Exception(f"Unknown layer variant {e}:\nbuilder = {builder.debug_string()}")

    i = 0
    while i < len(builder.blueprint):
        blueprint_instr = builder.blueprint[i]
        if blueprint_instr[0] == 129:
            builder.blueprint.pop(i)
        else:
            i += 1
    return builder


def _downgrade_6(world: "Shapez2World", builder: ShapeBuilder, remaining_processors: list[Processor],
                 missing_processor: Processor, original_complexity: int) -> ShapeBuilder:
    from .generate_hexagonal import Variant


def _unpaint(remaining_processors: list[Processor], *,
             parts: Iterable[str] = None, long: str = None) -> Iterable[str] | str:
    ...


def _unmix(remaining_processors: list[Processor], replacements: dict[str, str], *,
           parts: Iterable[str] = None, long: str = None) -> Iterable[str] | str:
    ...
