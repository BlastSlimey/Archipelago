from typing import Any

from ...output import Shapez2ScenarioContainer


def get_fixed_patches(container: "Shapez2ScenarioContainer") -> list[dict[str, Any]]:
    return [  # TODO add variation and colors
        {
            "Shape":"RuRuRuRu",
            "Position_LC":{"x":31,"y":30},
            "LocalTiles":[{},{"x":-1,"y":-2},{"y":-1},{"x":-1,"y":-1}]
        },
        {
            "Shape":"SuSuSuSu",
            "Position_LC":{"x":31,"y":34},
            "LocalTiles":[{},{"y":1},{"x":-1,"y":1},{"x":-1,"y":2}]
        },
        {
            "Shape":"CuCuCuCu",
            "Position_LC":{"x":29,"y":32},
            "LocalTiles":[{},{"x":-1},{"x":-1,"y":-1},{"x":-2}]
        },
        {
            "Shape":"WuWuWuWu",
            "Position_LC":{"x":33,"y":32},
            "LocalTiles":[{},{"x":1},{"y":1},{"y":-1}]
        }
    ]


def get_starting_chunks(container: "Shapez2ScenarioContainer") -> list[dict[str, Any]]:
    ...
