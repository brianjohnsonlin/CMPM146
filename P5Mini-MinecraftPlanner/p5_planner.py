from collections import namedtuple
from sys import maxint
from heapq import heappush, heappop
import time
import json
with open('Crafting.json') as f:
	Crafting = json.load(f)

def make_checker(rule):
	def check(state):
		if 'Consumes' in rule:
			for name, quan in rule['Consumes'].items():
				if state[1][Crafting['Items'].index(name)] < quan:
					return False
		if 'Requires' in rule:
			for name, bool in rule['Requires'].items():
				if not bool:
					continue
				if state[1][Crafting['Items'].index(name)] == 0:
					return False
		return True
	return check

def make_effector(rule):
	def effect(state):
		inv = list(state[1])
		if 'Consumes' in rule:
			for name, quan in rule['Consumes'].items():
				inv[Crafting['Items'].index(name)] = state[1][Crafting['Items'].index(name)] - quan
		for name, quan in rule['Produces'].items():
			inv[Crafting['Items'].index(name)] = state[1][Crafting['Items'].index(name)] + quan
		return tuple(inv)
	return effect

def make_goal_checker(goal):
	def is_goal(state):
		for name, quan in goal.items():
			if state[1][Crafting['Items'].index(name)] < quan:
				return False
		return True
	return is_goal

def graph(state):
	for r in all_recipes:
		if r.check(state):
			yield (r.name, r.effect(state), r.cost)

def heuristic(state):
	for i in Crafting['Items']:
		if i not in Crafting['Goal']: # unless the goal wants more
			if i == 'bench' or i == 'furnace' or "axe" in i: # tools
				if state[1][Crafting['Items'].index(i)] > 1: # we only need one of these
					return maxint-1000 # big number, but not as big as maxint
			elif i == 'wood' or i == 'ore' or i == "coal": # can be used singularly
				if state[1][Crafting['Items'].index(i)] > 1:
					return maxint-1000
			elif i == 'ingot': # need 6 for rails
				if state[1][Crafting['Items'].index(i)] > 6:
					return maxint-1000
			elif i == 'plank' or i == 'stick': # produced in 4s
				if state[1][Crafting['Items'].index(i)] > 7:
					return maxint-1000
			elif i == 'cobble': # need 8 for furnace
				if state[1][Crafting['Items'].index(i)] > 8:
					return maxint-1000					
	return 0

def closer_to_goal(old_state, new_state):
	for item, quan in Crafting['Goal'].items():
		oldquan = old_state[1][Crafting['Items'].index(item)]
		newquan = new_state[1][Crafting['Items'].index(item)]
		if oldquan < quan and newquan > oldquan:
			return True
	return False

def search(graph, initial, is_goal, limit, heuristic): # A*
	t_start = time.time()
	found = None
	initial_g = ('', initial[1], initial[2])
	visited = {initial_g:True}
	dist = {initial_g:0}
	prev = {initial_g:None}
	queue = [(0, initial)]
	checkpoint = initial
	while queue and time.time() < t_start + limit and not found:
		_, node = heappop(queue)
		node_g =('', node[1], node[2])
		if closer_to_goal(checkpoint, node):
			checkpoint = node
			queue = []
		for n in graph(node):
			if time.time() > t_start + limit:
				break
			if is_goal(node):
				found = node
				break
			n_g =('', n[1], n[2])
			alt = dist[node_g] + n[2]
			if n_g not in dist:
				dist[n_g] = maxint
			if alt < dist[n_g]:
				dist[n_g] = alt
				prev[n_g] = node
				heappush(queue, (alt + heuristic(n_g), n))
				visited[n_g] = True
	if not found:
		if time.time() >= t_start + limit:
			return "Timed out!" 
		else:
			return "Not possible!"
	else:
		curr = found
		curr_g = ('', curr[1], curr[2])
		plan = []
		while prev[curr_g]:
			plan.insert(0, curr[0])
			curr = prev[curr_g]
			curr_g = ('', curr[1], curr[2])
	return {"cost": dist[('', found[1], found[2])], "len": len(plan), "time": time.time() - t_start}

def make_initial_state(inventory):
	return ('start', tuple(inventory.get(name,0) for i,name in enumerate(Crafting['Items'])), 0)

# main function
Recipe = namedtuple('Recipe',['name','check','effect','cost'])
all_recipes = []
for name, rule in Crafting['Recipes'].items():
	checker = make_checker(rule)
	effector = make_effector(rule)
	recipe = Recipe(name, checker, effector, rule['Time'])
	all_recipes.append(recipe)

initial_state = make_initial_state(Crafting['Initial'])
is_goal = make_goal_checker(Crafting['Goal'])
print search(graph, initial_state, is_goal, 30, heuristic)
