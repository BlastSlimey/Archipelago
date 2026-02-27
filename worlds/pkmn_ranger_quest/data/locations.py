
table: dict[str, int] = {  # DO NOT modify in generation, it's directly used as the location lookup table
    f"Complete quest #{i}": i
    for i in range(1, 1001)
} | {
    "Inspect a pokémon": 10000
}
