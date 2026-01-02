from typing import TYPE_CHECKING

from . import Processor

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
    half = next_id()  # cutter & 1
    rotated_half = next_id()  # cutter & rotator & 2
    vertical_half_half = next_id()  # (swapper & 1) | (cutter & rotator & stacker & 5)
    horizontal_half_half = next_id()  # (swapper & rotator & 2) | (cutter & rotator & stacker & 5)
    cut_out = next_id()  # cutter & rotator & ((stacker & 5) | (swapper & 3))
    _3_1 = next_id()  # (cutter & rotator & stacker & 11) | (swapper & rotator & 3)
    cornered = next_id()  # (cutter & rotator & stacker & 8) | (cutter & rotator & swapper & 5)
    random_shapes_1_color = next_id()  # (cutter & rotator & stacker & 17) | (rotator & swapper & 5)
    checkered = next_id()  # (cutter & rotator & stacker & 9) | (rotator & swapper & 4)
    # (cutter & rotator & stacker & 17) | (rotator & swapper & 5) & painter & 1 (to be able to paint something)
    random_colors_1_shape = next_id()
    pins = next_id()  # pins

    begin_crystals = next_id()

    full_crystal = next_id()  # crystal & ((pins & 1) | (cutter & rotator & 6))
    half_crystal = next_id()  # crystal & cutter & rotator & 5
    rotated_half_crystal = next_id()  # crystal & cutter & rotator & 6
    vertical_half_half_crystal = next_id()  # crystal & cutter & rotator & 6
    horizontal_half_half_crystal = next_id()  # crystal & cutter & rotator & 7
    right_half_crystal_half_shape = next_id()  # crystal & cutter & 2
    left_half_crystal_half_shape = next_id()  # (crystal & cutter & rotator & 3)
    rotated_half_crystal_half_shape = next_id()  # crystal & cutter & rotator & 3
    cut_out_crystal = next_id()  # (crystal & cutter & rotator & swapper & 8)
    _3_1_crystals = next_id()  # (crystal & cutter & rotator & 8)
    _3_crystals_1_shape = next_id()  # (crystal & cutter & rotator & 4)
    _3_shapes_1_crystal = next_id()  # crystal & cutter & rotator & ((stacker & 7) | (swapper & 4))
    cornered_crystal = next_id()  # (crystal & cutter & rotator & swapper & 13)
    checkered_crystal = next_id()  # (crystal & cutter & rotator & swapper & 11)

    end_crystals = next_id()

    # Can have crystals, but not necessary
    single = next_id()  # cutter & rotator & 3
    _2_singles = next_id()  # (cutter & rotator & stacker & 6) | (cutter & rotator & swapper & 5)
    _3_singles = next_id()  # (cutter & rotator & stacker & 11) | (cutter & rotator & swapper & 5)
    _4_singles = next_id()  # (cutter & rotator & stacker & 17) | (rotator & swapper & 5)

    end = next_id()


