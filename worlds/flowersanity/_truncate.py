
options = {
    "min_votes": 9,
}


def default():
    with open("data/colornames_trunc.txt", "rt") as infile, open("data/colornames_trunc.py", "wt") as outfile:
        outfile.write("\n")
        for key, val in options.items():
            outfile.write(f"{key} = {val}\n")
        outfile.write("\ncolors: dict[int, tuple[str, int]] = {\n")
        lines = infile.readlines()
        names = set()
        for i in range(len(lines)):
            parts = lines[i][:-1].split(",")
            value = tuple(int(parts[0][j:j+2], 16) for j in (0, 2, 4))
            votes = int(parts[2])
            if sum(not 16 <= p <= 240 for p in value) > 1:
                if votes < 100:
                    continue
            elif any(not 16 <= p <= 240 for p in value):
                if votes < 25:
                    continue
            else:
                if votes < 9:
                    continue
            if parts[1].casefold() in names:
                continue
            outfile.write(f"    0x{parts[0]}: (\"{parts[1]}\", {votes}),\n")
            names.add(parts[1].casefold())
        outfile.write("}\n")


def testing():
    with open("temp/colornames.txt", "rt") as infile, open("temp/colornames_trunc_test.txt", "wt") as outfile:
        lines = infile.readlines()
        names = set()
        for i in range(1, len(lines)):
            parts = lines[i][:-1].split(",")
            votes = int(parts[2])
            if votes < 500:
                continue
            if parts[1].casefold() in names:
                continue
            outfile.write(lines[i])
            names.add(parts[1].casefold())


if __name__ == "__main__":
    default()
    # testing()
    pass
