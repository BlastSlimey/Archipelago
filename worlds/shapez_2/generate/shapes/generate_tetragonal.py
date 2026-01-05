from typing import TYPE_CHECKING

from . import Processor, ShapeBuilder

if TYPE_CHECKING:
    from ... import Shapez2World


_count = 0


def next_id(restart=False) -> int:
    global _count
    if restart:
        _count = 0
    _count += 1
    return _count - 1


class Variant:
    full = next_id(True)  # always
    half = next_id()  # cutter & 1 (+ rotator & (+1 | +2) for horizontal and left)
    half_half = next_id()  # (swapper & 1) | (cutter & rotator & stacker & 5) (+ rotator & +1 for horizontal)
    cut_out = next_id()  # cutter & rotator & ((stacker & 5) | (swapper & 3))
    _3_1 = next_id()  # rotator & ((cutter & stacker & 11) | (swapper & 3))
    cornered = next_id()  # cutter & rotator & ((stacker & 8) | (swapper & 5))
    random_shapes_1_color = next_id()  # rotator & ((cutter & stacker & 17) | (swapper & 5))
    checkered = next_id()  # rotator & ((cutter & stacker & 9) | (swapper & 4))
    random_colors_1_shape = next_id()  # rotator & ((cutter & stacker & 17) | (swapper & 5)) & painter & +1
    pins = next_id()  # pins

    begin_crystals = next_id()

    full_crystal = next_id()  # crystal & ((pins & 1) | (cutter & rotator & 6))
    half_crystal = next_id()  # crystal & cutter & rotator & 5
    half_half_crystal = next_id()  # crystal & cutter & rotator & 6 (+1 for horizontal)
    half_crystal_half_shape = next_id()  # crystal & cutter & 2 (+ rotator & (+1 | +2) for horizontal and right crystal)
    cut_out_crystal = next_id()  # (crystal & cutter & rotator & swapper & 8)
    _3_1_crystals = next_id()  # (crystal & cutter & rotator & 8)
    _3_crystals_1_shape = next_id()  # (crystal & cutter & rotator & 4)
    _3_shapes_1_crystal = next_id()  # crystal & cutter & rotator & ((stacker & 7) | (swapper & 4))
    cornered_crystal = next_id()  # (crystal & cutter & rotator & swapper & 13)
    checkered_crystal = next_id()  # (crystal & cutter & rotator & swapper & 11)

    end_crystals = next_id()

    # Can have crystals, but not necessary
    single = next_id()  # cutter & rotator & 3 (+ crystal & 6)
    _2_singles = next_id()  # cutter & rotator & ((stacker & 6) | (swapper & 5) )
                            # (+ crystal & 4 & not already has crystals)
    _3_singles = next_id()  # cutter & rotator & ((stacker & 11) | (swapper & 5) )
                            # (+ crystal & ((7 & swapper) | (9 & stacker)) & not already has crystals)
    _4_singles = next_id()  # rotator & ((cutter & stacker & 15) | (swapper & 5))
                            # (+ crystal & ((6 & swapper) | (13 & stacker)))

    end = next_id()


