##############################################################################
class MazeSquare:
	'Oject that maps the walls and openings of it\'s address in maze'
	def __init__(self):
		self.up = 'unknown'
		self.right = 'unknown'
		self.down = 'unknown'
		self.left = 'unknown'

##############################################################################
class Path:
	'Unique path starting from last square of the maze'
	def __init__(self, status):
		self.status = status # 'open', 'deadend' or 'solved'
		self.map = [] #holds two element arrays of address

##############################################################################

#--------------------------------------------------
#   Maze object creation
#--------------------------------------------------
def binToMaze(mazeBin):
	#create python variable from maze binary mapping
	maze = []
	mazeLength = len(mazeBin)
	for i in range(mazeLength):
		mazeRow = []
		for j in range(mazeLength):
			mazeSq = MazeSquare()	
			mazeSq.up = ('door' if ((mazeBin[i][j] & 1) > 0) else 'wall')
			mazeSq.right = ('door' if ((mazeBin[i][j] & 2) > 0) else 'wall')
			mazeSq.down = ('door' if ((mazeBin[i][j] & 4) > 0) else 'wall')
			mazeSq.left = ('door' if ((mazeBin[i][j] & 8) > 0) else 'wall')
			mazeRow.append(mazeSq)
		maze.append(mazeRow)

	return maze


def createUnknown(size): 
	#create python variable with unknown properties for each square
	#retuns the maze object
	maze = []
	for i in range(size):
		mazeRow = []
		for j in range(size):
			mazeSq = MazeSquare()	
			mazeRow.append(mazeSq)
		maze.append(mazeRow)
	return maze


#------------------------------------------------------
# Mapping maze
#------------------------------------------------------
'''
Data structure:
pi->ardu
[number]: move forward the specified number of squares (9 is max, 91 results in 10 squares)
l: turn left
r: turn right
e: explore mode drive forward

ardu-> pi
d: done fulfilling drive commands
[number]: explored square properties in binary, 
    DEC 1-open to left, 2 open to front, 4 open to right, 
    7 means open to left, right and forward
    6 means open forward and right, 
    5 means open left and right, 
    4 means open right,
    3 means open front and left, 
    2 means open to front, 
    1 means open to left,
    0 means dead end all sides closed  
line starting with B indicates debug printout
'''


def mapReport(mazeObj, report, currentAddress, currentOrientation):
#adds new info to maze object
#changes currentAddress and currentOrientation to end of searched path
	print "in mapReport ..."
	reportString = str(report)
	for i in range(0, len(reportString)): 
		print "CurrentAddress and orientation:", currentAddress, currentOrientation, ", report:", int(reportString[i])
		if (i>0):	
		#ignore first, because it is known area and does not include backside anyway 
			print "mapping ..."
			binary = int(reportString[i])
			binary += 8 #add 8 because backside is open
			mazeSq = mazeObj[currentAddress[0]][currentAddress[1]]
			# bitshift according to orientation: 0 right, 1 down, 2 left, 3 up
			squareBin = ((binary << currentOrientation) & 0x0F) + ( (binary >> (4-currentOrientation) & 0x0F ))
			#print "Square binary", currentAddress , " is ", squareBin
			#record data that we don't have yet
			if (mazeSq.up == 'unknown'):
				mazeSq.up = ('door' if ((squareBin & 1) > 0) else 'wall')
			if (mazeSq.right == 'unknown'):
				mazeSq.right = ('door' if ((squareBin & 2) > 0) else 'wall')
			if (mazeSq.down == 'unknown'):
				mazeSq.down = ('door' if ((squareBin & 4) > 0) else 'wall')
			if (mazeSq.left == 'unknown'):
				mazeSq.left = ('door' if ((squareBin & 8) > 0) else 'wall')

		if (i<len(reportString)-1):
			#find next address from orientation, skip last round
			if (currentOrientation == 0):
				currentAddress[1] += 1
			elif (currentOrientation == 1):
				currentAddress[0] += 1
			elif (currentOrientation == 2):
				currentAddress[1] -= 1
			elif (currentOrientation == 3):
				currentAddress[0] -= 1
			print "next address" , currentAddress




def mapInterpolate(maze):
	print "in mapInterpolate ..."
	for i in range(len(maze)):
		for j in range(len(maze)):
			mazeSq = maze[i][j]	
			if (mazeSq.up != 'unknown'): 
				if (i>0):
					if(maze[i-1][j].down != 'unknown' and maze[i-1][j].down != mazeSq.up):
						print "Error matching ", [i-1] ,[j], "and", [i], [j]
					maze[i-1][j].down = mazeSq.up
			if (mazeSq.down != 'unknown'): 
				if (i<len(maze)-1):
					if(maze[i+1][j].up != 'unknown' and maze[i+1][j].up != mazeSq.down):
						print "Error matching ", [i+1],[j], "and", [i], [j]
					maze[i+1][j].up = mazeSq.down
			if (mazeSq.left != 'unknown'): 
				if (j>0):
					if(maze[i][j-1].right != 'unknown' and maze[i][j-1].right != mazeSq.left):
						print "Error matching ", [i],[j-1], "and ", [i], [j]
					maze[i][j-1].right = mazeSq.left
			if (mazeSq.right != 'unknown'): 
				if (j<len(maze)-1):
					if(maze[i][j+1].left != 'unknown' and maze[i][j+1].left != mazeSq.right):
						print "Error matching ", [i],[j+1], "and ", [i], [j]
					maze[i][j+1].left = mazeSq.right
	return maze




