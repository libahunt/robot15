##############################################################################
class MazeSquare:
	'Oject that maps the walls and openings of it\'s address in maze'
	def __init__(self):
		self.known = False
		self.up = False
		self.right = False
		self.down = False
		self.left = False

##############################################################################
class Path:
	'Unique path starting from last square of the maze'
	def __init__(self, status):
		self.status = status # 'open', 'deadend' or 'solved'
		self.map = [] #holds two element arrays of address

##############################################################################

def solve(mazeBin, targetAddr): 

	#create python variable from maze binary mapping
	maze = []
	mazeLength = len(mazeBin)
	for i in range(mazeLength):
		mazeRow = []
		for j in range(mazeLength):
			mazeSq = MazeSquare()	
			mazeSq.up = (True if ((mazeBin[i][j] & 1) > 0) else False)
			mazeSq.right = (True if ((mazeBin[i][j] & 2) > 0) else False)
			mazeSq.down = (True if ((mazeBin[i][j] & 4) > 0) else False)
			mazeSq.left = (True if ((mazeBin[i][j] & 8) > 0) else False)
			mazeRow.append(mazeSq)
		maze.append(mazeRow)


	'''print " "
	print "Maze object: "

	for i in range(mazeLength):
		for j in range(mazeLength):
			print maze[i][j], maze[i][j].up, maze[i][j].right, maze[i][j].down, maze[i][j].left
	'''	

	mazeSize = mazeLength*mazeLength



	paths = []

	paths.append(Path('open')) #start our first path from starting square
	paths[0].map.append([mazeLength-1, mazeLength-1])

	
	#Maze solving sequence ----------------------------------

	solveStep = 0

	while 1:
		
		i = 0
		#print "Paths length: ", len(paths)
		existingPaths = len(paths)
		for i in range(existingPaths):
			#print 'solveStep: ', solveStep, '  path no: ', i, '  status: ', paths[i].status
			if (paths[i].status == 'open'):
				findMoves(paths[i], maze, targetAddr, paths)
			i += i

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
	if (maze[addr0][addr1].up):
		upAddr0 = (addr0-1)
		upAddr1 = addr1
		loops = ifLoops([upAddr0, upAddr1], pathObj)
		if (loops == False):
			nextAddrs.append([upAddr0, upAddr1])
			#print "Up "
	if (maze[addr0][addr1].right):
		rightAddr0 = addr0
		rightAddr1 = (addr1+1)
		loops = ifLoops([rightAddr0, rightAddr1], pathObj)
		if (loops == False):
			nextAddrs.append([rightAddr0, rightAddr1])
			#print "Right "
	if (maze[addr0][addr1].down):
		downAddr = [(addr0+1), addr1]
		loops = ifLoops(downAddr, pathObj)
		if (loops == False):
			nextAddrs.append(downAddr)
			#print "Down "
	if (maze[addr0][addr1].left):
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
				newPath = Path(checkAddrStatus([nextAddr0, nextAddr1], targetAddr))
				oldPathLen = len(pathObj.map) - 1 #ignore last item because it's added on this round
				for i in range(oldPathLen):
					newPath.map.append(pathObj.map[i])
				newPath.map.append([nextAddr0, nextAddr1])
				paths.append(newPath)
			else: #first way out, continue with same path object
				pathObj.map.append([nextAddr0, nextAddr1])
				pathObj.status = checkAddrStatus([nextAddr0, nextAddr1], targetAddr)
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

def checkAddrStatus(nextAddr, targetAddr):
#cheacks if the addr is target square, 
#returns path object status value 'open' or 'solved'
	#print "in checkAddrStatus: nextAddr = ", nextAddr, " solved? : ", True if (nextAddr == targetAddr) else False
	if (nextAddr == targetAddr):
		return 'solved'
	else:
		return 'open'

