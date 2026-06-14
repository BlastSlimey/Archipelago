
def average(c1: int, c2: int) -> int:
    return (((c1 & 0xff0000) + (c2 & 0xff0000)) // 2 & 0xff0000) + (((c1 & 0xff00) + (c2 & 0xff00)) // 2 & 0xff00) + (((c1 & 0xff) + (c2 & 0xff)) // 2 & 0xff)


def addition(c1: int, c2: int) -> int:
    return min((c1 & 0xff0000) + (c2 & 0xff0000), 0xff0000) + min((c1 & 0xff00) + (c2 & 0xff00), 0xff00) + min((c1 & 0xff) + (c2 & 0xff), 0xff)


def modulo_addition(c1: int, c2: int) -> int:
    return ((c1 & 0xff0000) + (c2 & 0xff0000) & 0xff0000) + ((c1 & 0xff00) + (c2 & 0xff00) & 0xff00) + ((c1 & 0xff) + (c2 & 0xff) & 0xff)


def subtraction(c1: int, c2: int) -> int:
    return abs((c1 & 0xff0000) - (c2 & 0xff0000)) + abs((c1 & 0xff00) - (c2 & 0xff00)) + abs((c1 & 0xff) - (c2 & 0xff))


def maximum(c1: int, c2: int) -> int:
    return max((c1 & 0xff0000), (c2 & 0xff0000)) + max((c1 & 0xff00), (c2 & 0xff00)) + max((c1 & 0xff), (c2 & 0xff))


def minimum(c1: int, c2: int) -> int:
    return min((c1 & 0xff0000), (c2 & 0xff0000)) + min((c1 & 0xff00), (c2 & 0xff00)) + min((c1 & 0xff), (c2 & 0xff))


item_names = {
    average: "Average (Calculation)",
    addition: "Addition (Calculation)",
    modulo_addition: "Modulo Addition (Calculation)",
    subtraction: "Subtraction (Calculation)",
    maximum: "Maximum (Calculation)",
    minimum: "Minimum (Calculation)",
}