def generate_layer(world: "Shapez2World", complexity: int, shape: list[str],
                   available: list[Processor], tasked: list[bool], important: bool) -> None:

    if important and (sum(tasked) > complexity or (
        sum(tasked) + 1 > complexity and tasked[Processor.ROTATOR] and (
            not tasked[Processor.CUTTER] or not tasked[Processor.SWAPPER]
        )
    )):
        raise Exception(f"Too low complexity ({complexity}) "
                        f"for important processors {', '.join(str(i) for i in range(8) if tasked[i])}")

    already_has_crystals = any(x == "c" for layer in shape for x in (layer[i] for i in range(0, 8, 2)))
    has_vertical_split = any(layer[0:2] != layer[6:8] or layer[2:4] != layer[4:6] for layer in shape)
    has_horizontal_split = any(layer[0:2] != layer[2:4] or layer[6:8] != layer[4:6] for layer in shape)
    if has_horizontal_split and has_vertical_split:
        tasked[Processor.ROTATOR] = False

    # Decide on the layer variant, but consider that mixer and/or painter might be important
    stored_complexity = 0
    if important:
        if tasked[Processor.MIXER]:
            if Processor.CRYSTALLIZER in available:
                stored_complexity = 1
            else:
                stored_complexity = 2
        elif tasked[Processor.PAINTER]:
            stored_complexity = 1
    complexity -= stored_complexity

    while True:
        # Calculate what's possible with available processors
        # IMPORTANT: do not make anything false before this
        variants = [False] * Variant.end
        variants[Variant.full] = True
        if Processor.PIN_PUSHER in available:
            variants[Variant.pins] = True
            if Processor.CRYSTALLIZER in available:
                _bulk_possible(variants, complexity, (), (Variant.full_crystal, 1))
        if Processor.CRYSTALLIZER in available:
            if Processor.CUTTER in available:
                _bulk_possible(variants, complexity, (), (Variant.right_half_crystal_half_shape, 2))
                if Processor.ROTATOR in available and complexity >= 3:
                    _bulk_possible(
                        variants, complexity,
                        (Variant.left_half_crystal_half_shape, Variant.rotated_half_crystal_half_shape),
                        (Variant._3_crystals_1_shape, 4), (Variant.half_crystal, 5), (Variant.full_crystal, 6),
                        (Variant.rotated_half_crystal, 6), (Variant.vertical_half_half_crystal, 6),
                        (Variant.horizontal_half_half_crystal, 7), (Variant._3_1_crystals, 8),
                    )
                    if Processor.STACKER in available:
                        variants[Variant._3_shapes_1_crystal] = True
                    if Processor.SWAPPER in available:
                        _bulk_possible(
                            variants, complexity, (), (Variant._3_shapes_1_crystal, 7), (Variant.cut_out_crystal, 8),
                            (Variant.checkered_crystal, 11), (Variant.cornered_crystal, 13),
                        )
        if Processor.CUTTER in available and complexity:
            variants[Variant.half] = True
            if Processor.ROTATOR in available and complexity >= 2:
                _bulk_possible(variants, complexity, (Variant.rotated_half, ), (Variant.single, 3))
                if Processor.STACKER in available and complexity >= 5:
                    _bulk_possible(
                        variants, complexity,
                        (Variant.vertical_half_half, Variant.horizontal_half_half, Variant.cut_out),
                        (Variant._2_singles, 6), (Variant.cornered, 8), (Variant.checkered, 9),
                        (Variant._3_singles, 11), (Variant._3_1, 11), (Variant.random_shapes_1_color, 17),
                        (Variant._4_singles, 17),
                    )
                    if Processor.PAINTER in available and complexity >= 18:
                        variants[Variant.random_colors_1_shape] = True
        if Processor.SWAPPER in available and complexity:
            variants[Variant.vertical_half_half] = True
            if Processor.ROTATOR in available and complexity >= 2:
                _bulk_possible(
                    variants, complexity, (Variant.horizontal_half_half, ), (Variant._3_1, 3), (Variant.checkered, 4),
                    (Variant.random_shapes_1_color, 5), (Variant._4_singles, 5),
                )
                if Processor.PAINTER in available and complexity >= 6:
                    variants[Variant.random_colors_1_shape] = True
                if Processor.CUTTER in available:
                    _bulk_possible(
                        variants, complexity, (Variant.cut_out, ), (Variant.cornered, 5), (Variant._2_singles, 5),
                        (Variant._3_singles, 5),
                    )

        def _bulk_remove(*v: int):
            for vv in v:
                variants[vv] = False

        # Remove everything that doesn't have the important buildings
        if important:
            if any(tasked):
                if tasked[Processor.CUTTER]:
                    _bulk_remove(
                        Variant.vertical_half_half, Variant.horizontal_half_half, Variant._3_1,
                        Variant.random_shapes_1_color, Variant.checkered, Variant.random_colors_1_shape, Variant.pins,
                        Variant.full_crystal, Variant.left_half_crystal_half_shape, Variant._4_singles, Variant.full
                    )
                if tasked[Processor.ROTATOR]:
                    # Still leave rotated half as available in case of low complexity
                    _bulk_remove(
                        Variant.half, Variant.pins, Variant.full_crystal, Variant.half_crystal,
                        Variant.right_half_crystal_half_shape, Variant.full
                    )
                    if not has_vertical_split:
                        _bulk_remove(Variant.horizontal_half_half, Variant.rotated_half_crystal_half_shape)
                    if not has_horizontal_split:
                        _bulk_remove(Variant.vertical_half_half, Variant.left_half_crystal_half_shape)
                if tasked[Processor.STACKER]:
                    # Should only happen in single layers
                    _bulk_remove(Variant.half, Variant.rotated_half, Variant.pins, Variant.single, Variant.full)
                    if sum(tasked) == 1:
                        variants[Variant.full] = True
                    for x in range(Variant.begin_crystals + 1, Variant.end_crystals):
                        if x != Variant._3_shapes_1_crystal:
                            variants[x] = False
                if tasked[Processor.PAINTER]:
                    # Painters don't have anything to do with crystallizers,
                    # so make sure you can paint something if needed
                    # Also this is a case where full layer is useful
                    _bulk_remove(
                        Variant.full_crystal, Variant.half_crystal, Variant.rotated_half_crystal,
                        Variant.vertical_half_half_crystal, Variant.horizontal_half_half_crystal,
                        Variant.cut_out_crystal, Variant._3_1_crystals, Variant.cornered_crystal,
                        Variant.checkered_crystal, Variant.pins,
                    )
                if tasked[Processor.PIN_PUSHER]:
                    for x in range(0, Variant.end):
                        if x not in (Variant.pins, Variant.full_crystal):
                            variants[x] = False
                if tasked[Processor.CRYSTALLIZER]:
                    for x in range(0, Variant.begin_crystals):
                        variants[x] = False
                    for x in range(Variant.end_crystals + 1, Variant.end):
                        variants[x] = False
                if tasked[Processor.SWAPPER]:
                    _bulk_remove(
                        Variant.half, Variant.rotated_half, Variant.pins, Variant.full_crystal, Variant.half_crystal,
                        Variant.rotated_half_crystal, Variant.vertical_half_half_crystal,
                        Variant.horizontal_half_half_crystal, Variant.right_half_crystal_half_shape,
                        Variant.left_half_crystal_half_shape, Variant.rotated_half_crystal_half_shape,
                        Variant._3_1_crystals, Variant._3_crystals_1_shape, Variant.single, Variant.full
                    )

        # Remove some things that are impossible due to shape context
        if already_has_crystals:
            # Putting new layers with crystal on top of or under other crystals is tricky, especially since
            # the swapper can destroy other layers
            if Processor.PIN_PUSHER not in available:
                variants[Variant.full_crystal] = False
            _bulk_remove(
                Variant.half_crystal, Variant.rotated_half_crystal, Variant.vertical_half_half_crystal,
                Variant.horizontal_half_half_crystal, Variant.cut_out_crystal, Variant._3_1_crystals,
                Variant.cornered_crystal, Variant.checkered_crystal,
            )
        if not len(shape):
            variants[Variant.pins] = False

        # Remove some low complexity variants if high complexity given
        if not important and complexity >= 12:
            _bulk_remove(
                Variant.horizontal_half_half, Variant.cut_out, Variant.left_half_crystal_half_shape,
                Variant.rotated_half_crystal_half_shape, Variant._3_crystals_1_shape
            )
            if Processor.CUTTER in available and Processor.ROTATOR in available:
                _bulk_remove(Variant.half, Variant.rotated_half)
                if Processor.STACKER in available or Processor.SWAPPER in available:
                    _bulk_remove(Variant.vertical_half_half, Variant.horizontal_half_half, Variant.cut_out)
                if Processor.SWAPPER in available:
                    variants[Variant._3_1] = False
                if Processor.CRYSTALLIZER in available:
                    _bulk_remove(Variant.right_half_crystal_half_shape, Variant.left_half_crystal_half_shape,
                                 Variant.rotated_half_crystal_half_shape, Variant._3_crystals_1_shape)
            if sum(variants) > 1:
                variants[Variant.full] = False

        # If none available anymore, try to save it in some way
        if not any(variants):
            if complexity <= sum(tasked) + 1:  # Maybe complexity was too restrictive
                complexity += 3
            elif not any(tasked):  # If nothing tasked, then a full layer doesn't do anything
                variants[Variant.full] = True
            else:  # Last resort, maybe a very bad combination?
                tasked[world.random.choice([x for x in range(8) if tasked[x]])] = False
            continue
        break

    # Restore complexity for painting and mixing
    complexity += stored_complexity

    def _tasked_sw_st(swc: int, stc: int, need_cu: bool):
        nonlocal complexity
        if Processor.SWAPPER in available:
            complexity -= swc
            if Processor.STACKER not in available or (Processor.CUTTER not in available and not need_cu):
                tasked[Processor.SWAPPER] = False
        else:
            complexity -= stc
            tasked[Processor.STACKER] = False
            tasked[Processor.CUTTER] = False if not need_cu else tasked[Processor.CUTTER]
        tasked[Processor.CUTTER] = False if need_cu else tasked[Processor.CUTTER]
        tasked[Processor.ROTATOR] = False

    def _bulk_tasked(comp: int, *t: Processor):
        nonlocal complexity
        complexity -= comp
        for tt in t:
            tasked[tt] = False

    def _2_parts(c1: bool, c2: bool, no_same: bool) -> tuple[str, str]:
        nonlocal complexity
        complexity_1 = world.random.triangular(0, complexity).__int__()
        complexity -= complexity_1
        p1 = generate_shape(world) + generate_color(
            world, complexity_1, shape, False, available, tasked, important
        ) if not c1 else "c" + generate_color(world, complexity_1, shape, True, available, tasked, important)
        p2 = generate_shape(world) + generate_color(
            world, complexity, shape, False, available, tasked, important
        ) if not c2 else "c" + generate_color(world, complexity, shape, True, available, tasked, important)
        if no_same and p1 == p2:
            p2 = generate_shape(world, p2[0]) + p2[1] if not c2 else "c" + generate_color(
                world, complexity, shape, True, available, tasked, important, p2[1]
            )
        return p1, p2

    variant_pool = [x for x in variants if variants[x]]
    match world.random.choice(variant_pool):
        case Variant.full:
            part = generate_shape(world) + generate_color(
                world, complexity, shape, False, available, tasked, important
            )
            stack(world, shape, part * 4, tasked, True, 0, already_has_crystals)
        case Variant.half:
            complexity -= 1
            tasked[Processor.CUTTER] = False
            part = generate_shape(world) + generate_color(
                world, complexity, shape, False, available, tasked, important
            )
            stack(world, shape, "----" + part * 2, tasked, True, 0, already_has_crystals)
        case Variant.rotated_half:
            complexity -= 2
            tasked[Processor.CUTTER] = False
            complexity_color = world.random.randint(0, complexity)
            complexity -= complexity_color
            part = generate_shape(world) + generate_color(
                world, complexity_color, shape, False, available, tasked, important
            )
            if tasked[Processor.ROTATOR]:
                if not has_vertical_split:
                    stack(world, shape, part * 2 + "----", tasked, True, 0, already_has_crystals)
                elif not has_horizontal_split:
                    stack(world, shape, part + "----" + part, tasked, True, 0, already_has_crystals)
                # Having both splits but still rotator tasked should not be happening here
            else:
                possible_positions = [part + "----" + part, "--" + part * 2 + "--"]
                if complexity:  # if still complexity there even after subtracting something for color
                    possible_positions.append(part * 2 + "----")
                stack(world, shape, world.random.choice(possible_positions), tasked, True, 0, already_has_crystals)
        case Variant.vertical_half_half:
            if Processor.SWAPPER in available:
                complexity -= 1
                if (
                    Processor.CUTTER not in available or
                    Processor.ROTATOR not in available or
                    Processor.STACKER not in available
                ):
                    tasked[Processor.SWAPPER] = False
            else:
                _bulk_tasked(5, Processor.CUTTER, Processor.ROTATOR, Processor.STACKER)
            part_1, part_2 = _2_parts(False, False, True)
            stack(world, shape, part_1 * 2 + part_2 * 2, tasked, True, 0, already_has_crystals)
        case Variant.horizontal_half_half:
            if Processor.SWAPPER in available:
                complexity -= 2
                if Processor.CUTTER not in available or Processor.STACKER not in available:
                    tasked[Processor.SWAPPER] = False
            else:
                _bulk_tasked(5, Processor.CUTTER, Processor.ROTATOR, Processor.STACKER)
            part_1, part_2 = _2_parts(False, False, True)
            stack(world, shape, part_1 + part_2 * 2 + part_1, tasked, True, 0, already_has_crystals)
        case Variant.cut_out:
            _tasked_sw_st(3, 5, True)
            part = generate_shape(world) + generate_color(
                world, complexity, shape, False, available, tasked, important
            )
            ordered_parts = [part, part, part, "--"]
            world.random.shuffle(ordered_parts)
            stack(world, shape, "".join(ordered_parts), tasked, True, 0, already_has_crystals)
        case Variant._3_1:
            _tasked_sw_st(3, 11, False)
            part_1, part_2 = _2_parts(False, False, True)
            ordered_parts = [part_1, part_1, part_1, part_2]
            world.random.shuffle(ordered_parts)
            stack(world, shape, "".join(ordered_parts), tasked, True, 0, already_has_crystals)
        case Variant.cornered:
            _tasked_sw_st(5, 8, True)
            part = generate_shape(world) + generate_color(
                world, complexity, shape, False, available, tasked, important
            )
            if world.random.random() < 0.5:
                stack(world, shape, (part + "--") * 2, tasked, True, 0, already_has_crystals)
            else:
                stack(world, shape, ("--" + part) * 2, tasked, True, 0, already_has_crystals)
        case Variant.random_shapes_1_color:
            _tasked_sw_st(5, 17, False)
            color = generate_color(
                world, complexity, shape, False, available, tasked, important
            )
            ordered_parts = [generate_shape(world)]
            ordered_parts.append(generate_shape(world, ordered_parts[-1]))
            ordered_parts.append(generate_shape(world, ordered_parts[-1]))
            ordered_parts.append(generate_shape(world, ordered_parts[-1]))
            world.random.shuffle(ordered_parts)
            stack(world, shape, "".join(p + color for p in ordered_parts), tasked, True, 0, already_has_crystals)
        case Variant.checkered:
            _tasked_sw_st(4, 9, False)
            part_1, part_2 = _2_parts(False, False, True)
            stack(world, shape, (part_1 + part_2) * 2, tasked, True, 0, already_has_crystals)
        case Variant.random_colors_1_shape:
            # Assumes the painter is available and at least one more complexity is still available
            _tasked_sw_st(5, 17, False)
            shape_part = generate_shape(world)
            comp_1 = world.random.triangular(0, complexity).__int__()
            comp_2 = world.random.triangular(0, complexity - comp_1).__int__()
            comp_3 = world.random.triangular(0, complexity - comp_1 - comp_2).__int__()
            complexity -= comp_1 + comp_2 + comp_3
            ordered_colors = [generate_color(world, complexity, shape, False, available, tasked, important)]
            ordered_colors.append(generate_color(
                world, comp_1, shape, False, available, tasked, important, ordered_colors[-1]
            ))
            ordered_colors.append(generate_color(
                world, comp_2, shape, False, available, tasked, important, ordered_colors[-1]
            ))
            ordered_colors.append(generate_color(
                world, comp_3, shape, False, available, tasked, important, ordered_colors[-1]
            ))
            world.random.shuffle(ordered_colors)
            stack(world, shape, "".join(shape_part + c for c in ordered_colors), tasked, True, 0, already_has_crystals)
        case Variant.pins:
            tasked[Processor.PIN_PUSHER] = False
            part = ""
            for i in range(0, 8, 2):
                part += "P-" if shape[0][i] != "-" else "--"
            shape.insert(0, part)
        case Variant.full_crystal:
            # Assumes either has pin pusher or not already_has_crystals
            # Needs extra handling because of that
            if Processor.PIN_PUSHER in available:
                complexity -= 1
                if Processor.ROTATOR not in available or Processor.CUTTER not in available:
                    tasked[Processor.PIN_PUSHER] = False
            else:
                _bulk_tasked(6, Processor.CUTTER, Processor.ROTATOR)
            tasked[Processor.CRYSTALLIZER] = False
            part = "c" + generate_color(world, complexity, shape, True, available, tasked, important)
            if already_has_crystals:
                fill_crystal(shape, part[1])
            shape.insert(0, part * 4)
        case Variant.half_crystal:
            # Assumes this doesn't happen when already_has_crystals
            _bulk_tasked(5, Processor.CUTTER, Processor.ROTATOR, Processor.CRYSTALLIZER)
            part = "c" + generate_color(world, complexity, shape, True, available, tasked, important)
            stack(world, shape, "----" + part * 2, tasked, False, 1, already_has_crystals)
        case Variant.rotated_half_crystal:
            # Assumes this doesn't happen when already_has_crystals
            _bulk_tasked(6, Processor.CUTTER, Processor.ROTATOR, Processor.CRYSTALLIZER)
            complexity_color = world.random.randint(0, complexity)
            complexity -= complexity_color
            part = "c" + generate_color(world, complexity_color, shape, True, available, tasked, important)
            possible_positions = [part + "----" + part, "--" + part * 2 + "--"]
            if complexity:  # if still complexity there even after subtracting something for color
                possible_positions.append(part * 2 + "----")
            stack(world, shape, world.random.choice(possible_positions), tasked, False, 1, already_has_crystals)
        case Variant.vertical_half_half_crystal:
            # Assumes this doesn't happen when already_has_crystals
            _bulk_tasked(6, Processor.CUTTER, Processor.ROTATOR, Processor.CRYSTALLIZER)
            part_1, part_2 = _2_parts(True, True, True)
            stack(world, shape, part_1 * 2 + part_2 * 2, tasked, False, 2, already_has_crystals)
        case Variant.horizontal_half_half_crystal:
            # Assumes this doesn't happen when already_has_crystals
            _bulk_tasked(6, Processor.CUTTER, Processor.ROTATOR, Processor.CRYSTALLIZER)
            part_1, part_2 = _2_parts(True, True, True)
            stack(world, shape, part_1 + part_2 * 2 + part_1, tasked, False, 2, already_has_crystals)
        case Variant.right_half_crystal_half_shape:
            _bulk_tasked(2, Processor.CUTTER, Processor.CRYSTALLIZER)
            part_1, part_2 = _2_parts(False, True, False)
            stack(world, shape, part_2 * 2 + part_1 * 2, tasked, True, 1, already_has_crystals)
        case Variant.left_half_crystal_half_shape:
            _bulk_tasked(3, Processor.CUTTER, Processor.ROTATOR, Processor.CRYSTALLIZER)
            part_1, part_2 = _2_parts(False, True, False)
            stack(world, shape, part_1 * 2 + part_2 * 2, tasked, True, 1, already_has_crystals)
        case Variant.rotated_half_crystal_half_shape:
            _bulk_tasked(3, Processor.CUTTER, Processor.ROTATOR, Processor.CRYSTALLIZER)
            part_1, part_2 = _2_parts(False, True, False)
            if world.random.random() < 0.5:
                stack(world, shape, part_1 + part_2 * 2 + part_1, tasked, True, 1, already_has_crystals)
            else:
                stack(world, shape, part_2 + part_1 * 2 + part_2, tasked, True, 1, already_has_crystals)
        case Variant.cut_out_crystal:
            # Assumes this doesn't happen when already_has_crystals
            _bulk_tasked(8, Processor.CUTTER, Processor.ROTATOR, Processor.CRYSTALLIZER, Processor.SWAPPER)
            part = "c" + generate_color(world, complexity, shape, True, available, tasked, important)
            ordered_parts = [part, part, part, "--"]
            world.random.shuffle(ordered_parts)
            stack(world, shape, "".join(ordered_parts), tasked, False, 1, already_has_crystals)
        case Variant._3_1_crystals:
            # Assumes this doesn't happen when already_has_crystals
            _bulk_tasked(8, Processor.CUTTER, Processor.ROTATOR, Processor.CRYSTALLIZER)
            part_1, part_2 = _2_parts(True, True, True)
            ordered_parts = [part_1, part_1, part_1, part_2]
            world.random.shuffle(ordered_parts)
            stack(world, shape, "".join(ordered_parts), tasked, False, 2, already_has_crystals)
        case Variant._3_crystals_1_shape:
            _bulk_tasked(4, Processor.CUTTER, Processor.ROTATOR, Processor.CRYSTALLIZER)
            part_1, part_2 = _2_parts(False, True, False)
            ordered_parts = [part_1, part_2, part_2, part_2]
            world.random.shuffle(ordered_parts)
            stack(world, shape, "".join(ordered_parts), tasked, True, 1, already_has_crystals)
        case Variant._3_shapes_1_crystal:
            _tasked_sw_st(4, 7, True)
            tasked[Processor.CRYSTALLIZER] = False
            part_1, part_2 = _2_parts(False, True, False)
            ordered_parts = [part_1, part_1, part_1, part_2]
            world.random.shuffle(ordered_parts)
            stack(world, shape, "".join(ordered_parts), tasked, True, 1, already_has_crystals)
        case Variant.cornered_crystal:
            # Assumes this doesn't happen when already_has_crystals
            _bulk_tasked(13, Processor.CUTTER, Processor.ROTATOR, Processor.CRYSTALLIZER, Processor.SWAPPER)
            part = "c" + generate_color(world, complexity, shape, True, available, tasked, important)
            if world.random.random() < 0.5:
                stack(world, shape, (part + "--") * 2, tasked, False, 1, already_has_crystals)
            else:
                stack(world, shape, ("--" + part) * 2, tasked, False, 1, already_has_crystals)
        case Variant.checkered_crystal:
            # Assumes this doesn't happen when already_has_crystals
            _bulk_tasked(11, Processor.CUTTER, Processor.ROTATOR, Processor.CRYSTALLIZER, Processor.SWAPPER)
            part_1, part_2 = _2_parts(True, True, True)
            stack(world, shape, (part_1 + part_2) * 2, tasked, False, 2, already_has_crystals)
        case Variant.single:
            _bulk_tasked(0, Processor.CUTTER, Processor.ROTATOR)
            if Processor.CRYSTALLIZER in available and complexity >= 7 and not already_has_crystals:
                complexity -= 7
                tasked[Processor.CRYSTALLIZER] = False
                part = "c" + generate_color(world, complexity, shape, True, available, tasked, important)
                a = (False, 1)
            else:
                complexity -= 3
                part = generate_shape(world) + generate_color(
                    world, complexity, shape, False, available, tasked, important
                )
                a = (True, 0)
            ordered_parts = [part, "--", "--", "--"]
            world.random.shuffle(ordered_parts)
            stack(world, shape, "".join(ordered_parts), tasked, *a, already_has_crystals)
        case Variant._2_singles:
            generate_2_shapes(world, complexity, shape, available, tasked, important, already_has_crystals)
        case Variant._3_singles:
            generate_3_shapes(world, complexity, shape, available, tasked, important, already_has_crystals)
        case Variant._4_singles:
            generate_4_shapes(world, complexity, shape, available, tasked, important, already_has_crystals)
        case e:
            raise Exception(f"Unknown layer variant {e}:\n"
                            f"complexity = {complexity}, shape = {shape}, important = {important}\n"
                            f"available = {available}, tasked = {tasked},\n"
                            f"already has crystals = {already_has_crystals}, has vertical split = {has_vertical_split},"
                            f"has horizontal split = {has_horizontal_split},\n"
                            f"variant pool = {variant_pool}")