def generate_layer(world: "Shapez2World", complexity: int, builder: ShapeBuilder, important: bool) -> None:

    if important and (sum(builder.tasked) > complexity or (
        sum(builder.tasked) + 1 > complexity and builder.tasked[Processor.ROTATOR] and (
            not builder.tasked[Processor.CUTTER] or not builder.tasked[Processor.SWAPPER]
        )
    )):
        raise Exception(f"Too low complexity ({complexity}) "
                        f"for important processors {', '.join(str(i) for i in range(8) if builder.tasked[i])}")

    has_vertical_split = any(layer[0:2] != layer[6:8] or layer[2:4] != layer[4:6] for layer in builder.shape)
    has_horizontal_split = any(layer[0:2] != layer[2:4] or layer[6:8] != layer[4:6] for layer in builder.shape)
    if has_horizontal_split and has_vertical_split:
        builder.tasked[Processor.ROTATOR] = False

    # Decide on the layer variant, but consider that mixer and/or painter might be important
    stored_complexity = 0
    if important:
        if builder.tasked[Processor.MIXER]:
            if Processor.CRYSTALLIZER in builder:
                stored_complexity = 1
            else:
                stored_complexity = 2
        elif builder.tasked[Processor.PAINTER]:
            stored_complexity = 1
    complexity -= stored_complexity

    while True:
        # Calculate what's possible with available processors
        # IMPORTANT: do not make anything false before this
        variants = [False] * Variant.end
        variants[Variant.full] = True
        if Processor.PIN_PUSHER in builder:
            variants[Variant.pins] = True
            if Processor.CRYSTALLIZER in builder and complexity:
                variants[Variant.full_crystal] = True
        if Processor.CRYSTALLIZER in builder and Processor.CUTTER in builder and complexity >= 2:
            variants[Variant.half_crystal_half_shape] = True
            if Processor.ROTATOR in builder and complexity >= 4:
                _bulk_possible(variants, complexity, (Variant._3_crystals_1_shape, ), (Variant.half_crystal, 5),
                               (Variant.full_crystal, 6), (Variant.half_half_crystal, 6), (Variant._3_1_crystals, 8))
                if not builder.has_crystals:
                    variants[Variant._2_singles] = True
                    if Processor.STACKER in builder and complexity >= 9:
                        variants[Variant._3_singles] = True
                if Processor.STACKER in builder and complexity >= 7:
                    _bulk_possible(variants, complexity, (Variant._3_shapes_1_crystal, ), (Variant._4_singles, 13))
                if Processor.SWAPPER in builder:  # and complexity >= 4 from outer scope
                    _bulk_possible(variants, complexity, (Variant._3_shapes_1_crystal, ), (Variant.cut_out_crystal, 8),
                                   (Variant.checkered_crystal, 11), (Variant.cornered_crystal, 13))
        if Processor.CUTTER in builder and complexity:
            variants[Variant.half] = True
            if Processor.ROTATOR in builder and complexity >= 3:
                variants[Variant.single] = True
                if Processor.STACKER in builder and complexity >= 5:
                    _bulk_possible(variants, complexity, (Variant.half_half, Variant.cut_out, ),
                                   (Variant._2_singles, 6), (Variant.cornered, 8), (Variant.checkered, 9),
                                   (Variant._3_singles, 11), (Variant._3_1, 11), (Variant._4_singles, 15),
                                   (Variant.random_shapes_1_color, 17))
                    if Processor.PAINTER in builder and complexity >= 18:
                        variants[Variant.random_colors_1_shape] = True
                if Processor.SWAPPER in builder:  # and complexity >= 3 from outer scope
                    _bulk_possible(variants, complexity, (Variant.cut_out, ), (Variant.cornered, 5),
                                   (Variant._2_singles, 5), (Variant._3_singles, 5), (Variant._4_singles, 5), )
        if Processor.SWAPPER in builder and complexity:
            variants[Variant.half_half] = True
            if Processor.ROTATOR in builder and complexity >= 3:
                _bulk_possible(variants, complexity, (Variant._3_1, ), (Variant.checkered, 4), (Variant._4_singles, 5),
                               (Variant.random_shapes_1_color, 5))
                if Processor.PAINTER in builder and complexity >= 6:
                    variants[Variant.random_colors_1_shape] = True

        def _bulk_remove(v: tuple[int, ...], *vc: tuple[int, int]):
            for vv in v:
                variants[vv] = False
            for vv, cc in vc:
                if complexity < cc:
                    variants[vv] = False
                else:
                    break

        # Remove everything that doesn't have the important buildings
        if important:
            if any(builder.tasked):
                if builder.tasked[Processor.CUTTER]:
                    _bulk_remove((Variant.full, Variant.pins, ))
                    if Processor.SWAPPER in builder:
                        _bulk_remove((Variant.half_half, Variant._3_1, Variant.checkered, Variant._4_singles,
                                      Variant.random_colors_1_shape, Variant.random_shapes_1_color, ))
                    if Processor.PIN_PUSHER in builder:
                        variants[Variant.full_crystal] = False
                if builder.tasked[Processor.ROTATOR]:
                    _bulk_remove((Variant.full, Variant.pins), (Variant.half, 2), (Variant.half_crystal_half_shape, 3))
                    if Processor.SWAPPER in builder:
                        variants[Variant.half_half] = False
                    if Processor.PIN_PUSHER in builder:
                        variants[Variant.full_crystal] = False
                if builder.tasked[Processor.STACKER]:
                    # Should only happen in single layers
                    _bulk_remove((Variant.half, Variant.pins, Variant.full, Variant.full_crystal,
                                  Variant.half_crystal, Variant.half_half_crystal, Variant.half_crystal_half_shape,
                                  Variant.cut_out_crystal, Variant._3_1_crystals, Variant._3_crystals_1_shape,
                                  Variant.cornered_crystal, Variant.checkered_crystal, Variant.single, ))
                    # Do not remove things that are also able with swapper, else everything would be False
                    if sum(builder.tasked) == 1:
                        variants[Variant.full] = True
                if builder.tasked[Processor.PAINTER]:
                    # Painters don't have anything to do with crystallizers,
                    # so make sure you can paint something if needed
                    # Also this is a case where full layer is useful
                    _bulk_remove((Variant.full_crystal, Variant.half_crystal, Variant.half_half_crystal,
                                  Variant.cut_out_crystal, Variant._3_1_crystals, Variant.cornered_crystal,
                                  Variant.checkered_crystal, Variant.pins, ))
                if builder.tasked[Processor.PIN_PUSHER]:
                    temp = (variants[Variant.pins], variants[Variant.full_crystal])
                    variants[:] = [False] * len(variants)
                    variants[Variant.pins], variants[Variant.full_crystal] = temp
                if builder.tasked[Processor.CRYSTALLIZER]:
                    for x in range(0, Variant.begin_crystals):
                        variants[x] = False
                    if complexity < 6:
                        variants[Variant.single] = False
                    if complexity < 4 or builder.has_crystals:
                        variants[Variant._2_singles] = False
                    if builder.has_crystals or ((Processor.SWAPPER not in builder or complexity < 7) and
                                                (Processor.STACKER not in builder or complexity < 9)):
                        variants[Variant._3_singles] = False
                    if Processor.CUTTER not in builder or ((Processor.SWAPPER not in builder or complexity < 6) and
                                                           (Processor.STACKER not in builder or complexity < 13)):
                        variants[Variant._4_singles] = False
                if builder.tasked[Processor.SWAPPER]:
                    _bulk_remove((Variant.full, Variant.half, Variant.pins, Variant.single, Variant._3_1_crystals,
                                  Variant.half_crystal, Variant.half_half_crystal, Variant.half_crystal_half_shape,
                                  Variant._3_crystals_1_shape, Variant.full_crystal, ))
                    if Processor.STACKER in builder:
                        _bulk_remove((Variant.cut_out, Variant.cornered, Variant._3_shapes_1_crystal,
                                      Variant._3_singles, Variant._2_singles, ))
                        if Processor.CUTTER in builder:
                            _bulk_remove((Variant._3_1, Variant.random_shapes_1_color, Variant.checkered,
                                          Variant._4_singles, Variant.random_colors_1_shape, ))
                            if Processor.ROTATOR in builder:
                                variants[Variant.half_half] = False

        # Remove some things that are impossible due to shape context
        if builder.has_crystals:
            # Putting new layers with crystal on top of or under other crystals is tricky since the swapper
            # can destroy other layers
            if Processor.PIN_PUSHER not in builder:
                variants[Variant.full_crystal] = False
            _bulk_remove((Variant.half_crystal, Variant.half_half_crystal, Variant.cut_out_crystal,
                          Variant.cornered_crystal, Variant.checkered_crystal, Variant._3_1_crystals, ))
        if not len(builder.shape):
            variants[Variant.pins] = False

        # Remove some low complexity variants if high complexity given
        if not important and complexity >= 16:
            _bulk_remove((Variant.cut_out, Variant._3_crystals_1_shape, Variant.checkered))
            if Processor.CUTTER in builder and Processor.ROTATOR in builder:
                variants[Variant.half] = False
                if Processor.STACKER in builder or Processor.SWAPPER in builder:
                    variants[Variant.half_half] = False
                if Processor.SWAPPER in builder:
                    variants[Variant._3_1] = False
                if Processor.CRYSTALLIZER in builder:
                    variants[Variant.half_crystal_half_shape] = False
            if sum(variants) > 1:
                variants[Variant.full] = False

        # If none available anymore, try to save it in some way
        if not any(variants):
            if complexity <= sum(builder.tasked) + 1:  # Maybe complexity was too restrictive
                complexity += 3
            elif not any(builder.tasked):  # If nothing tasked, then a full layer doesn't do anything
                variants[Variant.full] = True
            else:  # Last resort, maybe a very bad combination?
                builder.tasked[world.random.choice([x for x in range(8) if builder.tasked[x]])] = False
            continue
        break

    # Restore complexity for painting and mixing
    complexity += stored_complexity

    def _tasked_sw_st(swc: int, stc: int, need_cu: bool):
        nonlocal complexity
        if Processor.SWAPPER in builder:
            complexity -= swc
            if Processor.STACKER not in builder or (Processor.CUTTER not in builder and not need_cu):
                builder.tasked[Processor.SWAPPER] = False
        else:
            complexity -= stc
            builder.tasked[Processor.STACKER] = False
            builder.tasked[Processor.CUTTER] = False if not need_cu else builder.tasked[Processor.CUTTER]
        builder.tasked[Processor.CUTTER] = False if need_cu else builder.tasked[Processor.CUTTER]
        builder.tasked[Processor.ROTATOR] = False

    def _bulk_tasked(comp: int, *t: Processor):
        nonlocal complexity
        complexity -= comp
        for tt in t:
            builder.tasked[tt] = False

    def _2_parts(c1: bool, c2: bool, no_same: bool) -> tuple[str, str]:
        nonlocal complexity
        complexity_1 = world.random.triangular(0, complexity).__int__()
        complexity -= complexity_1
        p1 = generate_shape(world) + generate_color(
            world, complexity_1, False, builder, important
        ) if not c1 else "c" + generate_color(world, complexity_1, True, builder, important)
        p2 = generate_shape(world) + generate_color(
            world, complexity, False, builder, important
        ) if not c2 else "c" + generate_color(world, complexity, True, builder, important)
        if no_same and p1 == p2:
            p2 = generate_shape(world, p2[0]) + p2[1] if not c2 else "c" + generate_color(
                world, complexity, True, builder, important, p2[1]
            )
        return p1, p2

    variant_pool = [x for x in variants if variants[x]]
    match world.random.choice(variant_pool):
        case Variant.full:
            part = generate_shape(world) + generate_color(
                world, complexity, False, builder, important
            )
            stack_top = stack(world, builder, part * 4, True, 0)
            builder.blueprint.append((Variant.full, stack_top, {"part": part}))
        case Variant.half:
            complexity -= 1
            builder.tasked[Processor.CUTTER] = False
            complexity_color = world.random.randint(0, complexity)
            complexity -= complexity_color
            part = generate_shape(world) + generate_color(
                world, complexity_color, False, builder, important
            )
            direction = 0
            if builder.tasked[Processor.ROTATOR]:
                direction = 2 if has_horizontal_split else world.random.choice((1, 3))
            elif Processor.ROTATOR in builder:
                possible = [0] if not complexity else ([0, 1, 3] if complexity < 2 else [0, 1, 2, 3])
                direction = world.random.choice(possible)
            layer = [part * 2 + "----", "--" + part * 2 + "--", "----" + part * 2, part + "----" + part][direction]
            stack_top = stack(world, builder, layer, True, 0)
            builder.blueprint.append((Variant.half, stack_top, {"layer": layer, "part": part}))
        case Variant.half_half:
            if Processor.SWAPPER in builder:
                complexity -= 1
                if not builder.has_all(Processor.CUTTER, Processor.ROTATOR, Processor.STACKER):
                    builder.tasked[Processor.SWAPPER] = False
            else:
                _bulk_tasked(5, Processor.CUTTER, Processor.ROTATOR, Processor.STACKER)
            part_1, part_2 = _2_parts(False, False, True)
            direction = 0
            if builder.tasked[Processor.ROTATOR]:
                direction = 0 if has_horizontal_split else 1
            elif Processor.ROTATOR in builder:
                possible = [0, 1] if (builder.has_all(Processor.CUTTER, Processor.ROTATOR, Processor.STACKER)
                                      or complexity) else [0]
                direction = world.random.choice(possible)
            layer = [part_1 * 2 + part_2 * 2, part_1 + part_2 * 2 + part_1][direction]
            stack_top = stack(world, builder, layer, True, 0)
            builder.blueprint.append((Variant.half_half, stack_top,
                                      {"parts": (part_1, part_2), "layer" : layer}))  # part 1 is top right
        case Variant.cut_out:
            _tasked_sw_st(3, 5, True)
            part = generate_shape(world) + generate_color(
                world, complexity, False, builder, important
            )
            ordered_parts = [part, part, part, "--"]
            world.random.shuffle(ordered_parts)
            stack_top = stack(world, builder, "".join(ordered_parts), True, 0)
            builder.blueprint.append((Variant.cut_out, stack_top, {"ordered": ordered_parts}))
        case Variant._3_1:
            _tasked_sw_st(3, 11, False)
            part_1, part_2 = _2_parts(False, False, True)
            ordered_parts = [part_1, part_1, part_1, part_2]
            world.random.shuffle(ordered_parts)
            stack_top = stack(world, builder, "".join(ordered_parts), True, 0)
            builder.blueprint.append((Variant._3_1, stack_top, {"ordered": ordered_parts}))
        case Variant.cornered:
            _tasked_sw_st(5, 8, True)
            part = generate_shape(world) + generate_color(
                world, complexity, False, builder, important
            )
            if world.random.random() < 0.5:
                stack_top = stack(world, builder, (part + "--") * 2, True, 0)
                builder.blueprint.append((Variant.cornered, stack_top, {"half": (part, "--")}))
            else:
                stack_top = stack(world, builder, ("--" + part) * 2, True, 0)
                builder.blueprint.append((Variant.cornered, stack_top, {"half": ("--", part)}))
        case Variant.random_shapes_1_color:
            _tasked_sw_st(5, 17, False)
            color = generate_color(
                world, complexity, False, builder, important
            )
            ordered_parts = [generate_shape(world)]
            ordered_parts.append(generate_shape(world, ordered_parts[-1]))
            ordered_parts.append(generate_shape(world, ordered_parts[-1]))
            ordered_parts.append(generate_shape(world, ordered_parts[-1]))
            world.random.shuffle(ordered_parts)
            stack_top = stack(world, builder, "".join(p + color for p in ordered_parts), True, 0)
            builder.blueprint.append((Variant.random_shapes_1_color, stack_top,
                                      {"ordered": ordered_parts, "color": color}))
        case Variant.checkered:
            _tasked_sw_st(4, 9, False)
            part_1, part_2 = _2_parts(False, False, True)
            stack_top = stack(world, builder, (part_1 + part_2) * 2, True, 0)
            builder.blueprint.append((Variant.checkered, stack_top,
                                      {"parts": (part_1, part_2)}))  # parts are up right and down right
        case Variant.random_colors_1_shape:
            # Assumes the painter is available and at least one more complexity is still available
            _tasked_sw_st(5, 17, False)
            shape_part = generate_shape(world)
            comp_1 = world.random.triangular(0, complexity).__int__()
            comp_2 = world.random.triangular(0, complexity - comp_1).__int__()
            comp_3 = world.random.triangular(0, complexity - comp_1 - comp_2).__int__()
            complexity -= comp_1 + comp_2 + comp_3
            ordered_colors = [generate_color(world, complexity, False, builder, important)]
            ordered_colors.append(generate_color(
                world, comp_1, False, builder, important, ordered_colors[-1]
            ))
            ordered_colors.append(generate_color(
                world, comp_2, False, builder, important, ordered_colors[-1]
            ))
            ordered_colors.append(generate_color(
                world, comp_3, False, builder, important, ordered_colors[-1]
            ))
            world.random.shuffle(ordered_colors)
            stack_top = stack(world, builder, "".join(shape_part + c for c in ordered_colors), True, 0)
            builder.blueprint.append((Variant.random_colors_1_shape, stack_top,
                                      {"ordered": ordered_colors, "shape": shape_part}))
        case Variant.pins:
            builder.tasked[Processor.PIN_PUSHER] = False
            part = ""
            for i in range(0, 8, 2):
                part += "P-" if builder.shape[0][i] != "-" else "--"
            builder.shape.insert(0, part)
            builder.blueprint.append((Variant.pins, False, {}))
        case Variant.full_crystal:
            # Assumes either has pin pusher or not builder.has_crystals
            # Needs extra handling because of that
            if Processor.PIN_PUSHER in builder and builder.has_crystals:
                complexity -= 1
                if Processor.ROTATOR not in builder or Processor.CUTTER not in builder:
                    builder.tasked[Processor.PIN_PUSHER] = False
            else:
                _bulk_tasked(6, Processor.CUTTER, Processor.ROTATOR)
            builder.tasked[Processor.CRYSTALLIZER] = False
            part = "c" + generate_color(world, complexity, True, builder, important)
            if builder.has_crystals:
                fill_crystal(builder, part[1])
            builder.shape.insert(0, part * 4)
            builder.has_crystals = True
            builder.blueprint.append((Variant.full_crystal, False, {"part": part}))
        case Variant.half_crystal:
            # Assumes this doesn't happen when already_has_crystals
            _bulk_tasked(5, Processor.CUTTER, Processor.ROTATOR, Processor.CRYSTALLIZER)
            complexity_color = world.random.randint(0, complexity)
            complexity -= complexity_color
            part = "c" + generate_color(world, complexity_color, True, builder, important)
            possible_positions = [part * 2 + "----"]
            if complexity:
                possible_positions.extend([part + "----" + part, "--" + part * 2 + "--"])
                if complexity >= 2:
                    possible_positions.append("----" + part * 2)
            layer = world.random.choice(possible_positions)
            stack_top = stack(world, builder, layer, False, 1)
            builder.blueprint.append((Variant.half_crystal, stack_top, {"layer": layer, "part": part}))
        case Variant.half_half_crystal:
            # Assumes this doesn't happen when already_has_crystals
            _bulk_tasked(6, Processor.CUTTER, Processor.ROTATOR, Processor.CRYSTALLIZER)
            part_1, part_2 = _2_parts(True, True, True)
            layer = world.random.choice((part_1 * 2 + part_2 * 2, part_1 + part_2 * 2 + part_1))
            stack_top = stack(world, builder, layer, False, 2)
            builder.blueprint.append((Variant.half_half_crystal, stack_top,
                                      {"parts": (part_1, part_2), "layer": layer}))  # part 1 is top right
        case Variant.half_crystal_half_shape:
            _bulk_tasked(2, Processor.CUTTER, Processor.CRYSTALLIZER)
            part_1, part_2 = _2_parts(False, True, False)
            direction = 0
            if builder.tasked[Processor.ROTATOR]:
                direction = 2 if has_horizontal_split else world.random.choice((1, 3))
            elif Processor.ROTATOR in builder:
                possible = [0] if not complexity else ([0, 1, 3] if complexity < 2 else [0, 1, 2, 3])
                direction = world.random.choice(possible)
            layer = [part_1 * 2 + part_2 * 2, part_2 + part_1 * 2 + part_2,
                     part_2 * 2 + part_1 * 2, part_1 + part_2 * 2 + part_1][direction]
            stack_top = stack(world, builder, layer, True, 1)
            builder.blueprint.append((Variant.half_crystal_half_shape, stack_top,
                                      {"parts": (part_1, part_2), "layer": layer}))  # parts are shape to crystal
        case Variant.cut_out_crystal:
            # Assumes this doesn't happen when already_has_crystals
            _bulk_tasked(8, Processor.CUTTER, Processor.ROTATOR, Processor.CRYSTALLIZER, Processor.SWAPPER)
            part = "c" + generate_color(world, complexity, True, builder, important)
            ordered_parts = [part, part, part, "--"]
            world.random.shuffle(ordered_parts)
            stack_top = stack(world, builder, "".join(ordered_parts), False, 1)
            builder.blueprint.append((Variant.cut_out_crystal, stack_top, {"ordered": ordered_parts}))
        case Variant._3_1_crystals:
            # Assumes this doesn't happen when already_has_crystals
            _bulk_tasked(8, Processor.CUTTER, Processor.ROTATOR, Processor.CRYSTALLIZER)
            part_1, part_2 = _2_parts(True, True, True)
            ordered_parts = [part_1, part_1, part_1, part_2]
            world.random.shuffle(ordered_parts)
            stack_top = stack(world, builder, "".join(ordered_parts), False, 2)
            builder.blueprint.append((Variant._3_1_crystals, stack_top, {"ordered": ordered_parts}))
        case Variant._3_crystals_1_shape:
            _bulk_tasked(4, Processor.CUTTER, Processor.ROTATOR, Processor.CRYSTALLIZER)
            part_1, part_2 = _2_parts(False, True, False)
            ordered_parts = [part_1, part_2, part_2, part_2]
            world.random.shuffle(ordered_parts)
            stack_top = stack(world, builder, "".join(ordered_parts), True, 1)
            builder.blueprint.append((Variant._3_crystals_1_shape, stack_top, {"ordered": ordered_parts}))
        case Variant._3_shapes_1_crystal:
            _tasked_sw_st(4, 7, True)
            builder.tasked[Processor.CRYSTALLIZER] = False
            part_1, part_2 = _2_parts(False, True, False)
            ordered_parts = [part_1, part_1, part_1, part_2]
            world.random.shuffle(ordered_parts)
            stack_top = stack(world, builder, "".join(ordered_parts), True, 1)
            builder.blueprint.append((Variant._3_shapes_1_crystal, stack_top, {"ordered": ordered_parts}))
        case Variant.cornered_crystal:
            # Assumes this doesn't happen when already_has_crystals
            _bulk_tasked(13, Processor.CUTTER, Processor.ROTATOR, Processor.CRYSTALLIZER, Processor.SWAPPER)
            part = "c" + generate_color(world, complexity, True, builder, important)
            if world.random.random() < 0.5:
                stack_top = stack(world, builder, (part + "--") * 2, False, 1)
                builder.blueprint.append((Variant.cornered_crystal, stack_top, {"half": (part, "--")}))
            else:
                stack_top = stack(world, builder, ("--" + part) * 2, False, 1)
                builder.blueprint.append((Variant.cornered_crystal, stack_top, {"half": ("--" + part)}))
        case Variant.checkered_crystal:
            # Assumes this doesn't happen when already_has_crystals
            _bulk_tasked(11, Processor.CUTTER, Processor.ROTATOR, Processor.CRYSTALLIZER, Processor.SWAPPER)
            part_1, part_2 = _2_parts(True, True, True)
            stack_top = stack(world, builder, (part_1 + part_2) * 2, False, 2)
            builder.blueprint.append((Variant.checkered_crystal, stack_top,
                                      {"parts": (part_1, part_2)}))  # parts are up right and down right
        case Variant.single:
            _bulk_tasked(0, Processor.CUTTER, Processor.ROTATOR)
            if Processor.CRYSTALLIZER in builder and complexity >= 7 and not builder.has_crystals:
                complexity -= 7
                builder.tasked[Processor.CRYSTALLIZER] = False
                part = "c" + generate_color(world, complexity, True, builder, important)
                a = (False, 1)
            else:
                complexity -= 3
                part = generate_shape(world) + generate_color(
                    world, complexity, False, builder, important
                )
                a = (True, 0)
            ordered_parts = [part, "--", "--", "--"]
            world.random.shuffle(ordered_parts)
            stack_top = stack(world, builder, "".join(ordered_parts), *a)
            builder.blueprint.append((Variant.single, stack_top, {"ordered": ordered_parts}))
        case Variant._2_singles:
            generate_2_shapes(world, complexity, builder, important)
        case Variant._3_singles:
            generate_3_shapes(world, complexity, builder, important)
        case Variant._4_singles:
            generate_4_shapes(world, complexity, builder, important)
        case e:
            raise Exception(f"Unknown layer variant {e}:\n"
                            f"complexity = {complexity}, important = {important},\n"
                            f"builder = {builder.debug_string()}\n"
                            f"has vertical split = {has_vertical_split}, "
                            f"has horizontal split = {has_horizontal_split},\n"
                            f"variant pool = {variant_pool}")


