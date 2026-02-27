from test.bases import WorldTestBase


class RangerQuestTestBase(WorldTestBase):
    game = "Pokemon Ranger (Quest)"


class TestDefault(RangerQuestTestBase):
    options = {"quest_count": 20}


class TestLowQuestCount(RangerQuestTestBase):
    options = {"quest_count": 5, "goal_amount": 5}


class TestMinimumQuestCount(RangerQuestTestBase):
    options = {"quest_count": 1, "goal_amount": 1}


class TestMaximumQuestCount(RangerQuestTestBase):
    options = {"quest_count": 200, "duplicate_quests": True}


class TestLessGoalAmount(RangerQuestTestBase):
    options = {"goal_amount": 10}


class TestMinimumGoalAmount(RangerQuestTestBase):
    options = {"goal_amount": 1}


class TestAllQuestTypes(RangerQuestTestBase):
    options = {"modify_quest_pool": [
        "Captures (off-mission)",
        "Captures (missions-only)",
        "Legendary captures (off-mission)",
        "Captures (special missions)",
        "Poké Assists",
        # "Field moves (any level)",
        # "Field moves (specific level)",
    ]}


class TestSomeBlacklistedCaptures(RangerQuestTestBase):
    options = {"captures_blacklist": ["Snorlax", "Blastoise", "Ekans"]}


class TestSomeQuestPlando(RangerQuestTestBase):
    options = {"quest_plando": {"Capture a Blastoise": 1, "Use a Fire type Poké Assist": 1, "Capture a Mew": 3}}
