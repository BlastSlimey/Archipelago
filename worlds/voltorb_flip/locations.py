from BaseClasses import Location


class VoltorbFlipLocation(Location):
    game = "Voltorb Flip"


locations: dict[str, int] = {
    f"Win level {i}": i for i in range(1, 9)
} | {
    f"Collect {i} coins": i for i in range(10, 50001, 10)
}
