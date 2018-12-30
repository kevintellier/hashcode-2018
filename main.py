#DATASETS
A_ = "a_example.in"
B_ = "b_should_be_easy.in"
"""
C_ =
D_ =
E_ =
"""

DATASET_FILE = open(B_,"r")

lines = []
with DATASET_FILE as file:
	for line in file:
		line = line.strip()
		line = line.split()
		lines.append(line)
#CONST
R = int(lines[0][0])#Number of rows
C = int(lines[0][1])#Number of columns
F = int(lines[0][2])#Number of vehicles
N = int(lines[0][3])#Number of rides
B = int(lines[0][4])#Bonus
T = int(lines[0][5])#Number of steps

grid = [[0]*C for _ in range(R)]
vehicles_list = []
rides_list = []
score = 0

class Ride:
	def __init__(self, start_intersection, finish_intersection, earliest_start, latest_finish):
		rides_list.append(self)
		self.id = rides_list.index(self)
		self.start_intersection = start_intersection
		self.finish_intersection = finish_intersection
		self.earliest_start = earliest_start
		self.latest_finish = latest_finish
		self.vehicle_assignated = -1
		self.status = 0

	def assign_vehicle(self, vehicle):
		rides_list.remove(self)
		self.vehicle_assignated = vehicle.id
		vehicle.assign_ride(self)

class Vehicle:
	def __init__(self):
		self.pos = [0,0]
		self.current_ride = None
		self.rides = []
		self.fuel = 1
		vehicles_list.append(self)
		self.id = vehicles_list.index(self)
		self.rides_dist = 0

	def assign_ride(self, ride):
		if ride.earliest_start > self.rides_dist:
			self.rides_dist += dist(self.pos, ride.start_intersection) + dist(ride.start_intersection, ride.finish_intersection) + abs(ride.earliest_start - self.rides_dist)
		else:
			self.rides_dist += dist(self.pos, ride.start_intersection) + dist(ride.start_intersection, ride.finish_intersection)
		self.pos = ride.finish_intersection
		self.rides.append(ride)

	def next_ride(self):
		if len(self.rides) > 0:
			self.current_ride = self.rides.pop()

	def refuel(self):
		self.fuel = 1

	def go(self,pos):
		if self.fuel == 1:
			self.fuel = 0
			if self.pos[0] > pos[0]:
				self.pos[0] -= 1
			elif self.pos[0] < pos[0]:
				self.pos[0] += 1
			else:
				if self.pos[1] > pos[1]:
					self.pos[1] -= 1
				elif self.pos[1] < pos[1]:
					self.pos[1] += 1
				else:
					return 0
		else:
			return 0

def dist(start_pos, end_pos):
	return abs(end_pos[0]-start_pos[0]) + abs(end_pos[1]-start_pos[1])

#Prints header input
print(str(R) + " rows, " + str(C) + " columns, " + str(F) + " vehicles, " + str(N) + " rides, " + str(B) + " bonus, " + str(T) + " steps")
#Prints grid
print('\n'.join([''.join(['{:4}'.format(item) for item in row]) for row in grid]))

#Creates vehicles
for _ in range(F):
	Vehicle()

#Creates rides
for n in range(1,N+1):
	a = int(lines[n][0])
	b = int(lines[n][1])
	x = int(lines[n][2])
	y = int(lines[n][3])
	s = int(lines[n][4])
	f = int(lines[n][5])
	Ride([a,b], [x,y], s, f)

for ride in rides_list:
	print(str(ride.id) + " : ride from " + str(ride.start_intersection) + " to " + str(ride.finish_intersection) + ", earliest start " + str(ride.earliest_start) + ", latest finish " + str(ride.latest_finish))

