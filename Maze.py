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
#   Maze solving
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


	'''print " "
	print "Maze object: "

	for i in range(mazeLength):
		for j in range(mazeLength):
			print maze[i][j], maze[i][j].up, maze[i][j].right, maze[i][j].down, maze[i][j].left
	'''	



def solve(maze, targetAddr): 

	mazeLength = len(maze)
	mazeSize = len(maze)^2

	paths = []

	paths.append(Path('open')) #start our first path from starting square
	paths[0].map.append([mazeLength-1, mazeLength-1])

	
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
		return 'foreign'
	else:
		return 'open'


#--------------------------------------------------
#   Maze mapping
#--------------------------------------------------
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
    
B: line starting with B indicates debug printout
'''



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


def mapReport(mazeObj, report, currentAddress, currentOrientation):
	reportString = str(report)
	for i in range(0, len(reportString)):   
		binary = int(reportString[i])
		if (i>0):
			binary += 8 #for squares other than first add 8 because backside is open
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

		#find next address from orientation
		if (currentOrientation == 0):
			currentAddress[1] += 1
		elif (currentOrientation == 1):
			currentAddress[0] += 1
		elif (currentOrientation == 2):
			currentAddress[1] -= 1
		elif (currentOrientation == 3):
			currentAddress[0] -= 1


def mapInterpolate(maze):
	for i in range(len(maze)):
		for j in range(len(maze)):
			mazeSq = maze[i][j]	
			if (mazeSq.up != 'unknown'): 
				if (i>0):
					if(maze[i-1][j].down != 'unknown' and maze[i-1][j].down != mazeSq.up):
						print "B: Error matching ", [i-1] ,[j], "and", [i], [j]
					maze[i-1][j].down = mazeSq.up
			if (mazeSq.down != 'unknown'): 
				if (i<len(maze)-1):
					if(maze[i-1][j].up != 'unknown' and maze[i-1][j].up != mazeSq.down):
						print "B: Error matching ", [i+1],[j], "and", [i], [j]
					maze[i+1][j].up = mazeSq.down
			if (mazeSq.left != 'unknown'): 
				if (j>0):
					if(maze[i-1][j].right != 'unknown' and maze[i-1][j].right != mazeSq.left):
						print "B: Error matching ", [i],[j-1], "and ", [i], [j]
					maze[i][j-1].right = mazeSq.left
			if (mazeSq.right != 'unknown'): 
				if (j<len(maze)-1):
					if(maze[i-1][j].left != 'unknown' and maze[i-1][j].left != mazeSq.right):
						print "B: Error matching ", [i],[j+1], "and ", [i], [j]
					maze[i][j+1].left = mazeSq.right
	return maze


def chooseExplorePoint(maze, currentAddress, targetAddr):
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
				foreignPaths.append(paths[i])
			if (path.status == 'open'):
				unsolved += 1

		if (len(foreignPaths) > 0):
			print "Found some foreign square(s)"
			break

		if (unsolved == 0):
			print "All paths exhausted, no foreign area found"
			return False

		#print 'increment solveStep'
		solveStep += 1
		#print " "
			
	if (len(foreignPaths) == 1):
		return foreignPath[0]
	else:
		return "Multiple"