def generate_2_shapes(world: "Shapez2World", complexity: int, shape: list[str],
                      available: list[Processor], tasked: list[bool], important: bool,
                      already_has_crystals: bool) -> None:
    tasked[Processor.CUTTER] = False
    tasked[Processor.ROTATOR] = False

    # Decide on the layer variant, but consider that mixer and/or painter might be important
    stored_complexity = 0
    if important:
        if tasked[Processor.MIXER]:
            if Processor.CRYSTALLIZER in available:
                stored_complexity = 1
            else:
                stored_complexity = 2
        elif tasked[Processor.PAINTER]:
            stored_complexity = 1
    complexity -= stored_complexity

    subvariants = [False] * 6
    if Processor.CRYSTALLIZER in available and complexity >= 4 and not already_has_crystals:
        subvariants[4] = True
        if Processor.STACKER in available and complexity >= 12:
            subvariants[5] = True
        if Processor.SWAPPER in available and complexity >= 9:
            _bulk_possible(subvariants, complexity, (5, ), (3, 16), (2, 17))
    if Processor.SWAPPER in available and complexity >= 3:
        _bulk_possible(subvariants, complexity, (0, ), (1, 5))
    if Processor.STACKER in available and complexity >= 5:
        _bulk_possible(subvariants, complexity, (0, ), (1, 9))
    if tasked[Processor.PAINTER]:
        subvariants[2:4] = [False] * 2

    # Restore complexity for painting and mixing
    complexity += stored_complexity

    subvariant_pool = list(x for x in range(6) if subvariants[x])
    match subvariant_pool:
        case 0:
            _subvariant(world, shape, available, tasked, important, already_has_crystals, complexity,
                        True, 3, 5, False, False, None, None, 2, True, 0)
        case 1:
            _subvariant(world, shape, available, tasked, important, already_has_crystals, complexity,
                        True, 5, 9, False, False, None, None, 3, True, 0)
        case 2:
            complexity -= 16
            tasked[Processor.SWAPPER] = False
            tasked[Processor.CRYSTALLIZER] = False
            _subvariant(world, shape, available, tasked, important, already_has_crystals, complexity,
                        False, 0, 0, True, True, None, None, 2, False, 2)
        case 3:
            complexity -= 17
            tasked[Processor.SWAPPER] = False
            tasked[Processor.CRYSTALLIZER] = False
            _subvariant(world, shape, available, tasked, important, already_has_crystals, complexity,
                        False, 0, 0, True, True, None, None, 3, False, 2)
        case 4:
            complexity -= 4
            tasked[Processor.CRYSTALLIZER] = False
            _subvariant(world, shape, available, tasked, important, already_has_crystals, complexity,
                        False, 0, 0, False, True, None, None, 2, True, 1)
        case 5:
            tasked[Processor.CRYSTALLIZER] = False
            _subvariant(world, shape, available, tasked, important, already_has_crystals, complexity,
                        True, 9, 12, False, True, None, None, 3, True, 1)


