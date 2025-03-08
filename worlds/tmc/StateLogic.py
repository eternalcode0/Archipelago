def elementCount(state, player):
    return sum(map(lambda item: state.has(item, player), [
        "Earth Element",
        "Fire Element",
        "Water Element",
        "Wind Element"
    ]))

def swordCount(state, player):
    return sum(map(lambda item: state.has(item, player), [
        "Smith's Sword",
        "White Sword (Green)",
        "White Sword (Red)",
        "White Sword (Blue)",
        "Four Sword",
    ]))

def canShield(state, player):
    return state.has("Small Shield", player) or state.has("Mirror Shield", player)

def canAttack(state, player):
    return state.has("Smith's Sword", player)

def canPassTrees(state, player):
    return canAttack(state, player) or state.has("Lantern", player)
