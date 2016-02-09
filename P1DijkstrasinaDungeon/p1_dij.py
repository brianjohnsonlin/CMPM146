from p1_support import load_level, show_level
from math import sqrt
from heapq import heappush, heappop

def dijkstras_shortest_path(src, dst, graph, adj):
	prev = {}
	dist = {}
	queue = []
	
	prev[src] = None
	visited = [src]
	dist[src] = 0;
	queue = [(0,src)]
	node = src
	
	while queue:
		_, node = heappop(queue)
		neighbors = adj(graph, node)
		if len(neighbors) < 1:
			break
		if node == dst:
			break
		for next_el in neighbors:
			next_node, distance = next_el
			if next_node not in visited:
				alt = dist[node] + distance
				if next_node not in dist or alt < dist[next_node]:
					dist[next_node] = alt
					prev[next_node] = node
					heappush(queue, (dist[next_node], next_node))
		visited.append(node)

	if node == dst:
		path = []
		while node:
			path.append(node)
			node = prev[node]
		path.reverse()
		return path
	else:
		return []

def navigation_edges(level, cell):
	steps = []
	x, y = cell
	for dx in [-1,0,1]:
		for dy in [-1,0,1]:
			next_cell = (x + dx, y + dy)
			dist = sqrt(dx*dx+dy*dy)
			if dist > 0 and next_cell in level['spaces']:
				steps.append((next_cell, dist))
	return steps

def test_route(filename, src_waypoint, dst_waypoint):
	level = load_level(filename)

	show_level(level)

	src = level['waypoints'][src_waypoint]
	dst = level['waypoints'][dst_waypoint]

	path = dijkstras_shortest_path(src, dst, level, navigation_edges)

	if path:
		show_level(level, path)
	else:
		print "No path possible!"

if __name__ ==  '__main__':
	import sys
	_, filename, src_waypoint, dst_waypoint = sys.argv
	test_route(filename, src_waypoint, dst_waypoint)