def generate_3_shapes(world: "Shapez2World", complexity: int, shape: list[str],
                      available: list[Processor], tasked: list[bool], important: bool,
                      already_has_crystals: bool) -> None:
    tasked[Processor.CUTTER] = False
    tasked[Processor.ROTATOR] = False

    # Decide on the layer variant, but consider that mixer and/or painter might be important
    stored_complexity = 0
    if important:
        if tasked[Processor.MIXER]:
            if Processor.CRYSTALLIZER in available:
                stored_complexity = 1
            else:
                stored_complexity = 2
        elif tasked[Processor.PAINTER]:
            stored_complexity = 1
    complexity -= stored_complexity

    subvariants = [False] * 6
    if Processor.CRYSTALLIZER in available and complexity >= 7 and not already_has_crystals:
        if Processor.SWAPPER in available:
            _bulk_possible(subvariants, complexity, (1, 2, ), (4, 9), (3, 10), (5, 13))
        if Processor.STACKER in available and complexity >= 9:
            _bulk_possible(subvariants, complexity, (2, ), (1, 10), (3, 13))
    if Processor.SWAPPER in available and complexity >= 8:
        subvariants[0] = True
    if Processor.STACKER in available and complexity >= 12:
        subvariants[0] = True
    if tasked[Processor.PAINTER]:
        subvariants[5] = False

    # Restore complexity for painting and mixing
    complexity += stored_complexity

    subvariant_pool = list(x for x in range(6) if subvariants[x])
    match subvariant_pool:
        case 0:
            _subvariant(world, shape, available, tasked, important, already_has_crystals, complexity,
                        True, 8, 12, False, False, False, None, 1, True, 0)
        case 1:
            tasked[Processor.CRYSTALLIZER] = False
            _subvariant(world, shape, available, tasked, important, already_has_crystals, complexity,
                        True, 7, 10, False, False, True, None, 2, True, 1)
        case 2:
            tasked[Processor.CRYSTALLIZER] = False
            _subvariant(world, shape, available, tasked, important, already_has_crystals, complexity,
                        True, 7, 9, False, False, True, None, 3, True, 1)
        case 3:
            tasked[Processor.CRYSTALLIZER] = False
            _subvariant(world, shape, available, tasked, important, already_has_crystals, complexity,
                        True, 10, 13, True, True, False, None, 2, True, 2)
        case 4:
            complexity -= 9
            tasked[Processor.CRYSTALLIZER] = False
            tasked[Processor.SWAPPER] = False
            _subvariant(world, shape, available, tasked, important, already_has_crystals, complexity,
                        False, 0, 0, True, True, False, None, 3, True, 2)
        case 5:
            complexity -= 13
            tasked[Processor.CRYSTALLIZER] = False
            tasked[Processor.SWAPPER] = False
            _subvariant(world, shape, available, tasked, important, already_has_crystals, complexity,
                        False, 0, 0, True, True, True, None, 1, False, 3)