#Assign rides to vehicles
for ride in rides_list:
	for vehicle in vehicles_list:
		if ride.earliest_start > vehicle.rides_dist:
			if dist(vehicle.pos, ride.start_intersection) + dist(ride.start_intersection, ride.finish_intersection) + vehicle.rides_dist + abs(ride.earliest_start-vehicle.rides_dist) < ride.latest_finish:
				ride.assign_vehicle(vehicle)
				print("Vehicle " + str(vehicle.id) + "| pos " + str(vehicle.pos) + " | rides_dist " + str(vehicle.rides_dist))
				print("Vehicle " + str(vehicle.id) + " assigned to ride " + str(ride.id))
				break
		else:
			if dist(vehicle.pos, ride.start_intersection) + dist(ride.start_intersection, ride.finish_intersection) + vehicle.rides_dist < ride.latest_finish:
				ride.assign_vehicle(vehicle)
				print("Vehicle " + str(vehicle.id) + "| pos " + str(vehicle.pos) + " | rides_dist " + str(vehicle.rides_dist))
				print("Vehicle " + str(vehicle.id) + " assigned to ride " + str(ride.id))
				break

for vehicle in vehicles_list:
			vehicle.pos = [0,0]

for vehicle in vehicles_list:
	print("Vehicle " + str(vehicle.id) + " : pos " + str(vehicle.pos) + " ride " + str([ride.id for ride in vehicle.rides]))

print("-------------------------------------------------------------\n")

for t in range(T):
	for vehicle in vehicles_list:
		vehicle.refuel()
		if vehicle.current_ride is None and len(vehicle.rides) > 0:#Get next ride for not busy vehicles
			vehicle.next_ride()
			#print(str(t) + " : vehicle " + str(vehicle.id) + " | pos : " + str(vehicle.pos) + " | assigned to ride " + str(vehicle.current_ride.id))
		if vehicle.current_ride != None:
			if vehicle.pos != vehicle.current_ride.start_intersection and vehicle.current_ride.status is 0:#Ride waiting for the vehicle
				vehicle.go(vehicle.current_ride.start_intersection)
				#print(str(t) + " : vehicle " + str(vehicle.id) + " | pos : " + str(vehicle.pos) + " | Driving to pick up point of ride " + str(vehicle.current_ride.id))
			elif vehicle.pos == vehicle.current_ride.start_intersection and vehicle.current_ride.status is 0 and vehicle.current_ride.earliest_start <= t:#Vehicle at start_intersection
				#print(str(t) + " : vehicle " + str(vehicle.id) + " | pos : " + str(vehicle.pos) + " | picked up ride " + str(vehicle.current_ride.id))
				vehicle.go(vehicle.current_ride.finish_intersection)
				vehicle.current_ride.status = 1 #Processing
			if vehicle.pos == vehicle.current_ride.start_intersection and vehicle.current_ride.status is 0 and vehicle.current_ride.earliest_start > t:#Vehicle waiting for start
				#print(str(t) + " : vehicle " + str(vehicle.id) + " | pos : " + str(vehicle.pos) + " | waiting ride " + str(vehicle.current_ride.id))
				continue
			if vehicle.pos != vehicle.current_ride.start_intersection and vehicle.current_ride.status is 1:#Vehicle processing ride
				vehicle.go(vehicle.current_ride.finish_intersection)
				#print(str(t) + " : vehicle " + str(vehicle.id) + " | pos : " + str(vehicle.pos) + " | driving ride " + str(vehicle.current_ride.id))
				if vehicle.pos == vehicle.current_ride.finish_intersection and vehicle.current_ride.status is 1:#Arrived
					vehicle.current_ride.status = 2
					if vehicle.current_ride.latest_finish < t:
						#print(str(t) + " : vehicle " + str(vehicle.id) + " | pos : " + str(vehicle.pos) + " | finished ride " + str(vehicle.current_ride.id) + " delayed")
						continue
					else:
						score += B
						#print(str(t) + " : vehicle " + str(vehicle.id) + " | pos : " + str(vehicle.pos) + " | finished ride " + str(vehicle.current_ride.id) + " in time")
					vehicle.next_ride()

print("Final score : " + str(score))