def chooseExplorePoint(maze, currentAddress, targetAddr):
	print "in chooseExplorePoint ..."
	mazeLength = len(maze)
	mazeSize = len(maze)^2
	paths = []
	paths.append(Path('open')) #start our first path from starting square
	paths[0].map.append([currentAddress[0], currentAddress[1]])
	solveStep = 0
	while 1:		
		existingPaths = len(paths)
		for i in range(existingPaths):
			if (paths[i].status == 'open'):
				findMoves(paths[i], maze, targetAddr, paths)

		foreignPaths = []
		unsolved = 0
		for path in paths:
			if (path.status == 'foreign'):
				foreignPaths.append(path)
			if (path.status == 'open'):
				unsolved += 1

		if (len(foreignPaths) > 0):
			print "Found", len(foreignPaths), "foreign square(s)"
			break

		if (unsolved == 0):
			print "All paths exhausted, no foreign area found"
			return False

		solveStep += 1
	
	for path in foreignPaths:
		pathMap = path.map
		goodOrientation = False
		half = (mazeLength+1)/2
		#find target orientation and do a primitive evaluation if it is towards center
		if (pathMap[-1][0] < pathMap[-2][0]):
			targetOrientation = 3 #up
			if (pathMap[-1][0] > half):
				goodOrientation = True
		elif (pathMap[-1][0] > pathMap[-2][0]):
			targetOrientation = 1 #down
			if (pathMap[-1][0] < half):
				goodOrientation = True
		elif (pathMap[-1][1] < pathMap[-2][1]):
			targetOrientation = 2 #left
			if (pathMap[-1][1] > half):
				goodOrientation = True
		else:
			targetOrientation = 0 #right
			if (pathMap[-1][1] < half):
				goodOrientation = True
		
		#if orientation is "good", return
		if (goodOrientation):
			#remove last address from map
			print "The foreign square:", pathMap[-1]
			pathMap.pop()
			return pathMap, targetOrientation

	#if none returned so far, return the last one
	print "The foreign square:", pathMap[-1]
	pathMap.pop()
	print "Exploration result: ", pathMap, readableOrientation(targetOrientation)
	return pathMap, targetOrientation



def makeOrders(path, currentOrientation, targetOrientation, currentAddress):
	order = ''
	moveLength = 0
	for i in range(len(path)):
		#check if turn is needed
		if (i == len(path)-1):
			#last step turn according to target orientation
			nextOrientation = targetOrientation
		else:
			#turn according to currentorientation and next step direction
			nextOrientation = squareOrientation(path[i], path[i+1])
		
		if (i>0):
			#first address is current address, no move needed
			#at the change of address 1 square move is needed
			moveLength += 1
			currentAddress = path[i]

		print "Orientation computation from", readableOrientation(currentOrientation), "to", readableOrientation(nextOrientation)
		turn = turnOrder(currentOrientation, nextOrientation)

		if (turn !=  None):
			#add accumulated move length to order
			if (moveLength > 9):
				order += '9'
				moveLenght -= 9
			if (moveLength > 0):
				order += str(moveLength)
				moveLength = 0 
			#add turn command
			order += turn
			currentOrientation = nextOrientation
	if (moveLength>0):
		order += str(moveLength)

	print "Generated order", order
	return order




#------------------------------------------------------
# Solving maze
#------------------------------------------------------
def solve(maze, initialAddr, targetAddr): 

	mazeLength = len(maze)
	mazeSize = len(maze)^2

	paths = []

	paths.append(Path('open')) #start our first path from starting square
	paths[0].map.append(initialAddr)

	
	#Maze solving sequence ----------------------------------

	solveStep = 0

	while 1:
		
		#print "Paths length: ", len(paths)
		existingPaths = len(paths)
		for i in range(existingPaths):
			#print 'solveStep: ', solveStep, '  path no: ', i, '  status: ', paths[i].status
			if (paths[i].status == 'open'):
				findMoves(paths[i], maze, targetAddr, paths)

		if (solveStep >= mazeSize-1):
			print "End program, solveStep = ", solveStep
			break

		unsolved = 0
		for path in paths:
			if (path.status == 'open'):
				unsolved += 1
		if (unsolved == 0):
			print "End program, all paths solved"
			break

		#print 'increment solveStep'
		solveStep += 1
		#print " "


	print "---------------------------------------------"
	print " "
	solvedSum = 0
	deadendSum = 0
	for path in paths:
		if (path.status == 'solved'):
			solvedSum += 1
		if (path.status == 'deadend'):
			deadendSum += 1
	print "Paths graphed: ", len(paths)
	print "Solved paths: ", solvedSum, " dead end paths: ", deadendSum
	print " "
	i=0
	for path in paths:
		if (path.status == 'solved'):
			print "Solved path no ", i, " length ", len(path.map), "squares"
			print path.map
			i += 1
			print " "