def generate_4_shapes(world: "Shapez2World", complexity: int, shape: list[str],
                      available: list[Processor], tasked: list[bool], important: bool,
                      already_has_crystals: bool) -> None:
    tasked[Processor.ROTATOR] = False

    # Decide on the layer variant, but consider that mixer and/or painter might be important
    stored_complexity = 0
    if important:
        if tasked[Processor.MIXER]:
            if Processor.CRYSTALLIZER in available:
                stored_complexity = 1
            else:
                stored_complexity = 2
        elif tasked[Processor.PAINTER]:
            stored_complexity = 1
    complexity -= stored_complexity

    subvariants = [False] * 6
    if (
        Processor.CRYSTALLIZER in available and Processor.CUTTER in available and
        complexity >= 6
    ):
        if Processor.SWAPPER in available:
            subvariants[1] = True
            if not already_has_crystals:
                _bulk_possible(subvariants, complexity, (), (2, 7), (3, 10), (4, 10), (5, 13))
        if Processor.STACKER in available and complexity >= 10:
            _bulk_possible(subvariants, complexity, (), (1, 13))
            if not already_has_crystals:
                _bulk_possible(subvariants, complexity, (3, ), (4, 13), (2, 16))
    if Processor.SWAPPER in available and complexity >= 5:
        subvariants[0] = True
    if Processor.STACKER in available and Processor.CUTTER in available and complexity >= 15:
        subvariants[0] = True
    if tasked[Processor.PAINTER]:
        subvariants[5] = False

    # Restore complexity for painting and mixing
    complexity += stored_complexity

    subvariant_pool = list(x for x in range(6) if subvariants[x])
    match subvariant_pool:
        case 0:
            if Processor.SWAPPER in available:
                complexity -= 5
                if Processor.STACKER not in available:
                    tasked[Processor.SWAPPER] = False
            else:
                complexity -= 15
                tasked[Processor.STACKER] = False
                tasked[Processor.CUTTER] = False
            _subvariant(world, shape, available, tasked, important, already_has_crystals, complexity,
                        False, 0, 0, False, False, False, False, 0, True, 0)
        case 1:
            tasked[Processor.CRYSTALLIZER] = False
            tasked[Processor.CUTTER] = False
            _subvariant(world, shape, available, tasked, important, already_has_crystals, complexity,
                        True, 6, 13, False, False, False, True, 1, True, 1)
        case 2:
            tasked[Processor.CRYSTALLIZER] = False
            tasked[Processor.CUTTER] = False
            _subvariant(world, shape, available, tasked, important, already_has_crystals, complexity,
                        True, 7, 16, False, False, True, True, 2, True, 2)
        case 3:
            tasked[Processor.CRYSTALLIZER] = False
            tasked[Processor.CUTTER] = False
            _subvariant(world, shape, available, tasked, important, already_has_crystals, complexity,
                        True, 7, 10, False, False, True, True, 3, True, 2)
        case 4:
            tasked[Processor.CRYSTALLIZER] = False
            tasked[Processor.CUTTER] = False
            _subvariant(world, shape, available, tasked, important, already_has_crystals, complexity,
                        True, 10, 13, False, True, True, True, 1, True, 3)
        case 5:
            complexity -= 13
            tasked[Processor.CRYSTALLIZER] = False
            tasked[Processor.CUTTER] = False
            tasked[Processor.SWAPPER] = False
            _subvariant(world, shape, available, tasked, important, already_has_crystals, complexity,
                        False, 0, 0, True, True, True, True, 0, False, 4)