def generate_2_shapes(world: "Shapez2World", complexity: int, builder: ShapeBuilder, important: bool) -> None:
    builder.tasked[Processor.CUTTER] = False
    builder.tasked[Processor.ROTATOR] = False

    # Decide on the layer variant, but consider that mixer and/or painter might be important
    stored_complexity = 0
    if important:
        if builder.tasked[Processor.MIXER]:
            if Processor.CRYSTALLIZER in builder:
                stored_complexity = 1
            else:
                stored_complexity = 2
        elif builder.tasked[Processor.PAINTER]:
            stored_complexity = 1
    complexity -= stored_complexity

    subvariants = [False] * 6
    if Processor.CRYSTALLIZER in builder and complexity >= 4 and not builder.has_crystals:
        subvariants[4] = True
        if Processor.STACKER in builder and complexity >= 12:
            subvariants[5] = True
        if Processor.SWAPPER in builder and complexity >= 9:
            _bulk_possible(subvariants, complexity, (5, ), (3, 16), (2, 17))
    if Processor.SWAPPER in builder and complexity >= 3:
        _bulk_possible(subvariants, complexity, (0, ), (1, 5))
    if Processor.STACKER in builder and complexity >= 5:
        _bulk_possible(subvariants, complexity, (0, ), (1, 9))
    if important:
        if builder.tasked[Processor.PAINTER]:
            subvariants[2:4] = [False] * 2
        if builder.tasked[Processor.CRYSTALLIZER]:
            subvariants[:2] = [False] * 2

    # Restore complexity for painting and mixing
    complexity += stored_complexity

    subvariant_pool = list(x for x in range(6) if subvariants[x])
    match subvariant_pool:
        case 0:
            _subvariant(world, builder, important, complexity,
                        True, 3, 5, False, False, None, None, 2, True, 0)
        case 1:
            _subvariant(world, builder, important, complexity,
                        True, 5, 9, False, False, None, None, 3, True, 0)
        case 2:
            complexity -= 16
            builder.tasked[Processor.SWAPPER] = False
            builder.tasked[Processor.CRYSTALLIZER] = False
            _subvariant(world, builder, important, complexity,
                        False, 0, 0, True, True, None, None, 2, False, 2)
        case 3:
            complexity -= 17
            builder.tasked[Processor.SWAPPER] = False
            builder.tasked[Processor.CRYSTALLIZER] = False
            _subvariant(world, builder, important, complexity,
                        False, 0, 0, True, True, None, None, 3, False, 2)
        case 4:
            complexity -= 4
            builder.tasked[Processor.CRYSTALLIZER] = False
            _subvariant(world, builder, important, complexity,
                        False, 0, 0, False, True, None, None, 2, True, 1)
        case 5:
            builder.tasked[Processor.CRYSTALLIZER] = False
            _subvariant(world, builder, important, complexity,
                        True, 9, 12, False, True, None, None, 3, True, 1)


