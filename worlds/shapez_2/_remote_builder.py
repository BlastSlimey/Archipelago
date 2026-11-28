from collections import ChainMap


def collect_maps(chain: ChainMap) -> list[dict]:
    ret = []
    for _map in chain.maps:
        if isinstance(_map, ChainMap):
            ret.extend(collect_maps(_map))
        else:
            ret.append(_map)
    return ret


if __name__ == "__main__":
    from data.items import all_remote_items, all_standard_items

    with open("docs/remote_items.md", "wt") as file:
        file.write("# List of all items and their remote names in shapez 2\n\n" +
                   "| Item name".ljust(41) + "| Remote name".ljust(41) + "|\n"
                   "|" + "-" * 40 + "|" + "-" * 40 + "|\n")
        maps = collect_maps(all_remote_items)

        for _map in maps:
            for name, data in _map.items():
                file.write(f"| {name:39}| {data.remote_id:39}|\n")
                if name in all_standard_items:
                    print(f"            [\"{name}\"] = \"{data.remote_id}\",")
