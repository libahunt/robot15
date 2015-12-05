print("Starting main.py \n\n")

#--------------------------------------------
# Solving the maze
#--------------------------------------------

import Maze
import time

timelimit1 = 4*60 #time to switch from exploring to running
timelimit2 = 5*60 #timelimit altogether
starttime = 0

mazeLength = 16
maze = Maze.createUnknown(mazeLength)
print "Created a maze object of size", mazeLength
#robot starts from orientation to left
startOrientation = 2 # bitshift 0 right, 1 down, 2 left, 3 up
currentOrientation = startOrientation
#and from last address in the maze
startAddr = [mazeLength-1, mazeLength-1]
currentAddress = startAddr
#we know the mapping of first square
maze[currentAddress[0]][currentAddress[1]].up = 'wall'
maze[currentAddress[0]][currentAddress[1]].right = 'wall'
maze[currentAddress[0]][currentAddress[1]].down = 'wall'
maze[currentAddress[0]][currentAddress[1]].left = 'door'

targetAddr = [7,7]

print "Mapped center right square as starting point, facing left."
print ""
print ""

simRe = raw_input("Is this simulation over terminal (s) or real Arduino (r)?")

def simReRead():
	if (simRe == 'r'):
		arduSays = ser.readline()
		print 'Got "', command, '" from Ardu'
	else:
		arduSays = raw_input()
		print 'Got simulated input:', arduSays
	return arduSays

def simReWrite(command):
	if (simRe == 'r'):
		ser.write(command) 
	else:
		print '"Serial.write(', command, ')"'


if (simRe == 's'):
	import serial
	#ser = serial.Serial('/dev/ttyACM0', 9600)
	print "insert exploration results"

explorationStep = 0
starttime = time.time()

simReWrite('e')


while True:
	arduSays = simReRead()

	Maze.mapReport(maze, arduSays, currentAddress, currentOrientation)
	Maze.mapInterpolate(maze)
	Maze.printMaze(maze)
	explorePath, targetOrientation = Maze.chooseExplorePoint(maze, currentAddress, targetAddr)
	if (explorePath == None):
		break
	order = Maze.makeOrders(explorePath, currentOrientation, targetOrientation, currentAddress)
	
	simReWrite(order+'e')

	currentAddress = explorePath[-1]
	currentOrientation = targetOrientation

	if (explorationStep == 1):
		targetAddr = Maze.determineTarget(startAddr, targetAddr, maze)

	sq = maze[targetAddr[0]][targetAddr[1]]
	if (sq.up != 'unknown' or sq.right != 'unknown' or sq.left != 'unknown' or sq.left != 'unknown'):
		if (time.time() > starttime+timelimit1):
			break
	explorationStep += 1
	print "Time left:", starttime+timelimit2 - time.time()

#insert last piece of information
arduSays = simReRead()

Maze.mapReport(maze, arduSays, currentAddress, currentOrientation)
Maze.mapInterpolate(maze)
Maze.printMaze(maze)

#calculate way home
homePaths = Maze.solve(maze, currentAddress, startAddress)
bestHomePath = Maze.choosePath(homePaths)
homePathOrders  = Maze.makeOrdrers(bestHomePath, currentOrientation, startOrientation)

simReWrite(homePathOrders)

arduSays = simReRead() #Ardu should say 'd' when it got home

runPaths = Maze.solve(maze, startAddress, targetAddress)
bestRunPath = Maze.choosePath(runPaths)
runPathOrders = Maze.makeOrders(bestRunPath)
simReWrite(runPathOrders)