def generate_3_shapes(world: "Shapez2World", complexity: int, builder: ShapeBuilder, important: bool) -> None:
    builder.tasked[Processor.CUTTER] = False
    builder.tasked[Processor.ROTATOR] = False

    # Decide on the layer variant, but consider that mixer and/or painter might be important
    stored_complexity = 0
    if important:
        if builder.tasked[Processor.MIXER]:
            if Processor.CRYSTALLIZER in builder:
                stored_complexity = 1
            else:
                stored_complexity = 2
        elif builder.tasked[Processor.PAINTER]:
            stored_complexity = 1
    complexity -= stored_complexity

    subvariants = [False] * 6
    if Processor.CRYSTALLIZER in builder and complexity >= 7 and not builder.has_crystals:
        if Processor.SWAPPER in builder:
            _bulk_possible(subvariants, complexity, (1, 2, ), (4, 9), (3, 10), (5, 13))
        if Processor.STACKER in builder and complexity >= 9:
            _bulk_possible(subvariants, complexity, (2, ), (1, 10), (3, 13))
    if Processor.SWAPPER in builder and complexity >= 8:
        subvariants[0] = True
    if Processor.STACKER in builder and complexity >= 12:
        subvariants[0] = True
    if important:
        if builder.tasked[Processor.PAINTER]:
            subvariants[5] = False
        if builder.tasked[Processor.CRYSTALLIZER]:
            subvariants[0] = False

    # Restore complexity for painting and mixing
    complexity += stored_complexity

    subvariant_pool = list(x for x in range(6) if subvariants[x])
    match subvariant_pool:
        case 0:
            _subvariant(world, builder, important, complexity,
                        True, 8, 12, False, False, False, None, 1, True, 0)
        case 1:
            builder.tasked[Processor.CRYSTALLIZER] = False
            _subvariant(world, builder, important, complexity,
                        True, 7, 10, False, False, True, None, 2, True, 1)
        case 2:
            builder.tasked[Processor.CRYSTALLIZER] = False
            _subvariant(world, builder, important, complexity,
                        True, 7, 9, False, False, True, None, 3, True, 1)
        case 3:
            builder.tasked[Processor.CRYSTALLIZER] = False
            _subvariant(world, builder, important, complexity,
                        True, 10, 13, True, True, False, None, 2, True, 2)
        case 4:
            complexity -= 9
            builder.tasked[Processor.CRYSTALLIZER] = False
            builder.tasked[Processor.SWAPPER] = False
            _subvariant(world, builder, important, complexity,
                        False, 0, 0, True, True, False, None, 3, True, 2)
        case 5:
            complexity -= 13
            builder.tasked[Processor.CRYSTALLIZER] = False
            builder.tasked[Processor.SWAPPER] = False
            _subvariant(world, builder, important, complexity,
                        False, 0, 0, True, True, True, None, 1, False, 3)


