from p1_support import load_level, show_level
from math import sqrt


def dfs(src, dst, graph, adj):
	
	prev = {}

	prev[src] = None
	stack = [src]

	while stack:
		node = stack.pop()

		if node == dst:
			break

		neighbors = adj(graph, node)
		for next_node in neighbors:
			if next_node not in prev:
				prev[next_node] = node
				stack.append(next_node)

	if node == dst:
		path = []
		while node:
			path.append(node)
			node = prev[node]
		path.reverse()
		return path
	else:
		return []

def get_steps(level, cell):
	
	steps = []
	x, y = cell
	for dx in [-1,0,1]:
		for dy in [-1,0,1]:
			next_cell = (x + dx, y + dy)
			dist = sqrt(dx*dx+dy*dy)
			if dist > 0 and next_cell in level['spaces']:
				steps.append(next_cell)

	return steps


def test_route(filename, src_waypoint, dst_waypoint):

	level = load_level(filename)

	src = level['waypoints'][src_waypoint]
	dst = level['waypoints'][dst_waypoint]


	path = dfs(src, dst, level, get_steps)

	show_level(level, path)

if __name__ ==  '__main__':
	import sys
	_, filename, src_waypoint, dst_waypoint = sys.argv
	print filename, src_waypoint, dst_waypoint
	test_route(filename, src_waypoint, dst_waypoint)