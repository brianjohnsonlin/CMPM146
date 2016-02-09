import random

def think(state, quip):

	moves = state.get_moves()
	movesplus1 = []
	movesplus2 = []

	for move in moves:
		test_state = state.copy()
		test_state.apply_move(move)
		me = state.get_whos_turn()
		if test_state.get_score()[me] - state.get_score()[me] == 1:
			movesplus1.append(move)
		elif test_state.get_score()[me] - state.get_score()[me] == 2:
			movesplus2.append(move)
	
	if len(movesplus2) > 0:
		return random.choice(movesplus2)
	elif len(movesplus1) > 0:
		return random.choice(movesplus1)
	else:
		return random.choice(moves)
