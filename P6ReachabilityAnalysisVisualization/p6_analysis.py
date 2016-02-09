from p6_game import Simulator

ANALYSIS = {}
PREV = {}

def analyze(design):
	sim = Simulator(design)
	# TODO: fill in this function, populating the ANALYSIS dict
	queue = [sim.get_initial_state()]
	ANALYSIS.clear()
	PREV.clear()
	ANALYSIS[sim.get_initial_state()[0]] = [sim.get_initial_state()]
	PREV[sim.get_initial_state()] = None
	while(queue):
		current_state = queue.pop()
		for move in sim.get_moves():
			next_state = sim.get_next_state(current_state, move)
			if next_state:
				if next_state not in PREV:
					position, _ = next_state # or None if character dies
					if position not in ANALYSIS:
						ANALYSIS[position] = []
					ANALYSIS[position].append(next_state)
					PREV[next_state] = current_state
					queue.append(next_state)

def inspect((i,j), draw_line):
	# TODO: use ANALYSIS and (i,j) draw some lines
	# raise NotImplementedError
	offset = 0
	color = 0
	if (i,j) in ANALYSIS:
		for end_state in ANALYSIS[(i,j)]:
			curr_state = PREV[end_state]
			last_state = end_state
			while curr_state:
				posl, abill = last_state
				pos, abil = curr_state
				if abill is not abil:
					color = color + 1
				draw_line(posl, pos, offset, color)
				last_state = curr_state
				curr_state = PREV[curr_state]
			offset = offset + 1
		