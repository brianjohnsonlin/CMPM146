import time
import random
import math

def think(state, quip):
	def reward(score, me):
		if me == 'red':
			return score['red'] - score['blue']
		else:
			return score['blue'] - score['red']
	
	moves = state.get_moves()
	rootnode = Node(state, None, None)
	t_start = time.time()
	t_deadline = t_start + 1
	iterations = 0
	
	while time.time() < t_deadline:
		iterations += 1
		node = rootnode
		test_state = state.copy()

		# Select
		while node.untried_moves == [] and node.children != []:# node is fully expanded and non-terminal
			node = node.UCTSelectChild()
			test_state.apply_move(node.move)

		# Expand
		if node.untried_moves != []: # if we can expand (i.e. state/node is non-terminal)
			m = random.choice(node.untried_moves) 
			currentPlayer = test_state.get_whos_turn()
			test_state.apply_move(m)
			node = node.addChild(test_state, m, currentPlayer) # add child and descend tree
		
		# Rollout - this can often be made orders of magnitude quicker using a state.GetRandomMove() function
		rolloutIter = 0
		while rolloutIter < 5 and test_state.get_moves() != []: # while state is non-terminal
			test_state.apply_move(random.choice(test_state.get_moves()))
			rolloutIter += 1
		
		# Backpropagate
		while node != None: # backpropagate from the expanded node and work back to the root node
			node.update(reward(test_state.get_score(), node.who)) # state is terminal
			node = node.parent
	
	quip("rollout rate: " + str(float(iterations)/(time.time() - t_start)) + " iterations per second")
	return sorted(rootnode.children, key = lambda c: c.visits)[-1].move # return the move that was most visited

class Node:
	def __init__(self, state, parent = None, move = None, who = None):
		self.parent = parent
		self.who = who
		self.children = []
		self.untried_moves = state.get_moves()
		self.visits = 0
		self.score = 0.0
		self.move = move
		
	def UCTSelectChild(self):
		s = sorted(self.children, key = lambda c: c.score/c.visits + math.sqrt(2*math.log(self.visits)/c.visits))[-1]
		return s
	
	def addChild(self, state, move, who):
		n = Node(state, self, move, who)
		self.untried_moves.remove(move)
		self.children.append(n)
		return n
	
	def update(self, score):
		self.visits += 1
		self.score += score