def generate_shape(world: "Shapez2World", exclude: str | None = None) -> str:
    shapes = ["C", "R", "S", "W"]
    if exclude is not None:
        shapes.remove(exclude)
    return world.random.choice(shapes)


adjacent_colors = {
    "r": ("y", "p"),
    "b": ("p", "c"),
    "g": ("y", "c"),
    "y": ("r", "g"),
    "c": ("g", "b"),
    "p": ("b", "r"),
    "w": ("p", "c", "y"),
}


def generate_color(world: "Shapez2World", complexity: int, shape: list[str], is_crystal: bool,
                   available: list[Processor], tasked: list[bool], important: bool, exclude: str | None = None) -> str:

    white_comp = 2 if is_crystal else 3
    mixing_comp = 1 if is_crystal else 2
    base_comp = 0 if is_crystal else 1

    # Disable colors based on importance, availability, and complexity
    # True means must be included, False means must not be included, None means it doesn't matter
    color_types: dict[str, bool] = {c: True for c in ("u", "p", "s", "w")}
    if Processor.MIXER not in available:
        color_types["s"] = False
        color_types["w"] = False
        if Processor.PAINTER not in available and not is_crystal:
            color_types["p"] = False
    if is_crystal:
        color_types["u"] = False
    if complexity < white_comp:
        color_types["w"] = False
    if important and tasked[Processor.MIXER]:
        color_types["p"] = False
        if Processor.PAINTER in available:
            color_types["u"] = False
    elif complexity < mixing_comp:
        color_types["s"] = False
        if complexity < base_comp and not (important and tasked[Processor.PAINTER]):
            color_types["p"] = False
    if important and tasked[Processor.PAINTER]:
        color_types["u"] = False
    if Processor.PAINTER not in available and not is_crystal:
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
        colors.extend(("y", "c", "p"))

    # Try to make color scheme a bit nicer
    if shape:
        preferred_layer = world.random.choice(shape)
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
        raise Exception(f"No color left to pick:\n"
                        f"complexity = {complexity}, shape = {shape}, is crystal = {is_crystal},\n"
                        f"available = {available}, tasked = {tasked}, important = {important}")

    final = world.random.choice(colors)
    if final in "ypcw":
        tasked[Processor.MIXER] = False
    if final != "u" and not is_crystal:
        tasked[Processor.PAINTER] = False
    return final