def generate_4_shapes(world: "Shapez2World", complexity: int, builder: ShapeBuilder, important: bool) -> None:
    builder.tasked[Processor.ROTATOR] = False

    # Decide on the layer variant, but consider that mixer and/or painter might be important
    stored_complexity = 0
    if important:
        if builder.tasked[Processor.MIXER]:
            if Processor.CRYSTALLIZER in builder:
                stored_complexity = 1
            else:
                stored_complexity = 2
        elif builder.tasked[Processor.PAINTER]:
            stored_complexity = 1
    complexity -= stored_complexity

    subvariants = [False] * 6
    if (
        Processor.CRYSTALLIZER in builder and Processor.CUTTER in builder and
        complexity >= 6
    ):
        if Processor.SWAPPER in builder:
            subvariants[1] = True
            if not builder.has_crystals:
                _bulk_possible(subvariants, complexity, (), (2, 7), (3, 10), (4, 10), (5, 13))
        if Processor.STACKER in builder and complexity >= 10:
            _bulk_possible(subvariants, complexity, (), (1, 13))
            if not builder.has_crystals:
                _bulk_possible(subvariants, complexity, (3, ), (4, 13), (2, 16))
    if Processor.SWAPPER in builder and complexity >= 5:
        subvariants[0] = True
    if Processor.STACKER in builder and Processor.CUTTER in builder and complexity >= 15:
        subvariants[0] = True
    if important:
        if builder.tasked[Processor.PAINTER]:
            subvariants[5] = False
        if builder.tasked[Processor.CRYSTALLIZER]:
            subvariants[0] = False

    # Restore complexity for painting and mixing
    complexity += stored_complexity

    subvariant_pool = list(x for x in range(6) if subvariants[x])
    match subvariant_pool:
        case 0:
            if Processor.SWAPPER in builder:
                complexity -= 5
                if Processor.STACKER not in builder:
                    builder.tasked[Processor.SWAPPER] = False
            else:
                complexity -= 15
                builder.tasked[Processor.STACKER] = False
                builder.tasked[Processor.CUTTER] = False
            _subvariant(world, builder, important, complexity,
                        False, 0, 0, False, False, False, False, 0, True, 0)
        case 1:
            builder.tasked[Processor.CRYSTALLIZER] = False
            builder.tasked[Processor.CUTTER] = False
            _subvariant(world, builder, important, complexity,
                        True, 6, 13, False, False, False, True, 1, True, 1)
        case 2:
            builder.tasked[Processor.CRYSTALLIZER] = False
            builder.tasked[Processor.CUTTER] = False
            _subvariant(world, builder, important, complexity,
                        True, 7, 16, False, False, True, True, 2, True, 2)
        case 3:
            builder.tasked[Processor.CRYSTALLIZER] = False
            builder.tasked[Processor.CUTTER] = False
            _subvariant(world, builder, important, complexity,
                        True, 7, 10, False, False, True, True, 3, True, 2)
        case 4:
            builder.tasked[Processor.CRYSTALLIZER] = False
            builder.tasked[Processor.CUTTER] = False
            _subvariant(world, builder, important, complexity,
                        True, 10, 13, False, True, True, True, 1, True, 3)
        case 5:
            complexity -= 13
            builder.tasked[Processor.CRYSTALLIZER] = False
            builder.tasked[Processor.CUTTER] = False
            builder.tasked[Processor.SWAPPER] = False
            _subvariant(world, builder, important, complexity,
                        False, 0, 0, True, True, True, True, 0, False, 4)


