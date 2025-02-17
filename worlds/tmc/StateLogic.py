def canShield(state, player):
    return state.has("Small Shield", player) or state.has("Mirror Shield", player)

def canAttack(state, player):
    return state.has("Smith's Sword", player)