def stack(world: "Shapez2World", shape: list[str], layer: str, tasked: list[bool],
          has_non_crystal: bool, crystal_colors: int, already_has_crystals: bool) -> None:

    tasked[Processor.STACKER] = False

    if already_has_crystals:
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
            if tasked[Processor.ROTATOR]:
                layer = layer[6:8] + layer[0:6]
                tasked[Processor.ROTATOR] = False
            for i in range(0, 8, 2):
                if layer[i] not in "Pc-" and shape[-1][i] != "-":
                    break
            else:
                tasked[Processor.ROTATOR] = False
                for _ in range(3):
                    layer = layer[6:8] + layer[0:6]
                    if layer[0] not in "Pc-" and shape[-1][0] != "-":
                        break
                else:
                    raise Exception(f"new layer supposed to be placed on top, but not possible:\n"
                                    f"shape = {shape}, new layer = {layer}, "
                                    f"already has crystals = {already_has_crystals}")
            crys_col = ""
            for i in range(0, 8, 2):
                if layer[i] == "c":
                    crys_col = layer[i+1]
                    break
            fill_crystal(shape, crys_col)
            shape.append(layer)
        else:
            for j in range(0, 8, 2):
                if layer[j:j+2] != "--" and shape[-1][j:j+2] != "--":
                    shape.append(layer)
                    break
            else:
                for i in reversed(range(len(shape) - 1)):
                    for j in range(0, 8, 2):
                        if layer[j:j+2] != "--" and shape[i][j:j+2] != "--":
                            shape[i+1] = merge_layers(layer, shape[i+1])
                            break
                    else:
                        continue
                    break
                else:
                    shape[0] = merge_layers(layer, shape[0])
    else:
        for j in range(0, 8, 2):
            if layer[j:j+2] != "--" and shape[0][j:j+2] != "--":
                shape.insert(0, layer)
                for i in range(0, 8, 2):
                    if shape[0][i] == "-" and shape[1][i] == "P":
                        for k in range(2, len(shape)):
                            if shape[k][i] != "P":
                                shape[k-1] = shape[k-1][:i] + "-" + shape[k-1][i+1:]
                                shape[0] = shape[0][:i] + "P" + shape[0][i+1:]
                                break
                        else:
                            shape[-1] = shape[-1][:i] + "-" + shape[-1][i+1:]
                            shape[0] = shape[0][:i] + "P" + shape[0][i+1:]
                break
        else:
            shape[0] = merge_layers(layer, shape[0])


