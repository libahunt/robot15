print("Starting main.py \n\n")

#--------------------------------------------
# Solving the maze
#--------------------------------------------

import Maze



mazeLength = 8
maze = Maze.createUnknown(mazeLength)
print "Created a maze object of size", mazeLength
#robot starts from orientation to left
currentOrientation = 2 # bitshift 0 right, 1 down, 2 left, 3 up
#and from last address in the maze
currentAddress = [mazeLength-1, mazeLength-1]
#we know the mapping of first square
maze[currentAddress[0]][currentAddress[1]].up = 'wall'
maze[currentAddress[0]][currentAddress[1]].right = 'wall'
maze[currentAddress[0]][currentAddress[1]].down = 'wall'
maze[currentAddress[0]][currentAddress[1]].left = 'door'

targetAddr = [0,0]

print "Mapped bottom right square as starting point, facing left."
print ""
print ""

print "insert exploration results"

while True:
	arduSays = raw_input()
	Maze.mapReport(maze, arduSays, currentAddress, currentOrientation)
	Maze.mapInterpolate(maze)
	Maze.printMaze(maze)
	explorePath, targetOrientation = Maze.chooseExplorePoint(maze, currentAddress, targetAddr)
	order = Maze.makeOrders(explorePath, currentOrientation, targetOrientation, currentAddress)
	currentAddress = explorePath[-1]
	currentOrientation = targetOrientation

#pretend received dummy report, in real life report ends with "d"

#Maze.mapReport(maze, '2260', currentAddress, currentOrientation)
#Maze.mapReport(maze, '75', currentAddress, currentOrientation)
#3234
#64
#622325
#60
#32221
#324
#65
#31
#325
#661
#334
#64
#6221
#35
#32221
#34
#64
#61
#31
#3221
#724
#65
#31
#721
#3321
#764
#64
#620


#60
#23234