#------------------------------------------------------
# Universal helpers
#------------------------------------------------------

def findMoves(pathObj, maze, targetAddr, paths):
#checks open sides and graphes them into new paths
	#print " "
	#print "in findmoves: ", pathObj
	addr0 = pathObj.map[-1][0]
	addr1 = pathObj.map[-1][1]

	#print 'position address: ', addr0, ' ', addr1

	nextAddrs = []
	if (maze[addr0][addr1].up == 'door'):
		upAddr = [(addr0-1), addr1]
		loops = ifLoops(upAddr, pathObj)
		if (loops == False):
			nextAddrs.append(upAddr)
			#print "Up "
	if (maze[addr0][addr1].right == 'door'):
		rightAddr = [addr0,(addr1+1)]
		loops = ifLoops(rightAddr, pathObj)
		if (loops == False):
			nextAddrs.append(rightAddr)
			#print "Right "
	if (maze[addr0][addr1].down == 'door'):
		downAddr = [(addr0+1), addr1]
		loops = ifLoops(downAddr, pathObj)
		if (loops == False):
			nextAddrs.append(downAddr)
			#print "Down "
	if (maze[addr0][addr1].left == 'door'):
		leftAddr = [addr0, (addr1-1)]
		loops = ifLoops(leftAddr, pathObj)
		if (loops == False):
			nextAddrs.append(leftAddr)
			#print "Left "

	if (len(nextAddrs) == 0): #no way out, declare a dead end
		#print "Declare deadend"
		pathObj.status = 'deadend'
	else:
		i = 0
		for nextAddr0, nextAddr1 in nextAddrs:
			#print "Adding way out no ", i, " nextAddr", nextAddr0, " ", nextAddr1
			if (i > 0): #this is at least second way out, create new path object
				newPath = Path(checkAddrStatus(maze, [nextAddr0, nextAddr1], targetAddr))
				oldPathLen = len(pathObj.map) - 1 #ignore last item because it's added on this round
				for i in range(oldPathLen):
					newPath.map.append(pathObj.map[i])
				newPath.map.append([nextAddr0, nextAddr1])
				paths.append(newPath)
			else: #first way out, continue with same path object
				pathObj.map.append([nextAddr0, nextAddr1])
				pathObj.status = checkAddrStatus(maze, [nextAddr0, nextAddr1], targetAddr)
			i += 1
	#print "end findmoves"



def ifLoops(nextAddr, pathObj): 
#compares if the nextAddr is already on path
	
	loops = False
	for prevAddr in pathObj.map:
		if (nextAddr == prevAddr):
			loops = True
	#print "in ifLoops: nextAddr = ", nextAddr, " pathObj.map = ", pathObj.map, " looping: ", loops
	return loops



def checkAddrStatus(maze, nextAddr, targetAddr):
#checks if the addr is target square, 
#returns path object status value 'open','solved' or 'foreign'
	
	if (nextAddr == targetAddr):
		return 'solved'

	square = maze[nextAddr[0]][nextAddr[1]]
	if (square.up == 'unknown' or square.right == 'unknown' or square.down == 'unknown' or square.left == 'unknown'):
		print "Foreign square at", nextAddr[0], nextAddr[1]
		print square.up, square.right, square.down, square.left
		return 'foreign'
	else:
		return 'open'



def turnOrder(current, target):
	if (current == target):
		return None
	elif (current-target == 1 or current-target == -3):
		return 'l'
	elif (current-target == -1 or current-target == 3):
		return 'r'
	else:
		return 'rr'



def squareOrientation(thisAddr, nextAddr):
	if (thisAddr[0] - nextAddr[0] == 1):
		return 3 #up
	elif (thisAddr[0] - nextAddr[0] == -1):
		return 1 #down
	elif (thisAddr[1] - nextAddr[1] == 1):
		return 2 #left
	else:
		return 0 #right


#---------------------------------------------------
# Debbuging helpers
#---------------------------------------------------

def printMaze(maze):
	print "Current maze map:"
	mazeLength = len(maze)
	for i in range(mazeLength):
		for j in range(mazeLength):
			print "[", i, ",",j , "]:", maze[i][j].up, maze[i][j].right, maze[i][j].down, maze[i][j].left


def readableOrientation(num):
	if (num == 0):
		return 'right'
	elif (num == 1):
		return 'down'
	elif (num == 2):
		return 'left'
	else:
		return 'up'










