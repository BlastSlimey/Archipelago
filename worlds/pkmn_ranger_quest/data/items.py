from . import CaptureItemData, AssistItemData, FieldItemData, pokemon


capture: dict[str, CaptureItemData] = {
    f"Capture {'an' if name in 'AEIOU' else 'a'} {name}": CaptureItemData(data.number + 1000, data.number,
                                                                          pokemon.internal_ids[name])
    for name, data in pokemon.by_name.items()
}

assist: dict[str, AssistItemData] = {  # TODO get missing ids
    "Use a Fighting type Poké Assist": AssistItemData(101, 1),
    "Use a Poison type Poké Assist": AssistItemData(102, 2),
    "Use a Ground type Poké Assist": AssistItemData(103, 3),
    "Use a Flying type Poké Assist": AssistItemData(104, 4),
    "Use a Bug type Poké Assist": AssistItemData(105, 5),
    "Use a Rock type Poké Assist": AssistItemData(106, 6),
    "Use a Ghost type Poké Assist": AssistItemData(107, 7),
    # "Use a ??? type Poké Assist": AssistItemData(108, 8),
    "Use a Fire type Poké Assist": AssistItemData(109, 9),
    "Use a Water type Poké Assist": AssistItemData(110, 10),
    # "Use a ??? type Poké Assist": AssistItemData(111, 11),
    "Use a Grass type Poké Assist": AssistItemData(112, 12),
    "Use an Ice type Poké Assist": AssistItemData(113, 13),
    # "Use a ??? type Poké Assist": AssistItemData(114, 14),
    # "Use a ??? type Poké Assist": AssistItemData(115, 15),
    "Use a Dark type Poké Assist": AssistItemData(116, 16),
    # "Use a ??? type Poké Assist": AssistItemData(117, 17),
}

_field_ids: list[tuple[str, int]] = [  # TODO ids are only placeholders
    ("Cross", 1),
    ("Cut", 2),
    ("Crush", 3),
    ("Soak", 4),
    ("Burn", 5),
    ("Recharge", 6),
    ("Tackle", 7),
    ("Gust", 8),
    # ("Flash", 9), missions only
]

field_any: dict[str, FieldItemData] = {
    f"Use a {name} Field Move": FieldItemData(200 + field_id, field_id, 0)
    for name, field_id in _field_ids
}

field_level: dict[str, FieldItemData] = {
    f"Use a {name} Field Move (Level {i})": FieldItemData(200 + i*100 + field_id, field_id, 0)
    for name, field_id in _field_ids[1:]  # [1:] because Cross doesn't have multiple levels
    for i in (1, 2, 3)
}
