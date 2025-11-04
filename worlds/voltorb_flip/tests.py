import random

from test.bases import WorldTestBase


class VoltorbFlipTestBase(WorldTestBase):
    game = "Voltorb Flip"
    options = {"accessibility": "full"}


class TestRandom1(VoltorbFlipTestBase):
    coins_maximum = random.randint(10, 50000)
    options = {
        "goal": "random",
        "level_locations_adjustments": {
            "Maximum": random.randint(1, 9),
        },
        "coin_locations_adjustments": {
            "Maximum": coins_maximum,
            "Steps": random.randint(10, coins_maximum),
        },
        "artificial_logic": "random",
    }


class TestRandom2(TestRandom1):
    coins_maximum = random.randint(10, 50000)
    options = {
        "goal": "random",
        "level_locations_adjustments": {
            "Maximum": random.randint(1, 9),
        },
        "coin_locations_adjustments": {
            "Maximum": coins_maximum,
            "Steps": random.randint(10, coins_maximum),
        },
        "artificial_logic": "random",
    }


class TestRandom3(TestRandom1):
    coins_maximum = random.randint(10, 50000)
    options = {
        "goal": "random",
        "level_locations_adjustments": {
            "Maximum": random.randint(1, 9),
        },
        "coin_locations_adjustments": {
            "Maximum": coins_maximum,
            "Steps": random.randint(10, coins_maximum),
        },
        "artificial_logic": "random",
    }


class TestRandom4(TestRandom1):
    coins_maximum = random.randint(10, 50000)
    options = {
        "goal": "random",
        "level_locations_adjustments": {
            "Maximum": random.randint(1, 9),
        },
        "coin_locations_adjustments": {
            "Maximum": coins_maximum,
            "Steps": random.randint(10, coins_maximum),
        },
        "artificial_logic": "random",
    }


class TestRandom5(TestRandom1):
    coins_maximum = random.randint(10, 50000)
    options = {
        "goal": "random",
        "level_locations_adjustments": {
            "Maximum": random.randint(1, 9),
        },
        "coin_locations_adjustments": {
            "Maximum": coins_maximum,
            "Steps": random.randint(10, coins_maximum),
        },
        "artificial_logic": "random",
    }


class TestRandom6(TestRandom1):
    coins_maximum = random.randint(10, 50000)
    options = {
        "goal": "random",
        "level_locations_adjustments": {
            "Maximum": random.randint(1, 9),
        },
        "coin_locations_adjustments": {
            "Maximum": coins_maximum,
            "Steps": random.randint(10, coins_maximum),
        },
        "artificial_logic": "random",
    }


class TestRandom7(TestRandom1):
    coins_maximum = random.randint(10, 50000)
    options = {
        "goal": "random",
        "level_locations_adjustments": {
            "Maximum": random.randint(1, 9),
        },
        "coin_locations_adjustments": {
            "Maximum": coins_maximum,
            "Steps": random.randint(10, coins_maximum),
        },
        "artificial_logic": "random",
    }


class TestRandom8(TestRandom1):
    coins_maximum = random.randint(10, 50000)
    options = {
        "goal": "random",
        "level_locations_adjustments": {
            "Maximum": random.randint(1, 9),
        },
        "coin_locations_adjustments": {
            "Maximum": coins_maximum,
            "Steps": random.randint(10, coins_maximum),
        },
        "artificial_logic": "random",
    }


class TestRandom9(TestRandom1):
    coins_maximum = random.randint(10, 50000)
    options = {
        "goal": "random",
        "level_locations_adjustments": {
            "Maximum": random.randint(1, 9),
        },
        "coin_locations_adjustments": {
            "Maximum": coins_maximum,
            "Steps": random.randint(10, coins_maximum),
        },
        "artificial_logic": "random",
    }