def generate_shape(world: "Shapez2World", exclude: str | None = None) -> str:
    shapes = ["C", "R", "S", "W"]
    if exclude is not None:
        shapes.remove(exclude)
    return world.random.choice(shapes)


adjacent_colors = {
    "r": ("y", "m"),
    "b": ("m", "c"),
    "g": ("y", "c"),
    "y": ("r", "g"),
    "c": ("g", "b"),
    "m": ("b", "r"),
    "w": ("m", "c", "y"),
}


def generate_color(world: "Shapez2World", complexity: int, is_crystal: bool,
                   builder: ShapeBuilder, important: bool, exclude: str | None = None) -> str:

    white_comp = 2 if is_crystal else 3
    mixing_comp = 1 if is_crystal else 2
    base_comp = 0 if is_crystal else 1

    # Disable colors based on importance, availability, and complexity
    # True means must be included, False means must not be included, None means it doesn't matter
    color_types: dict[str, bool] = {c: True for c in ("u", "p", "s", "w")}
    if Processor.MIXER not in builder:
        color_types["s"] = False
        color_types["w"] = False
        if Processor.PAINTER not in builder and not is_crystal:
            color_types["p"] = False
    if is_crystal:
        color_types["u"] = False
    if complexity < white_comp:
        color_types["w"] = False
    if important and builder.tasked[Processor.MIXER]:
        color_types["p"] = False
        if Processor.PAINTER in builder:
            color_types["u"] = False
    elif complexity < mixing_comp:
        color_types["s"] = False
        if complexity < base_comp and not (important and builder.tasked[Processor.PAINTER]):
            color_types["p"] = False
    if important and builder.tasked[Processor.PAINTER]:
        color_types["u"] = False
    if Processor.PAINTER not in builder and not is_crystal:
        color_types["p"] = False
        color_types["s"] = False
        color_types["w"] = False

    # Build colors list
    colors = []
    if color_types["u"]:
        colors.append("u")
    if color_types["w"]:
        colors.append("w")
    if color_types["p"]:
        colors.extend(("r", "b", "g"))
    if color_types["s"]:
        colors.extend(("y", "c", "m"))

    # Try to make color scheme a bit nicer
    if builder.shape:
        preferred_layer = world.random.choice(builder.shape)
        preferred: str | None = None
        for i in range(1, 8, 2):
            if preferred_layer[i] not in "u-":
                preferred = preferred_layer[i]
        if preferred is not None:
            colors.append(preferred)
        if color_types["p"] and color_types["s"]:
            colors.extend(adjacent_colors[preferred])

    # Reduce complexity waste
    if color_types["p"] and color_types["u"] and complexity >= 6:
        colors.remove("u")
    if color_types["s"] and color_types["p"] and complexity >= 8:
        colors.remove("r")
        colors.remove("b")
        colors.remove("g")

    # Remove excluded color
    # Assumes that mixed colors are present and not removed before this
    # Uncolored must not be removed because there might be no complexity left for colors
    if exclude is not None and exclude != "u":
        while exclude in colors:
            colors.remove(exclude)

    # Error handling for when there is none left for some reason:
    if not colors:
        raise Exception(f"No color left to pick:\nbuilder = {builder.debug_string()},\n"
                        f"complexity = {complexity}, is crystal = {is_crystal}, important = {important}")

    final = world.random.choice(colors)
    if final in "ymcw":
        builder.tasked[Processor.MIXER] = False
    if final != "u" and not is_crystal:
        builder.tasked[Processor.PAINTER] = False
    return final


