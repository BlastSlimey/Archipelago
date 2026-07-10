from typing import NamedTuple


class VersionCompatibility(NamedTuple):
    ap_minimum: tuple[int, int, int]


version: tuple[int, int, int] = (1, 1, 0)

compatibility: dict[tuple[int, int, int], VersionCompatibility] = {
    (1, 1, 0): VersionCompatibility((0, 6, 5)),
    (1, 0, 0): VersionCompatibility((0, 6, 5)),
}


def ap_minimum() -> tuple[int, int, int]:
    return compatibility[version].ap_minimum


if __name__ == "__main__":
    import orjson
    import os
    import zipfile
    from worlds.Files import container_version

    apworld = "flowersanity"
    dev_dir = "D:/Games/Archipelago/custom_worlds/dev/"

    with zipfile.ZipFile(dev_dir + apworld + ".apworld", 'w', zipfile.ZIP_DEFLATED, True, 9) as zipf2:
        metadata = {
            "game": "Flowersanity",
            "minimum_ap_version": ".".join(str(i) for i in ap_minimum()),
            "authors": ["BlastSlimey"],
            "world_version": ".".join(str(i) for i in version),
            "version": container_version,
            "compatible_version": 7,
        }
        zipf2.writestr(os.path.join(apworld, "archipelago.json"), orjson.dumps(metadata))
        ignore: list[str] = []
        for root, dirs, files in os.walk("../"):
            if "__pycache__" in root:
                continue
            if "temp" in root:
                continue
            for file in files:
                zipf2.write(os.path.join(root, file),
                            os.path.relpath(os.path.join(root, file),
                                            "../../"))
