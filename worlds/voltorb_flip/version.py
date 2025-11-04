
from typing import NamedTuple


class VersionCompatibility(NamedTuple):
    ap_minimum: tuple[int, int, int]


# DO NOT put any number higher than 255
version: tuple[int, int, int] = (1, 1, 0)

compatibility: dict[tuple[int, int, int], VersionCompatibility] = {
    (1, 1, 0): VersionCompatibility((0, 6, 3)),
    (1, 0, 0): VersionCompatibility((0, 6, 3)),
    (0, 1, 0): VersionCompatibility((0, 6, 3)),
}


def ap_minimum() -> tuple[int, int, int]:
    return compatibility[version].ap_minimum


if __name__ == "__main__":
    import orjson, os, zipfile

    apworld = "voltorb_flip"
    dev_dir = "D:/Games/Archipelago/custom_worlds/dev/"

    with (zipfile.ZipFile(dev_dir + apworld + ".apworld", 'w', zipfile.ZIP_DEFLATED, True, 9) as zipf2):
        metadata = {
            "game": "Voltorb Flip",
            "minimum_ap_version": ".".join(str(i) for i in ap_minimum()),
            "authors": ["BlastSlimey"],
            "world_version": ".".join(str(i) for i in version)
        }
        zipf2.writestr(os.path.join(apworld, "archipelago.json"), orjson.dumps(metadata))
        for root, dirs, files in os.walk("."):
            if "__pycache__" in root:
                continue
            for file in files:
                print(f"{root} {file}")
                zipf2.write(os.path.join(root, file),
                            os.path.relpath(os.path.join(root, file),
                                            "../"))