def stack(world: "Shapez2World", builder: ShapeBuilder, layer: str, has_non_crystal: bool,
          crystal_colors: int, *, blueprint: int | None = None) -> bool:

    builder.tasked[Processor.STACKER] = False

    if blueprint is not None:
        stack_top = builder.blueprint[blueprint][1]
    elif builder.has_crystals:
        # Assumes that in this case the new layer only has one crystal color (if any) and no empty part
        stack_top = True
    elif crystal_colors > 1 or not has_non_crystal or (crystal_colors and has_non_crystal and "--" in layer):
        stack_top = False
    else:
        stack_top = world.random.choice((False, True))

    if stack_top:
        if crystal_colors:
            # Make sure the non-crystal part is always placed on a non-empty corner
            # Assumes either there is the rotator at this point or the left side is not empty
            # Also assumes there is only one crystal color
            if builder.tasked[Processor.ROTATOR]:
                layer = layer[6:8] + layer[0:6]
                builder.tasked[Processor.ROTATOR] = False
            for i in range(0, 8, 2):
                if layer[i] not in "Pc-" and builder.shape[-1][i] != "-":
                    break
            else:
                builder.tasked[Processor.ROTATOR] = False
                for _ in range(3):
                    layer = layer[6:8] + layer[0:6]
                    if layer[0] not in "Pc-" and builder.shape[-1][0] != "-":
                        break
                else:
                    raise Exception(f"new layer supposed to be placed on top, but not possible:\n"
                                    f"builder = {builder.debug_string()}, new layer = {layer}")
            crys_col = ""
            for i in range(0, 8, 2):
                if layer[i] == "c":
                    crys_col = layer[i+1]
                    break
            fill_crystal(builder, crys_col)
            builder.shape.append(layer)
        else:
            for j in range(0, 8, 2):
                if layer[j:j+2] != "--" and builder.shape[-1][j:j+2] != "--":
                    builder.shape.append(layer)
                    break
            else:
                for i in reversed(range(len(builder.shape) - 1)):
                    for j in range(0, 8, 2):
                        if layer[j:j+2] != "--" and builder.shape[i][j:j+2] != "--":
                            builder.shape[i+1] = merge_layers(layer, builder.shape[i+1])
                            break
                    else:
                        continue
                    break
                else:
                    builder.shape[0] = merge_layers(layer, builder.shape[0])
    else:
        for j in range(0, 8, 2):
            if layer[j:j+2] != "--" and builder.shape[0][j:j+2] != "--":
                builder.shape.insert(0, layer)
                for i in range(0, 8, 2):
                    if builder.shape[0][i] == "-" and builder.shape[1][i] == "P":
                        for k in range(2, len(builder.shape)):
                            if builder.shape[k][i] != "P":
                                builder.shape[k-1] = builder.shape[k-1][:i] + "-" + builder.shape[k-1][i+1:]
                                builder.shape[0] = builder.shape[0][:i] + "P" + builder.shape[0][i+1:]
                                break
                        else:
                            builder.shape[-1] = builder.shape[-1][:i] + "-" + builder.shape[-1][i+1:]
                            builder.shape[0] = builder.shape[0][:i] + "P" + builder.shape[0][i+1:]
                break
        else:
            builder.shape[0] = merge_layers(layer, builder.shape[0])

    if crystal_colors:
        builder.has_crystals = True

    return stack_top