def merge_layers(layer_1: str, layer_2: str) -> str:
    merged = ""
    for k in range(0, 8, 2):
        if layer_1[k:k + 2] != "--":
            merged += layer_1[k:k + 2]
        else:
            merged += layer_2[k:k + 2]
    return merged


def fill_crystal(shape: list[str], color: str) -> None:
    for j in range(len(shape)):
        for i in range(1, 8, 2):
            if shape[j][i] == "-":
                shape[j] = shape[j][:i-1] + "c" + color + shape[j][i+1:]


def _bulk_possible(variants: list[bool], complexity: int, v: tuple[int, ...], *vc: tuple[int, int]):
    # IMPORTANT: Always sort by complexity in bulks
    for vv in v:
        variants[vv] = True
    for vv, cc in vc:
        if complexity >= cc:
            variants[vv] = True
        else:
            break


def _subvariant(world: "Shapez2World", shape: list[str], available: list[Processor], tasked: list[bool],
                important: bool, already_has_crystals, complexity: int, swapper_stacker: bool, a: int, b: int,
                c1: bool, c2: bool, c3: bool | None, c4: bool | None, kind: int, has_non_crys: bool, crys_col: int):
    if swapper_stacker:
        if Processor.SWAPPER in available:
            complexity -= a
            if Processor.STACKER not in available:
                tasked[Processor.SWAPPER] = False
        else:
            complexity -= b
            tasked[Processor.STACKER] = False
    complexity_1 = world.random.triangular(0, complexity).__int__()
    complexity_2 = 0 if c3 is None else world.random.triangular(0, complexity - complexity_1).__int__()
    complexity_3 = 0 if c4 is None else world.random.triangular(0, complexity - complexity_1 - complexity_2).__int__()
    complexity -= complexity_1 + complexity_2 + complexity_3
    p1 = generate_shape(world) + generate_color(
        world, complexity_1, shape, False, available, tasked, important
    ) if not c1 else "c" + generate_color(world, complexity_1, shape, True, available, tasked, important)
    p2 = generate_shape(world) + generate_color(
        world, complexity, shape, False, available, tasked, important
    ) if not c2 else "c" + generate_color(world, complexity, shape, True, available, tasked, important)
    p3 = "--" if c3 is None else (
        generate_shape(world) + generate_color(
            world, complexity_2, shape, False, available, tasked, important
        ) if not c3 else "c" + generate_color(world, complexity_2, shape, True, available, tasked, important)
    )
    p4 = "--" if c4 is None else (
        generate_shape(world) + generate_color(
            world, complexity_3, shape, False, available, tasked, important
        ) if not c4 else "c" + generate_color(world, complexity_3, shape, True, available, tasked, important)
    )
    if kind == 0:  # All same type
        stack(world, shape, p1 + p2 + p3 + p4, tasked, has_non_crys, crys_col, already_has_crystals)
    elif kind == 1:  # 3 to 1 types
        ordered = [p1, p2, p3, p4]
        world.random.shuffle(ordered)
        stack(world, shape, "".join(ordered), tasked, has_non_crys, crys_col, already_has_crystals)
    elif kind == 2:  # half-half types
        # p1-p2 and p3-p4 same types
        possible = [
            p1 + p2 + p3 + p4, p2 + p1 + p3 + p4, p1 + p2 + p4 + p3, p2 + p1 + p4 + p3,
            p3 + p1 + p2 + p4, p3 + p2 + p1 + p4, p4 + p1 + p2 + p3, p4 + p2 + p1 + p3,
            p3 + p4 + p1 + p2, p3 + p4 + p2 + p1, p4 + p3 + p1 + p2, p4 + p3 + p2 + p1,
            p2 + p3 + p4 + p1, p1 + p3 + p4 + p2, p2 + p4 + p3 + p1, p1 + p4 + p3 + p2,
        ]
        stack(world, shape, world.random.choice(possible), tasked, has_non_crys, crys_col, already_has_crystals)
    elif kind == 3:  # cornered/checkered types
        # p1-p2 and p3-p4 same type
        possible = [
            p1 + p3 + p2 + p4, p2 + p3 + p1 + p4, p1 + p4 + p2 + p3, p2 + p4 + p1 + p3,
            p3 + p1 + p4 + p2, p3 + p2 + p4 + p1, p4 + p1 + p3 + p2, p4 + p2 + p3 + p1,
        ]
        stack(world, shape, world.random.choice(possible), tasked, has_non_crys, crys_col, already_has_crystals)
