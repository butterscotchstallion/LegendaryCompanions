"""
AI Archetypes that can be used for companions
"""


class AIArchetype:
    def __init__(self, name):
        self.name = name


class HealerRanged(AIArchetype):
    def __init__(self):
        self.name = "healer_ranged"


class HealerMelee(AIArchetype):
    def __init__(self):
        self.name = "healer_melee"


class MindFlayer(AIArchetype):
    def __init__(self, name):
        self.name = "mindflayer"