def merge_layers(layer_1: str, layer_2: str) -> str:
    merged = ""
    for k in range(0, 8, 2):
        if layer_1[k:k + 2] != "--":
            merged += layer_1[k:k + 2]
        else:
            merged += layer_2[k:k + 2]
    return merged


def fill_crystal(builder: ShapeBuilder, color: str) -> None:
    for j in range(len(builder.shape)):
        for i in range(1, 8, 2):
            if builder.shape[j][i] == "-":
                builder.shape[j] = builder.shape[j][:i-1] + "c" + color + builder.shape[j][i+1:]


def _bulk_possible(variants: list[bool], complexity: int, v: tuple[int, ...], *vc: tuple[int, int]):
    # IMPORTANT: Always sort by complexity in bulks
    for vv in v:
        variants[vv] = True
    for vv, cc in vc:
        if complexity >= cc:
            variants[vv] = True
        else:
            break


def _subvariant(world: "Shapez2World", builder: ShapeBuilder,
                important: bool, complexity: int, swapper_stacker: bool, a: int, b: int,
                c1: bool, c2: bool, c3: bool | None, c4: bool | None, kind: int, has_non_crys: bool, crys_col: int):
    if swapper_stacker:
        if Processor.SWAPPER in builder:
            complexity -= a
            if Processor.STACKER not in builder:
                builder.tasked[Processor.SWAPPER] = False
        else:
            complexity -= b
            builder.tasked[Processor.STACKER] = False
    complexity_1 = world.random.triangular(0, complexity).__int__()
    complexity_2 = 0 if c3 is None else world.random.triangular(0, complexity - complexity_1).__int__()
    complexity_3 = 0 if c4 is None else world.random.triangular(0, complexity - complexity_1 - complexity_2).__int__()
    complexity -= complexity_1 + complexity_2 + complexity_3
    p1 = generate_shape(world) + generate_color(
        world, complexity_1, False, builder, important
    ) if not c1 else "c" + generate_color(world, complexity_1, True, builder, important)
    p2 = generate_shape(world) + generate_color(
        world, complexity, False, builder, important
    ) if not c2 else "c" + generate_color(world, complexity, True, builder, important)
    p3 = "--" if c3 is None else (
        generate_shape(world) + generate_color(
            world, complexity_2, False, builder, important
        ) if not c3 else "c" + generate_color(world, complexity_2, True, builder, important)
    )
    p4 = "--" if c4 is None else (
        generate_shape(world) + generate_color(
            world, complexity_3, False, builder, important
        ) if not c4 else "c" + generate_color(world, complexity_3, True, builder, important)
    )
    if kind == 0:  # All same type
        stack_top = stack(world, builder, p1 + p2 + p3 + p4, has_non_crys, crys_col)
        builder.blueprint.append((128, stack_top, {"layer": p1 + p2 + p3 + p4}))
    elif kind == 1:  # 3 to 1 types
        ordered = [p1, p2, p3, p4]
        world.random.shuffle(ordered)
        stack_top = stack(world, builder, "".join(ordered), has_non_crys, crys_col)
        builder.blueprint.append((128, stack_top, {"ordered": ordered}))
    elif kind == 2:  # half-half types
        # p1-p2 and p3-p4 same types
        possible = [
            p1 + p2 + p3 + p4, p2 + p1 + p3 + p4, p1 + p2 + p4 + p3, p2 + p1 + p4 + p3,
            p3 + p1 + p2 + p4, p3 + p2 + p1 + p4, p4 + p1 + p2 + p3, p4 + p2 + p1 + p3,
            p3 + p4 + p1 + p2, p3 + p4 + p2 + p1, p4 + p3 + p1 + p2, p4 + p3 + p2 + p1,
            p2 + p3 + p4 + p1, p1 + p3 + p4 + p2, p2 + p4 + p3 + p1, p1 + p4 + p3 + p2,
        ]
        layer = world.random.choice(possible)
        stack_top = stack(world, builder, layer, has_non_crys, crys_col)
        builder.blueprint.append((128, stack_top, {"layer": layer}))
    elif kind == 3:  # cornered/checkered types
        # p1-p2 and p3-p4 same type
        possible = [
            p1 + p3 + p2 + p4, p2 + p3 + p1 + p4, p1 + p4 + p2 + p3, p2 + p4 + p1 + p3,
            p3 + p1 + p4 + p2, p3 + p2 + p4 + p1, p4 + p1 + p3 + p2, p4 + p2 + p3 + p1,
        ]
        layer = world.random.choice(possible)
        stack_top = stack(world, builder, layer, has_non_crys, crys_col)
        builder.blueprint.append((128, stack_top, {"layer": layer}))
