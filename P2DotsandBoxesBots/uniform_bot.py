import random
def think(state, quip):
  return random.choice(state.get_moves())
