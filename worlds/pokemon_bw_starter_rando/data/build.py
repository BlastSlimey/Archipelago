
def build(name: str, version: str, author: str):
    import orjson
    import os
    import zipfile

    apworld = os.path.split(os.path.abspath("./"))[-1]

    with zipfile.ZipFile(os.path.join("../", apworld + ".apworld"), 'w', zipfile.ZIP_DEFLATED, True, 9) as zipf2:
        metadata = {
            "game": name,
            "minimum_ap_version": "0.6.4",
            "authors": [author],
            "world_version": version,
            "version": 7,
            "compatible_version": 7,
        }
        for root, dirs, files in os.walk("./"):
            if "__pycache__" in root:
                continue
            if "_temp" in root:
                continue
            for file in files:
                if file == "archipelago.json":
                    continue
                if "_temp" in file:
                    continue
                zipf2.write(os.path.join(root, file),
                            os.path.relpath(os.path.join(root, file),
                                            "../"))
        zipf2.writestr(os.path.join(apworld, "archipelago.json"), orjson.dumps(metadata))
