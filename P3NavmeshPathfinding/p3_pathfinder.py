from sys import maxint
from math import hypot
from heapq import heappush, heappop

def find_path(source_point, destination_point, mesh):
	source = in_box(source_point, mesh['boxes'])
	destination = in_box(destination_point, mesh['boxes'])
	
	#test for valid points
	if source is None or destination is None:
		print "Invalid points!"
		return ([], [])
	
	#test to see if in the same box
	found = None
	if source is destination:
		found = source
	
	#A*
	detail_points = {source:source_point, destination:destination_point}
	forward_visited = {source:True}
	backward_visited = {destination:True}
	forward_dist = {source:0}
	backward_dist = {destination:0}
	forward_prev = {source:None}
	backward_prev = {destination:None}
	queue = [(0, source, destination), (0, destination, source)]
	for i in mesh['boxes']:
		if i is not source and i is not destination:
			forward_dist[i] = maxint
			backward_dist[i] = maxint
	while queue and not found:
		_, box, goal = heappop(queue)
		for n in mesh['adj'][box]:
			dp = detail_points[box]
			if dp[0] < n[0]:
				pointx = n[0]
			elif dp[0] > n[1]:
				pointx = n[1]
			else:
				pointx = dp[0]
			if dp[1] < n[2]:
				pointy = n[2]
			elif dp[1] > n[3]:
				pointy = n[3]
			else:
				pointy = dp[1]
			if goal is destination:
				alt = forward_dist[box] + distance((pointx, pointy), dp)
				if alt < forward_dist[n]:
					forward_dist[n] = alt
					forward_prev[n] = box
					heappush(queue, (alt + distance((pointx, pointy), destination_point), n, destination))
					forward_visited[n] = True
					if n is destination or n in backward_visited:
						found = n
						break
					detail_points[n] = (pointx, pointy)
			elif goal is source:
				alt = backward_dist[box] + distance((pointx, pointy), dp)
				if alt < backward_dist[n]:
					backward_dist[n] = alt
					backward_prev[n] = box
					heappush(queue, (alt + distance((pointx, pointy), source_point), n, source))
					backward_visited[n] = True
					if n is source or n in forward_visited:
						found = n
						break
					detail_points[n] = (pointx, pointy)

	#test for no path
	if not found:
		print "No path!"
		return ([], [])
	else:
		#reconstruct path
		curr = found
		path = []
		while forward_prev[curr]:
			path.insert(0, (detail_points[forward_prev[curr]], detail_points[curr]))
			curr = forward_prev[curr]
		curr = found
		while backward_prev[curr]:
			path.insert(0, (detail_points[backward_prev[curr]], detail_points[curr]))
			curr = backward_prev[curr]
		return (path, forward_visited.keys() + backward_visited.keys())

def distance(a, b):
	return hypot(a[0] - b[0], a[1] - b[1])

def in_box(point, boxes):
	x,y = point
	for box in boxes:
		bx1,bx2,by1,by2 = box
		if x >= bx1 and x < bx2 and y >= by1 and y < by2:
			return box
