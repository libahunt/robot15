print("Starting main.py \n\n")

#--------------------------------------------
# Solving the maze
#--------------------------------------------


#sample only stuff

sampleMazeLength = 5
sampleMaze5bin =[
	[ 6, 10, 10, 10, 12],
	[ 7, 14, 12,  6, 13],
	[ 5,  5,  1,  5,  5],
	[ 5,  3, 10,  9,  5],
	[ 3, 10, 10, 10,  9]
]

print "Maze binary:"
for i in range(sampleMazeLength):
	print sampleMaze5bin[i]

sampleMaze5Target = [2, 2]

class MazeSquare:
	def __init__(self):
		self.up = 'false'
		self.right = 'false'
		self.down = 'false'
		self.left = 'false'


#fill maze with sample data
maze = [] #[[[MazeSquare] for i in range(sampleMazeLength)] for j in range(sampleMazeLength)]

for i in range(sampleMazeLength):
	mazeRow = []
	for j in range(sampleMazeLength):
		mazeSq = MazeSquare()	
		mazeSq.up = ('true' if ((sampleMaze5bin[i][j] & 1) > 0) else 'false')
		mazeSq.right = ('true' if ((sampleMaze5bin[i][j] & 2) > 0) else 'false')
		mazeSq.down = ('true' if ((sampleMaze5bin[i][j] & 4) > 0) else 'false')
		mazeSq.left = ('true' if ((sampleMaze5bin[i][j] & 8) > 0) else 'false')
		mazeRow.append(mazeSq)
	maze.append(mazeRow)

mazeLength = sampleMazeLength
targetAddr = sampleMaze5Target


print " "
print "Maze object: "

for i in range(sampleMazeLength):
	for j in range(sampleMazeLength):
		print maze[i][j], maze[i][j].up, maze[i][j].right, maze[i][j].down, maze[i][j].left
	

#real program
mazeSize = mazeLength^2


class Path:
	'Unique path starting from last square of the maze'

	def __init__(self, path, status):
		self.map = []
		self.status = status # 'open', 'deadend' or 'solved'


paths = []

paths.append(Path([mazeLength-1, mazeLength-1], 'open')) #start our first path from starting square



def findMoves(pathObj):
#checks open sides and graphes them into new paths
	if (solveStep == 0):
		addr0 = 0 #for fist square use opposite corner to clean check
		addr1 = 0

	else:
		addr0 = [pathObj.map[-1][0]]
		addr1 = [pathObj.map[-1][1]]

	nextAddrs = []
	if (maze[addr0][addr1].up):
		upAddr = [(addr0-1), addr1]
		loops = ifLoops(upAddr, pathObj)
		if (loops == 'false'):
			nextAddrs.append(upAddr)
	if (maze[addr0][addr1].right):
		rightAddr = [addr0, (addr1+1)]
		loops = ifLoops(rightAddr, pathObj)
		if (loops == 'false'):
			nextAddrs.append(rightAddr)
	if (maze[addr0][addr1].down):
		downAddr = [(addr0+1), addr1]
		loops = ifLoops(downAddr, pathObj)
		if (loops == 'false'):
			nextAddrs.append(downAddr)
	if (maze[addr0][addr1].left):
		leftAddr = [addr0, (addr1-1)]
		loops = ifLoops(leftAddr, pathObj)
		if (loops == 'false'):
			nextAddrs.append(leftAddr)

	if (len(nextAddrs) == 0): #no way out, declare a dead end
		pathObj.status = 'deadend'
	else:
		for i, nextAddr in nextAddrs:
			if (i > 0): #this is at least second way out, create new path object
				newPath = Path(pathObj.map, checkAddrStatus(nextAddr))
				newPath.map.append(nextAddr)
				paths.append(newPath)
			else: #first way out, continue with same path object
				pathObj.map.append(nextAddr)
				pathObj.status = checkAddrStatus(nextAddr)


def ifLoops(nextAddr, pathObj): 
#compares if the nextAddr is already on path
	loops = 'false'
	for prevAddr in pathObj.map:
		if (nextAddr == prevAddr):
			loops = 'true'
	return loops

def checkAddrStatus(nextAddr):
#cheacks if the addr is target square, 
#returns path object status value 'open' or 'solved'
	if (nextAddr == targetAddr):
		return 'solved'
	else:
		return 'open'


solveStep = 0

while 1:
	for path in paths:
		if (path.status == 'open'):
			findMoves(path)
	if (solveStep >= mazeSize-1):
		break
	solveStep += 1



