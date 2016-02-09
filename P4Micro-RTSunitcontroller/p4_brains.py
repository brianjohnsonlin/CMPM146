import random

# EXAMPLE STATE MACHINE
class MantisBrain:

	def __init__(self, body):
		self.body = body
		self.state = 'idle'
		self.target = None

	def handle_event(self, message, details):

		if self.state is 'idle':

			if message == 'timer':
				# go to a random point, wake up sometime in the next 10 seconds
				world = self.body.world
				x, y = random.random()*world.width, random.random()*world.height
				self.body.go_to((x,y))
				self.body.set_alarm(random.random()*10)

			elif message == 'collide' and details['what'] == 'Slug':
				# a slug bumped into us; get curious
				self.state = 'curious'
				self.body.set_alarm(1) # think about this for a sec
				self.body.stop()
				self.target = details['who']

		elif self.state == 'curious':

			if message == 'timer':
				# chase down that slug who bumped into us
				if self.target:
					if random.random() < 0.5:
						self.body.stop()
						self.state = 'idle'
					else:
						self.body.follow(self.target)
					self.body.set_alarm(1)
			elif message == 'collide' and details['what'] == 'Slug':
				# we meet again!
				slug = details['who']
				slug.amount -= 0.01 # take a tiny little bite
		
class SlugBrain:

	def __init__(self, body):
		self.body = body
		self.state = 'idle'
		self.target = None
		self.have_resource = False
	
	def go_idle(self):
		self.state = 'idle'
		self.target = None
		self.body.stop()

	# TODO: IMPLEMENT THIS METHOD
	#  (Use helper methods and classes to keep your code organized where
	#  approprioate.)
	def handle_event(self, message, details):
		if message == 'order' and self.state is not 'flee':
			if type(details) == tuple:
				self.go_idle()
				self.body.go_to(details)
			elif type(details) == str:
				if details == 'i':
					self.go_idle()
				elif details == 'a':
					self.state = 'attack'
				elif details == 'h':
					self.state = 'harvest'
				elif details == 'b':
					self.state = 'build'
			self.body.set_alarm(0) #reset timer
		
		elif message == 'timer': #timer is a loop that makes checks
			if self.state == 'flee' and self.body.amount == 1.0: #check if no need to flee
				self.go_idle()
			try: #update target
				if self.state == 'attack':
					self.target = self.body.find_nearest('Mantis')
				elif self.state == 'build' or self.state == 'flee':
					self.target = self.body.find_nearest('Nest')
				elif self.state == 'harvest':
					if self.have_resource:
						self.target = self.body.find_nearest('Nest')
					else:
						self.target = self.body.find_nearest('Resource')
			except: #if no target, go to idle
				self.go_idle()
			if self.target is not None: #follow target
				self.body.follow(self.target)
			self.body.set_alarm(1) #start new timer
		
		elif message == 'collide':
			if self.body.amount < 0.5: #check if need to flee
				self.state = 'flee' #health can only lower from a collision event, so this is the only check
			if self.state == 'attack' and details['what'] == 'Mantis':
				details['who'].amount -= 0.05
			elif self.state == 'build' and details['what'] == 'Nest':
				details['who'].amount += 0.01
			elif self.state == 'flee' and details['what'] == 'Nest':
				self.body.amount += 0.05
			elif self.state == 'harvest':
				if not self.have_resource and details['what'] == 'Resource':
					details['who'].amount -= 0.25
					self.have_resource = True
				elif self.have_resource and details['what'] == 'Nest':
					self.have_resource = False
			self.body.set_alarm(0) #reset timer
				

world_specification = {
	#'worldgen_seed': 13, # comment-out to randomize
	'nests': 2,
	'obstacles': 25,
	'resources': 5,
	'slugs': 5,
	'mantises': 5,
}

brain_classes = {
	'mantis': MantisBrain,
	'slug': SlugBrain,
}
